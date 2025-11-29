"""
LLM Service

Main service for interacting with LLMs.
Manages client selection, fallback, and common operations.
"""

import logging
from typing import Dict, Any, List, Optional, AsyncGenerator
from django.conf import settings

from apps.llm.clients.base import BaseLLMClient, LLMResponse
from apps.llm.clients.ollama import OllamaClient, OllamaConfig
from apps.llm.clients.external import ExternalAIClient, ExternalAIConfig
from apps.llm.services.token_service import TokenCounter
from apps.llm.services.prompt_service import PromptService

logger = logging.getLogger(__name__)


class LLMService:
    """
    Main LLM service.

    Handles:
    - Client management (Ollama, OpenAI, Anthropic)
    - Automatic fallback
    - Token counting
    - Prompt construction
    - Response parsing
    """

    def __init__(
        self,
        model: Optional[str] = None,
        client: Optional[BaseLLMClient] = None
    ):
        """
        Initialize LLM service.

        Args:
            model: Model name to use
            client: Optional pre-configured client
        """
        self.model = model or settings.DEVO_SETTINGS.get('DEFAULT_LLM_MODEL')
        self._client = client
        self.token_counter = TokenCounter()
        self.prompt_service = PromptService()

    @property
    def client(self) -> BaseLLMClient:
        """Get or create LLM client."""
        if self._client is None:
            # Check if external AI service is configured
            use_external = settings.DEVO_SETTINGS.get('USE_EXTERNAL_AI', False)

            if use_external:
                # Use external AI service (DeepSeek Coder)
                config = ExternalAIConfig(
                    model=settings.DEVO_SETTINGS.get('EXTERNAL_AI_MODEL', self.model),
                    base_url=settings.DEVO_SETTINGS.get('EXTERNAL_AI_BASE_URL', 'http://34.136.165.200:8000'),
                    api_key=settings.DEVO_SETTINGS.get('EXTERNAL_AI_API_KEY', 'sk-test-123456'),
                    # DeepSeek Coder specific parameters
                    top_p=settings.DEVO_SETTINGS.get('DEEPSEEK_TOP_P', 0.9),
                    top_k=settings.DEVO_SETTINGS.get('DEEPSEEK_TOP_K', 40),
                    repeat_penalty=settings.DEVO_SETTINGS.get('DEEPSEEK_REPEAT_PENALTY', 1.1),
                    num_ctx=settings.DEVO_SETTINGS.get('DEEPSEEK_NUM_CTX', 8192),
                    default_max_tokens=settings.DEVO_SETTINGS.get('DEEPSEEK_MAX_TOKENS', 4096),
                )
                self._client = ExternalAIClient(config)
            # Determine client type based on model
            elif 'deepseek' in self.model.lower() or 'ollama' in self.model.lower():
                config = OllamaConfig(
                    model=self.model,
                    base_url=settings.DEVO_SETTINGS.get('OLLAMA_BASE_URL'),
                    num_ctx=settings.DEVO_SETTINGS.get('MAX_CONTEXT_TOKENS', 32768)
                )
                self._client = OllamaClient(config)
            # TODO: Add OpenAI and Anthropic clients
            else:
                # Default to Ollama
                config = OllamaConfig(
                    model=self.model,
                    base_url=settings.DEVO_SETTINGS.get('OLLAMA_BASE_URL'),
                    num_ctx=settings.DEVO_SETTINGS.get('MAX_CONTEXT_TOKENS', 32768)
                )
                self._client = OllamaClient(config)

        return self._client

    async def generate(
        self,
        prompt: str,
        system: Optional[str] = None,
        messages: Optional[List[Dict[str, str]]] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        tools: Optional[List[Dict]] = None,
    ) -> LLMResponse:
        """
        Generate a response (non-streaming).

        Args:
            prompt: User prompt
            system: System prompt
            messages: Previous conversation messages
            temperature: Generation temperature
            max_tokens: Maximum tokens to generate
            tools: Tool definitions

        Returns:
            Structured LLMResponse
        """
        # Build full prompt from messages if provided
        if messages:
            full_prompt = "\n\n".join([
                f"{msg['role']}: {msg['content']}"
                for msg in messages
            ]) + f"\n\nuser: {prompt}"
        else:
            full_prompt = prompt

        # Generate response
        response_text = await self.client.generate(
            prompt=full_prompt,
            system=system,
            temperature=temperature,
            max_tokens=max_tokens,
            tools=tools,
        )

        # Parse response
        return self.client.parse_response(response_text)

    async def generate_stream(
        self,
        prompt: str,
        system: Optional[str] = None,
        messages: Optional[List[Dict[str, str]]] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        tools: Optional[List[Dict]] = None,
    ) -> AsyncGenerator[str, None]:
        """
        Generate a response with streaming.

        Args:
            prompt: User prompt
            system: System prompt
            messages: Previous conversation messages
            temperature: Generation temperature
            max_tokens: Maximum tokens to generate
            tools: Tool definitions

        Yields:
            Chunks of generated text
        """
        logger.info(f"[LLMService] generate_stream() called!")
        # Build full prompt from messages if provided
        if messages:
            full_prompt = "\n\n".join([
                f"{msg['role']}: {msg['content']}"
                for msg in messages
            ]) + f"\n\nuser: {prompt}"
        else:
            full_prompt = prompt

        logger.info(f"[LLMService] About to call client.generate_stream")
        # Stream response
        async for chunk in self.client.generate_stream(
            prompt=full_prompt,
            system=system,
            temperature=temperature,
            max_tokens=max_tokens,
            tools=tools,
        ):
            logger.info(f"[LLMService] Got chunk from client")
            yield chunk
        logger.info(f"[LLMService] Stream complete")

    async def check_health(self) -> bool:
        """Check if LLM service is healthy."""
        try:
            return await self.client.check_health()
        except Exception as e:
            logger.error(f"LLM health check failed: {e}")
            return False

    async def close(self):
        """Close LLM client."""
        if self._client:
            await self._client.close()

    def count_tokens(self, text: str) -> int:
        """Count tokens in text."""
        return self.token_counter.count(text, self.model)

    def truncate_text(self, text: str, max_tokens: int) -> str:
        """Truncate text to maximum tokens."""
        return self.token_counter.truncate(text, max_tokens, self.model)

    def build_system_prompt(
        self,
        agent_type: str,
        persona: str,
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """Build system prompt for agent."""
        return self.prompt_service.build_system_prompt(
            agent_type, persona, context
        )

    def format_task_prompt(self, task: Dict[str, Any]) -> str:
        """Format task as prompt."""
        return self.prompt_service.format_task_prompt(task)
