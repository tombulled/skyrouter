import dataclasses

import bs4
import httpx

from . import enums
from . import models


@dataclasses.dataclass
class SkyHub:
    host: str

    username: str = "admin"
    password: str = "admin"

    session: httpx.Client = dataclasses.field(default_factory=httpx.Client, repr=False)

    def _url(self, endpoint: str = '') -> str:
        return f'http://{self.host}/{endpoint}'

    def system(self) -> models.System:
        uri = f'/{enums.Endpoint.SYSTEM}'
        url = self._url(enums.Endpoint.SYSTEM)
        response = self.session.get(url)
        soup = bs4.BeautifulSoup(response.text, 'html.parser')

        return soup
