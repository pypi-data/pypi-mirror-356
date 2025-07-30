from typing import Optional, Dict, Any

from ..client import CopadoClient


class OrganizationService:
    def __init__(self, client: CopadoClient) -> None:
        self._client = client

    def get(self) -> Dict[str, Any]:
        """Get organization details."""
        url = f"/organizations/{self._client.organization_id}/"
        return self._client._request("GET", url).json()

    def update(
        self,
        name: Optional[str] = None,
        settings: Optional[Dict[str, Any]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Update organization details."""
        url = f"/organizations/{self._client.organization_id}/"
        payload = {}
        if name:
            payload["name"] = name
        if settings:
            payload["settings"] = settings
        if metadata:
            payload["metadata"] = metadata
        return self._client._request("PATCH", url, json=payload).json()

    def check_system_status(self) -> Dict[str, Any]:
        """Check the system status for the organization."""
        url = f"/organizations/{self._client.organization_id}/check-system-status"
        return self._client._request("GET", url).json()

    def healthz(self) -> Dict[str, Any]:
        """Check the health of the API."""
        return self._client._request("GET", "/healthz").json()


