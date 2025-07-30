from enum import Enum
from typing import List, Optional, Dict, Any, Union
from datetime import datetime
from pydantic import BaseModel


class WorkspaceCapability(str, Enum):
    """Available workspace capabilities/features."""
    FOLLOW_UP_QUESTIONS = "FollowUpQuestions"
    DATA_ANALYSIS = "DataAnalysis"
    REASONING_MODE = "ReasoningMode"
    WEB_SEARCH = "WebSearch"
    DIAGRAM_GENERATION = "DiagramGeneration"
    DEVOPS_AUTOMATIONS = "DevOpsAutomations"
    
    # Additional capabilities returned by the API
    CUSTOM_KNOWLEDGE = "CustomKnowledge"
    ESSENTIALS_KNOWLEDGE = "EssentialsKnowledge"
    CRT_KNOWLEDGE = "CRTKnowledge"
    METADATA_FORMAT_KNOWLEDGE = "MetadataFormatKnowledge"
    SOURCE_FORMAT_KNOWLEDGE = "SourceFormatKnowledge"
    AGENT_FRAMEWORK = "AgentFramework"
    OTHER_KNOWLEDGE = "OtherKnowledge"


class WorkspaceMemberPermission(str, Enum):
    """Workspace member permission levels."""
    MANAGE = "Manage"
    MEMBER = "Member"


class IntegrationType(str, Enum):
    """Available integration types."""
    COPADO_CICD = "copado_cicd"


class IntegrationLevel(str, Enum):
    """Integration access levels."""
    MEMBER = "MEMBER"
    USER = "USER"


class TrackedAction(str, Enum):
    """Types of tracked activities."""
    DELETE_DATASET = "delete_dataset"
    CREATE_WORKSPACE = "create_workspace"
    DELETE_WORKSPACE = "delete_workspace"
    CREATE_DIALOGUE = "create_dialogue"
    DELETE_DIALOGUE = "delete_dialogue"
    SEND_MESSAGE = "send_message"
    UPLOAD_DOCUMENT = "upload_document"
    DELETE_DOCUMENT = "delete_document"


class MessageRole(str, Enum):
    """Message roles in dialogues."""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


# Data Models

class Document(BaseModel):
    """Document metadata."""
    id: str
    created_at: datetime
    modified_at: datetime
    created_by: int
    filename: str
    size: int


class WorkspaceMember(BaseModel):
    """Workspace member details."""
    id: str
    created_at: datetime
    modified_at: datetime
    created_by: int
    user_id: int
    permission: WorkspaceMemberPermission


class Assistant(BaseModel):
    """AI Assistant configuration."""
    id: str
    created_at: datetime
    modified_at: datetime
    created_by: int
    name: str
    visible_name: str
    is_builtin: bool
    agent: Optional[str] = None  # Can be None according to API response
    description: str = ""
    instructions: str = ""
    suggested_prompts: List[str] = []
    copado_knowledge: bool = True


class WorkspaceIntegration(BaseModel):
    """Workspace integration details."""
    id: str
    created_at: datetime
    modified_at: datetime
    created_by: int
    name: str
    workspace_id: str
    type: str
    level: str
    user_id: int
    config: Dict[str, Any] = {}


class Workspace(BaseModel):
    """Complete workspace details."""
    id: str
    created_at: datetime
    modified_at: datetime
    created_by: int
    name: str
    description: str = ""
    organization_id: int
    icon_url: Optional[str] = None
    default_dataset_id: Optional[str] = None
    members: List[WorkspaceMember] = []
    assistants: List[Assistant] = []
    current_user_member: Optional[WorkspaceMember] = None
    capabilities: List[WorkspaceCapability] = []
    integrations: List[WorkspaceIntegration] = []


class WorkspaceSummary(BaseModel):
    """Simplified workspace details for listing."""
    id: str
    created_at: datetime
    modified_at: datetime
    created_by: int
    name: str
    description: str = ""
    organization_id: int
    icon_url: Optional[str] = None


class WorkspaceCreate(BaseModel):
    """Data for creating a new workspace."""
    name: str
    description: str = ""
    icon_url: Optional[str] = None
    capabilities: List[WorkspaceCapability] = []


class WorkspaceUpdate(BaseModel):
    """Data for updating a workspace."""
    name: Optional[str] = None
    description: Optional[str] = None
    icon_url: Optional[str] = None
    capabilities: Optional[List[WorkspaceCapability]] = None
    default_dataset_id: Optional[str] = None


class WorkspaceMemberCreate(BaseModel):
    """Data for adding a workspace member."""
    user_id: int
    permission: WorkspaceMemberPermission = WorkspaceMemberPermission.MEMBER


class WorkspaceMemberUpdate(BaseModel):
    """Data for updating a workspace member."""
    permission: WorkspaceMemberPermission


class FollowUpQuestion(BaseModel):
    """Follow-up question suggestion."""
    question: str


class LearnMoreLink(BaseModel):
    """Learn more link in responses."""
    title: str
    url: str


class Plot(BaseModel):
    """Data visualization plot."""
    type: str
    data: Dict[str, Any]
    title: Optional[str] = None


class Message(BaseModel):
    """Message in a dialogue."""
    role: str
    content: str
    timestamp: str
    dialogue_id: str
    message_offset: int
    request_id: Optional[str] = None
    probability: Optional[float] = None
    learn_more_links: List[LearnMoreLink] = []
    follow_up_questions: List[FollowUpQuestion] = []
    plots: List[Plot] = []
    assistant: Optional[str] = None


class DialogueResponse(BaseModel):
    """Dialogue details without messages."""
    id: str
    name: str
    workspace_id: str
    message_count: int
    document_count: int
    assistant_id: str
    created_at: datetime


class DialogueWithMessages(BaseModel):
    """Complete dialogue with all messages."""
    id: str
    name: str
    workspace_id: str
    message_count: int
    document_count: int
    assistant_id: str
    created_at: datetime
    messages: List[Message] = []


class DialogueCreate(BaseModel):
    """Data for creating a new dialogue."""
    name: str
    workspace_id: str
    assistant_id: str = "knowledge"


class DialogueUpdate(BaseModel):
    """Data for updating a dialogue."""
    name: Optional[str] = None


class DevBuffer(BaseModel):
    """Development context buffer."""
    name: str
    content: str
    description: Optional[str] = None


class FunctionSchema(BaseModel):
    """Function schema for AI tools."""
    name: str
    parameters: Dict[str, Any]
    description: Optional[str] = None


class DevContext(BaseModel):
    """Development context for AI messages."""
    libraries: Optional[List[str]] = None
    functions: Optional[List[FunctionSchema]] = None
    buffers: Optional[List[DevBuffer]] = None


class MessageCreate(BaseModel):
    """Data for creating a new message."""
    request_id: str
    prompt: str
    dev_context: Optional[DevContext] = None
    system_prompt: Optional[str] = None
    assistant_id: Optional[str] = None
    integrations: Optional[Dict[str, Any]] = None
    tools: Optional[List[Dict[str, Any]]] = None
    tool_choice: Optional[str] = None
    messages: Optional[List[Dict[str, Any]]] = None


class FeedbackCreate(BaseModel):
    """Data for creating message feedback."""
    prompt: str
    response: str
    feedback: str
    sentiment: bool


class TrackedActivity(BaseModel):
    """Activity tracking entry."""
    id: str
    created_at: datetime
    user_id: int
    organization_id: int
    action: TrackedAction
    workspace_id: Optional[str] = None
    dataset_id: Optional[str] = None
    dialogue_id: Optional[str] = None
    member_user_id: Optional[int] = None
    message: Optional[str] = None


class UserActivity(BaseModel):
    """User activity summary."""
    user_id: int
    count_messages: int
    count_documents: int
    count_workspaces: int
    max_messages: int
    max_documents_total: int


class Organization(BaseModel):
    """Organization details."""
    icon_url: Optional[str] = None


class OrganizationUpdate(BaseModel):
    """Data for updating organization."""
    icon_url: Optional[str] = None


class IntegrationCreate(BaseModel):
    """Data for creating an integration."""
    name: str = ""
    workspace_id: str
    credential: Dict[str, Any] = {}
    config: Dict[str, str] = {}
    type: IntegrationType = IntegrationType.COPADO_CICD
    level: IntegrationLevel = IntegrationLevel.MEMBER


class IntegrationConfigure(BaseModel):
    """Data for configuring an integration."""
    config: Dict[str, str]
    type: IntegrationType


class IntegrationResponse(BaseModel):
    """Integration response data."""
    id: str
    name: str
    workspace_id: str
    config: Dict[str, str]
    level: str
    type: str


class HealthResponse(BaseModel):
    """Health check response."""
    release_id: str
    status: str


class SuccessResponse(BaseModel):
    """Generic success response."""
    detail: str 