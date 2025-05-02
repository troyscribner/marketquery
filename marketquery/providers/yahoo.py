"""
Yahoo Finance provider implementation
"""

from typing import Dict, Any, Union, Optional, List
import pandas as pd
import yfinance as yf
from .base import BaseProvider

class YahooProvider(BaseProvider):
    """
    Yahoo Finance market data provider
    """
    
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
        multi_level_index: bool = True,
        **kwargs
    ) -> Optional[pd.DataFrame]:
        """
        Download market data from Yahoo Finance
        
        Args:
            tickers: Ticker symbol or list of ticker symbols
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
            multi_level_index: Use multi-level index for DataFrame
            **kwargs: Additional provider-specific parameters
            
        Returns:
            pandas.DataFrame containing the market data or None if download fails
        """
        try:
            df = yf.download(
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
            
            return self._handle_empty_dataframe(df, tickers)
            
        except Exception as e:
            # Handle rate limiting and other errors
            print(f"Error downloading {tickers}: {str(e)}")
            return None
