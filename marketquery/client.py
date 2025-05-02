"""
MarketDataClient - Main client class for interacting with market data providers
"""

from typing import Dict, List, Optional, Union, Any
from tqdm import tqdm
import pandas as pd
from .providers.base import BaseProvider
from .providers.yahoo import YahooProvider
from .providers.alpha_vantage import AlphaVantageProvider
from .providers.stooq import StooqProvider
from .providers.polygon import PolygonProvider
from .providers.tiingo import TiingoProvider
from .cache import CacheManager


class MarketDataClient:
    """
    Main client class for interacting with market data providers.
    
    This class provides a unified interface for downloading market data
    from various providers. It handles provider initialization and data
    retrieval in a consistent way.
    """
    
    def __init__(
        self,
        provider: str = "yahoo",
        api_key: Optional[str] = None,
        premium_api_key: Optional[str] = None,
        cache_dir: Optional[str] = None
    ):
        """
        Initialize the MarketDataClient with a specific provider.
        
        Args:
            provider: Name of the provider to use (default: "yahoo")
            api_key: Optional API key for the provider
            premium_api_key: Optional premium API key for the provider
            cache_dir: Optional custom cache directory
        """
        self.provider = self._get_provider(provider, api_key, premium_api_key)
        self.cache = CacheManager(cache_dir)
    
    def _get_provider(self, provider: str, api_key: Optional[str], premium_api_key: Optional[str]) -> BaseProvider:
        """
        Get the appropriate provider instance.
        
        Args:
            provider: Name of the provider
            api_key: Optional API key
            premium_api_key: Optional premium API key
            
        Returns:
            BaseProvider instance
            
        Raises:
            ValueError: If provider is not supported
        """
        providers = {
            "yahoo": YahooProvider,
            "alpha_vantage": AlphaVantageProvider,
            "stooq": StooqProvider,
            "polygon": PolygonProvider,
            "tiingo": TiingoProvider
        }
        
        if provider not in providers:
            raise ValueError(f"Provider '{provider}' not supported. Available providers: {list(providers.keys())}")
            
        # Stooq doesn't need an API key
        if provider == "stooq":
            return providers[provider]()
            
        return providers[provider](api_key=api_key, premium_api_key=premium_api_key)
    
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
        save: bool = True,
        load: bool = True,
        **kwargs
    ) -> pd.DataFrame:
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
            save: Whether to save results to cache
            load: Whether to load results from cache
            **kwargs: Additional provider-specific parameters
            
        Returns:
            pandas.DataFrame containing the market data
            
        Raises:
            ValueError: If tickers is empty or invalid
        """
        if not tickers:
            raise ValueError("At least one ticker must be provided")
            
        if isinstance(tickers, str):
            tickers = [tickers]
            
        # Determine data type (adjusted or unadjusted)
        data_type = "adjusted" if auto_adjust or back_adjust else "unadjusted"
        
        # Download data for each ticker
        dfs = []
        ticker_iter = tickers if not progress else tqdm(tickers, desc="Downloading symbols")
        
        for ticker in ticker_iter:
            # Try to load from cache first
            cached_data = None
            if load:
                cached_data = self.cache.load_data(
                    provider=self.provider.__class__.__name__.lower().replace("provider", ""),
                    data_type=data_type,
                    symbol=ticker,
                    start_date=start or "",
                    end_date=end or "",
                    interval=interval
                )
            
            if cached_data is not None:
                print(f"Using cached data for {ticker} (use load=False to disable cache)")
                dfs.append(cached_data)
            else:
                # Download fresh data
                df = self.provider.download(
                    tickers=ticker,
                    start=start,
                    end=end,
                    actions=actions,
                    threads=threads,
                    ignore_tz=ignore_tz,
                    group_by=group_by,
                    auto_adjust=auto_adjust,
                    back_adjust=back_adjust,
                    repair=repair,
                    keepna=keepna,
                    progress=False,  # We handle progress at client level
                    period=period,
                    interval=interval,
                    prepost=prepost,
                    proxy=proxy,
                    rounding=rounding,
                    timeout=timeout,
                    session=session,
                    **kwargs
                )

                # Save to cache if requested
                if save and df is not None:
                    print(f"Saving data to cache for {ticker} (use save=False to disable cache)")
                    self.cache.save_data(
                        provider=self.provider.__class__.__name__.lower().replace("provider", ""),
                        data_type=data_type,
                        symbol=ticker,
                        data=df,
                        start_date=start or "",
                        end_date=end or "",
                        interval=interval
                    )
                
                dfs.append(df)
            
        if not dfs:
            raise Exception("No data was successfully downloaded")
            
        # Combine all dataframes
        if len(dfs) == 1:
            return dfs[0]
        else:
            return pd.concat(dfs, axis=1)
    
    def clear_cache(self, provider: Optional[str] = None):
        """
        Clear cache for a specific provider or all providers
        
        Args:
            provider: Optional provider to clear cache for. If None, clears all caches.
        """
        self.cache.clear_cache(provider) 
