"""
FastAPI application for Mistral 7B inference
OpenAI-compatible API endpoints
"""
from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
import time
import uuid
from typing import Optional
import logging

from .config import settings
from .models import (
    ChatCompletionRequest,
    ChatCompletionResponse,
    CompletionRequest,
    CompletionResponse,
    HealthResponse,
    ChatCompletionChoice,
    CompletionChoice,
    Message,
    Role,
    Usage
)
from .model_loader import mistral_model

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="AI Inference Service - Mistral 7B",
    description="OpenAI-compatible API for Mistral 7B model inference",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# API Key validation (optional)
async def verify_api_key(authorization: Optional[str] = Header(None)):
    """Verify API key if configured"""
    if settings.API_KEY:
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Missing or invalid authorization header")
        
        token = authorization.replace("Bearer ", "")
        if token != settings.API_KEY:
            raise HTTPException(status_code=401, detail="Invalid API key")
    return True


@app.on_event("startup")
async def startup_event():
    """Load model on startup"""
    logger.info("Starting AI Inference Service")
    logger.info(f"Model: {settings.MODEL_NAME}")
    logger.info(f"Device: {settings.DEVICE}")
    logger.info(f"Max Input Tokens: {settings.MAX_INPUT_TOKENS}")
    logger.info(f"Max Output Tokens: {settings.MAX_OUTPUT_TOKENS}")
    
    try:
        mistral_model.load()
        logger.info("Model loaded successfully - Service ready")
    except Exception as e:
        logger.error(f"Failed to load model: {str(e)}")
        raise


@app.get("/")
async def root():
    """Service information"""
    return {
        "service": "AI Inference Service",
        "model": settings.MODEL_NAME,
        "version": "1.0.0",
        "endpoints": [
            "GET /health",
            "POST /v1/chat/completions",
            "POST /v1/completions"
        ]
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy" if mistral_model.is_loaded else "unhealthy",
        model_loaded=mistral_model.is_loaded,
        model_name=settings.MODEL_NAME,
        device=settings.DEVICE
    )


@app.post("/v1/chat/completions", response_model=ChatCompletionResponse)
async def chat_completions(
    request: ChatCompletionRequest,
    _: bool = Depends(verify_api_key)
):
    """
    OpenAI-compatible chat completions endpoint
    Converts chat messages to prompt and generates response
    """
    if not mistral_model.is_loaded:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    if request.stream:
        raise HTTPException(status_code=400, detail="Streaming not yet supported")
    
    try:
        # Convert messages to prompt format
        prompt = ""
        for msg in request.messages:
            if msg.role == Role.system:
                prompt += f"<s>[INST] {msg.content} [/INST]\n"
            elif msg.role == Role.user:
                prompt += f"[INST] {msg.content} [/INST]\n"
            elif msg.role == Role.assistant:
                prompt += f"{msg.content}\n"
        
        # Count input tokens
        prompt_tokens = mistral_model.count_tokens(prompt)
        
        # Generate response
        max_tokens = request.max_tokens or settings.MAX_OUTPUT_TOKENS
        generated_text = mistral_model.generate(
            prompt=prompt,
            max_new_tokens=max_tokens,
            temperature=request.temperature,
            top_p=request.top_p
        )
        
        # Count completion tokens
        completion_tokens = mistral_model.count_tokens(generated_text)
        
        # Create response
        response = ChatCompletionResponse(
            id=f"chatcmpl-{uuid.uuid4().hex[:8]}",
            created=int(time.time()),
            model=request.model,
            choices=[
                ChatCompletionChoice(
                    index=0,
                    message=Message(role=Role.assistant, content=generated_text),
                    finish_reason="stop"
                )
            ],
            usage=Usage(
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
                total_tokens=prompt_tokens + completion_tokens
            )
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Chat completion failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/v1/completions", response_model=CompletionResponse)
async def completions(
    request: CompletionRequest,
    _: bool = Depends(verify_api_key)
):
    """
    OpenAI-compatible completions endpoint
    Direct text completion without chat formatting
    """
    if not mistral_model.is_loaded:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        # Count input tokens
        prompt_tokens = mistral_model.count_tokens(request.prompt)
        
        # Generate response
        max_tokens = request.max_tokens or settings.MAX_OUTPUT_TOKENS
        generated_text = mistral_model.generate(
            prompt=request.prompt,
            max_new_tokens=max_tokens,
            temperature=request.temperature,
            top_p=request.top_p
        )
        
        # Count completion tokens
        completion_tokens = mistral_model.count_tokens(generated_text)
        
        # Create response
        response = CompletionResponse(
            id=f"cmpl-{uuid.uuid4().hex[:8]}",
            created=int(time.time()),
            model=request.model,
            choices=[
                CompletionChoice(
                    text=generated_text,
                    index=0,
                    finish_reason="stop"
                )
            ],
            usage=Usage(
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
                total_tokens=prompt_tokens + completion_tokens
            )
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Completion failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)
