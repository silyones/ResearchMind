import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

import asyncio
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.routes import router
from backend.config import settings
from backend.utils.logger import get_logger

logger = get_logger(__name__)

# Create FastAPI app
app = FastAPI(
    title="ResearchMind",
    description="AI-powered research assistant with web search and synthesis",
    version="1.0.0",
)

# Add CORS middleware for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins in development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router)


@app.on_event("startup")
async def startup_event():
    """Application startup event."""
    logger.info("=" * 60)
    logger.info("ResearchMind backend started")
    logger.info(f"Environment: {settings.env}")
    logger.info(f"Model: {settings.model_name_llm}")
    logger.info(f"LangSmith Tracing: {settings.langsmith_tracing}")
    logger.info(f"Max Agent Iterations: {settings.max_agent_iterations}")
    logger.info(f"Host: {settings.fastapi_host}")
    logger.info(f"Port: {settings.fastapi_port}")
    logger.info("=" * 60)


@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown event."""
    logger.info("ResearchMind backend shutting down")


if __name__ == "__main__":
    # Run with uvicorn
    uvicorn.run(
        "main:app",
        host=settings.fastapi_host,
        port=settings.fastapi_port,
        reload=settings.env == "development",
        log_level=settings.log_level.lower(),
    )
