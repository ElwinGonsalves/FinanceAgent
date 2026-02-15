import requests
import os
from dotenv import load_dotenv

load_dotenv(override=True)

api_key = os.getenv("EXCHANGERATE_API_KEY")
print(f"API Key found: {bool(api_key)}")

if api_key:
    url = f"http://api.exchangeratesapi.io/v1/latest?access_key={api_key}&symbols=USD,INR,GBP,EUR"
    print(f"Requesting: {url.replace(api_key, 'HIDDEN_KEY')}")
    
    try:
        response = requests.get(url, timeout=10)
        print(f"Status Code: {response.status_code}")
        print("Response Body:")
        print(response.text)
    except Exception as e:
        print(f"Error: {e}")
else:
    print("No API Key loaded.")
