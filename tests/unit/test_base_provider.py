"""
Unit tests for the BaseProvider class
"""

import pytest
import pandas as pd
from typing import Union, List, Optional
from marketquery.providers.base import BaseProvider


class TestProvider(BaseProvider):
    """Concrete test implementation of BaseProvider"""
    
    def download(
        self,
        tickers: Union[str, List[str]],
        start: Optional[str] = None,
        end: Optional[str] = None,
        interval: str = "1d",
        **kwargs
    ) -> Optional[pd.DataFrame]:
        """Test implementation that raises NotImplementedError"""
        raise NotImplementedError("Test implementation")


class TestBaseProvider:
    """Test suite for BaseProvider class"""
    
    def test_init_with_api_key(self):
        """Test initialization with API key"""
        api_key = "test_key"
        provider = TestProvider(api_key=api_key)
        assert provider.api_key == api_key
        assert provider.premium_api_key is None
        
    def test_init_with_premium_api_key(self):
        """Test initialization with premium API key"""
        api_key = "test_key"
        premium_api_key = "premium_test_key"
        provider = TestProvider(api_key=api_key, premium_api_key=premium_api_key)
        assert provider.api_key == api_key
        assert provider.premium_api_key == premium_api_key
        
    def test_init_without_api_key(self):
        """Test initialization without API key"""
        provider = TestProvider()
        assert provider.api_key is None
        assert provider.premium_api_key is None
        
    def test_download_not_implemented(self):
        """Test that download method raises NotImplementedError"""
        provider = TestProvider()
        with pytest.raises(NotImplementedError):
            provider.download(tickers="AAPL")
            
    def test_handle_empty_dataframe_with_none(self):
        """Test _handle_empty_dataframe with None input"""
        provider = TestProvider()
        tickers = ["AAPL", "GOOGL"]
        result = provider._handle_empty_dataframe(None, tickers)
        
        assert isinstance(result, pd.DataFrame)
        assert result.empty
        assert len(result.columns.levels[0]) == 2  # Two tickers
        assert "AAPL" in result.columns.levels[0]
        assert "GOOGL" in result.columns.levels[0]
        
    def test_handle_empty_dataframe_with_empty_df(self):
        """Test _handle_empty_dataframe with empty DataFrame"""
        provider = TestProvider()
        tickers = ["AAPL"]
        empty_df = pd.DataFrame()
        result = provider._handle_empty_dataframe(empty_df, tickers)
        
        assert isinstance(result, pd.DataFrame)
        assert result.empty
        assert "AAPL" in result.columns.levels[0]
        
    def test_handle_empty_dataframe_with_missing_tickers(self):
        """Test _handle_empty_dataframe with missing tickers"""
        provider = TestProvider()
        
        # Create a DataFrame with only AAPL data
        dates = pd.date_range('2025-01-01', periods=3)
        df = pd.DataFrame({
            ('AAPL', 'adj_close'): [150.0, 151.0, 152.0],
            ('AAPL', 'volume'): [1000, 1100, 1200]
        }, index=dates)
        df.columns = pd.MultiIndex.from_tuples(df.columns)
        
        # Request both AAPL and GOOGL
        tickers = ["AAPL", "GOOGL"]
        result = provider._handle_empty_dataframe(df, tickers)
        
        assert isinstance(result, pd.DataFrame)
        assert not result.empty
        assert "AAPL" in result.columns.levels[0]
        assert "GOOGL" in result.columns.levels[0]
        assert len(result.columns.levels[0]) == 2
