import dataclasses

import bs4
import furl
import httpx

from . import constants
from . import enums
from . import models

from typing import List


@dataclasses.dataclass
class SkyRouter:
    host: str = constants.DEFAULT_HOST

    username: str = constants.DEFAULT_USERNAME
    password: str = constants.DEFAULT_PASSWORD

    session: httpx.Client = dataclasses.field(default_factory=httpx.Client, repr=False)

    def _url(self, endpoint: str = "") -> str:
        return str(furl.furl(scheme="http", host=self.host, path=endpoint))

    def _get(self, endpoint: str) -> bs4.BeautifulSoup:
        response: httpx.Response = self.session.get(
            self._url(endpoint), auth=httpx.DigestAuth(self.username, self.password)
        )

        response.raise_for_status()

        return bs4.BeautifulSoup(response.text, "html.parser")

    def system(self) -> List[models.RouterStatistics]:
        soup: bs4.BeautifulSoup = self._get(enums.Endpoint.SYSTEM)

        statistics: List[models.RouterStatistics] = []

        for row in soup.table.findAll("tr")[1:]:
            (
                port,
                status,
                transmitted_packets,
                received_packets,
                collision_packets,
                transmitted_bytes_per_second,
                received_bytes_per_second,
                uptime,
            ) = (data.text for data in row.findAll("td"))

            statistics.append(
                models.RouterStatistics(
                    port=port,
                    status=status,
                    transmitted_packets=int(transmitted_packets),
                    received_packets=int(received_packets),
                    collision_packets=int(collision_packets),
                    transmitted_bytes_per_second=int(transmitted_bytes_per_second),
                    received_bytes_per_second=int(received_bytes_per_second),
                    uptime=uptime,
                )
            )

        return statistics
