#!/usr/bin/env python3
"""
Trading Bot Management API
FastAPI backend for the complete trading system
"""

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from contextlib import asynccontextmanager
import logging
import time

from api.database import engine, Base
from api.routers import symbols, models, trading, analytics, system

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully")
    yield
    # Shutdown
    logger.info("Shutting down...")

app = FastAPI(
    title="Trading Bot API",
    description="API for managing trading bot operations",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Trading Bot API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/metrics", response_class=PlainTextResponse)
async def metrics():
    """Prometheus metrics endpoint"""
    logger.info("Metrics endpoint called")
    
    # Return metrics in Prometheus text format
    metrics_text = """# HELP trading_bot_api_requests_total Total number of API requests
# TYPE trading_bot_api_requests_total counter
trading_bot_api_requests_total 0

# HELP trading_bot_api_requests_duration_seconds Duration of API requests
# TYPE trading_bot_api_requests_duration_seconds histogram
trading_bot_api_requests_duration_seconds 0.0

# HELP trading_bot_api_active_connections Number of active connections
# TYPE trading_bot_api_active_connections gauge
trading_bot_api_active_connections 0

# HELP trading_bot_api_uptime_seconds API uptime in seconds
# TYPE trading_bot_api_uptime_seconds gauge
trading_bot_api_uptime_seconds 0
"""
    return metrics_text

# Include routers
app.include_router(symbols.router, prefix="/api/v1/symbols", tags=["symbols"])
app.include_router(models.router, prefix="/api/v1/models", tags=["models"])
app.include_router(trading.router, prefix="/api/v1/trading", tags=["trading"])
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["analytics"])
app.include_router(system.router, prefix="/api/v1/system", tags=["system"])
