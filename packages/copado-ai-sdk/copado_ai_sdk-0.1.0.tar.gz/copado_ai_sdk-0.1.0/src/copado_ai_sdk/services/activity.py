from typing import Optional, Dict, Any, List
from datetime import datetime
from ..client import CopadoClient


class ActivityService:
    def __init__(self, client: CopadoClient) -> None:
        self._client = client

    def list(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[Dict[str, Any]]:
        """List activity for the organization."""
        url = f"/organizations/{self._client.organization_id}/activity"
        params = {"limit": limit, "offset": offset}
        if start_date:
            params["start_date"] = start_date.isoformat()
        if end_date:
            params["end_date"] = end_date.isoformat()
        
        return self._client._request("GET", url, params=params).json()

    def summary(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> Dict[str, Any]:
        """Get activity summary for the organization."""
        url = f"/organizations/{self._client.organization_id}/activity/summary"
        params = {}
        if start_date:
            params["start_date"] = start_date.isoformat()
        if end_date:
            params["end_date"] = end_date.isoformat()
        
        return self._client._request("GET", url, params=params).json() 