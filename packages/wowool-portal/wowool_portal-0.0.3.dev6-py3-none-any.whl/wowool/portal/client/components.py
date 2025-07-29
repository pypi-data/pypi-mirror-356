from dataclasses import dataclass

from wowool.portal.client.error import ClientError
from wowool.portal.client.httpcode import HttpCode
from wowool.portal.client.portal import Portal


@dataclass
class Component:
    name: str
    type: str
    description: str


class Components:
    """
    :class:`Components` is a
    """

    def __init__(self, type: str = "", language: str = "", portal: Portal | None = None):
        self._portal = portal or Portal()
        self.type = type
        self.language = language
        self._components = self.get(type=type, language=language)

    def get(self, type: str = "", language: str = "", **kwargs):
        payload = self._portal._service.get(
            url="components/",
            status_code=HttpCode.OK,
            data={
                "type": type,
                "language": language,
            },
            **kwargs,
        )
        return [Component(**c) for c in payload]

    def __iter__(self):
        return iter(self._components)

    def __len__(self):
        return len(self._components)
