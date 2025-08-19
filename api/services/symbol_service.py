#!/usr/bin/env python3
"""
Symbol service for managing trading symbols
"""

from sqlalchemy.orm import Session
from typing import List, Optional
import logging

from api.database import Symbol
from api.schemas.symbol import SymbolCreate, SymbolUpdate

logger = logging.getLogger(__name__)

class SymbolService:
    def __init__(self, db: Session):
        self.db = db

    def get_symbols(self, enabled_only: bool = False) -> List[Symbol]:
        """Get all symbols or only enabled ones"""
        query = self.db.query(Symbol)
        if enabled_only:
            query = query.filter(Symbol.enabled == True)
        return query.all()

    def create_symbol(self, symbol: SymbolCreate) -> Symbol:
        """Create a new symbol"""
        db_symbol = Symbol(**symbol.dict())
        self.db.add(db_symbol)
        self.db.commit()
        self.db.refresh(db_symbol)
        return db_symbol

    def update_symbol(self, symbol_id: int, symbol: SymbolUpdate) -> Symbol:
        """Update symbol configuration"""
        db_symbol = self.db.query(Symbol).filter(Symbol.id == symbol_id).first()
        if not db_symbol:
            raise ValueError("Symbol not found")
        
        update_data = symbol.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_symbol, field, value)
        
        self.db.commit()
        self.db.refresh(db_symbol)
        return db_symbol

    def delete_symbol(self, symbol_id: int):
        """Delete a symbol"""
        db_symbol = self.db.query(Symbol).filter(Symbol.id == symbol_id).first()
        if db_symbol:
            self.db.delete(db_symbol)
            self.db.commit()

    def enable_symbol(self, symbol_id: int):
        """Enable a symbol for trading"""
        db_symbol = self.db.query(Symbol).filter(Symbol.id == symbol_id).first()
        if db_symbol:
            db_symbol.enabled = True
            self.db.commit()

    def disable_symbol(self, symbol_id: int):
        """Disable a symbol for trading"""
        db_symbol = self.db.query(Symbol).filter(Symbol.id == symbol_id).first()
        if db_symbol:
            db_symbol.enabled = False
            self.db.commit()

    def batch_enable_symbols(self, symbol_ids: List[int]) -> int:
        """Enable multiple symbols at once"""
        count = self.db.query(Symbol).filter(Symbol.id.in_(symbol_ids)).update(
            {"enabled": True}, synchronize_session=False
        )
        self.db.commit()
        return count

    def get_symbol_status(self, symbol_id: int) -> dict:
        """Get detailed status of a symbol"""
        db_symbol = self.db.query(Symbol).filter(Symbol.id == symbol_id).first()
        if not db_symbol:
            raise ValueError("Symbol not found")
        
        return {
            "id": db_symbol.id,
            "okx_symbol": db_symbol.okx_symbol,
            "enabled": db_symbol.enabled,
            "risk_multiplier": db_symbol.risk_multiplier,
            "created_at": db_symbol.created_at
        }

    def batch_disable_symbols(self, symbol_ids: List[int]) -> int:
        """Disable multiple symbols at once"""
        count = self.db.query(Symbol).filter(Symbol.id.in_(symbol_ids)).update(
            {"enabled": False}, synchronize_session=False
        )
        self.db.commit()
        return count

    def bulk_enable_by_names(self, symbol_names: List[str]) -> int:
        """Enable symbols by their OKX symbol names"""
        count = self.db.query(Symbol).filter(Symbol.okx_symbol.in_(symbol_names)).update(
            {"enabled": True}, synchronize_session=False
        )
        self.db.commit()
        return count

    def bulk_disable_by_names(self, symbol_names: List[str]) -> int:
        """Disable symbols by their OKX symbol names"""
        count = self.db.query(Symbol).filter(Symbol.okx_symbol.in_(symbol_names)).update(
            {"enabled": False}, synchronize_session=False
        )
        self.db.commit()
        return count

    def bulk_add_symbols(self, symbol_names: List[str], default_service) -> int:
        """Add multiple symbols from default configuration"""
        count = 0
        for symbol_name in symbol_names:
            default_symbol = default_service.get_symbol_by_name(symbol_name)
            if default_symbol:
                # Check if symbol already exists
                existing = self.db.query(Symbol).filter(Symbol.okx_symbol == default_symbol["okx_symbol"]).first()
                if not existing:
                    symbol_create = SymbolCreate(**default_symbol)
                    self.create_symbol(symbol_create)
                    count += 1
        return count

    def load_default_symbols(self, default_service) -> int:
        """Load all default symbols into the database"""
        default_symbols = default_service.get_default_symbols()
        count = 0
        
        for default_symbol in default_symbols:
            # Check if symbol already exists
            existing = self.db.query(Symbol).filter(Symbol.okx_symbol == default_symbol["okx_symbol"]).first()
            if not existing:
                symbol_create = SymbolCreate(**default_symbol)
                self.create_symbol(symbol_create)
                count += 1
        
        return count
