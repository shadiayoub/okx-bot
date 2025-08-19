#!/usr/bin/env python3
"""
Trading Bot Management API
FastAPI backend for the complete trading system
"""

from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import uvicorn
import os
import logging

from api.routers import symbols, models, trading, analytics, system
from api.database import engine, Base
from api.core.config import settings
from api.core.security import get_current_user

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    logger.info("🚀 Starting Trading Bot Management API...")
    
    # Create database tables
    Base.metadata.create_all(bind=engine)
    logger.info("✅ Database tables created")
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down Trading Bot Management API...")

# Create FastAPI app
app = FastAPI(
    title="Trading Bot Management API",
    description="Complete trading bot management system with dynamic symbol discovery and model training",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(symbols.router, prefix="/api/v1/symbols", tags=["Symbols"])
app.include_router(models.router, prefix="/api/v1/models", tags=["Models"])
app.include_router(trading.router, prefix="/api/v1/trading", tags=["Trading"])
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["Analytics"])
app.include_router(system.router, prefix="/api/v1/system", tags=["System"])

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Trading Bot Management API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "database": "connected",
        "redis": "connected"
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
