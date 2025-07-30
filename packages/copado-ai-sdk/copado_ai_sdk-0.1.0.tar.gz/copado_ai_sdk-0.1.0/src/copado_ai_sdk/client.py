from __future__ import annotations

import httpx
from typing import Optional, Any, Dict

from .auth import APIKeyAuth
from .exceptions import HTTPError


class CopadoClient:
    """
    High-level entrypoint for the Copado AI SDK.
    
    Provides access to all Copado AI services:
    - workspaces: Workspace management with capabilities like data analysis, 
      web search, diagram generation, and DevOps automations
    - dialogues: AI conversations and chat functionality with document support
    - documents: Document management within dialogues for AI analysis
    - integrations: External system integrations (Copado CI/CD)
    - activity: Usage monitoring and analytics
    - organization: Organization-level settings and status
    
    Key Features Supported:
    - DevOps Agent Automations: Enable agents to take actions in Copado CI/CD
    - Data Analysis: Upload CSV/XLSX files for analytical tasks and visualizations
    - Follow Up Questions: Get additional question suggestions
    - Reasoning Mode: Display step-by-step thinking for complex tasks
    - Web Search: Enable web-based information retrieval
    - Diagram Generation: Create Mermaid diagrams from textual descriptions
    
    Session Persistence:
    - Pass workspace_id to reuse existing workspace across sessions
    - Access current_workspace_id to save for future sessions
    - No automatic workspace creation - create workspaces explicitly
    """

    def __init__(
        self,
        base_url: str,
        api_key: str,
        organization_id: int,
        workspace_id: Optional[str] = None,
        timeout: float = 20.0,
        httpx_client: Optional[httpx.Client] = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.organization_id = organization_id
        self._auth = APIKeyAuth(api_key)
        self._http = httpx_client or httpx.Client(base_url=self.base_url, timeout=timeout)

        from .services.dialogue import DialogueService
        from .services.document import DocumentService
        from .services.workspace import WorkspaceService
        from .services.integration import IntegrationService
        from .services.activity import ActivityService
        from .services.organization import OrganizationService

        self.dialogues = DialogueService(self)
        self.documents = DocumentService(self)
        self.workspaces = WorkspaceService(self)
        self.integrations = IntegrationService(self)
        self.activity = ActivityService(self)
        self.organization = OrganizationService(self)
        self.current_workspace_id = self._initialize_workspace(workspace_id) if workspace_id else None

    def _initialize_workspace(self, workspace_id: str) -> str:
        """
        Initialize workspace for the session.
        
        Validates that the provided workspace exists and user has access.
        
        Args:
            workspace_id: Existing workspace ID to use
            
        Returns:
            The validated workspace ID
            
        Raises:
            HTTPError: If workspace doesn't exist or user lacks access
        """
        try:
            workspace = self.workspaces.get(workspace_id)
            return workspace.id
        except HTTPError as e:
            if "404" in str(e):
                raise HTTPError(f"Workspace {workspace_id} not found or access denied")
            raise

    def get_workspace_id(self) -> Optional[str]:
        """
        Get the current workspace ID for this session.
        
        Save this ID to reuse the same workspace in future sessions.
        
        Returns:
            Current workspace ID if set, None otherwise
        """
        return self.current_workspace_id

    def switch_workspace(self, workspace_id: str) -> str:
        """
        Switch to a different workspace for this session.
        
        Args:
            workspace_id: ID of workspace to switch to
            
        Returns:
            The new current workspace ID
            
        Raises:
            HTTPError: If workspace doesn't exist or user lacks access
        """
        validated_id = self._initialize_workspace(workspace_id)
        self.current_workspace_id = validated_id
        return validated_id

    def set_workspace(self, workspace_id: str) -> str:
        """
        Set the current workspace for this session.
        
        Alias for switch_workspace for convenience.
        
        Args:
            workspace_id: ID of workspace to use
            
        Returns:
            The current workspace ID
        """
        return self.switch_workspace(workspace_id)

    def _headers(self) -> Dict[str, str]:
        return {
            "Accept": "application/json",
            "Content-Type": "application/json",
            **self._auth.headers(),
        }

    def _request(
        self, method: str, url: str, *, json: Any | None = None, **kwargs
    ) -> httpx.Response:
        kwargs.pop('stream', None)
        
        if 'files' in kwargs:
            headers = self._auth.headers()
            headers["Accept"] = "application/json"
        else:
            headers = self._headers()
            
        resp = self._http.request(method, url, headers=headers, json=json, **kwargs)
            
        if resp.status_code >= 400:
            raise HTTPError(f"{resp.status_code} – {resp.text}")
        return resp

    def close(self) -> None:
        """Close the underlying httpx client."""
        self._http.close()

    def __enter__(self) -> "CopadoClient":
        return self

    def __exit__(self, *_exc) -> None:
        self.close()
