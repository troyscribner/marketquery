"""
Base provider class for market data providers
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Union, Any
import pandas as pd


class BaseProvider(ABC):
    """
    Abstract base class for market data providers.
    
    All market data providers must implement this interface.
    """
    
    def __init__(self, api_key: Optional[str] = None, premium_api_key: Optional[str] = None):
        """
        Initialize the provider.
        
        Args:
            api_key: Optional regular API key for the provider
            premium_api_key: Optional premium API key for the provider
        """
        self.api_key = api_key
        self.premium_api_key = premium_api_key
    
    def _handle_empty_dataframe(self, df: pd.DataFrame, tickers: Union[str, List[str]]) -> Optional[pd.DataFrame]:
        """
        Handle empty DataFrames consistently across all providers.
        
        Args:
            df: The DataFrame to check
            tickers: The ticker(s) that were requested
            
        Returns:
            The DataFrame if not empty, None otherwise
        """
        if df.empty:
            print(f"No data found for {tickers}")
            return None
        return df
    
    @abstractmethod
    def download(
        self,
        tickers: Union[str, List[str]],
        start: Optional[str] = None,
        end: Optional[str] = None,
        actions: bool = False,
        threads: bool = True,
        ignore_tz: Optional[bool] = None,
        group_by: str = 'column',
        auto_adjust: Optional[bool] = None,
        back_adjust: bool = False,
        repair: bool = False,
        keepna: bool = False,
        progress: bool = True,
        period: str = "max",
        interval: str = "1d",
        prepost: bool = False,
        proxy: Optional[str] = None,
        rounding: bool = False,
        timeout: int = 10,
        session: Optional[Any] = None,
        **kwargs
    ) -> Optional[pd.DataFrame]:
        """
        Download market data for the given tickers.
        
        Args:
            tickers: Single ticker symbol or list of ticker symbols
            start: Download start date string (YYYY-MM-DD) or _datetime
            end: Download end date string (YYYY-MM-DD) or _datetime
            actions: Download stock dividends and stock splits events
            threads: Use threads for mass downloading
            ignore_tz: Ignore timezone when aligning data from different exchanges
            group_by: Group by ticker or column
            auto_adjust: Adjust all OHLC automatically
            back_adjust: Back-adjusted data to mimic true historical prices
            repair: Repair missing data
            keepna: Keep NaN values
            progress: Show download progress
            period: Valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
            interval: Valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
            prepost: Include pre and post market data
            proxy: Proxy URL scheme
            rounding: Round values to 2 decimal places
            timeout: Timeout for requests
            session: Custom requests session
            **kwargs: Additional provider-specific parameters
            
        Returns:
            pandas.DataFrame containing the market data or None if download fails
        """
        pass
