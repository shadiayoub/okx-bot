#!/usr/bin/env python3
"""
Database configuration and models
"""

from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
import os

# Database URL
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://trading_user:trading_pass@localhost:5432/trading_bot")

# Create engine
engine = create_engine(DATABASE_URL)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class
Base = declarative_base()

# Database models
class Symbol(Base):
    """Trading symbol configuration"""
    __tablename__ = "symbols"
    
    id = Column(Integer, primary_key=True, index=True)
    okx_symbol = Column(String, unique=True, index=True, nullable=False)
    model_symbol = Column(String, nullable=False)
    display_name = Column(String, nullable=False)
    enabled = Column(Boolean, default=True)
    risk_multiplier = Column(Float, default=1.0)
    min_balance = Column(Float, default=0.0)
    max_position_size = Column(Float, default=0.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Model(Base):
    """ML model configuration"""
    __tablename__ = "models"
    
    id = Column(Integer, primary_key=True, index=True)
    symbol_id = Column(Integer, nullable=False)
    model_type = Column(String, nullable=False)  # gradient_boosting, random_forest, etc.
    model_path = Column(String, nullable=False)
    version = Column(String, nullable=False)
    accuracy = Column(Float, default=0.0)
    training_date = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)
    hyperparameters = Column(JSON, default={})
    performance_metrics = Column(JSON, default={})

class TradingSession(Base):
    """Trading session configuration"""
    __tablename__ = "trading_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    session_name = Column(String, nullable=False)
    status = Column(String, default="stopped")  # running, stopped, paused
    leverage = Column(Integer, default=10)
    risk_per_trade = Column(Float, default=0.05)
    min_signal_strength = Column(Float, default=0.3)
    stop_loss_pct = Column(Float, default=0.02)
    take_profit_pct = Column(Float, default=0.04)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Trade(Base):
    """Trade history"""
    __tablename__ = "trades"
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, nullable=False)
    side = Column(String, nullable=False)  # buy, sell
    quantity = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    signal_strength = Column(Float, nullable=False)
    profit_loss = Column(Float, default=0.0)
    status = Column(String, default="open")  # open, closed, cancelled
    entry_time = Column(DateTime(timezone=True), server_default=func.now())
    exit_time = Column(DateTime(timezone=True), nullable=True)
    stop_loss = Column(Float, nullable=True)
    take_profit = Column(Float, nullable=True)

class TrainingJob(Base):
    """Model training jobs"""
    __tablename__ = "training_jobs"
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, nullable=False)
    model_type = Column(String, nullable=False)
    status = Column(String, default="pending")  # pending, running, completed, failed
    progress = Column(Float, default=0.0)
    start_time = Column(DateTime(timezone=True), server_default=func.now())
    end_time = Column(DateTime(timezone=True), nullable=True)
    error_message = Column(Text, nullable=True)
    hyperparameters = Column(JSON, default={})
    results = Column(JSON, default={})

class SystemConfig(Base):
    """System configuration"""
    __tablename__ = "system_config"
    
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, nullable=False)
    value = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

# Database dependency
def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
