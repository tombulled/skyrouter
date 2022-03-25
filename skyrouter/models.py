import dataclasses


@dataclasses.dataclass(frozen=True, eq=True)
class RouterStatistics:
    port: str
    status: str
    transmitted_packets: int
    received_packets: int
    collision_packets: int
    transmitted_bytes_per_second: int
    received_bytes_per_second: int
    uptime: str
