"""
MarketQuery - A unified interface for market data APIs
"""

__version__ = "0.1.0"
__author__ = "troyscribner"
__license__ = "MIT"

from .client import MarketDataClient
from typing import List, Optional, Union, Any
import pandas as pd

__all__ = ["MarketDataClient", "download", "help"]

def help():
    """
    Display help information about MarketQuery.
    
    This function provides information about:
    - Available providers
    - Basic usage examples
    - Common parameters
    - Cache management
    """
    print("\nMarketQuery Help")
    print("===============\n")
    
    print("Quick Start:")
    print("-----------")
    print("import marketquery as mq")
    print("")
    print("# Download data for a single ticker")
    print("data = mq.download('AAPL', start='2024-01-01', end='2024-01-31')")
    print("")
    print("# Download data for multiple tickers")
    print("data = mq.download(['AAPL', 'GOOGL', 'MSFT'], start='2024-01-01', end='2024-01-31')")
    print("")
    print("# Use a different provider (e.g., Tiingo)")
    print("data = mq.download('AAPL', provider='tiingo', api_key='your_api_key')")
    
    print("\nAvailable Providers:")
    print("-------------------")
    print("1. Yahoo Finance (default)")
    print("   - Free, no API key required")
    print("   - Supports most major exchanges")
    print("   - Rate limits may apply\n")
    
    print("2. Stooq")
    print("   - Free, no API key required")
    print("   - Limited to US stocks\n")
    
    print("3. Tiingo")
    print("   - Requires API key")
    print("   - Free tier available")
    print("   - Good for historical data\n")
    
    print("4. Alpha Vantage")
    print("   - Requires API key")
    print("   - Free tier available")
    print("   - Premium tier for adjusted prices\n")
    
    print("5. Polygon.io")
    print("   - Requires paid subscription")
    print("   - Professional-grade data\n")
    
    print("\nCommon Parameters:")
    print("----------------")
    print("tickers: Single ticker or list of tickers (e.g., 'AAPL' or ['AAPL', 'GOOGL'])")
    print("start: Start date in YYYY-MM-DD format (e.g., '2024-01-01')")
    print("end: End date in YYYY-MM-DD format (e.g., '2024-01-31')")
    print("interval: Data interval ('1d', '1wk', '1mo')")
    print("auto_adjust: Adjust prices for splits/dividends (True/False)")
    print("threads: Use parallel downloads for multiple tickers (True/False)")
    print("provider: Data provider to use ('yahoo', 'tiingo', etc.)")
    print("api_key: API key for providers that require one")
    
    print("\nCache Management:")
    print("---------------")
    print("MarketQuery automatically caches downloaded data to improve performance and reduce API calls.")
    print("")
    print("Cache Location:")
    print("  - macOS: ~/Library/Caches/marketquery/")
    print("  - Linux: ~/.cache/marketquery/")
    print("  - Windows: %LOCALAPPDATA%\\marketquery\\")
    print("")
    print("Cache Behavior:")
    print("  - Data is cached by provider, ticker, date range, and interval")
    print("  - Cache is checked before making API requests")
    print("  - Cache is automatically updated when new data is downloaded")
    print("")
    print("Cache Control Parameters:")
    print("  save: Whether to save downloaded data to cache (default: True)")
    print("  load: Whether to load data from cache (default: True)")
    print("")
    print("\nExamples:")
    print("--------")
    print("# Basic usage with default provider (Yahoo)")
    print("data = mq.download('AAPL')")
    print("")
    print("# Use Stooq provider (free, no API key required)")
    print("data = mq.download('AAPL', provider='stooq')")
    print("")
    print("# Use Tiingo provider (requires API key)")
    print("data = mq.download('AAPL', provider='tiingo', api_key='your_api_key')")
    print("")
    print("# Specify date range")
    print("data = mq.download('AAPL', start='2024-01-01', end='2024-01-31')")
    print("")
    print("# Use weekly data")
    print("data = mq.download('AAPL', interval='1wk')")
    print("")
    print("# Get adjusted prices")
    print("data = mq.download('AAPL', auto_adjust=True)")
    print("")
    print("# Download multiple tickers")
    print("data = mq.download(['AAPL', 'GOOGL', 'MSFT'])")
    print("")
    print("# Disable caching")
    print("data = mq.download('AAPL', save=False)  # Don't save to cache")
    print("data = mq.download('AAPL', load=False)  # Don't use cached data")
    print("data = mq.download('AAPL', save=False, load=False)  # Disable caching completely")
    print("")
    print("# Clear cache")
    print("client = mq.MarketDataClient()")
    print("client.clear_cache()  # Clear all caches")
    print("client.clear_cache('tiingo')  # Clear specific provider's cache")

def download(
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
    provider: str = "yahoo",
    api_key: Optional[str] = None,
    premium_api_key: Optional[str] = None,
    **kwargs
) -> pd.DataFrame:
    """
    Download market data for the given tickers.
    
    This function mirrors yfinance's download interface while adding support for
    multiple providers.
    
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
        provider: Data provider to use (default: "yahoo")
        api_key: Optional API key for the provider
        premium_api_key: Optional premium API key for the provider
        **kwargs: Additional provider-specific parameters
        
    Returns:
        pandas.DataFrame containing the market data
        
    Raises:
        ValueError: If tickers is empty or invalid
    """
    client = MarketDataClient(
        provider=provider,
        api_key=api_key,
        premium_api_key=premium_api_key
    )
    
    return client.download(
        tickers=tickers,
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
        progress=progress,
        period=period,
        interval=interval,
        prepost=prepost,
        proxy=proxy,
        rounding=rounding,
        timeout=timeout,
        session=session,
        **kwargs
    ) 
