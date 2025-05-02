"""
Integration tests for the YahooProvider class
"""

import pytest
import pandas as pd
from marketquery import MarketDataClient


class TestYahooProviderIntegration:
    """Integration test suite for YahooProvider"""
    
    @pytest.fixture
    def client(self):
        """Create a MarketDataClient instance"""
        return MarketDataClient()
    
    def test_download_single_ticker(self, client):
        """Test downloading data for a single ticker"""
        # Test with a well-known stock (Apple)
        data = client.download(
            tickers="AAPL",
            start="2023-01-01",
            end="2023-01-31",
            interval="1d"
        )

        # Verify the data structure
        assert isinstance(data, pd.DataFrame)
        assert not data.empty
        assert "Open" in data.columns
        assert "High" in data.columns
        assert "Low" in data.columns
        assert "Close" in data.columns
        assert "Volume" in data.columns
        
        # Verify date range
        assert data.index[0].strftime("%Y-%m-%d") >= "2023-01-01"
        assert data.index[-1].strftime("%Y-%m-%d") <= "2023-01-31"
    #
    # def test_download_multiple_tickers(self, client):
    #     """Test downloading data for multiple tickers"""
    #     # Test with multiple well-known stocks
    #     data = client.download(
    #         tickers=["AAPL", "MSFT", "GOOGL"],
    #         start_date="2023-01-01",
    #         end_date="2023-01-31",
    #         interval="1d"
    #     )
    #
    #     # Verify the data structure
    #     assert isinstance(data, pd.DataFrame)
    #     assert not data.empty
    #
    #     # For multiple tickers, yfinance returns a multi-level column index
    #     assert isinstance(data.columns, pd.MultiIndex)
    #     assert all(ticker in data.columns.levels[1] for ticker in ["AAPL", "MSFT", "GOOGL"])
    #
    #     # Verify each ticker has the expected columns
    #     for ticker in ["AAPL", "MSFT", "GOOGL"]:
    #         assert ("Open", ticker) in data.columns
    #         assert ("High", ticker) in data.columns
    #         assert ("Low", ticker) in data.columns
    #         assert ("Close", ticker) in data.columns
    #         assert ("Volume", ticker) in data.columns
    #
    # def test_download_invalid_ticker(self, client):
    #     """Test downloading data for an invalid ticker"""
    #     with pytest.raises(Exception):
    #         client.download(
    #             tickers="INVALIDTICKER",
    #             start_date="2023-01-01",
    #             end_date="2023-01-31"
    #         )
    #
    # def test_download_different_intervals(self, client):
    #     """Test downloading data with different intervals"""
    #     intervals = ["1d", "1wk", "1mo"]
    #
    #     for interval in intervals:
    #         data = client.download(
    #             tickers="AAPL",
    #             start_date="2023-01-01",
    #             end_date="2023-01-31",
    #             interval=interval
    #         )
    #
    #         assert isinstance(data, pd.DataFrame)
    #         assert not data.empty
    #
    #         # Verify the data has the expected columns
    #         assert "Open" in data.columns
    #         assert "High" in data.columns
    #         assert "Low" in data.columns
    #         assert "Close" in data.columns
    #         assert "Volume" in data.columns
