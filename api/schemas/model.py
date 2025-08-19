#!/usr/bin/env python3
"""
Model schemas for API
"""

from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class ModelBase(BaseModel):
    symbol_id: int
    model_type: str
    model_path: str
    version: str
    accuracy: float = 0.0
    is_active: bool = True
    hyperparameters: Dict[str, Any] = {}
    performance_metrics: Dict[str, Any] = {}

class ModelCreate(ModelBase):
    pass

class ModelUpdate(BaseModel):
    accuracy: Optional[float] = None
    is_active: Optional[bool] = None
    hyperparameters: Optional[Dict[str, Any]] = None
    performance_metrics: Optional[Dict[str, Any]] = None

class ModelResponse(ModelBase):
    id: int
    training_date: datetime

    class Config:
        from_attributes = True

class TrainingJobCreate(BaseModel):
    symbol: str
    model_type: str
    hyperparameters: Dict[str, Any] = {}

class TrainingJobResponse(BaseModel):
    id: int
    symbol: str
    model_type: str
    status: str
    progress: float
    start_time: datetime
    end_time: Optional[datetime] = None
    error_message: Optional[str] = None
    hyperparameters: Dict[str, Any] = {}
    results: Dict[str, Any] = {}

    class Config:
        from_attributes = True
