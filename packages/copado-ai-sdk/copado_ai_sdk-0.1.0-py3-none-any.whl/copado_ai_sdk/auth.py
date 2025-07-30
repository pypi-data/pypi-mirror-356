from typing import Dict


class APIKeyAuth:
    """Simple `X-Authorization: <token>` header."""

    def __init__(self, api_key: str) -> None:
        self._api_key = api_key

    def headers(self) -> Dict[str, str]:
        return {"X-Authorization": self._api_key}
