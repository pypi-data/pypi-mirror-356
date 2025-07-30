from typing import Optional
# from aiohttp import ClientSession
import aiohttp
import asyncio
import time
from pawnlib.config import pawn, LoggerMixinVerbose
from pawnlib.utils.http import  NetworkInfo, AsyncIconRpcHelper, append_http
from pawnlib.blockchain.goloop.models import PeerEndpoint, PeerInfo


class P2PNetworkParser(LoggerMixinVerbose):
    def __init__(
            self,
            url: str,
            max_concurrent: int = 10,
            timeout: int = 5,
            max_depth: int = 5,
            verbose: int = 0,
            logger=None,
            nid=None,
    ):
        self.init_logger(logger=logger, verbose=verbose)
        self.logger.info("Start P2PNetworkParser")

        self.start_url = url
        self.max_concurrent = max_concurrent
        self.timeout = timeout
        self.max_depth = max_depth

        self.verbose = verbose

        # 아직 session, helper, semaphore 생성 안 함
        self.session: Optional[aiohttp.ClientSession] = None
        self.rpc_helper: Optional[AsyncIconRpcHelper] = None
        self.semaphore: Optional[asyncio.Semaphore] = None

        self.visited = set()
        self.ip_set = set()
        self.ip_to_hx = {}
        self.hx_to_ip = {}
        self.start_time = time.time()
        self.nid = nid
        self.preps_info = {}

        self.logger.info(f"***** P2PNetworkParser Initialized with max_concurrent={max_concurrent}")

    def extract_ip_and_port(self, url_str: str) -> (str, str):
        # 간단 문자열 파싱 예시
        url_str = url_str.replace("http://", "").replace("https://", "")
        if ":" in url_str:
            ip, port = url_str.split(":", 1)
        else:
            ip, port = url_str, "7100"
        return ip, port

    # def add_hx_to_ip(self, hx: str, ip: str, peer_type: str, rtt=None):
    #     """
    #     HX/IP 매핑 예시
    #     """
    #     self.ip_to_hx[ip] = {"hx": hx, "peer_type": peer_type, "rtt": rtt}
    #
    #     if not self.hx_to_ip.get(hx):
    #         self.hx_to_ip[hx] = {
    #             "ip_address": {},
    #             "name": ""
    #         }
    #     if not self.hx_to_ip[hx]["ip_address"].get(ip):
    #         self.hx_to_ip[hx]["ip_address"][ip] = 0
    #         if self.preps_info.get(hx):
    #             self.hx_to_ip[hx]["name"] = self.preps_info[hx].get('name')
    #     self.hx_to_ip[hx][ip] +=1

    def add_hx_to_ip(self, hx: str, ip: str, peer_type: str, rtt: Optional[float] = None):
        """
        HX 주소(hx)와 IP 정보를 추가하는 메서드

        - hx_to_ip[hx] 딕셔너리에 대응되는 PeerInfo 객체가 있는지 확인
        - 없으면 생성하고, 있으면 기존 정보 업데이트
        - 새로운 IP가 등록될 경우 `ip_count += 1`
        - 기존 IP가 있을 경우 `count += 1` 및 필요한 필드 갱신

        구조체:
            @dataclass
            class PeerInfo:
                hx: str
                name: str = ""
                ip_addresses: Dict[str, PeerEndpoint] = field(default_factory=dict)
                ip_count: int = 0
        """

        # 1) hx에 해당하는 PeerInfo 객체 확인 (없으면 생성)
        if hx not in self.hx_to_ip:
            # preps_info에서 이름(name) 가져오기 (없으면 기본값 "")
            node_name = self.preps_info.get(hx, {}).get('name', "")
            self.hx_to_ip[hx] = PeerInfo(hx=hx, name=node_name)

        peer_info = self.hx_to_ip[hx]

        # 2) 새로운 IP라면 추가 후 ip_count 증가
        if ip not in peer_info.ip_addresses:
            peer_info.ip_count += 1  # 새로운 IP 등록
            peer_info.ip_addresses[ip] = PeerEndpoint(count=1, peer_type=peer_type, rtt=rtt)
        else:
            # 기존 IP라면 count 증가 & 필요시 필드 업데이트
            ip_attr = peer_info.ip_addresses[ip]
            ip_attr.count += 1

            # peer_type이 새롭게 들어오면 업데이트
            if peer_type:
                ip_attr.peer_type = peer_type
            # rtt가 새롭게 들어오면 업데이트
            if rtt is not None:
                ip_attr.rtt = rtt


    async def initialize_resources(self):
        """
        비동기 자원(aiohttp.ClientSession, AsyncIconRpcHelper, Semaphore) 생성
        """
        # 1) 세션
        if not self.session or self.session.closed:
            self.session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.timeout))
            self.logger.debug("[SESSION INIT] Created new session")

        # 2) 헬퍼 (공용 1개만 사용)
        self.rpc_helper = AsyncIconRpcHelper(
            session=self.session,
            logger=None,
            verbose=self.verbose if self.verbose > 1 else -1,
            timeout=self.timeout,
            max_concurrent=self.max_concurrent,
            retries=1
        )

        self.logger.debug("[RPC HELPER INIT] Created single AsyncIconRpcHelper")
        self.semaphore = asyncio.Semaphore(self.max_concurrent)
        self.logger.debug(f"[SEMAPHORE INIT] max_concurrent={self.max_concurrent}")

    async def close_resources(self):
        """
        사용 후 자원 정리
        """
        # rpc_helper는 session을 닫지 않음. session을 명시적으로 닫아야 함
        if self.session and not self.session.closed:
            await self.session.close()
            self.logger.debug("[SESSION CLOSED]")

    async def collect_ips(self, current_url: str, depth: int = 0):
        """
        재귀적으로 P2P 노드(IP) 수집
        """
        # async with self.semaphore:
        self.logger.debug(f"[COLLECT_IPS] {current_url}, depth={depth}")
        if current_url in self.visited or depth > self.max_depth:
            return
        self.visited.add(current_url)

        ip, _ = self.extract_ip_and_port(current_url)
        if not ip:
            self.logger.warning(f"[FORMAT ERROR] Invalid URL: {current_url}")
            return

        query_url = f"http://{ip}:9000"
        try:
            # self.logger.info(f"Start ::: {query_url}")

            if not self.preps_info:
                self.preps_info = await self.rpc_helper.get_preps(url=query_url, return_dict_key="nodeAddress")

            if not self.nid:
                chain_info = await self.rpc_helper.fetch(url=f"{query_url}/admin/chain", return_first=True)
                self.logger.debug(f"[IP RESPONSE] {query_url} - {chain_info}")
                if not chain_info or 'nid' not in chain_info:
                    return
                nid = chain_info['nid']
                self.nid = nid
            else:
                nid = self.nid

            detailed_info = await self.rpc_helper.fetch(url=f"{query_url}/admin/chain/{nid}")
            self.logger.debug(f"[IP DETAIL RESPONSE] {query_url} - {detailed_info}")
            if not detailed_info or 'module' not in detailed_info:
                return

            p2p_info = detailed_info['module']['network'].get('p2p', {})
            self_info = p2p_info.get('self', {})
            if self_info.get('addr'):
                self.ip_set.add(self_info['addr'])

            peers_to_explore = []
            for peer_type in ['friends', 'children', 'nephews', 'orphanages']:
                for peer in p2p_info.get(peer_type, []):
                    peer_ip = peer.get('addr', '')
                    if peer_ip and peer_ip not in self.visited:
                        self.ip_set.add(peer_ip)
                        peers_to_explore.append(peer_ip)

            # 재귀 호출
            tasks = [self.collect_ips(peer_ip, depth + 1) for peer_ip in peers_to_explore]
            await asyncio.gather(*tasks, return_exceptions=True)

        except Exception as e:
            self.logger.error(f"[IP ERROR] {query_url} - {e}")

    async def collect_hx(self, ip: str):
        """
        HX 정보 수집
        """
        async with self.semaphore:
            self.logger.debug(f"[COLLECT_HX] {ip}")
            base_ip, _ = self.extract_ip_and_port(ip)
            if not base_ip:
                return
            query_url = f"http://{base_ip}:9000"
            try:
                chain_info = await self.rpc_helper.fetch(url=f"{query_url}/admin/chain", return_first=True)
                self.logger.debug(f"[HX NID RESPONSE] {query_url} - {chain_info}")
                if not chain_info or 'nid' not in chain_info:
                    return
                nid = chain_info['nid']

                detailed_info = await self.rpc_helper.fetch(url=f"{query_url}/admin/chain/{nid}")
                self.logger.debug(f"[HX DETAIL RESPONSE] {query_url} - {detailed_info}")
                if not detailed_info or 'module' not in detailed_info:
                    return

                p2p_info = detailed_info['module']['network'].get('p2p', {})
                # children/friends/orphanages/others/parent
                for item in ['children', 'friends', 'orphanages', 'others', 'parent']:
                    value = p2p_info.get(item)
                    if isinstance(value, list):
                        for peer in value:
                            self.add_hx_to_ip(peer['id'], peer['addr'], peer_type=item, rtt=peer.get('rtt'))
                    elif isinstance(value, dict):
                        # parent가 dict인 경우 등
                        peer = value
                        if peer.get('id'):
                            self.add_hx_to_ip(peer.get('id'), peer['addr'], peer_type=item, rtt=peer.get('rtt'))

                # roots/seed
                for p2p_attr in ['roots', 'seed']:
                    if p2p_attr in p2p_info:
                        for ip_addr, hx in p2p_info[p2p_attr].items():
                            self.add_hx_to_ip(hx, ip_addr, peer_type=p2p_attr)

                # self 정보
                self_info = p2p_info.get('self', {})
                if self_info.get('id'):
                    self.add_hx_to_ip(self_info['id'], ip, peer_type="self")
            except Exception as e:
                self.logger.error(f"[HX ERROR] {query_url} - {e}")

    async def run(self):
        """
        메인 실행 함수
        """
        # 1) 자원 초기화
        await self.initialize_resources()

        # [PHASE 1] IP 수집
        self.logger.info("[PHASE 1] Collecting IPs")
        await self.collect_ips(self.start_url, depth=0)
        self.logger.info(f"[PHASE 1 COMPLETE] IPs collected: {len(self.ip_set)}")

        # [PHASE 2] HX 수집
        self.logger.info("[PHASE 2] Collecting HX addresses")
        tasks = [self.collect_hx(ip) for ip in self.ip_set]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        for ip_addr, result in zip(self.ip_set, results):
            if isinstance(result, Exception):
                self.logger.error(f"[HX TASK ERROR] {ip_addr} - {result}")
            else:
                self.logger.debug(f"[HX TASK SUCCESS] {ip_addr}")

        self.logger.info(f"[PHASE 2 COMPLETE] HX collected for {len(self.ip_to_hx)} IPs")

        total_elapsed = time.time() - self.start_time
        self.logger.info(
            f"[TOTAL COMPLETE] Total time: {total_elapsed:.2f}s, "
            f"IPs: {len(self.ip_set)}, Visited: {len(self.visited)}"
        )
        await self.close_resources()
        return {"ip_to_hx": self.ip_to_hx, "hx_to_ip": self.hx_to_ip}
