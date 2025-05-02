"""
Standardized constants for market data providers
"""

# Standard column names for market data
COLUMNS = {
    # Regular prices
    'open': 'open',
    'high': 'high',
    'low': 'low',
    'close': 'close',
    'volume': 'volume',
    
    # Adjusted prices
    'open_adj': 'open_adj',
    'high_adj': 'high_adj',
    'low_adj': 'low_adj',
    'close_adj': 'close_adj',
    'volume_adj': 'volume_adj',
    
    # Corporate actions
    'dividends': 'dividends',
    'splits': 'splits'
}

# Alpha Vantage specific column mappings
ALPHA_VANTAGE_COLUMNS = {
    '1. open': 'open',
    '2. high': 'high',
    '3. low': 'low',
    '4. close': 'close',
    '5. adjusted close': 'close_adj',
    '6. volume': 'volume',
    '7. dividend amount': 'dividend',
    '8. split coefficient': 'split'
}

# Supported intervals
INTERVALS = {
    '1m': '1min',
    '5m': '5min',
    '15m': '15min',
    '30m': '30min',
    '60m': '60min',
    '1d': 'daily',
    '1wk': 'weekly',
    '1mo': 'monthly'
}

# Environment variable names
ENV_VARS = {
    'premium_api_key': 'ALPHA_VANTAGE_PREMIUM_API_KEY',
    'api_key': 'ALPHA_VANTAGE_API_KEY'
} 
