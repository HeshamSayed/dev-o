"""
Pydantic models for request/response validation
OpenAI-compatible API models
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum


class Role(str, Enum):
    """Message role types"""
    system = "system"
    user = "user"
    assistant = "assistant"


class Message(BaseModel):
    """Chat message format"""
    role: Role
    content: str


class ChatCompletionRequest(BaseModel):
    """Request model for chat completions endpoint"""
    model: str = Field(default="mistral-7b", description="Model to use")
    messages: List[Message] = Field(..., description="List of messages")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: Optional[int] = Field(default=2048, ge=1, le=2048)
    top_p: float = Field(default=1.0, ge=0.0, le=1.0)
    stream: bool = Field(default=False, description="Stream responses (not yet supported)")
    

class CompletionRequest(BaseModel):
    """Request model for completions endpoint"""
    model: str = Field(default="mistral-7b")
    prompt: str = Field(..., description="Text prompt")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: Optional[int] = Field(default=2048, ge=1, le=2048)
    top_p: float = Field(default=1.0, ge=0.0, le=1.0)


class CompletionChoice(BaseModel):
    """Single completion choice"""
    text: str
    index: int
    finish_reason: str
    logprobs: Optional[Dict[str, Any]] = None


class ChatCompletionChoice(BaseModel):
    """Single chat completion choice"""
    index: int
    message: Message
    finish_reason: str


class Usage(BaseModel):
    """Token usage statistics"""
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class CompletionResponse(BaseModel):
    """Response model for completions"""
    id: str
    object: str = "text_completion"
    created: int
    model: str
    choices: List[CompletionChoice]
    usage: Usage


class ChatCompletionResponse(BaseModel):
    """Response model for chat completions"""
    id: str
    object: str = "chat.completion"
    created: int
    model: str
    choices: List[ChatCompletionChoice]
    usage: Usage


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    model_loaded: bool
    model_name: str
    device: str
