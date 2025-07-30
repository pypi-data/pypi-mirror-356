from typing import Optional, List, Union
from ..types import (
    Workspace, 
    WorkspaceSummary, 
    WorkspaceCreate, 
    WorkspaceUpdate,
    WorkspaceCapability,
    WorkspaceMember,
    WorkspaceMemberCreate,
    WorkspaceMemberUpdate,
    WorkspaceMemberPermission
)
from ..client import CopadoClient


class WorkspaceService:
    """
    Service for managing workspaces and their members.
    
    Workspaces are containers for AI conversations (dialogues) and provide
    different capabilities like data analysis, web search, diagram generation,
    and DevOps automations.
    """
    
    def __init__(self, client: CopadoClient) -> None:
        self._client = client

    def list(self) -> List[WorkspaceSummary]:
        """
        List all workspaces for the organization.
        
        Returns:
            List of workspace summaries
        """
        url = f"/organizations/{self._client.organization_id}/workspaces"
        response = self._client._request("GET", url)
        return [WorkspaceSummary(**ws) for ws in response.json()]

    def create(
        self,
        name: str,
        description: Optional[str] = None,
        icon_url: Optional[str] = None,
        capabilities: Optional[List[WorkspaceCapability]] = None,
    ) -> Workspace:
        """
        Create a new workspace.
        
        Args:
            name: Workspace name
            description: Optional workspace description
            icon_url: Optional icon URL in data URI format
            capabilities: List of capabilities to enable for this workspace
            
        Returns:
            Complete workspace details including members and assistants
        """
        url = f"/organizations/{self._client.organization_id}/workspaces"
        
        payload = {
            "name": name,
            "description": description or "",
        }
        
        if icon_url:
            payload["icon_url"] = icon_url
            
        if capabilities:
            payload["capabilities"] = [cap.value for cap in capabilities]
            
        response = self._client._request("POST", url, json=payload)
        return Workspace(**response.json())

    def create_with_features(
        self,
        name: str,
        description: Optional[str] = None,
        enable_data_analysis: bool = False,
        enable_web_search: bool = False,
        enable_diagram_generation: bool = False,
        enable_devops_automations: bool = False,
        enable_reasoning_mode: bool = False,
        enable_follow_up_questions: bool = True,
    ) -> Workspace:
        """
        Create a workspace with specific features enabled.
        
        This is a convenience method that makes it easy to enable specific
        capabilities without dealing with the enum values directly.
        
        Args:
            name: Workspace name
            description: Optional workspace description
            enable_data_analysis: Enable CSV/XLSX file analysis
            enable_web_search: Enable web search capabilities
            enable_diagram_generation: Enable Mermaid diagram generation
            enable_devops_automations: Enable DevOps agent automations
            enable_reasoning_mode: Enable step-by-step reasoning display
            enable_follow_up_questions: Enable follow-up question suggestions
            
        Returns:
            Complete workspace details
        """
        capabilities = []
        
        if enable_follow_up_questions:
            capabilities.append(WorkspaceCapability.FOLLOW_UP_QUESTIONS)
        if enable_data_analysis:
            capabilities.append(WorkspaceCapability.DATA_ANALYSIS)
        if enable_web_search:
            capabilities.append(WorkspaceCapability.WEB_SEARCH)
        if enable_diagram_generation:
            capabilities.append(WorkspaceCapability.DIAGRAM_GENERATION)
        if enable_devops_automations:
            capabilities.append(WorkspaceCapability.DEVOPS_AUTOMATIONS)
        if enable_reasoning_mode:
            capabilities.append(WorkspaceCapability.REASONING_MODE)
            
        return self.create(name, description, capabilities=capabilities)

    def create_with_knowledge_capabilities(
        self,
        name: str,
        description: Optional[str] = None,
        enable_custom_knowledge: bool = False,
        enable_essentials_knowledge: bool = False,
        enable_crt_knowledge: bool = False,
        enable_metadata_format_knowledge: bool = False,
        enable_source_format_knowledge: bool = False,
        enable_follow_up_questions: bool = True,
    ) -> Workspace:
        """
        Create a workspace with specific Copado knowledge capabilities enabled.
        
        This method allows you to specifically control which knowledge types
        are available to the AI assistant in this workspace.
        
        Args:
            name: Workspace name
            description: Optional workspace description
            enable_custom_knowledge: Enable custom knowledge base access
            enable_essentials_knowledge: Enable Copado Essentials knowledge
            enable_crt_knowledge: Enable CRT (Copado Robotic Testing) knowledge
            enable_metadata_format_knowledge: Enable metadata format knowledge
            enable_source_format_knowledge: Enable source format knowledge
            enable_follow_up_questions: Enable follow-up question suggestions
            
        Returns:
            Complete workspace details
        """
        capabilities = []
        
        if enable_follow_up_questions:
            capabilities.append(WorkspaceCapability.FOLLOW_UP_QUESTIONS)
        if enable_custom_knowledge:
            capabilities.append(WorkspaceCapability.CUSTOM_KNOWLEDGE)
        if enable_essentials_knowledge:
            capabilities.append(WorkspaceCapability.ESSENTIALS_KNOWLEDGE)
        if enable_crt_knowledge:
            capabilities.append(WorkspaceCapability.CRT_KNOWLEDGE)
        if enable_metadata_format_knowledge:
            capabilities.append(WorkspaceCapability.METADATA_FORMAT_KNOWLEDGE)
        if enable_source_format_knowledge:
            capabilities.append(WorkspaceCapability.SOURCE_FORMAT_KNOWLEDGE)
            
        return self.create(name, description, capabilities=capabilities)

    def get(self, workspace_id: str) -> Workspace:
        """
        Get a specific workspace by ID.
        
        Args:
            workspace_id: The workspace ID
            
        Returns:
            Complete workspace details including members and assistants
        """
        url = f"/organizations/{self._client.organization_id}/workspaces/{workspace_id}"
        response = self._client._request("GET", url)
        return Workspace(**response.json())

    def update(
        self,
        workspace_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        icon_url: Optional[str] = None,
        capabilities: Optional[List[WorkspaceCapability]] = None,
        default_dataset_id: Optional[str] = None,
    ) -> Workspace:
        """
        Update a workspace.
        
        Args:
            workspace_id: The workspace ID
            name: New workspace name
            description: New workspace description
            icon_url: New icon URL in data URI format
            capabilities: New list of capabilities
            default_dataset_id: New default dataset ID
            
        Returns:
            Updated workspace details
        """
        url = f"/organizations/{self._client.organization_id}/workspaces/{workspace_id}"
        payload = {}
        
        if name is not None:
            payload["name"] = name
        if description is not None:
            payload["description"] = description
        if icon_url is not None:
            payload["icon_url"] = icon_url
        if capabilities is not None:
            payload["capabilities"] = [cap.value for cap in capabilities]
        if default_dataset_id is not None:
            payload["default_dataset_id"] = default_dataset_id
            
        response = self._client._request("PATCH", url, json=payload)
        return Workspace(**response.json())

    def delete(self, workspace_id: str) -> None:
        """
        Delete a workspace.
        
        Warning: This will delete all dialogues and documents in the workspace.
        
        Args:
            workspace_id: The workspace ID
        """
        url = f"/organizations/{self._client.organization_id}/workspaces/{workspace_id}"
        self._client._request("DELETE", url)

    def add_member(
        self,
        workspace_id: str,
        user_id: int,
        permission: WorkspaceMemberPermission = WorkspaceMemberPermission.MEMBER,
    ) -> WorkspaceMember:
        """
        Add a member to a workspace.
        
        Args:
            workspace_id: The workspace ID
            user_id: The user ID to add
            permission: The permission level for the user
            
        Returns:
            Member details
        """
        url = f"/organizations/{self._client.organization_id}/workspaces/{workspace_id}/members"
        payload = {
            "user_id": user_id,
            "permission": permission.value,
        }
        response = self._client._request("POST", url, json=payload)
        return WorkspaceMember(**response.json())

    def update_member(
        self,
        workspace_id: str,
        member_id: str,
        permission: WorkspaceMemberPermission,
    ) -> WorkspaceMember:
        """
        Update a member's permission in a workspace.
        
        Args:
            workspace_id: The workspace ID
            member_id: The member ID
            permission: The new permission level
            
        Returns:
            Updated member details
        """
        url = f"/organizations/{self._client.organization_id}/workspaces/{workspace_id}/members/{member_id}"
        payload = {"permission": permission.value}
        response = self._client._request("PATCH", url, json=payload)
        return WorkspaceMember(**response.json())

    def remove_member(self, workspace_id: str, member_id: str) -> None:
        """
        Remove a member from a workspace.
        
        Args:
            workspace_id: The workspace ID
            member_id: The member ID to remove
        """
        url = f"/organizations/{self._client.organization_id}/workspaces/{workspace_id}/members/{member_id}"
        self._client._request("DELETE", url)

    def get_or_create(
        self, 
        name: str, 
        description: Optional[str] = None,
        capabilities: Optional[List[WorkspaceCapability]] = None,
    ) -> Workspace:
        """
        Get an existing workspace by name or create a new one.
        
        Args:
            name: Workspace name to search for or create
            description: Description for new workspace if created
            capabilities: Capabilities for new workspace if created
            
        Returns:
            Existing or newly created workspace
        """
        workspaces = self.list()
        for workspace in workspaces:
            if workspace.name == name:
                return self.get(workspace.id)
        return self.create(name, description, capabilities=capabilities)

    def enable_capability(
        self, 
        workspace_id: str, 
        capability: WorkspaceCapability
    ) -> Workspace:
        """
        Enable a specific capability for a workspace.
        
        Args:
            workspace_id: The workspace ID
            capability: The capability to enable
            
        Returns:
            Updated workspace details
        """
        workspace = self.get(workspace_id)
        current_capabilities = workspace.capabilities
        
        if capability not in current_capabilities:
            current_capabilities.append(capability)
            return self.update(workspace_id, capabilities=current_capabilities)
        return workspace

    def disable_capability(
        self, 
        workspace_id: str, 
        capability: WorkspaceCapability
    ) -> Workspace:
        """
        Disable a specific capability for a workspace.
        
        Args:
            workspace_id: The workspace ID
            capability: The capability to disable
            
        Returns:
            Updated workspace details
        """
        workspace = self.get(workspace_id)
        current_capabilities = workspace.capabilities
        
        if capability in current_capabilities:
            current_capabilities.remove(capability)
            return self.update(workspace_id, capabilities=current_capabilities)
        return workspace

    def has_capability(self, workspace_id: str, capability: WorkspaceCapability) -> bool:
        """
        Check if a workspace has a specific capability enabled.
        
        Args:
            workspace_id: The workspace ID
            capability: The capability to check
            
        Returns:
            True if the capability is enabled
        """
        workspace = self.get(workspace_id)
        return capability in workspace.capabilities

    def list_datasets(self, workspace_id: str) -> List:
        """
        List datasets owned by the workspace.
        
        Args:
            workspace_id: The workspace ID
            
        Returns:
            List of datasets owned by this workspace
        """
        url = f"/organizations/{self._client.organization_id}/workspaces/{workspace_id}/datasets"
        response = self._client._request("GET", url)
        return response.json()