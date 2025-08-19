#!/usr/bin/env python3
"""
Model service for managing ML models
"""

from sqlalchemy.orm import Session
from typing import List, Optional
import logging

from api.database import Model
from api.schemas.model import ModelCreate, ModelUpdate

logger = logging.getLogger(__name__)

class ModelService:
    def __init__(self, db: Session):
        self.db = db

    def get_models(self, symbol: Optional[str] = None, active_only: bool = False) -> List[Model]:
        """Get all models or filter by symbol"""
        query = self.db.query(Model)
        if symbol:
            query = query.filter(Model.symbol_id == symbol)
        if active_only:
            query = query.filter(Model.is_active == True)
        return query.all()

    def get_available_model_types(self) -> List[str]:
        """Get list of available model types"""
        return [
            "gradient_boosting",
            "random_forest",
            "neural_network",
            "ensemble"
        ]

    def activate_model(self, model_id: int):
        """Activate a model for trading"""
        db_model = self.db.query(Model).filter(Model.id == model_id).first()
        if db_model:
            db_model.is_active = True
            self.db.commit()

    def deactivate_model(self, model_id: int):
        """Deactivate a model"""
        db_model = self.db.query(Model).filter(Model.id == model_id).first()
        if db_model:
            db_model.is_active = False
            self.db.commit()

    def delete_model(self, model_id: int):
        """Delete a model"""
        db_model = self.db.query(Model).filter(Model.id == model_id).first()
        if db_model:
            self.db.delete(db_model)
            self.db.commit()

    def get_model_performance(self, model_id: int) -> dict:
        """Get model performance metrics"""
        db_model = self.db.query(Model).filter(Model.id == model_id).first()
        if not db_model:
            raise ValueError("Model not found")
        
        return {
            "id": db_model.id,
            "accuracy": db_model.accuracy,
            "performance_metrics": db_model.performance_metrics,
            "training_date": db_model.training_date
        }
