# execution/hyperliquid_client.py (or a new data/hyperliquid_price_client.py)
import requests

def get_hype_candles(interval="1d", start_ms=None, end_ms=None):
    url = "https://api.hyperliquid.xyz/info"
    payload = {
        "type": "candleSnapshot",
        "req": {"coin": "HYPE", "interval": interval, "startTime": start_ms, "endTime": end_ms}
    }
    resp = requests.post(url, json=payload)
    resp.raise_for_status()
    return resp.json()