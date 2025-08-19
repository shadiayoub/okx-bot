#!/usr/bin/env python3
"""
Symbols management router
Dynamic symbol discovery and configuration
"""

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
import logging

from api.database import get_db, Symbol
from api.schemas.symbol import SymbolCreate, SymbolUpdate, SymbolResponse, SymbolDiscovery
from api.services.symbol_service import SymbolService
from api.services.okx_service import OKXService
from api.services.default_configuration_service import DefaultConfigurationService

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/", response_model=List[SymbolResponse])
async def get_symbols(
    enabled_only: bool = False,
    db: Session = Depends(get_db)
):
    """Get all symbols or only enabled ones"""
    try:
        service = SymbolService(db)
        symbols = service.get_symbols(enabled_only=enabled_only)
        return symbols
    except Exception as e:
        logger.error(f"Failed to get symbols: {e}")
        raise HTTPException(status_code=500, detail="Failed to get symbols")

@router.get("/discover", response_model=List[SymbolDiscovery])
async def discover_symbols(
    db: Session = Depends(get_db)
):
    """Discover available symbols from OKX"""
    try:
        okx_service = OKXService()
        available_symbols = await okx_service.get_available_symbols()
        
        # Get existing symbols
        symbol_service = SymbolService(db)
        existing_symbols = symbol_service.get_symbols()
        existing_okx_symbols = [s.okx_symbol for s in existing_symbols]
        
        # Filter out existing symbols
        new_symbols = []
        for symbol in available_symbols:
            if symbol not in existing_okx_symbols:
                new_symbols.append({
                    "okx_symbol": symbol,
                    "model_symbol": symbol.replace("-USDT-SWAP", "USDT"),
                    "display_name": symbol.replace("-USDT-SWAP", ""),
                    "available": True
                })
        
        return new_symbols
    except Exception as e:
        logger.error(f"Failed to discover symbols: {e}")
        raise HTTPException(status_code=500, detail="Failed to discover symbols")

@router.post("/", response_model=SymbolResponse)
async def create_symbol(
    symbol: SymbolCreate,
    db: Session = Depends(get_db)
):
    """Create a new symbol"""
    try:
        service = SymbolService(db)
        created_symbol = service.create_symbol(symbol)
        return created_symbol
    except Exception as e:
        logger.error(f"Failed to create symbol: {e}")
        raise HTTPException(status_code=500, detail="Failed to create symbol")

@router.put("/{symbol_id}", response_model=SymbolResponse)
async def update_symbol(
    symbol_id: int,
    symbol: SymbolUpdate,
    db: Session = Depends(get_db)
):
    """Update symbol configuration"""
    try:
        service = SymbolService(db)
        updated_symbol = service.update_symbol(symbol_id, symbol)
        return updated_symbol
    except Exception as e:
        logger.error(f"Failed to update symbol: {e}")
        raise HTTPException(status_code=500, detail="Failed to update symbol")

@router.delete("/{symbol_id}")
async def delete_symbol(
    symbol_id: int,
    db: Session = Depends(get_db)
):
    """Delete a symbol"""
    try:
        service = SymbolService(db)
        service.delete_symbol(symbol_id)
        return {"message": "Symbol deleted successfully"}
    except Exception as e:
        logger.error(f"Failed to delete symbol: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete symbol")

@router.post("/{symbol_id}/enable")
async def enable_symbol(
    symbol_id: int,
    db: Session = Depends(get_db)
):
    """Enable a symbol for trading"""
    try:
        service = SymbolService(db)
        service.enable_symbol(symbol_id)
        return {"message": "Symbol enabled successfully"}
    except Exception as e:
        logger.error(f"Failed to enable symbol: {e}")
        raise HTTPException(status_code=500, detail="Failed to enable symbol")

@router.post("/{symbol_id}/disable")
async def disable_symbol(
    symbol_id: int,
    db: Session = Depends(get_db)
):
    """Disable a symbol for trading"""
    try:
        service = SymbolService(db)
        service.disable_symbol(symbol_id)
        return {"message": "Symbol disabled successfully"}
    except Exception as e:
        logger.error(f"Failed to disable symbol: {e}")
        raise HTTPException(status_code=500, detail="Failed to disable symbol")

@router.post("/batch-enable")
async def batch_enable_symbols(
    symbol_ids: List[int],
    db: Session = Depends(get_db)
):
    """Enable multiple symbols at once"""
    try:
        service = SymbolService(db)
        enabled_count = service.batch_enable_symbols(symbol_ids)
        return {"message": f"{enabled_count} symbols enabled successfully"}
    except Exception as e:
        logger.error(f"Failed to batch enable symbols: {e}")
        raise HTTPException(status_code=500, detail="Failed to batch enable symbols")

@router.get("/{symbol_id}/status")
async def get_symbol_status(
    symbol_id: int,
    db: Session = Depends(get_db)
):
    """Get detailed status of a symbol"""
    try:
        service = SymbolService(db)
        status = service.get_symbol_status(symbol_id)
        return status
    except Exception as e:
        logger.error(f"Failed to get symbol status: {e}")
        raise HTTPException(status_code=500, detail="Failed to get symbol status")

@router.post("/batch-disable")
async def batch_disable_symbols(
    symbol_ids: List[int],
    db: Session = Depends(get_db)
):
    """Disable multiple symbols at once"""
    try:
        service = SymbolService(db)
        count = service.batch_disable_symbols(symbol_ids)
        return {"message": f"Disabled {count} symbols successfully"}
    except Exception as e:
        logger.error(f"Failed to batch disable symbols: {e}")
        raise HTTPException(status_code=500, detail="Failed to batch disable symbols")

@router.post("/bulk-operations")
async def bulk_symbol_operations(
    operation: str,
    symbol_names: List[str],
    db: Session = Depends(get_db)
):
    """Perform bulk operations on symbols by name"""
    try:
        service = SymbolService(db)
        default_service = DefaultConfigurationService()
        
        if operation == "enable":
            count = service.bulk_enable_by_names(symbol_names)
            return {"message": f"Enabled {count} symbols successfully"}
        elif operation == "disable":
            count = service.bulk_disable_by_names(symbol_names)
            return {"message": f"Disabled {count} symbols successfully"}
        elif operation == "add":
            count = service.bulk_add_symbols(symbol_names, default_service)
            return {"message": f"Added {count} symbols successfully"}
        else:
            raise HTTPException(status_code=400, detail="Invalid operation")
    except Exception as e:
        logger.error(f"Failed to perform bulk operation: {e}")
        raise HTTPException(status_code=500, detail="Failed to perform bulk operation")

@router.get("/default-configuration")
async def get_default_configuration():
    """Get default recommended symbols and models"""
    try:
        default_service = DefaultConfigurationService()
        return {
            "symbols": default_service.get_default_symbols(),
            "models": default_service.get_default_models(),
            "bulk_operations": default_service.get_bulk_operations()
        }
    except Exception as e:
        logger.error(f"Failed to get default configuration: {e}")
        raise HTTPException(status_code=500, detail="Failed to get default configuration")

@router.post("/load-defaults")
async def load_default_symbols(
    db: Session = Depends(get_db)
):
    """Load default recommended symbols into the database"""
    try:
        service = SymbolService(db)
        default_service = DefaultConfigurationService()
        count = service.load_default_symbols(default_service)
        return {"message": f"Loaded {count} default symbols successfully"}
    except Exception as e:
        logger.error(f"Failed to load default symbols: {e}")
        raise HTTPException(status_code=500, detail="Failed to load default symbols")
