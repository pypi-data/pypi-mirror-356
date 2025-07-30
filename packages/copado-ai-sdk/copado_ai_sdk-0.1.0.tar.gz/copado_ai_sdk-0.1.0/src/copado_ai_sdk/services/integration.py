from typing import Optional, Dict, Any, List
from ..client import CopadoClient


class IntegrationService:
    def __init__(self, client: CopadoClient) -> None:
        self._client = client

    def list(self) -> List[Dict[str, Any]]:
        """List all integrations for the organization."""
        url = f"/organizations/{self._client.organization_id}/integrations"
        return self._client._request("GET", url).json()

    def create(
        self,
        name: str,
        type: str,
        configuration: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Create a new integration."""
        url = f"/organizations/{self._client.organization_id}/integrations"
        payload = {
            "name": name,
            "type": type,
            "configuration": configuration,
        }
        if metadata:
            payload["metadata"] = metadata
        return self._client._request("POST", url, json=payload).json()

    def configure(
        self,
        type: str,
        configuration: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Configure an integration (simplified endpoint)."""
        url = f"/organizations/{self._client.organization_id}/integrations/configure"
        payload = {
            "type": type,
            "configuration": configuration,
        }
        return self._client._request("POST", url, json=payload).json()

    def delete(self, integration_id: str) -> None:
        """Delete an integration."""
        url = f"/organizations/{self._client.organization_id}/integrations/{integration_id}"
        self._client._request("DELETE", url) 