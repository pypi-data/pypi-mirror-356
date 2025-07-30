import json
import uuid
from pathlib import Path
from typing import Optional, List, Union, Iterator

from ..types import (
    DialogueResponse,
    DialogueWithMessages,
    DialogueCreate,
    DialogueUpdate,
    Document,
    MessageCreate,
    FeedbackCreate,
    DevContext
)
from ..exceptions import HTTPError
from ..client import CopadoClient


class DialogueService:
    """
    Service for managing AI dialogues and conversations.
    
    Dialogues are conversations with AI assistants within workspaces. They support
    document uploads, streaming responses, and various AI capabilities depending
    on the workspace configuration.
    """
    
    def __init__(self, client: CopadoClient) -> None:
        self._client = client

    def create(
        self,
        name: str,
        workspace_id: Optional[str] = None,
        workspace_name: Optional[str] = None,
        assistant_id: str = "knowledge",
        x_client: Optional[str] = None,
    ) -> DialogueResponse:
        """
        Create a new dialogue.
        
        Args:
            name: Name for the dialogue
            workspace_id: ID of the workspace (uses current session workspace if not provided)
            workspace_name: Name of workspace to create/find (alternative to workspace_id)
            assistant_id: ID of the assistant to use (default: "knowledge")
            x_client: Optional client identifier header
            
        Returns:
            Dialogue details
            
        Raises:
            ValueError: If workspace_name is provided but workspace creation fails
        """
        # Handle workspace creation/retrieval if needed
        if workspace_name:
            from .workspace import WorkspaceService
            ws_service = WorkspaceService(self._client)
            workspace = ws_service.get_or_create(workspace_name)
            workspace_id = workspace.id
        elif not workspace_id:
            if not self._client.current_workspace_id:
                raise ValueError("No workspace specified and no current workspace set. Either provide workspace_id, workspace_name, or set a workspace using client.set_workspace()")
            workspace_id = self._client.current_workspace_id
            
        url = f"/organizations/{self._client.organization_id}/dialogues"
        headers = self._client._headers()
        if x_client:
            headers["x-client"] = x_client

        payload = {
            "name": name,
            "workspaceId": workspace_id,
            "assistantId": assistant_id,
        }
        response = self._client._request("POST", url, json=payload)
        return DialogueResponse(**response.json())

    def chat(
        self,
        dialogue_id: str,
        prompt: str,
        *,
        request_id: Optional[str] = None,
        assistant_id: Optional[str] = None,
        stream: bool = False,
        dev_context: Optional[DevContext] = None,
        system_prompt: Optional[str] = None,
    ) -> str:
        """
        Send a message to the AI and get a response.
        
        Args:
            dialogue_id: ID of the dialogue
            prompt: The message to send
            request_id: Optional request ID (auto-generated if not provided)
            assistant_id: Optional assistant to use for this message
            stream: Whether to stream the response to stdout
            dev_context: Optional development context for code-related queries
            system_prompt: Optional system prompt override
            
        Returns:
            The complete AI response as a string
        """
        url = (
            f"/organizations/{self._client.organization_id}"
            f"/dialogues/{dialogue_id}/messages"
        )
        if request_id is None:
            request_id = str(uuid.uuid4())

        payload = {"request_id": request_id, "prompt": prompt}
        
        if assistant_id:
            payload["assistantId"] = assistant_id
        if dev_context:
            payload["dev_context"] = dev_context.dict()
        if system_prompt:
            payload["system_prompt"] = system_prompt

        resp = self._client._request("POST", url, json=payload, stream=True)

        full: List[str] = []
        for line in resp.iter_lines():
            if not line:
                continue
            try:
                data = json.loads(line)
                if data.get("type") == "token":
                    token = data.get("content", "")
                    full.append(token)
                    if stream:
                        print(token, end="", flush=True)
            except json.JSONDecodeError:
                continue

        if stream:
            print()
        return "".join(full)

    def chat_with_documents(
        self,
        dialogue_id: str,
        prompt: str,
        document_paths: List[Union[str, Path]],
        *,
        stream: bool = False,
        assistant_id: Optional[str] = None,
    ) -> str:
        """
        Send a message with document uploads and get a response.
        
        This convenience method uploads documents and then sends a chat message.
        
        Args:
            dialogue_id: ID of the dialogue
            prompt: The message to send
            document_paths: List of file paths to upload
            stream: Whether to stream the response to stdout
            assistant_id: Optional assistant to use
            
        Returns:
            The complete AI response as a string
        """
        # Upload documents first
        for doc_path in document_paths:
            self.upload_document(dialogue_id, str(doc_path))
            
        # Then send the chat message
        return self.chat(
            dialogue_id, 
            prompt, 
            stream=stream, 
            assistant_id=assistant_id
        )

    def list(
        self,
        workspace_id: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[DialogueResponse]:
        """
        List dialogues in the organization.
        
        Args:
            workspace_id: Optional workspace filter
            limit: Maximum number of results
            offset: Number of results to skip
            
        Returns:
            List of dialogue summaries
        """
        url = f"/organizations/{self._client.organization_id}/dialogues"
        params = {"limit": limit, "offset": offset}
        if workspace_id:
            params["workspace_id"] = workspace_id
        response = self._client._request("GET", url, params=params)
        return [DialogueResponse(**dialogue) for dialogue in response.json()]

    def get(self, dialogue_id: str) -> DialogueWithMessages:
        """
        Get a dialogue with all its messages.
        
        Args:
            dialogue_id: The dialogue ID
            
        Returns:
            Complete dialogue details including all messages
        """
        url = f"/organizations/{self._client.organization_id}/dialogues/{dialogue_id}"
        response = self._client._request("GET", url)
        return DialogueWithMessages(**response.json())

    def update(
        self,
        dialogue_id: str,
        name: Optional[str] = None,
    ) -> DialogueResponse:
        """
        Update a dialogue.
        
        Args:
            dialogue_id: The dialogue ID
            name: New name for the dialogue
            
        Returns:
            Updated dialogue details
        """
        url = f"/organizations/{self._client.organization_id}/dialogues/{dialogue_id}"
        payload = {}
        if name is not None:
            payload["name"] = name
        response = self._client._request("PATCH", url, json=payload)
        return DialogueResponse(**response.json())

    def delete(self, dialogue_id: str) -> None:
        """
        Delete a dialogue and all its documents.
        
        Args:
            dialogue_id: The dialogue ID
        """
        url = f"/organizations/{self._client.organization_id}/dialogues/{dialogue_id}"
        self._client._request("DELETE", url)

    def cancel_message(self, dialogue_id: str, request_id: str) -> dict:
        """
        Cancel a message that's being processed.
        
        Args:
            dialogue_id: The dialogue ID
            request_id: The request ID of the message to cancel
            
        Returns:
            Cancellation response
        """
        url = (
            f"/organizations/{self._client.organization_id}"
            f"/dialogues/{dialogue_id}/messages/{request_id}/cancel"
        )
        return self._client._request("POST", url).json()

    def create_feedback(
        self,
        dialogue_id: str,
        request_id: str,
        prompt: str,
        response: str,
        feedback: str,
        sentiment: bool,
    ) -> dict:
        """
        Create feedback for a message.
        
        Args:
            dialogue_id: The dialogue ID
            request_id: The request ID of the message
            prompt: The original prompt
            response: The AI response
            feedback: Feedback text
            sentiment: True for positive, False for negative
            
        Returns:
            Feedback response
        """
        url = (
            f"/organizations/{self._client.organization_id}"
            f"/dialogues/{dialogue_id}/messages/{request_id}/feedback"
        )
        payload = {
            "prompt": prompt,
            "response": response,
            "feedback": feedback,
            "sentiment": sentiment,
        }
        return self._client._request("POST", url, json=payload).json()

    def upload_document(
        self,
        dialogue_id: str,
        file_path: Union[str, Path],
        filename: Optional[str] = None,
    ) -> Document:
        """
        Upload a document to a dialogue.
        
        Args:
            dialogue_id: The dialogue ID
            file_path: Path to the file to upload
            filename: Optional custom filename
            
        Returns:
            Document metadata
            
        Raises:
            FileNotFoundError: If the file doesn't exist
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
            
        url = f"/organizations/{self._client.organization_id}/dialogues/{dialogue_id}/documents"
        
        filename = filename or path.name
        with open(path, 'rb') as file:
            files = {'file': (filename, file)}
            response = self._client._request("POST", url, files=files)
            return Document(**response.json())



    def list_documents(self, dialogue_id: str) -> List[Document]:
        """
        List all documents in a dialogue.
        
        Args:
            dialogue_id: The dialogue ID
            
        Returns:
            List of document metadata
        """
        url = f"/organizations/{self._client.organization_id}/dialogues/{dialogue_id}/documents"
        response = self._client._request("GET", url)
        return [Document(**doc) for doc in response.json()]

    def delete_document(self, dialogue_id: str, filename: str) -> None:
        """
        Delete a document from a dialogue.
        
        Args:
            dialogue_id: The dialogue ID
            filename: The filename to delete
        """
        url = f"/organizations/{self._client.organization_id}/dialogues/{dialogue_id}/documents/{filename}"
        self._client._request("DELETE", url)

    def get_document_count(self, dialogue_id: str) -> int:
        """
        Get the number of documents in a dialogue.
        
        Args:
            dialogue_id: The dialogue ID
            
        Returns:
            Number of documents
        """
        documents = self.list_documents(dialogue_id)
        return len(documents)

    def get_document_total_size(self, dialogue_id: str) -> int:
        """
        Get the total size of all documents in a dialogue.
        
        Args:
            dialogue_id: The dialogue ID
            
        Returns:
            Total size in bytes
        """
        documents = self.list_documents(dialogue_id)
        return sum(doc.size for doc in documents)
