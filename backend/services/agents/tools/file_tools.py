"""Custom tools for CrewAI agents to interact with project files."""

from typing import Dict, Any, List
from crewai.tools import BaseTool
from pydantic import Field, BaseModel
import logging

logger = logging.getLogger(__name__)


class FileWriteInput(BaseModel):
    """Input schema for file write tool."""
    path: str = Field(..., description="File path relative to project root")
    content: str = Field(..., description="Complete file content")


class FileReadInput(BaseModel):
    """Input schema for file read tool."""
    path: str = Field(..., description="File path relative to project root")


class FileListInput(BaseModel):
    """Input schema for file list tool."""
    directory: str = Field(default="", description="Directory to list files from")


class FileWriteTool(BaseTool):
    """Tool for writing files to the project."""
    
    name: str = "write_file"
    description: str = (
        "Write content to a file in the project. Creates or updates the file. "
        "Use this to create code files, configuration files, documentation, etc."
    )
    args_schema: type[BaseModel] = FileWriteInput
    
    file_storage: Dict[str, str] = Field(default_factory=dict)
    
    def _run(self, path: str, content: str) -> str:
        """Execute the file write operation."""
        try:
            # Store file in memory (will be persisted later)
            self.file_storage[path] = content
            logger.info(f"[FILE_TOOL] Wrote file: {path} ({len(content)} chars)")
            return f"Successfully wrote {len(content)} characters to {path}"
        except Exception as e:
            logger.error(f"[FILE_TOOL] Error writing file {path}: {e}")
            return f"Error writing file: {str(e)}"


class FileReadTool(BaseTool):
    """Tool for reading files from the project."""
    
    name: str = "read_file"
    description: str = (
        "Read the content of a file from the project. "
        "Use this to check existing files before modifying them."
    )
    args_schema: type[BaseModel] = FileReadInput
    
    file_storage: Dict[str, str] = Field(default_factory=dict)
    
    def _run(self, path: str) -> str:
        """Execute the file read operation."""
        try:
            if path in self.file_storage:
                content = self.file_storage[path]
                logger.info(f"[FILE_TOOL] Read file: {path} ({len(content)} chars)")
                return content
            else:
                return f"File not found: {path}"
        except Exception as e:
            logger.error(f"[FILE_TOOL] Error reading file {path}: {e}")
            return f"Error reading file: {str(e)}"


class FileListTool(BaseTool):
    """Tool for listing files in the project."""
    
    name: str = "list_files"
    description: str = (
        "List all files in the project or a specific directory. "
        "Use this to understand the current project structure."
    )
    args_schema: type[BaseModel] = FileListInput
    
    file_storage: Dict[str, str] = Field(default_factory=dict)
    
    def _run(self, directory: str = "") -> str:
        """Execute the file list operation."""
        try:
            files = list(self.file_storage.keys())
            if directory:
                files = [f for f in files if f.startswith(directory)]
            
            if not files:
                return f"No files found in {directory or 'project'}"
            
            file_list = "\n".join(sorted(files))
            logger.info(f"[FILE_TOOL] Listed {len(files)} files in {directory or 'project'}")
            return f"Files in {directory or 'project'}:\n{file_list}"
        except Exception as e:
            logger.error(f"[FILE_TOOL] Error listing files: {e}")
            return f"Error listing files: {str(e)}"


def create_file_tools(shared_storage: Dict[str, str] = None) -> List[BaseTool]:
    """Create file tools with shared storage."""
    if shared_storage is None:
        shared_storage = {}
    
    return [
        FileWriteTool(file_storage=shared_storage),
        FileReadTool(file_storage=shared_storage),
        FileListTool(file_storage=shared_storage),
    ]
