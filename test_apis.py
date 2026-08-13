# test_apis.py
"""
Quick sanity check for all three data sources before wiring them into
the real data_loader. Run this, eyeball the output, confirm shapes make sense.
Delete this file once confirmed — it's not part of the production architecture.
"""

import time
from datetime import datetime, timedelta

from config.settings import COINGECKO_API_KEY
from data.coingecko_client import get_market_chart
from data.defillama_client import get_hyperliquid_revenue


def test_coingecko():
    print("\n=== CoinGecko: HYPE market_chart (30 days) ===")
    try:
        data = get_market_chart("hyperliquid", days=30)
        prices = data.get("prices", [])
        market_caps = data.get("market_caps", [])
        volumes = data.get("total_volumes", [])

        print(f"Got {len(prices)} price points")
        if prices:
            latest_ts, latest_price = prices[-1]
            latest_date = datetime.fromtimestamp(latest_ts / 1000)
            print(f"Latest price point: {latest_date} -> ${latest_price:,.2f}")
        if market_caps:
            _, latest_mcap = market_caps[-1]
            print(f"Latest circulating market cap: ${latest_mcap:,.0f}")
        if volumes:
            _, latest_vol = volumes[-1]
            print(f"Latest 24h volume: ${latest_vol:,.0f}")

        print("CoinGecko: OK")
    except Exception as e:
        print(f"CoinGecko FAILED: {e}")


def test_defillama():
    print("\n=== DefiLlama: Hyperliquid daily revenue ===")
    try:
        data = get_hyperliquid_revenue()
        chart = data.get("totalDataChart", [])
        print(f"Got {len(chart)} daily revenue data points")
        if chart:
            latest_ts, latest_rev = chart[-1]
            latest_date = datetime.fromtimestamp(latest_ts)
            print(f"Latest day: {latest_date} -> ${latest_rev:,.0f} revenue")

        # sanity check: does this match the ~$726M annualized figure roughly?
        if chart:
            last_30 = chart[-30:]
            total_30d = sum(rev for _, rev in last_30)
            annualized = total_30d * (365 / 30)
            print(f"Rough annualized estimate from last 30d: ${annualized:,.0f}")

        print("DefiLlama: OK")
    except Exception as e:
        print(f"DefiLlama FAILED: {e}")


def test_hyperliquid_candles():
    print("\n=== Hyperliquid: candleSnapshot (HYPE, last 30 days, 1d interval) ===")
    try:
        import requests

        end_ms = int(time.time() * 1000)
        start_ms = int((datetime.now() - timedelta(days=30)).timestamp() * 1000)

        url = "https://api.hyperliquid.xyz/info"
        payload = {
            "type": "candleSnapshot",
            "req": {
                "coin": "HYPE",
                "interval": "1d",
                "startTime": start_ms,
                "endTime": end_ms,
            },
        }
        resp = requests.post(url, json=payload)
        resp.raise_for_status()
        candles = resp.json()

        print(f"Got {len(candles)} daily candles")
        if candles:
            latest = candles[-1]
            print(f"Latest candle: open={latest['o']} close={latest['c']} "
                  f"high={latest['h']} low={latest['l']} volume={latest['v']}")

        print("Hyperliquid candleSnapshot: OK")
    except Exception as e:
        print(f"Hyperliquid candleSnapshot FAILED: {e}")


if __name__ == "__main__":
    print("Running API sanity checks...")
    print(f"CoinGecko key loaded: {'yes' if COINGECKO_API_KEY else 'NO - CHECK .env'}")

    test_coingecko()
    test_defillama()
    test_hyperliquid_candles()

    print("\nDone. Check output above for any FAILED lines.")