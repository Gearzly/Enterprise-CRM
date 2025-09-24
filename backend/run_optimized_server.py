#!/usr/bin/env python3
"""
Optimized startup script for CRM Backend with performance improvements
"""
import uvicorn
import sys
import os
import asyncio
from pathlib import Path

# Add the app directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

def run_server():
    """Run the server with optimized settings"""
    try:
        # Configure uvicorn with performance optimizations
        config = uvicorn.Config(
            "app.main:app",
            host="0.0.0.0",
            port=8000,
            reload=False,  # Disable reload for better performance
            log_level="info",
            access_log=True,
            # Performance optimizations
            timeout_keep_alive=180,  # 3 minutes keep-alive
            timeout_graceful_shutdown=45,  # 45 seconds graceful shutdown
            backlog=4096,  # Increase connection backlog
            # Worker settings
            workers=1,  # Single worker for testing, increase for production
            loop="auto",  # Let uvicorn choose the best event loop
            http="auto",  # Let uvicorn choose the best HTTP implementation
            # Limits
            limit_concurrency=2000,  # Max concurrent connections
            limit_max_requests=50000,  # Max requests per worker
            # Additional timeout settings
            timeout_notify=30,  # Notify timeout
        )
        
        server = uvicorn.Server(config)
        print("🚀 Starting CRM Backend Server with optimized settings...")
        print(f"📡 Server will be available at: http://localhost:8000")
        print(f"📖 API Documentation: http://localhost:8000/docs")
        print("⚡ Performance optimizations enabled")
        
        # Run the server
        server.run()
        
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    print("🔧 CRM Backend - Optimized Server Startup")
    run_server()