"""
Unit tests for the MarketDataClient class
"""

import pytest
import pandas as pd
from marketquery import MarketDataClient


class TestMarketDataClient:
    """Test suite for MarketDataClient class"""
    
    def test_init_default_provider(self):
        """Test initialization with default provider"""
        client = MarketDataClient()
        assert client.provider.__class__.__name__ == "YahooProvider"
        
    def test_init_with_api_key(self):
        """Test initialization with API key"""
        api_key = "test_key"
        client = MarketDataClient(api_key=api_key)
        assert client.provider.api_key == api_key
        
    def test_init_invalid_provider(self):
        """Test initialization with invalid provider"""
        with pytest.raises(ValueError) as exc_info:
            MarketDataClient(provider="invalid")
        assert "Provider 'invalid' not supported" in str(exc_info.value)
        
    def test_download_empty_tickers(self):
        """Test download with empty tickers"""
        client = MarketDataClient()
        with pytest.raises(ValueError) as exc_info:
            client.download(tickers=[])
        assert "No tickers provided" in str(exc_info.value)
        
    def test_download_single_ticker(self, mocker):
        """Test download with single ticker"""
        client = MarketDataClient()
        
        # Create mock DataFrame with MultiIndex columns
        dates = pd.date_range('2025-01-01', periods=3)
        mock_data = pd.DataFrame({
            ('AAPL', 'close'): [150.0, 151.0, 152.0],
            ('AAPL', 'volume'): [1000, 1100, 1200]
        }, index=dates)
        mock_data.columns = pd.MultiIndex.from_tuples(mock_data.columns)
        
        mocker.patch.object(client.provider, "download", return_value=mock_data)
        
        result = client.download(tickers="AAPL", save=False)  # Disable caching for test
        assert isinstance(result, pd.DataFrame)
        assert "AAPL" in result.columns.levels[0]
        client.provider.download.assert_called_once_with(
            tickers=["AAPL"],
            start=None,
            end=None,
            interval="1d"
        )
        
    def test_download_multiple_tickers(self, mocker):
        """Test download with multiple tickers"""
        client = MarketDataClient()
        
        # Create mock DataFrame with MultiIndex columns for multiple tickers
        dates = pd.date_range('2025-01-01', periods=3)
        mock_data = pd.DataFrame({
            ('AAPL', 'close'): [150.0, 151.0, 152.0],
            ('AAPL', 'volume'): [1000, 1100, 1200],
            ('MSFT', 'close'): [300.0, 301.0, 302.0],
            ('MSFT', 'volume'): [2000, 2100, 2200]
        }, index=dates)
        mock_data.columns = pd.MultiIndex.from_tuples(mock_data.columns)
        
        mocker.patch.object(client.provider, "download", return_value=mock_data)
        
        result = client.download(tickers=["AAPL", "MSFT"], save=False)  # Disable caching for test
        assert isinstance(result, pd.DataFrame)
        assert "AAPL" in result.columns.levels[0]
        assert "MSFT" in result.columns.levels[0]
        client.provider.download.assert_called_once_with(
            tickers=["AAPL", "MSFT"],
            start=None,
            end=None,
            interval="1d"
        ) 
