"""
Cache manager for market data
"""

import os
import json
import pickle
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, Union
import pandas as pd
from appdirs import user_cache_dir


class CacheManager:
    """Manages caching of market data"""
    
    def __init__(self, cache_dir: Optional[str] = None):
        """
        Initialize cache manager
        
        Args:
            cache_dir: Optional custom cache directory. Defaults to platform-specific cache directory.
        """
        # Use appdirs to get the correct cache directory for the platform
        self.cache_dir = cache_dir or user_cache_dir("marketquery")
        self._ensure_cache_structure()
    
    def _ensure_cache_structure(self):
        """Create cache directory structure if it doesn't exist"""
        # Create base cache directory
        Path(self.cache_dir).mkdir(parents=True, exist_ok=True)
        
        # Create provider directories
        for provider in ["stooq", "yahoo", "tiingo", "alpha_vantage", "polygon"]:
            for data_type in ["unadjusted", "adjusted"]:
                Path(self.cache_dir, provider, data_type).mkdir(parents=True, exist_ok=True)
    
    def _get_cache_path(self, provider: str, data_type: str, symbol: str) -> tuple[Path, Path]:
        """
        Get paths for data and metadata files
        
        Args:
            provider: Data provider (e.g., 'stooq', 'yahoo')
            data_type: Type of data ('unadjusted' or 'adjusted')
            symbol: Stock symbol
            
        Returns:
            Tuple of (data_path, metadata_path)
        """
        base_path = Path(self.cache_dir, provider, data_type)
        return (
            base_path / f"{symbol}.pkl",
            base_path / f"{symbol}.json"
        )
    
    def save_data(
        self,
        provider: str,
        data_type: str,
        symbol: str,
        data: pd.DataFrame,
        start_date: str,
        end_date: str,
        interval: str
    ):
        """
        Save data to cache
        
        Args:
            provider: Data provider
            data_type: Type of data ('unadjusted' or 'adjusted')
            symbol: Stock symbol
            data: DataFrame to cache
            start_date: Start date of data
            end_date: End date of data
            interval: Data interval (e.g., '1d', '1wk')
        """
        data_path, metadata_path = self._get_cache_path(provider, data_type, symbol)

        # Save data
        data.to_pickle(data_path)
        
        # Save metadata
        metadata = {
            "start_date": start_date,
            "end_date": end_date,
            "interval": interval,
            "cached_at": datetime.now().isoformat()
        }
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f)
    
    def load_data(
        self,
        provider: str,
        data_type: str,
        symbol: str,
        start_date: str,
        end_date: str,
        interval: str
    ) -> Optional[pd.DataFrame]:
        """
        Load data from cache if available and valid
        
        Args:
            provider: Data provider
            data_type: Type of data ('unadjusted' or 'adjusted')
            symbol: Stock symbol
            start_date: Requested start date
            end_date: Requested end date
            interval: Requested interval
            
        Returns:
            Cached DataFrame if available and valid, None otherwise
        """
        data_path, metadata_path = self._get_cache_path(provider, data_type, symbol)
        
        # Check if cache exists
        if not data_path.exists() or not metadata_path.exists():
            return None
            
        # Load metadata
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)
            
        # Check if cache is valid
        if (
            metadata["start_date"] == start_date and
            metadata["end_date"] == end_date and
            metadata["interval"] == interval
        ):
            # Load and return cached data
            return pd.read_pickle(data_path)
            
        return None
    
    def clear_cache(self, provider: Optional[str] = None):
        """
        Clear cache for a specific provider or all providers
        
        Args:
            provider: Optional provider to clear cache for. If None, clears all caches.
        """
        if provider:
            # Clear specific provider
            provider_path = Path(self.cache_dir, provider)
            if provider_path.exists():
                for data_type in ["unadjusted", "adjusted"]:
                    type_path = provider_path / data_type
                    if type_path.exists():
                        for file in type_path.glob("*"):
                            file.unlink()
        else:
            # Clear all caches
            for provider_path in Path(self.cache_dir).glob("*"):
                if provider_path.is_dir():
                    for data_type in ["unadjusted", "adjusted"]:
                        type_path = provider_path / data_type
                        if type_path.exists():
                            for file in type_path.glob("*"):
                                file.unlink() 
