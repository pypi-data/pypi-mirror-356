# Copado AI SDK Features Guide

A comprehensive reference guide to all available features and functions in the Copado AI SDK.

## Table of Contents
- [Workspace Management](#workspace-management)
- [Dialogue & Chat](#dialogue--chat)
- [Document Management](#document-management)
- [Integrations](#integrations)
- [Activity & Analytics](#activity--analytics)
- [Organization Management](#organization-management)
- [Error Handling](#error-handling)
- [Advanced Usage](#advanced-usage)

---

## Workspace Management

### List & Get Workspaces
```python
# List all workspaces
workspaces = client.workspaces.list()

# Get specific workspace
workspace = client.workspaces.get(workspace_id: str)

# Get or create workspace by name
workspace = client.workspaces.get_or_create(
    name: str,
    description: Optional[str] = None,
    capabilities: Optional[List[WorkspaceCapability]] = None
)

# Set as current workspace
client.set_workspace(workspace.id)
```

### Create Workspaces
```python
# Basic creation
workspace = client.workspaces.create(
    name: str,
    description: Optional[str] = None,
    icon_url: Optional[str] = None,
    capabilities: Optional[List[WorkspaceCapability]] = None
)

# Create with specific features
workspace = client.workspaces.create_with_features(
    name: str,
    description: Optional[str] = None,
    enable_data_analysis: bool = False,
    enable_web_search: bool = False,
    enable_diagram_generation: bool = False,
    enable_devops_automations: bool = False,
    enable_reasoning_mode: bool = False,
    enable_follow_up_questions: bool = True
)

# Create with knowledge capabilities
workspace = client.workspaces.create_with_knowledge_capabilities(
    name: str,
    description: Optional[str] = None,
    enable_custom_knowledge: bool = False,
    enable_essentials_knowledge: bool = False,
    enable_crt_knowledge: bool = False,
    enable_metadata_format_knowledge: bool = False,
    enable_source_format_knowledge: bool = False,
    enable_follow_up_questions: bool = True
)
```

### Update & Delete Workspaces
```python
# Update workspace
workspace = client.workspaces.update(
    workspace_id: str,
    name: Optional[str] = None,
    description: Optional[str] = None,
    icon_url: Optional[str] = None,
    capabilities: Optional[List[WorkspaceCapability]] = None,
    default_dataset_id: Optional[str] = None
)

# Delete workspace (WARNING: Deletes all dialogues and documents)
client.workspaces.delete(workspace_id: str)
```

### Capability Management
```python
from copado_ai_sdk.types import WorkspaceCapability

# Enable/disable capabilities
workspace = client.workspaces.enable_capability(workspace_id: str, capability: WorkspaceCapability)
workspace = client.workspaces.disable_capability(workspace_id: str, capability: WorkspaceCapability)

# Check capability
has_capability = client.workspaces.has_capability(workspace_id: str, capability: WorkspaceCapability)

# Available capabilities
# WorkspaceCapability.DATA_ANALYSIS
# WorkspaceCapability.WEB_SEARCH
# WorkspaceCapability.DIAGRAM_GENERATION
# WorkspaceCapability.DEVOPS_AUTOMATIONS
# WorkspaceCapability.REASONING_MODE
# WorkspaceCapability.FOLLOW_UP_QUESTIONS
# WorkspaceCapability.CUSTOM_KNOWLEDGE
# WorkspaceCapability.ESSENTIALS_KNOWLEDGE
# WorkspaceCapability.CRT_KNOWLEDGE
# WorkspaceCapability.METADATA_FORMAT_KNOWLEDGE
# WorkspaceCapability.SOURCE_FORMAT_KNOWLEDGE
```

### Member Management
```python
from copado_ai_sdk.types import WorkspaceMemberPermission

# Add member
member = client.workspaces.add_member(
    workspace_id: str,
    user_id: int,
    permission: WorkspaceMemberPermission = WorkspaceMemberPermission.MEMBER
)

# Update member permission
member = client.workspaces.update_member(
    workspace_id: str,
    member_id: str,
    permission: WorkspaceMemberPermission
)

# Remove member
client.workspaces.remove_member(workspace_id: str, member_id: str)

# Permission levels
# WorkspaceMemberPermission.OWNER
# WorkspaceMemberPermission.ADMIN
# WorkspaceMemberPermission.MEMBER
# WorkspaceMemberPermission.VIEWER
```

### Session Management
```python
# Get current workspace ID (may be None if no workspace set)
workspace_id = client.get_workspace_id()

# Set/switch to a workspace
client.set_workspace("workspace-id")

# Alternative: switch workspace (same as set_workspace)
client.switch_workspace("another-workspace-id")

# Check current workspace details
if client.current_workspace_id:
    current_workspace = client.workspaces.get(client.current_workspace_id)
    print(f"Using: {current_workspace.name}")
else:
    print("No workspace set")
```

### Datasets
```python
# List workspace datasets
datasets = client.workspaces.list_datasets(workspace_id: str)
```

---

## Dialogue & Chat

### Create & Manage Dialogues
```python
# Create dialogue
dialogue = client.dialogues.create(
    name: str,
    workspace_id: Optional[str] = None,      # Uses current session workspace if None
    workspace_name: Optional[str] = None,   # Alternative to workspace_id
    assistant_id: str = "knowledge",
    x_client: Optional[str] = None
)
# Note: If no workspace_id/workspace_name provided and no current workspace set, 
# this will raise an error with guidance on how to set a workspace

# List dialogues
dialogues = client.dialogues.list(
    workspace_id: Optional[str] = None,
    limit: int = 100,
    offset: int = 0
)

# Get dialogue with messages
dialogue = client.dialogues.get(dialogue_id: str)

# Update dialogue
dialogue = client.dialogues.update(dialogue_id: str, name: Optional[str] = None)

# Delete dialogue
client.dialogues.delete(dialogue_id: str)
```

### Chat & Messaging
```python
from copado_ai_sdk.types import DevContext

# Send message and get response
response = client.dialogues.chat(
    dialogue_id: str,
    prompt: str,
    request_id: Optional[str] = None,      # Auto-generated if None
    assistant_id: Optional[str] = None,
    stream: bool = False,                  # Stream to stdout
    dev_context: Optional[DevContext] = None,
    system_prompt: Optional[str] = None
)

# Chat with document uploads
response = client.dialogues.chat_with_documents(
    dialogue_id: str,
    prompt: str,
    document_paths: List[Union[str, Path]],
    stream: bool = False,
    assistant_id: Optional[str] = None
)

# Cancel message
result = client.dialogues.cancel_message(dialogue_id: str, request_id: str)
```

### Document Management in Dialogues
```python
# Upload document to dialogue
document = client.dialogues.upload_document(
    dialogue_id: str,
    file_path: Union[str, Path],
    filename: Optional[str] = None
)

# List documents in dialogue
documents = client.dialogues.list_documents(dialogue_id: str)

# Delete document from dialogue
client.dialogues.delete_document(dialogue_id: str, filename: str)

# Get document stats
count = client.dialogues.get_document_count(dialogue_id: str)
size = client.dialogues.get_document_total_size(dialogue_id: str)
```

### Feedback
```python
# Create feedback for message
feedback = client.dialogues.create_feedback(
    dialogue_id: str,
    request_id: str,
    prompt: str,
    response: str,
    feedback: str,
    sentiment: bool
)
```

---

## Document Management

### Upload Documents
```python
# Upload to dialogue
document = client.documents.upload_to_dialogue(
    dialogue_id: str,
    file_path: Union[str, Path],
    filename: Optional[str] = None
)

# Upload to dataset (workspace-level)
document = client.documents.upload_to_dataset(
    dataset_id: str,
    file_path: Union[str, Path],
    filename: Optional[str] = None
)

# Update document (replace existing)
document = client.documents.update_in_dialogue(
    dialogue_id: str,
    file_path: Union[str, Path],
    filename: Optional[str] = None
)
```

### List & Delete Documents
```python
# List documents in dialogue
documents = client.documents.list_in_dialogue(dialogue_id: str)

# Delete document from dialogue
client.documents.delete_from_dialogue(dialogue_id: str, filename: str)

# Get document statistics
count = client.documents.get_dialogue_document_count(dialogue_id: str)
total_size = client.documents.get_dialogue_document_size(dialogue_id: str)
```

### Supported File Types
The SDK supports various file types for analysis:

- **CSV/XLSX** - Data analysis and visualization
- **PDF** - Knowledge reference and content extraction
- **Text files** (.txt, .md) - Content analysis
- **Images** (.png, .jpg, .gif) - Visual analysis
- **Word documents** (.docx) - Document analysis
- **PowerPoint** (.pptx) - Presentation analysis
- **JSON/XML** - Configuration and data files
- **Code files** (.py, .js, .yml, etc.) - Code analysis

---

## Integrations

### Integration Management
```python
# List integrations
integrations = client.integrations.list()

# Create integration
integration = client.integrations.create(
    name: str,
    type: str,
    configuration: Dict[str, Any],
    metadata: Optional[Dict[str, Any]] = None
)

# Configure integration (simplified)
result = client.integrations.configure(
    type: str,
    configuration: Dict[str, Any]
)

# Delete integration
client.integrations.delete(integration_id: str)
```

### Integration Types
Common integration types include:
- **github** - GitHub repository integration
- **jira** - Jira project management
- **slack** - Slack notifications
- **salesforce** - Salesforce DevOps Center
- **custom** - Custom webhook integrations

---

## Activity & Analytics

### Activity Tracking
```python
from datetime import datetime

# List activities
activities = client.activity.list(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    limit: int = 100,
    offset: int = 0
)

# Get activity summary
summary = client.activity.summary(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
)
```

### Activity Types
Activities tracked include:
- Dialogue creation and updates
- Document uploads and analysis
- Workspace modifications
- Integration usage
- User interactions

---

## Organization Management

### Organization Operations
```python
# Get organization details
org = client.organization.get()

# Update organization
org = client.organization.update(
    name: Optional[str] = None,
    settings: Optional[Dict[str, Any]] = None,
    metadata: Optional[Dict[str, Any]] = None
)

# Check system status
status = client.organization.check_system_status()

# Health check
health = client.organization.healthz()
```

---

## Error Handling

### Exception Types
```python
from copado_ai_sdk.exceptions import (
    CopadoAPIException,
    AuthenticationError,
    ValidationError,
    ResourceNotFoundError,
    RateLimitError
)

try:
    dialogue = client.dialogues.create(name="Test")
except AuthenticationError:
    print("Invalid API key or credentials")
except ValidationError as e:
    print(f"Validation error: {e}")
except ResourceNotFoundError:
    print("Workspace or resource not found")
except RateLimitError:
    print("Rate limit exceeded, please retry later")
except CopadoAPIException as e:
    print(f"API error: {e}")
```

### Retry Logic
```python
import time
from copado_ai_sdk.exceptions import RateLimitError

def robust_chat(client, dialogue_id, prompt, max_retries=3):
    for attempt in range(max_retries):
        try:
            return client.dialogues.chat(dialogue_id=dialogue_id, prompt=prompt)
        except RateLimitError:
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
                continue
            raise
```

---

## Advanced Usage

### Environment Configuration
```python
import os
from copado_ai_sdk import CopadoClient

# Set environment variables
os.environ["COPADO_API_KEY"] = "your-api-key"
os.environ["COPADO_ORG_ID"] = "12345"
os.environ["COPADO_BASE_URL"] = "https://copadogpt-api.robotic.copado.com"
os.environ["COPADO_WORKSPACE_ID"] = "workspace-id"

# Client will automatically pick up environment variables
client = CopadoClient()
```

### Configuration File
```python
# config.json
{
    "api_key": "your-api-key",
    "organization_id": 12345,
    "base_url": "https://copadogpt-api.robotic.copado.com",
    "workspace_id": "optional-workspace-id"
}

# Load from config
client = CopadoClient.from_config("config.json")
```

### Async Support
```python
import asyncio
from copado_ai_sdk import AsyncCopadoClient

async def async_example():
    async with AsyncCopadoClient(api_key="key", organization_id=123) as client:
        dialogue = await client.dialogues.create(name="Async Chat")
        response = await client.dialogues.chat(
            dialogue_id=dialogue.id,
            prompt="Hello async world!"
        )
        return response

# Run async code
response = asyncio.run(async_example())
```

### Bulk Operations
```python
# Upload multiple documents
documents = []
for file_path in ["file1.pdf", "file2.csv", "file3.json"]:
    doc = client.dialogues.upload_document(dialogue_id, file_path)
    documents.append(doc)

# Batch chat with multiple prompts
prompts = [
    "Analyze the PDF document",
    "Summarize the CSV data",
    "Validate the JSON configuration"
]

responses = []
for prompt in prompts:
    response = client.dialogues.chat(dialogue_id=dialogue.id, prompt=prompt)
    responses.append(response)
```

### Streaming Responses
```python
# Stream responses for long-running operations
response = client.dialogues.chat(
    dialogue_id=dialogue.id,
    prompt="Generate a comprehensive Copado CI/CD pipeline",
    stream=True  # Outputs to console as it generates
)

# The response is returned once streaming completes
print(f"Final response: {response}")
```

### Custom Headers and Request Options
```python
# Initialize with custom headers
client = CopadoClient(
    api_key="your-key",
    organization_id=123,
    headers={"X-Custom-Header": "value"}
)

# Per-request customization
response = client.dialogues.chat(
    dialogue_id=dialogue.id,
    prompt="Hello",
    x_client="custom-client-identifier"
)
```

### Knowledge Integration Patterns

#### CRT (Copado Robotic Testing) Knowledge
```python
# Create workspace with CRT knowledge
workspace = client.workspaces.create_with_knowledge_capabilities(
    name="CRT Testing Workspace",
    enable_crt_knowledge=True
)

# Ask CRT-specific questions
response = client.dialogues.chat(
    dialogue_id=dialogue.id,
    prompt="How do I create a CRT test for login functionality?"
)
```

#### Copado Essentials Knowledge
```python
# Enable Essentials knowledge
workspace = client.workspaces.create_with_knowledge_capabilities(
    name="Essentials Workspace",
    enable_essentials_knowledge=True
)

# Ask about Copado platform features
response = client.dialogues.chat(
    dialogue_id=dialogue.id,
    prompt="Explain the deployment pipeline best practices in Copado"
)
```

#### Custom Knowledge Base
```python
# Create workspace for custom knowledge
workspace = client.workspaces.create_with_knowledge_capabilities(
    name="Custom Knowledge Workspace",
    enable_custom_knowledge=True
)

# Upload custom documentation
client.dialogues.upload_document(dialogue.id, "company_devops_guide.pdf")
client.dialogues.upload_document(dialogue.id, "custom_scripts.zip")

# Query against custom knowledge
response = client.dialogues.chat(
    dialogue_id=dialogue.id,
    prompt="Based on our company guide, what's the process for hotfixes?"
)
```