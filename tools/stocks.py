import json

def get_stock_data(country_name: str):
    """
    Returns major stock indices and their current values for a given country.
    """
    country_name = country_name.lower().strip()
    
    # Mock Data Source
    data = {
        "japan": {
            "exchange": "Tokyo Stock Exchange (TSE)",
            "indices": [
                {"name": "Nikkei 225", "value": 38915.00, "change": "+1.2%"},
                {"name": "TOPIX", "value": 2650.50, "change": "+0.8%"}
            ]
        },
        "india": {
            "exchange": "Bombay Stock Exchange (BSE) / National Stock Exchange (NSE)",
            "indices": [
                {"name": "NIFTY 50", "value": 24500.00, "change": "-0.5%"},
                {"name": "SENSEX", "value": 81000.00, "change": "-0.4%"}
            ]
        },
        "us": {
            "exchange": "New York Stock Exchange (NYSE) / NASDAQ",
            "indices": [
                {"name": "S&P 500", "value": 5400.00, "change": "+0.3%"},
                {"name": "Dow Jones", "value": 39000.00, "change": "+0.1%"},
                {"name": "NASDAQ", "value": 17000.00, "change": "+0.5%"}
            ]
        },
        "usa": {
            "exchange": "New York Stock Exchange (NYSE) / NASDAQ",
            "indices": [
                {"name": "S&P 500", "value": 5400.00, "change": "+0.3%"},
                {"name": "Dow Jones", "value": 39000.00, "change": "+0.1%"},
                {"name": "NASDAQ", "value": 17000.00, "change": "+0.5%"}
            ]
        },
        "united states": {
            "exchange": "New York Stock Exchange (NYSE) / NASDAQ",
            "indices": [
                {"name": "S&P 500", "value": 5400.00, "change": "+0.3%"},
                {"name": "Dow Jones", "value": 39000.00, "change": "+0.1%"},
                {"name": "NASDAQ", "value": 17000.00, "change": "+0.5%"}
            ]
        },
        "south korea": {
            "exchange": "Korea Exchange (KRX)",
            "indices": [
                {"name": "KOSPI", "value": 2700.00, "change": "+0.9%"},
                {"name": "KOSDAQ", "value": 850.00, "change": "+1.1%"}
            ]
        },
        "china": {
            "exchange": "Shanghai Stock Exchange (SSE)",
            "indices": [
                {"name": "Shanghai Composite", "value": 3050.00, "change": "-0.2%"},
                {"name": "Shenzhen Component", "value": 9500.00, "change": "-0.3%"}
            ]
        },
        "uk": {
            "exchange": "London Stock Exchange (LSE)",
            "indices": [
                {"name": "FTSE 100", "value": 8200.00, "change": "+0.4%"},
                {"name": "FTSE 250", "value": 20100.00, "change": "+0.6%"}
            ]
        },
        "united kingdom": {
            "exchange": "London Stock Exchange (LSE)",
            "indices": [
                {"name": "FTSE 100", "value": 8200.00, "change": "+0.4%"},
                {"name": "FTSE 250", "value": 20100.00, "change": "+0.6%"}
            ]
        }
    }
    
    if country_name in data:
        return json.dumps(data[country_name])
    else:
        return json.dumps({"error": "Country not found in mock database."})
