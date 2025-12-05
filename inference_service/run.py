"""
Entry point for running the AI Inference Service
"""
import uvicorn
from app.config import settings

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=False,
        workers=1,  # Single worker for GPU efficiency
        log_level="info"
    )
