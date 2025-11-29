"""
Utility functions shared across the project.
"""

import hashlib
import secrets
from typing import Any, Dict, List
from django.utils.text import slugify


def generate_api_key() -> str:
    """Generate a secure API key."""
    return f"devo_{secrets.token_urlsafe(32)}"


def hash_api_key(key: str) -> str:
    """Hash an API key for storage."""
    return hashlib.sha256(key.encode()).hexdigest()


def generate_slug(text: str, max_length: int = 50) -> str:
    """Generate a URL-safe slug from text."""
    return slugify(text)[:max_length]


def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 100) -> List[str]:
    """
    Chunk text into overlapping segments.

    Args:
        text: Text to chunk
        chunk_size: Maximum size of each chunk
        overlap: Number of characters to overlap between chunks

    Returns:
        List of text chunks
    """
    if len(text) <= chunk_size:
        return [text]

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)

        # Move start forward by (chunk_size - overlap)
        start += chunk_size - overlap

        # Break if we're near the end
        if end >= len(text):
            break

    return chunks


def count_tokens(text: str, model: str = 'gpt-3.5-turbo') -> int:
    """
    Estimate token count for text.

    This is a simple approximation. For accurate counts, use tiktoken.

    Args:
        text: Text to count
        model: Model name (for future tiktoken integration)

    Returns:
        Estimated token count
    """
    # Simple approximation: ~4 characters per token for English text
    return len(text) // 4


def truncate_text(text: str, max_tokens: int = 500, model: str = 'gpt-3.5-turbo') -> str:
    """
    Truncate text to a maximum number of tokens.

    Args:
        text: Text to truncate
        max_tokens: Maximum token count
        model: Model name

    Returns:
        Truncated text
    """
    estimated_tokens = count_tokens(text, model)

    if estimated_tokens <= max_tokens:
        return text

    # Calculate approximate character limit
    char_limit = max_tokens * 4

    return text[:char_limit] + '...'


def format_bytes(bytes_count: int) -> str:
    """Format bytes as human-readable string."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_count < 1024.0:
            return f"{bytes_count:.2f} {unit}"
        bytes_count /= 1024.0
    return f"{bytes_count:.2f} PB"


def safe_get(dictionary: Dict[str, Any], *keys: str, default: Any = None) -> Any:
    """
    Safely get nested dictionary values.

    Example:
        safe_get(data, 'user', 'profile', 'email', default='')

    Args:
        dictionary: Dictionary to traverse
        *keys: Keys to access in order
        default: Default value if key not found

    Returns:
        Value at nested key or default
    """
    result = dictionary

    for key in keys:
        if isinstance(result, dict):
            result = result.get(key)
            if result is None:
                return default
        else:
            return default

    return result if result is not None else default
