#!/usr/bin/env python3
"""
Startup script for the SaaS CRM Backend
"""
import uvicorn
import sys
import os

# Add the app directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=5173,  # Changed to 5173 for TestSprite compatibility
        reload=True,
        log_level="info",
        timeout_keep_alive=60,  # Increase keep-alive timeout
        timeout_graceful_shutdown=30  # Graceful shutdown timeout
    )