# config/settings.py
import os
from dotenv import load_dotenv

load_dotenv()  # reads .env into the environment

COINGECKO_API_KEY = os.getenv("COINGECKO_API_KEY")
MAIN_WALLET_ADDRESS = os.getenv("MAIN_WALLET_ADDRESS")
AGENT_WALLET_SECRET = os.getenv("AGENT_WALLET_SECRET")
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

if not COINGECKO_API_KEY:
    raise ValueError("Missing COINGECKO_API_KEY in .env")