# data/coingecko_client.py
import requests
from config.settings import COINGECKO_API_KEY

BASE_URL = "https://api.coingecko.com/api/v3"

def get_market_chart(coin_id: str, days: int = 365):
    url = f"{BASE_URL}/coins/{coin_id}/market_chart"
    params = {"vs_currency": "usd", "days": days}
    headers = {"x-cg-demo-api-key": COINGECKO_API_KEY}
    resp = requests.get(url, params=params, headers=headers)
    resp.raise_for_status()
    return resp.json()  # {"prices": [...], "market_caps": [...], "total_volumes": [...]}