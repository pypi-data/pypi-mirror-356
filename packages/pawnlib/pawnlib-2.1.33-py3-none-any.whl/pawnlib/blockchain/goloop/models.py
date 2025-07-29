from dataclasses import dataclass, field
from typing import Dict, Optional

@dataclass
class PeerEndpoint:
    """
    IP 하나에 대한 부가 정보
    - count: 몇 번 등장했는지 (중복 횟수)
    - peer_type: 'friends', 'children' 같은 유형
    - rtt: 왕복 지연시간 (Round Trip Time)
    """
    count: int = 0
    peer_type: str = ""
    rtt: Optional[float] = None


@dataclass
class PeerInfo:
    """
    하나의 HX 주소(hx)에 대응되는 정보
    - hx: 이 노드의 HX 주소
    - name: P-Rep 이름(혹은 별칭), preps_info[hx]에서 가져옴
    - ip_address: { ip_string: PeerEndpoint } 형태로
                  여러 IP에 대한 정보를 관리
    """
    hx: str
    name: str = ""
    ip_addresses: Dict[str, PeerEndpoint] = field(default_factory=dict)
    ip_count: int = 0

    def add_ip(self, ip: str, peer_type: str = "", rtt: Optional[float] = None):
        """
        새 IP를 추가하거나, 이미 있는 IP면 count만 증가
        """
        if ip not in self.ip_addresses:
            # 새로운 IP이므로 ip_count 증가
            self.ip_count += 1
            self.ip_addresses[ip] = PeerEndpoint(count=1, peer_type=peer_type, rtt=rtt)
        else:
            # 이미 있는 IP → 카운트만 증가, 필요 시 peer_type, rtt 업데이트
            self.ip_addresses[ip].count += 1
            if peer_type:
                self.ip_addresses[ip].peer_type = peer_type
            if rtt is not None:
                self.ip_addresses[ip].rtt = rtt
