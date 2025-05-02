"""
Integration tests for the AlphaVantageProvider class
"""

import os
import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from marketquery import MarketDataClient
from marketquery.constants import ALPHA_VANTAGE_COLUMNS


class TestAlphaVantageProviderIntegration:
    """Integration test suite for AlphaVantageProvider"""
    
    @pytest.fixture
    def mock_alpha_vantage(self):
        """Mock Alpha Vantage API responses"""
        with patch('alpha_vantage.timeseries.TimeSeries') as mock_ts:
            # Create mock data for unadjusted prices
            mock_unadjusted = pd.DataFrame({
                '1. open': [100.0, 101.0],
                '2. high': [102.0, 103.0],
                '3. low': [99.0, 100.0],
                '4. close': [101.0, 102.0],
                '5. volume': [1000000, 1100000]
            }, index=pd.date_range('2023-01-01', periods=2))
            
            # Create mock data for adjusted prices
            mock_adjusted = pd.DataFrame({
                '1. open': [100.0, 101.0],
                '2. high': [102.0, 103.0],
                '3. low': [99.0, 100.0],
                '4. close': [101.0, 102.0],
                '5. adjusted close': [100.5, 101.5],
                '6. volume': [1000000, 1100000],
                '7. dividend amount': [0.0, 0.5],
                '8. split coefficient': [1.0, 1.0]
            }, index=pd.date_range('2023-01-01', periods=2))
            
            # Set up mock methods
            mock_ts.return_value.get_intraday.return_value = (mock_unadjusted, None)
            mock_ts.return_value.get_daily.return_value = (mock_unadjusted, None)
            mock_ts.return_value.get_daily_adjusted.return_value = (mock_adjusted, None)
            mock_ts.return_value.get_weekly.return_value = (mock_unadjusted, None)
            mock_ts.return_value.get_monthly.return_value = (mock_unadjusted, None)
            
            yield mock_ts
    
    def test_premium_api_key_from_constructor(self, mock_alpha_vantage):
        """Test premium API key provided in constructor"""
        premium_key = "premium_key"
        client = MarketDataClient(provider="alpha_vantage", premium_api_key=premium_key)
        
        # Verify premium API key was passed to Alpha Vantage
        mock_alpha_vantage.assert_called_once_with(key=premium_key, output_format='pandas')
        
        # Test data download with adjusted prices
        data = client.download(tickers="AAPL", auto_adjust=True)
        assert isinstance(data, pd.DataFrame)
        assert not data.empty
        assert "close_adj" in data.columns.levels[1]
        assert "dividend" in data.columns.levels[1]
        assert "split" in data.columns.levels[1]
        
    def test_regular_api_key_from_constructor(self, mock_alpha_vantage):
        """Test regular API key provided in constructor"""
        regular_key = "regular_key"
        client = MarketDataClient(provider="alpha_vantage", api_key=regular_key)
        
        # Verify regular API key was passed to Alpha Vantage
        mock_alpha_vantage.assert_called_once_with(key=regular_key, output_format='pandas')
        
        # Test data download with unadjusted prices
        data = client.download(tickers="AAPL")
        assert isinstance(data, pd.DataFrame)
        assert not data.empty
        assert "close" in data.columns.levels[1]
        assert "close_adj" not in data.columns.levels[1]
        
    def test_premium_api_key_from_env(self, mock_alpha_vantage, monkeypatch):
        """Test premium API key from environment variable"""
        premium_key = "premium_key"
        monkeypatch.setenv("ALPHA_VANTAGE_PREMIUM_API_KEY", premium_key)
        
        client = MarketDataClient(provider="alpha_vantage")
        
        # Verify premium API key was passed to Alpha Vantage
        mock_alpha_vantage.assert_called_once_with(key=premium_key, output_format='pandas')
        
        # Test data download with adjusted prices
        data = client.download(tickers="AAPL", auto_adjust=True)
        assert isinstance(data, pd.DataFrame)
        assert not data.empty
        assert "close_adj" in data.columns.levels[1]
        
    def test_regular_api_key_from_env(self, mock_alpha_vantage, monkeypatch):
        """Test regular API key from environment variable"""
        regular_key = "regular_key"
        monkeypatch.setenv("ALPHA_VANTAGE_API_KEY", regular_key)
        
        client = MarketDataClient(provider="alpha_vantage")
        
        # Verify regular API key was passed to Alpha Vantage
        mock_alpha_vantage.assert_called_once_with(key=regular_key, output_format='pandas')
        
        # Test data download with unadjusted prices
        data = client.download(tickers="AAPL")
        assert isinstance(data, pd.DataFrame)
        assert not data.empty
        assert "close" in data.columns.levels[1]
        assert "close_adj" not in data.columns.levels[1]
        
    def test_api_key_prompt(self, mock_alpha_vantage, monkeypatch):
        """Test API key prompt when no key is provided"""
        # Remove any existing API keys
        monkeypatch.delenv("ALPHA_VANTAGE_PREMIUM_API_KEY", raising=False)
        monkeypatch.delenv("ALPHA_VANTAGE_API_KEY", raising=False)
        
        # Mock user input
        premium_key = "premium_key"
        with patch('builtins.input', return_value=premium_key):
            client = MarketDataClient(provider="alpha_vantage")
            
            # Verify premium API key was passed to Alpha Vantage
            mock_alpha_vantage.assert_called_once_with(key=premium_key, output_format='pandas')
            
            # Test data download
            data = client.download(tickers="AAPL")
            assert isinstance(data, pd.DataFrame)
            assert not data.empty
            
    def test_premium_fallback_to_regular(self, mock_alpha_vantage):
        """Test fallback to regular API when premium is not available"""
        # Mock premium API error
        mock_alpha_vantage.return_value.get_daily_adjusted.side_effect = Exception("Premium API key required")
        
        client = MarketDataClient(provider="alpha_vantage", api_key="regular_key")
        
        # Test data download with warning
        with patch('builtins.print') as mock_print:
            data = client.download(tickers="AAPL", auto_adjust=True)
            mock_print.assert_called_with("Warning: Premium API key required for adjusted data. Using unadjusted data for AAPL.")
            
        assert isinstance(data, pd.DataFrame)
        assert not data.empty
        assert "close" in data.columns.levels[1]
        assert "close_adj" not in data.columns.levels[1]
        
    def test_date_filtering(self, mock_alpha_vantage):
        """Test date filtering functionality"""
        client = MarketDataClient(provider="alpha_vantage", api_key="test_key")
        
        # Test with date range
        data = client.download(
            tickers="AAPL",
            start="2023-01-01",
            end="2023-01-02"
        )
        
        assert isinstance(data, pd.DataFrame)
        assert not data.empty
        assert len(data) == 2  # Should have both dates
        
        # Test with single date
        data = client.download(
            tickers="AAPL",
            start="2023-01-01"
        )
        
        assert isinstance(data, pd.DataFrame)
        assert not data.empty
        assert len(data) == 2  # Should have both dates
        
    def test_multiple_tickers(self, mock_alpha_vantage):
        """Test downloading data for multiple tickers"""
        client = MarketDataClient(provider="alpha_vantage", api_key="test_key")
        
        data = client.download(tickers=["AAPL", "MSFT"])
        assert isinstance(data, pd.DataFrame)
        assert not data.empty
        
        # Verify multi-index columns
        assert isinstance(data.columns, pd.MultiIndex)
        assert "AAPL" in data.columns.levels[0]
        assert "MSFT" in data.columns.levels[0]
        
        # Verify each ticker has the expected columns
        for ticker in ["AAPL", "MSFT"]:
            assert (ticker, "open") in data.columns
            assert (ticker, "high") in data.columns
            assert (ticker, "low") in data.columns
            assert (ticker, "close") in data.columns
            assert (ticker, "volume") in data.columns
            
    def test_invalid_interval(self, mock_alpha_vantage):
        """Test invalid interval raises ValueError"""
        client = MarketDataClient(provider="alpha_vantage", api_key="test_key")
        
        with pytest.raises(ValueError) as exc_info:
            client.download(tickers="AAPL", interval="invalid")
        assert "Interval 'invalid' not supported by Alpha Vantage" in str(exc_info.value)
