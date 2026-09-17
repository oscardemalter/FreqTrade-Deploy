import re, time
from typing import Dict, List, Any
from datetime import datetime, timezone
try:
    import ccxt, numpy as np
except ImportError:
    ccxt = None; np = None

# TOP 50 Cryptos globally traded
TOP50_SYMBOLS = [
    ("BTC/USDT", "BTC/USDT:USDT"), ("ETH/USDT", "ETH/USDT:USDT"), ("BNB/USDT", "BNB/USDT:USDT"),
    ("SOL/USDT", "SOL/USDT:USDT"), ("XRP/USDT", "XRP/USDT:USDT"), ("ADA/USDT", "ADA/USDT:USDT"),
    ("AVAX/USDT", "AVAX/USDT:USDT"), ("DOGE/USDT", "DOGE/USDT:USDT"), ("DOT/USDT", "DOT/USDT:USDT"),
    ("LINK/USDT", "LINK/USDT:USDT"), ("TON/USDT", "TON/USDT:USDT"), ("TRX/USDT", "TRX/USDT:USDT"),
    ("LTC/USDT", "LTC/USDT:USDT"), ("BCH/USDT", "BCH/USDT:USDT"), ("UNI/USDT", "UNI/USDT:USDT"),
    ("ATOM/USDT", "ATOM/USDT:USDT"), ("NEAR/USDT", "NEAR/USDT:USDT"), ("APT/USDT", "APT/USDT:USDT"),
    ("SHIB/USDT", "SHIB/USDT:USDT"), ("PEPE/USDT", "PEPE/USDT:USDT"), ("SUI/USDT", "SUI/USDT:USDT"),
    ("INJ/USDT", "INJ/USDT:USDT"), ("TIA/USDT", "TIA/USDT:USDT"), ("RNDR/USDT", "RNDR/USDT:USDT"),
    ("FET/USDT", "FET/USDT:USDT"), ("STX/USDT", "STX/USDT:USDT"), ("FIL/USDT", "FIL/USDT:USDT"),
    ("ICP/USDT", "ICP/USDT:USDT"), ("ETC/USDT", "ETC/USDT:USDT"), ("XLM/USDT", "XLM/USDT:USDT"),
    ("SEI/USDT", "SEI/USDT:USDT"), ("OP/USDT", "OP/USDT:USDT"), ("ARB/USDT", "ARB/USDT:USDT"),
    ("MKR/USDT", "MKR/USDT:USDT"), ("AAVE/USDT", "AAVE/USDT:USDT"), ("GRT/USDT", "GRT/USDT:USDT"),
    ("ALGO/USDT", "ALGO/USDT:USDT"), ("FLOW/USDT", "FLOW/USDT:USDT"), ("SAND/USDT", "SAND/USDT:USDT"),
    ("MANA/USDT", "MANA/USDT:USDT"), ("AXS/USDT", "AXS/USDT:USDT"), ("GALA/USDT", "GALA/USDT:USDT"),
    ("EGLD/USDT", "EGLD/USDT:USDT"), ("THETA/USDT", "THETA/USDT:USDT"), ("FTM/USDT", "FTM/USDT:USDT"),
    ("KSM/USDT", "KSM/USDT:USDT"), ("NEO/USDT", "NEO/USDT:USDT"), ("EOS/USDT", "EOS/USDT:USDT"),
    ("SNX/USDT", "SNX/USDT:USDT"), ("CRV/USDT", "CRV/USDT:USDT")
]

NAME_MAP = {s[0].split("/")[0].lower(): s[0] for s in TOP50_SYMBOLS}
NAME_MAP.update({"bitcoin": "BTC/USDT", "ethereum": "ETH/USDT", "solana": "SOL/USDT", "cardano": "ADA/USDT"})

RISK_RULES = {
    "max_risk_per_trade_pct": 1.0,
    "max_daily_loss_pct": 5.0,
    "max_open_positions": 5,
    "min_reward_risk": 1.5,
    "require_a_plus_setup": True,
    "no_revenge_trading": True
}

def _sma(a, p):
    return float(np.mean(a[-p:])) if len(a) >= p and np is not None else None

def _rsi(c, period=14):
    if len(c) < period + 1 or np is None: return None
    d = np.diff(c); g = np.where(d > 0, d, 0.0); l = np.where(d < 0, -d, 0.0)
    ag, al = np.mean(g[-period:]), np.mean(l[-period:])
    return 100.0 if al == 0 else float(100 - 100 / (1 + ag / al))

def _atr(h, l, c, period=14):
    if len(c) < period + 1 or np is None: return None
    tr = np.maximum(h[1:] - l[1:], np.maximum(abs(h[1:] - c[:-1]), abs(l[1:] - c[:-1])))
    return float(np.mean(tr[-period:]))

def _detect_squeeze_and_reversal(o):
    """
    Computes Bollinger Bands vs Keltner Channels squeeze condition,
    plus bullish/bearish major reversal signals across OHLCV bars.
    """
    if not o or len(o) < 30 or np is None:
        return {"squeeze": False, "reversal": "none"}

    h = np.array([x[2] for x in o], dtype=float)
    l = np.array([x[3] for x in o], dtype=float)
    c = np.array([x[4] for x in o], dtype=float)
    v = np.array([x[5] for x in o], dtype=float)

    # Bollinger Bands
    basis = np.mean(c[-20:])
    dev = np.std(c[-20:]) * 2.0
    bb_upper = basis + dev
    bb_lower = basis - dev

    # Keltner Channels
    atr_val = _atr(h, l, c, 10) or (np.mean(h[-10:] - l[-10:]))
    kc_upper = basis + (atr_val * 1.5)
    kc_lower = basis - (atr_val * 1.5)

    squeeze = bool(bb_upper <= kc_upper and bb_lower >= kc_lower)

    rsi = _rsi(c, 14) or 50.0
    vol_sma = np.mean(v[-20:]) if len(v) >= 20 else v[-1]
    vol_breakout = bool(v[-1] > vol_sma * 1.4)

    reversal = "none"
    if rsi < 35 and vol_breakout and c[-1] > c[-2]:
        reversal = "major_bullish_reversal"
    elif rsi > 65 and vol_breakout and c[-1] < c[-2]:
        reversal = "major_bearish_reversal"

    return {"squeeze": squeeze, "reversal": reversal, "rsi": round(rsi, 1)}

class RiskManager:
    def __init__(self):
        self.daily_pnl_pct = 0.0; self.open_positions = 0
    def can_trade(self, risk_pct=1.0):
        reasons, ok = [], True
        if risk_pct > RISK_RULES["max_risk_per_trade_pct"]: ok = False; reasons.append("Risque trop élevé")
        if self.open_positions >= RISK_RULES["max_open_positions"]: ok = False; reasons.append("Positions maximales atteintes")
        return {"allowed": ok, "reasons": reasons, "rules": RISK_RULES}

class SignalEngine:
    def __init__(self):
        self._cache = {}; self._ttl = 20; self._ex = None
    def _get_exchange(self):
        if self._ex: return self._ex
        if ccxt is None: return None
        try:
            ex = ccxt.okx({"enableRateLimit": True, "options": {"defaultType": "spot"}})
            ex.load_markets(); self._ex = ex; return ex
        except Exception:
            try:
                ex = ccxt.binance({"enableRateLimit": True}); self._ex = ex; return ex
            except Exception:
                return None
    def _fetch(self, sym, tf="15m", limit=60):
        ex = self._get_exchange()
        if not ex: return None
        k = f"{sym}:{tf}"; now = time.time()
        if k in self._cache:
            ts, data = self._cache[k]
            if now - ts < self._ttl: return data
        try:
            o = ex.fetch_ohlcv(sym, timeframe=tf, limit=limit)
            self._cache[k] = (now, o); return o
        except Exception:
            return None

    def _watch(self, spot, disp):
        o = self._fetch(spot, "15m", 40)
        if not o or len(o) < 25 or np is None: return None
        c = np.array([x[4] for x in o], dtype=float)
        rsi = _rsi(c, 14); pct = round((c[-1] - c[-2]) / c[-2] * 100, 3)
        sq_rev = _detect_squeeze_and_reversal(o)
        return {
            "symbol": disp,
            "price": float(c[-1]),
            "pct": pct,
            "rsi": round(rsi, 1) if rsi else None,
            "squeeze": sq_rev["squeeze"],
            "reversal": sq_rev["reversal"]
        }

    def scan_radar(self):
        wl = []
        for spot, disp in TOP50_SYMBOLS:
            w = self._watch(spot, disp)
            if w: wl.append(w)
            time.sleep(0.02)
        return {"signals": [], "watchlist": wl, "scanned": len(wl), "ts": datetime.now(timezone.utc).isoformat()}

class QuantCore:
    def __init__(self):
        self.risk = RiskManager(); self.signals = SignalEngine()
    def status(self):
        return {"radar": "TOP 50 Cryptos mondial", "risk_rules": RISK_RULES, "message": "Radar Quant 50 Cryptos online - temps réel"}
    def check_trade(self, r=1.0):
        return self.risk.can_trade(r)
    def radar_scan(self):
        return self.signals.scan_radar()
    def any_crypto(self, q):
        spot = NAME_MAP.get(q.lower()) or (q.upper() if "/" in q else f"{q.upper()}/USDT")
        ex = self.signals._get_exchange()
        if not ex: return {"error": "Marché indisponible"}
        try:
            t = ex.fetch_ticker(spot)
            o = self.signals._fetch(spot, "15m", 60)
            rsi = None; up = False; sq_rev = {"squeeze": False, "reversal": "none"}
            if o and len(o) > 25:
                c = np.array([x[4] for x in o], dtype=float); rsi = _rsi(c, 14); up = bool(c[-1] > _sma(c, 20))
                sq_rev = _detect_squeeze_and_reversal(o)
            return {
                "symbol": spot, "price": t.get("last"), "pct": round(t.get("percentage") or 0, 2),
                "rsi": round(rsi, 1) if rsi else None, "trend_up": up,
                "squeeze": sq_rev["squeeze"], "reversal": sq_rev["reversal"]
            }
        except Exception as e:
            return {"error": str(e)}

quant_core = QuantCore()
