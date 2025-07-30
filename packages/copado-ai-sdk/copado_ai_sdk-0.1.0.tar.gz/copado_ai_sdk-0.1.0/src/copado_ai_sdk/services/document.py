from pathlib import Path
from typing import List, Union, Optional
from ..types import Document
from ..client import CopadoClient


class DocumentService:
    """
    Service for managing documents within dialogues.
    
    This service provides functionality to upload, list, and delete documents
    that are associated with specific dialogues. Documents uploaded to dialogues
    are available for AI analysis and reference during conversations.
    
    Supported file types include:
    - CSV and XLSX files for data analysis
    - PDF documents for knowledge reference
    - Text files for content analysis
    - Images for visual analysis
    - Word documents (.docx)
    - PowerPoint presentations (.pptx)
    """
    
    def __init__(self, client: CopadoClient) -> None:
        self._client = client

    def upload_to_dialogue(
        self,
        dialogue_id: str,
        file_path: Union[str, Path],
        filename: Optional[str] = None,
    ) -> Document:
        """
        Upload a document to a dialogue.
        
        Args:
            dialogue_id: The ID of the dialogue to upload to
            file_path: Path to the file to upload
            filename: Optional custom filename (defaults to original filename)
            
        Returns:
            Document metadata including ID, size, and timestamps
            
        Raises:
            FileNotFoundError: If the file doesn't exist
            HTTPError: If the upload fails
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
            
        if not path.is_file():
            raise ValueError(f"Path is not a file: {file_path}")
            
        filename = filename or path.name
        url = f"/organizations/{self._client.organization_id}/dialogues/{dialogue_id}/documents"
        
        with open(path, 'rb') as file:
            files = {"file": (filename, file, "text/csv" if filename.endswith('.csv') else "application/octet-stream")}
            response = self._client._request("POST", url, files=files)
            return Document(**response.json())

    def list_in_dialogue(self, dialogue_id: str) -> List[Document]:
        """
        List all documents in a dialogue.
        
        Args:
            dialogue_id: The ID of the dialogue
            
        Returns:
            List of document metadata
        """
        url = f"/organizations/{self._client.organization_id}/dialogues/{dialogue_id}/documents"
        response = self._client._request("GET", url)
        return [Document(**doc) for doc in response.json()]

    def delete_from_dialogue(self, dialogue_id: str, filename: str) -> None:
        """
        Delete a document from a dialogue.
        
        Args:
            dialogue_id: The ID of the dialogue
            filename: The name of the file to delete
            
        Raises:
            HTTPError: If the deletion fails (e.g., file not found)
        """
        url = f"/organizations/{self._client.organization_id}/dialogues/{dialogue_id}/documents/{filename}"
        self._client._request("DELETE", url)

    def update_in_dialogue(
        self,
        dialogue_id: str,
        file_path: Union[str, Path],
        filename: Optional[str] = None,
    ) -> Document:
        """
        Update a document in a dialogue by replacing it.
        
        This method will delete the existing document with the same filename
        and upload the new version.
        
        Args:
            dialogue_id: The ID of the dialogue
            file_path: Path to the new file
            filename: Optional custom filename (defaults to original filename)
            
        Returns:
            Updated document metadata
        """
        path = Path(file_path)
        filename = filename or path.name
        
        # Try to delete existing file (ignore if it doesn't exist)
        try:
            self.delete_from_dialogue(dialogue_id, filename)
        except Exception:
            pass  # File might not exist, which is fine
            
        return self.upload_to_dialogue(dialogue_id, file_path, filename)

    def get_dialogue_document_count(self, dialogue_id: str) -> int:
        """
        Get the total number of documents in a dialogue.
        
        Args:
            dialogue_id: The ID of the dialogue
            
        Returns:
            Number of documents in the dialogue
        """
        documents = self.list_in_dialogue(dialogue_id)
        return len(documents)

    def get_dialogue_document_size(self, dialogue_id: str) -> int:
        """
        Get the total size of all documents in a dialogue.
        
        Args:
            dialogue_id: The ID of the dialogue
            
        Returns:
            Total size in bytes of all documents
        """
        documents = self.list_in_dialogue(dialogue_id)
        return sum(doc.size for doc in documents)

    upload = upload_to_dialogue
    list_documents = list_in_dialogue
    delete = delete_from_dialogue
    upload_document = upload_to_dialogue
    delete_document = delete_from_dialogue

    def upload_to_dataset(
        self,
        dataset_id: str,
        file_path: Union[str, Path],
        filename: Optional[str] = None,
    ) -> Document:
        """
        Upload a document to a dataset (workspace-level upload).
                
        Args:
            dataset_id: The ID of the dataset to upload to
            file_path: Path to the file to upload
            filename: Optional custom filename (defaults to original filename)
            
        Returns:
            Document metadata including ID, size, and timestamps
            
        Raises:
            FileNotFoundError: If the file doesn't exist
            HTTPError: If the upload fails
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
            
        if not path.is_file():
            raise ValueError(f"Path is not a file: {file_path}")
            
        filename = filename or path.name
        url = f"/organizations/{self._client.organization_id}/datasets/{dataset_id}/documents"
        
        with open(path, 'rb') as file:
            files = {"file": (filename, file, "text/csv" if filename.endswith('.csv') else "application/octet-stream")}
            response = self._client._request("POST", url, files=files)
            return Document(**response.json()) 