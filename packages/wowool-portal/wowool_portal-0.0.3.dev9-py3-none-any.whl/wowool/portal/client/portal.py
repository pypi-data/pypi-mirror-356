from wowool.portal.client.defines import (
    WOWOOL_PORTAL_API_KEY_ENV_NAME,
    WOWOOL_PORTAL_HOST_DEFAULT,
    WOWOOL_PORTAL_HOST_ENV_NAME,
)
from wowool.portal.client.environment import resolve_variable
from wowool.portal.client.service import Service


class Portal:
    """
    :class:`Portal` is a class that holds the information required to connect to the Portal server. An instance of this class is passed to each :class:`Pipeline <wowool.portal.client.pipeline.Pipeline>` or :class:`Compiler <wowool.portal.client.compiler.Compiler>` instance so that the latter is able to send the required request:

    .. literalinclude:: init_pipeline.py
        :language: python

    Alternatively, instances of this class can also be used as a context manager avoiding the need to pass it to each pipeline or compiler explicitly:

    .. literalinclude:: init_pipeline_context.py
        :language: python
    """

    def __init__(self, api_key: str | None = None, host: str | None = None):
        self._api_key = resolve_variable(WOWOOL_PORTAL_API_KEY_ENV_NAME, api_key)
        self._host: str = resolve_variable(WOWOOL_PORTAL_HOST_ENV_NAME, host or WOWOOL_PORTAL_HOST_DEFAULT)
        headers = {
            "X-Api-Key": self._api_key,
            "X-Client": "wowool-portal-python",
            "X-Client-Version": "0.1.0",
        }
        self._service = Service(self._host, headers)

    def __repr__(self):
        return f"""wowool.portal.Portal(host="{self._host}", api_key="***{self._api_key[-3:]}")"""
