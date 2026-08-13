# data/defillama_client.py
import requests

def get_hyperliquid_revenue():
    url = "https://api.llama.fi/summary/fees/hyperliquid"
    params = {"dataType": "dailyRevenue"}
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    return resp.json()  # includes totalDataChart: [[timestamp, revenue], ...]