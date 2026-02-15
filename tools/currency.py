import json
import os
import requests

def get_exchange_rates(country_name: str):
    """
    Returns the official currency and exchange rates for a given country.
    Target output currencies: USD, INR, GBP, EUR.
    Uses EXCHANGERATE_API_KEY if available, otherwise Mock Data.
    """
    country_name = country_name.lower().strip()
    
    # 1. Map Country to Currency Code
    country_currency_map = {
        "japan": "JPY", "india": "INR", "us": "USD", "usa": "USD", "united states": "USD",
        "south korea": "KRW", "china": "CNY", "uk": "GBP", "united kingdom": "GBP",
        "germany": "EUR", "france": "EUR", "italy": "EUR", "spain": "EUR"
    }
    
    base_currency = country_currency_map.get(country_name)
    
    # 2. Try Live API if Key exists
    api_key = os.getenv("EXCHANGERATE_API_KEY")
    if api_key and base_currency:
        try:
            # User is using https://www.exchangerate-api.com/ (v6)
            # URL format: https://v6.exchangerate-api.com/v6/YOUR-API-KEY/latest/USD
            url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{base_currency}"
            
            response = requests.get(url, timeout=5)
            data = response.json()
            
            if data.get("result") == "success":
                rates = data["conversion_rates"]
                
                # Direct rates since we asked for the base currency
                cross_rates = {
                    "USD": rates.get("USD"),
                    "INR": rates.get("INR"),
                    "GBP": rates.get("GBP"),
                    "EUR": rates.get("EUR")
                }
                
                return json.dumps({
                    "currency": base_currency,
                    "rates": cross_rates,
                    "source": "Live API"
                })
            else:
                api_error = f"API returned '{data.get('result')}': {data.get('error-type', 'Unknown error')}"
        except Exception as e:
            print(f"API Error: {e}")
            # Capture the error to return it
            api_error = str(e)
            
    # 3. Mock Data Fallback
    # Added core Eurozone for fallback coverage
    eur_rates = {"USD": 1.08, "INR": 90.50, "GBP": 0.85, "EUR": 1.0}
    
    data = {
        "japan": {
            "currency": "JPY",
            "rates": {"USD": 0.0067, "INR": 0.56, "GBP": 0.0053, "EUR": 0.0062}
        },
        "india": {
            "currency": "INR",
            "rates": {"USD": 0.011, "INR": 1.0, "GBP": 0.0095, "EUR": 0.011}
        },
        "us": {
            "currency": "USD",
            "rates": {"USD": 1.0, "INR": 90.56, "GBP": 0.79, "EUR": 0.92}
        },
        "usa": {
            "currency": "USD",
            "rates": {"USD": 1.0, "INR": 90.56, "GBP": 0.79, "EUR": 0.92}
        },
        "united states": {
            "currency": "USD",
            "rates": {"USD": 1.0, "INR": 90.56, "GBP": 0.79, "EUR": 0.92}
        },
        "south korea": {
            "currency": "KRW",
            "rates": {"USD": 0.00075, "INR": 0.062, "GBP": 0.00059, "EUR": 0.00069}
        },
        "china": {
            "currency": "CNY",
            "rates": {"USD": 0.14, "INR": 11.5, "GBP": 0.11, "EUR": 0.13}
        },
        "uk": {
            "currency": "GBP",
            "rates": {"USD": 1.26, "INR": 105.4, "GBP": 1.0, "EUR": 1.17}
        },
        "united kingdom": {
            "currency": "GBP",
            "rates": {"USD": 1.26, "INR": 105.4, "GBP": 1.0, "EUR": 1.17}
        },
        "germany": {"currency": "EUR", "rates": eur_rates},
        "france": {"currency": "EUR", "rates": eur_rates},
        "italy": {"currency": "EUR", "rates": eur_rates},
        "spain": {"currency": "EUR", "rates": eur_rates}
    }
    
    if country_name in data:
        result = data[country_name]
        result["source"] = "Mock Data"
        result["debug_info"] = "API failed or key missing"
        if 'api_error' in locals():
             result["api_error"] = api_error
        return json.dumps(result)
    else:
        return json.dumps({"error": f"Country '{country_name}' not found in database.", "api_status": "failed"})
