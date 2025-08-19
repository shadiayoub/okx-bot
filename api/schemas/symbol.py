#!/usr/bin/env python3
"""
Symbol schemas for API
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SymbolBase(BaseModel):
    okx_symbol: str
    model_symbol: str
    display_name: str
    risk_multiplier: float = 1.0
    min_balance: float = 0.0
    max_position_size: float = 0.0

class SymbolCreate(SymbolBase):
    enabled: bool = False

class SymbolUpdate(BaseModel):
    display_name: Optional[str] = None
    enabled: Optional[bool] = None
    risk_multiplier: Optional[float] = None
    min_balance: Optional[float] = None
    max_position_size: Optional[float] = None

class SymbolResponse(SymbolBase):
    id: int
    enabled: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class SymbolDiscovery(BaseModel):
    okx_symbol: str
    model_symbol: str
    display_name: str
    available: bool = True
