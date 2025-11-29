"""
Token Counting Service

Provides token counting and text truncation utilities.
"""

import logging
from typing import Optional

logger = logging.getLogger(__name__)


class TokenCounter:
    """
    Token counting service.

    Uses simple approximation for now. Can be upgraded to use tiktoken
    for accurate counts in the future.
    """

    def __init__(self):
        # Simple approximation: ~4 characters per token for English text
        self.chars_per_token = 4

    def count(self, text: str, model: str = 'gpt-3.5-turbo') -> int:
        """
        Estimate token count for text.

        Args:
            text: Text to count
            model: Model name (for future tiktoken integration)

        Returns:
            Estimated token count
        """
        if not text:
            return 0

        # Simple approximation
        return len(text) // self.chars_per_token

    def count_messages(self, messages: list, model: str = 'gpt-3.5-turbo') -> int:
        """
        Count tokens in a list of messages.

        Args:
            messages: List of message dicts with 'role' and 'content'
            model: Model name

        Returns:
            Estimated token count
        """
        total = 0
        for message in messages:
            # Count message overhead (role, etc.)
            total += 4  # Approximate overhead per message

            # Count content
            if 'content' in message:
                total += self.count(str(message['content']), model)

        total += 2  # Approximate overhead for message list

        return total

    def truncate(
        self,
        text: str,
        max_tokens: int,
        model: str = 'gpt-3.5-turbo',
        suffix: str = '...'
    ) -> str:
        """
        Truncate text to a maximum number of tokens.

        Args:
            text: Text to truncate
            max_tokens: Maximum token count
            model: Model name
            suffix: Suffix to add if truncated

        Returns:
            Truncated text
        """
        if not text:
            return text

        estimated_tokens = self.count(text, model)

        if estimated_tokens <= max_tokens:
            return text

        # Calculate approximate character limit
        char_limit = max_tokens * self.chars_per_token - len(suffix)

        return text[:char_limit] + suffix

    def chunk_text(
        self,
        text: str,
        chunk_size: int = 1000,
        overlap: int = 100,
        model: str = 'gpt-3.5-turbo'
    ) -> list:
        """
        Chunk text into token-based segments with overlap.

        Args:
            text: Text to chunk
            chunk_size: Maximum tokens per chunk
            overlap: Number of tokens to overlap between chunks
            model: Model name

        Returns:
            List of text chunks
        """
        if not text:
            return []

        # Convert token sizes to character estimates
        chunk_chars = chunk_size * self.chars_per_token
        overlap_chars = overlap * self.chars_per_token

        if len(text) <= chunk_chars:
            return [text]

        chunks = []
        start = 0

        while start < len(text):
            end = start + chunk_chars
            chunk = text[start:end]
            chunks.append(chunk)

            # Move start forward by (chunk_size - overlap)
            start += chunk_chars - overlap_chars

            # Break if we're near the end
            if end >= len(text):
                break

        return chunks

    def fits_in_context(
        self,
        text: str,
        max_tokens: int,
        model: str = 'gpt-3.5-turbo'
    ) -> bool:
        """
        Check if text fits within token limit.

        Args:
            text: Text to check
            max_tokens: Maximum token count
            model: Model name

        Returns:
            True if text fits, False otherwise
        """
        return self.count(text, model) <= max_tokens
