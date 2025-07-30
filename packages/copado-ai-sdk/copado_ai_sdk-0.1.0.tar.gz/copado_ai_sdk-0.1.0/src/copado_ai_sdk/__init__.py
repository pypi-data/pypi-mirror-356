from .client import CopadoClient
from .exceptions import HTTPError
from ._version import __version__

# Import types for public API
from .types import (
    WorkspaceCapability,
    WorkspaceMemberPermission,
    IntegrationType,
    IntegrationLevel,
    TrackedAction,
    MessageRole,
    Document,
    Workspace,
    WorkspaceSummary,
    DialogueResponse,
    DialogueWithMessages,
)

__all__ = [
    "CopadoClient", 
    "HTTPError", 
    "__version__",
    # Types
    "WorkspaceCapability",
    "WorkspaceMemberPermission", 
    "IntegrationType",
    "IntegrationLevel",
    "TrackedAction",
    "MessageRole",
    "Document",
    "Workspace", 
    "WorkspaceSummary",
    "DialogueResponse",
    "DialogueWithMessages",
]