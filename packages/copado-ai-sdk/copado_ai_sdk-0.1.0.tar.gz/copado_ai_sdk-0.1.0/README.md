# Copado AI SDK

The official Python SDK for Copado AI Platform. Build intelligent automation, chat with your data, and integrate Copado's AI capabilities into your DevOps workflows.

## 🚀 Quick Start

### Installation

Install the SDK using pip:

```bash
pip install copado-ai-sdk
```

### Prerequisites

Before using the SDK, you'll need:

1. **Copado AI Organization** - Access to a Copado AI Platform organization
2. **Personal Access Key** - API key generated from your Copado AI Platform profile
3. **Organization ID** - Your organization's ID from the platform

### Getting Your Credentials

#### 1. Create a Personal Access Key
1. Navigate to your profile in the Copado AI Platform
2. Click the **New Key** button
3. Give it a name (e.g., "Python SDK Key")
4. Click **Submit** and copy the key value

#### 2. Get Your Organization ID
1. Click your profile icon on the top right
2. Select **Organization** to see your Org ID

### Authentication & Setup

Choose your base URL based on your region:

```python
from copado_ai_sdk import CopadoClient

# Region-specific base URLs
BASE_URLS = {
    "US": "https://copadogpt-api.robotic.copado.com",
    "EU": "https://copadogpt-api.eu-robotic.copado.com", 
    "Australia": "https://copadogpt-api.au-robotic.copado.com",
    "Singapore": "https://copadogpt-api.sg-robotic.copado.com"
}

# Initialize client with your region
client = CopadoClient(
    base_url=BASE_URLS["US"],  # Choose your region
    api_key="your-personal-access-key",
    organization_id=12345  # Your org ID
)
```

### Create Your First Workspace

```python
# Create a workspace with AI capabilities
workspace = client.workspaces.create_with_features(
    name="My Project Workspace",
    description="Workspace for my automation project",
    enable_data_analysis=True,
    enable_web_search=True,
    enable_reasoning_mode=True
)

# Set as current workspace
client.set_workspace(workspace.id)

# Save the workspace ID for future sessions
print(f"Save this for future sessions: {workspace.id}")
```

### Start Chatting

```python
# Create a dialogue (conversation)
dialogue = client.dialogues.create(name="My First Chat")

# Send a message and get AI response
response = client.dialogues.chat(
    dialogue_id=dialogue.id,
    prompt="Hello! How can you help me with Copado DevOps?",
    stream=True  # Streams response to console
)

print(response)
```

## 📖 Usage Patterns

### Using an Existing Workspace

```python
# If you already have a workspace ID
client = CopadoClient(
    base_url="https://copadogpt-api.robotic.copado.com",
    api_key="your-api-key",
    organization_id=123,
    workspace_id="your-saved-workspace-id"  # Use existing workspace
)

# Ready to use immediately - no need to create/set workspace
dialogue = client.dialogues.create(name="Continuing Work")
```

### Session Management

```python
# Check current workspace
workspace_id = client.get_workspace_id()
if workspace_id:
    print(f"Using workspace: {workspace_id}")
else:
    print("No workspace set")

# Switch between workspaces
client.set_workspace("workspace-id-1")  # Switch to different workspace
client.switch_workspace("workspace-id-2")  # Alternative method

# For environment-based persistence
import os
os.environ["COPADO_WORKSPACE_ID"] = workspace.id  # Save for scripts
```

### Document Analysis

```python
# Create workspace with knowledge capabilities
workspace = client.workspaces.create_with_knowledge_capabilities(
    name="Document Analysis Workspace",
    description="Workspace for analyzing Copado configurations",
    enable_custom_knowledge=True,
    enable_essentials_knowledge=True,
    enable_crt_knowledge=True,          # Copado Robotic Testing knowledge
    enable_metadata_format_knowledge=True,
    enable_source_format_knowledge=True
)

client.set_workspace(workspace.id)

# Create dialogue and upload documents
dialogue = client.dialogues.create(name="Document Analysis")

# Upload and analyze files
response = client.dialogues.chat_with_documents(
    dialogue_id=dialogue.id,
    prompt="Analyze these Copado configurations and suggest improvements",
    document_paths=["pipeline.yml", "metadata.xml", "rules.json"],
    stream=True
)
```

## 📚 Documentation

- **[Features Guide](FEATURES.md)** - Comprehensive API reference
- **[Copado AI Documentation](https://docs.copado.com/articles/#!copadoai-publication/copado-ai-platform-api)** - Official platform docs
- **[REST API Specification (Swagger)](https://copadogpt-api.robotic.copado.com/docs)** - Interactive API documentation

## 🔑 Key Features

- **🤖 AI Conversations** - Chat with Copado's AI about DevOps, automation, and best practices
- **📄 Document Analysis** - Upload and analyze Copado configurations, metadata, and pipeline files
- **🧠 Knowledge Integration** - Access Copado Essentials, CRT documentation, and custom knowledge bases
- **⚡ Workspace Management** - Persistent sessions with customizable AI capabilities
- **🔗 DevOps Automation** - Integrate AI insights into your CI/CD workflows
- **🌐 Web Search** - AI can search for real-time information when needed

## 🌍 Regional Endpoints

The Copado AI Platform is available in multiple regions:

| Region | Base URL |
|--------|----------|
| **US** | `https://copadogpt-api.robotic.copado.com` |
| **EU** | `https://copadogpt-api.eu-robotic.copado.com` |
| **Australia** | `https://copadogpt-api.au-robotic.copado.com` |
| **Singapore** | `https://copadogpt-api.sg-robotic.copado.com` |



## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/CopadoSolutions/copado_ai_sdk/issues)
- **Documentation**: [Copado AI Docs](https://docs.copado.com/articles/#!copadoai-publication/copado-ai-platform-api)
- **Community**: [Copado Community](https://success.copado.com)

**Made with ❤️ by the Copado Team**