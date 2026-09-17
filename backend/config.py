import os
from dotenv import load_dotenv

# Charger .env
load_dotenv()

class Settings:
    def __init__(self):
        self.ENVIRONMENT = os.getenv("ENVIRONMENT", "dev")
        self.ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin@ubergestalt.local")
        self.DEFAULT_ADMIN_PASSWORD_HASH = "$pbkdf2-sha256$29000$J2TsXSullHIOoZSyNqb0fg$n4M9pwJ1V5uk0VK0RzVNA9RLdT5WRWDKbcFI/P6ZYXs"
        self.ADMIN_PASSWORD_HASH = os.getenv("ADMIN_PASSWORD_HASH") or self.DEFAULT_ADMIN_PASSWORD_HASH
        self.SECRET_KEY = os.getenv("SECRET_KEY", "ubergestalt_secret_key_ultra_secure_2026_jwt")
        self.WEBHOOK_HMAC_SECRET = os.getenv("WEBHOOK_HMAC_SECRET", "ubergestalt_webhook_secret")
        self.OKX_OAUTH_CLIENT_ID = os.getenv("OKX_OAUTH_CLIENT_ID", "")
        self.OKX_OAUTH_CLIENT_SECRET = os.getenv("OKX_OAUTH_CLIENT_SECRET", "")
        self.OKX_OAUTH_REDIRECT_URI = os.getenv("OKX_OAUTH_REDIRECT_URI", "https://ubergestalt.local/api/okx/oauth/callback")
        self.OKX_DEMO = os.getenv("OKX_DEMO", "True").lower() == "true"
        self.TRADING_MODE = os.getenv("TRADING_MODE", "paper")
        self.EXCHANGE_ID = os.getenv("EXCHANGE_ID", "okx")
        self.API_KEY = os.getenv("API_KEY", "")
        self.API_SECRET = os.getenv("API_SECRET", "")
        self.API_PASSPHRASE = os.getenv("API_PASSPHRASE", "")
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
        self.LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")
        self.MIN_ORDER_USDT = float(os.getenv("MIN_ORDER_USDT", "1.0"))
        self.MAX_DAILY_LOSS_PERCENT = float(os.getenv("MAX_DAILY_LOSS_PERCENT", "5.0"))
        self.MAX_ORDER_NOTIONAL_USDT = float(os.getenv("MAX_ORDER_NOTIONAL_USDT", "1000.0"))
        self.WEBHOOK_SYMBOL_WHITELIST = os.getenv("WEBHOOK_SYMBOL_WHITELIST", "BTC/USDT,ETH/USDT,SOL/USDT,BNB/USDT,XRP/USDT,ADA/USDT,AVAX/USDT,DOGE/USDT")
        self.PAPER_LEDGER_PATH = os.getenv("PAPER_LEDGER_PATH", "data/paper_ledger.json")
        self.KEYSTORE_PATH = os.getenv("KEYSTORE_PATH", "data/keystore.json")
        self.AUDIT_PATH = os.getenv("AUDIT_PATH", "data/audit.jsonl")
        self.USER_DATA_DIR = os.getenv("USER_DATA_DIR", "user_data")
        self.VERIFICATION_RECORDS_PATH = os.getenv("VERIFICATION_RECORDS_PATH", "verification/tradingview.json")
        self.VERIFICATION_PINE_PATH = os.getenv("VERIFICATION_PINE_PATH", "pine/uberox_emitter_v6.pine")

    def update_password(self, new_password: str):
        from passlib.context import CryptContext
        pwd_ctx = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
        self.ADMIN_PASSWORD_HASH = pwd_ctx.hash(new_password)

settings = Settings()

if settings.ENVIRONMENT == "production" and (not settings.SECRET_KEY or not settings.ADMIN_PASSWORD_HASH):
    raise RuntimeError("production: SECRET_KEY et ADMIN_PASSWORD_HASH requis")
