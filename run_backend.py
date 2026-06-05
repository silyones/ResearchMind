#!/usr/bin/env python
"""
Entry point for running the ResearchMind backend.
Run from the project root: python run_backend.py
"""

import sys
import uvicorn
from backend.config import settings
from backend.utils.logger import get_logger

logger = get_logger(__name__)

if __name__ == "__main__":
    logger.info("Starting ResearchMind backend...")
    uvicorn.run(
        "backend.main:app",
        host=settings.fastapi_host,
        port=settings.fastapi_port,
        reload=settings.env == "development",
        log_level=settings.log_level.lower(),
    )
