"""
Base LLM Client

Defines the interface that all LLM clients must implement.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, AsyncGenerator
from dataclasses import dataclass


@dataclass
class LLMConfig:
    """Base configuration for LLM clients."""
    model: str
    temperature: float = 0.7
    max_tokens: Optional[int] = 16000  # Maximum context for better quality
    timeout: int = 600  # 10 minutes for longer responses


@dataclass
class LLMResponse:
    """Structured LLM response."""
    content: str
    thinking: str = ""  # For reasoning models like DeepSeek-R1
    tool_calls: List[Dict[str, Any]] = None
    is_final: bool = True
    needs_user_input: bool = False
    user_question: str = ""
    is_blocked: bool = False
    blocker_description: str = ""
    files_created: List[str] = None
    files_modified: List[str] = None
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.tool_calls is None:
            self.tool_calls = []
        if self.files_created is None:
            self.files_created = []
        if self.files_modified is None:
            self.files_modified = []
        if self.metadata is None:
            self.metadata = {}


class BaseLLMClient(ABC):
    """
    Abstract base class for LLM clients.

    All LLM clients (Ollama, OpenAI, Anthropic) must implement this interface.
    """

    @abstractmethod
    async def generate(
        self,
        prompt: str,
        system: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        tools: Optional[List[Dict]] = None,
    ) -> str:
        """
        Generate a response (non-streaming).

        Args:
            prompt: User prompt
            system: System prompt
            temperature: Generation temperature
            max_tokens: Maximum tokens to generate
            tools: Tool definitions (will be added to prompt)

        Returns:
            Generated text
        """
        pass

    @abstractmethod
    async def generate_stream(
        self,
        prompt: str,
        system: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        tools: Optional[List[Dict]] = None,
    ) -> AsyncGenerator[str, None]:
        """
        Generate a response with streaming.

        Args:
            prompt: User prompt
            system: System prompt
            temperature: Generation temperature
            max_tokens: Maximum tokens to generate
            tools: Tool definitions

        Yields:
            Chunks of generated text as they arrive
        """
        pass

    @abstractmethod
    def parse_response(self, response: str) -> LLMResponse:
        """
        Parse LLM response into structured format.

        Args:
            response: Raw LLM response

        Returns:
            Structured LLMResponse
        """
        pass

    @abstractmethod
    async def check_health(self) -> bool:
        """
        Check if LLM service is accessible.

        Returns:
            True if healthy, False otherwise
        """
        pass

    @abstractmethod
    async def close(self):
        """Close the client and cleanup resources."""
        pass
