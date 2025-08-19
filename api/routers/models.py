#!/usr/bin/env python3
"""
Models management router
ML model training and management
"""

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
import logging

from api.database import get_db, Model, TrainingJob
from api.schemas.model import ModelCreate, ModelResponse, TrainingJobCreate, TrainingJobResponse
from api.services.model_service import ModelService
from api.services.training_service import TrainingService
from api.services.model_recommendation_service import ModelRecommendationService
import pandas as pd
import numpy as np

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/", response_model=List[ModelResponse])
async def get_models(
    symbol: Optional[str] = None,
    active_only: bool = False,
    db: Session = Depends(get_db)
):
    """Get all models or filter by symbol"""
    try:
        service = ModelService(db)
        models = service.get_models(symbol=symbol, active_only=active_only)
        return models
    except Exception as e:
        logger.error(f"Failed to get models: {e}")
        raise HTTPException(status_code=500, detail="Failed to get models")

@router.get("/available")
async def get_available_models(
    db: Session = Depends(get_db)
):
    """Get list of available model types"""
    try:
        service = ModelService(db)
        available_models = service.get_available_model_types()
        return available_models
    except Exception as e:
        logger.error(f"Failed to get available models: {e}")
        raise HTTPException(status_code=500, detail="Failed to get available models")

@router.get("/recommendations/{symbol}")
async def get_model_recommendations(
    symbol: str,
    trading_style: str = "balanced",
    data_availability: str = "medium",
    db: Session = Depends(get_db)
):
    """Get model recommendations for a specific symbol"""
    try:
        # This would fetch historical data for the symbol
        # For now, return a mock recommendation
        recommendation_service = ModelRecommendationService()
        
        # Mock market data (in real implementation, fetch from OKX API)
        mock_data = pd.DataFrame({
            'close': [100 + i * 0.1 + np.random.normal(0, 0.5) for i in range(1000)]
        })
        
        recommendation = recommendation_service.recommend_model_type(
            mock_data, trading_style, data_availability
        )
        
        # Add hyperparameters
        recommendation['hyperparameters'] = recommendation_service.get_model_hyperparameters(
            recommendation['recommended_model'], 
            recommendation['market_type']
        )
        
        return recommendation
        
    except Exception as e:
        logger.error(f"Error getting model recommendations: {e}")
        raise HTTPException(status_code=500, detail="Failed to get model recommendations")

@router.post("/train", response_model=TrainingJobResponse)
async def start_training(
    training_job: TrainingJobCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Start a new model training job"""
    try:
        training_service = TrainingService(db)
        job = training_service.create_training_job(training_job)
        
        # Start training in background
        background_tasks.add_task(
            training_service.train_model_async,
            job.id,
            training_job.symbol,
            training_job.model_type,
            training_job.hyperparameters
        )
        
        return job
    except Exception as e:
        logger.error(f"Failed to start training: {e}")
        raise HTTPException(status_code=500, detail="Failed to start training")

@router.get("/training-jobs", response_model=List[TrainingJobResponse])
async def get_training_jobs(
    status: Optional[str] = None,
    symbol: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get training jobs with optional filtering"""
    try:
        service = TrainingService(db)
        jobs = service.get_training_jobs(status=status, symbol=symbol)
        return jobs
    except Exception as e:
        logger.error(f"Failed to get training jobs: {e}")
        raise HTTPException(status_code=500, detail="Failed to get training jobs")

@router.get("/training-jobs/{job_id}", response_model=TrainingJobResponse)
async def get_training_job(
    job_id: int,
    db: Session = Depends(get_db)
):
    """Get specific training job details"""
    try:
        service = TrainingService(db)
        job = service.get_training_job(job_id)
        if not job:
            raise HTTPException(status_code=404, detail="Training job not found")
        return job
    except Exception as e:
        logger.error(f"Failed to get training job: {e}")
        raise HTTPException(status_code=500, detail="Failed to get training job")

@router.post("/training-jobs/{job_id}/cancel")
async def cancel_training_job(
    job_id: int,
    db: Session = Depends(get_db)
):
    """Cancel a training job"""
    try:
        service = TrainingService(db)
        service.cancel_training_job(job_id)
        return {"message": "Training job cancelled successfully"}
    except Exception as e:
        logger.error(f"Failed to cancel training job: {e}")
        raise HTTPException(status_code=500, detail="Failed to cancel training job")

@router.post("/{model_id}/activate")
async def activate_model(
    model_id: int,
    db: Session = Depends(get_db)
):
    """Activate a model for trading"""
    try:
        service = ModelService(db)
        service.activate_model(model_id)
        return {"message": "Model activated successfully"}
    except Exception as e:
        logger.error(f"Failed to activate model: {e}")
        raise HTTPException(status_code=500, detail="Failed to activate model")

@router.post("/{model_id}/deactivate")
async def deactivate_model(
    model_id: int,
    db: Session = Depends(get_db)
):
    """Deactivate a model"""
    try:
        service = ModelService(db)
        service.deactivate_model(model_id)
        return {"message": "Model deactivated successfully"}
    except Exception as e:
        logger.error(f"Failed to deactivate model: {e}")
        raise HTTPException(status_code=500, detail="Failed to deactivate model")

@router.delete("/{model_id}")
async def delete_model(
    model_id: int,
    db: Session = Depends(get_db)
):
    """Delete a model"""
    try:
        service = ModelService(db)
        service.delete_model(model_id)
        return {"message": "Model deleted successfully"}
    except Exception as e:
        logger.error(f"Failed to delete model: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete model")

@router.get("/{model_id}/performance")
async def get_model_performance(
    model_id: int,
    db: Session = Depends(get_db)
):
    """Get model performance metrics"""
    try:
        service = ModelService(db)
        performance = service.get_model_performance(model_id)
        return performance
    except Exception as e:
        logger.error(f"Failed to get model performance: {e}")
        raise HTTPException(status_code=500, detail="Failed to get model performance")

@router.post("/batch-train")
async def batch_train_models(
    symbols: List[str],
    model_type: str = "gradient_boosting",
    hyperparameters: dict = {},
    background_tasks: BackgroundTasks = None,
    db: Session = Depends(get_db)
):
    """Start training for multiple symbols"""
    try:
        training_service = TrainingService(db)
        jobs = []
        
        for symbol in symbols:
            job = training_service.create_training_job({
                "symbol": symbol,
                "model_type": model_type,
                "hyperparameters": hyperparameters
            })
            jobs.append(job)
            
            # Start training in background
            if background_tasks:
                background_tasks.add_task(
                    training_service.train_model_async,
                    job.id,
                    symbol,
                    model_type,
                    hyperparameters
                )
        
        return {
            "message": f"Started training for {len(symbols)} symbols",
            "jobs": jobs
        }
    except Exception as e:
        logger.error(f"Failed to batch train models: {e}")
        raise HTTPException(status_code=500, detail="Failed to batch train models")
