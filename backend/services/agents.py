from typing import Dict, List

AGENTS = [
    {
        "id": "jarvis",
        "name": "JARVIS",
        "role_fr": "Orchestrateur Central & Chat IA",
        "role_en": "Central Orchestrator & AI Chat",
        "color": "#00f0ff",
        "description_fr": "Orchestre toute l'APK et les 9 robots. Répond immédiatement et profondément à toutes vos exigences de trading crypto.",
        "description_en": "Orchestrates the entire platform and 9 bots. Provides deep and instant responses to all crypto trading requirements."
    },
    {
        "id": "dawn",
        "name": "DAWN",
        "role_fr": "Assistant Personnel & Exécution",
        "role_en": "Personal Assistant & Execution",
        "color": "#39ff14",
        "description_fr": "Planifie les opérations quotidiennes et assiste dans l'exécution de la stratégie.",
        "description_en": "Schedules daily operations and assists in strategy execution."
    },
    {
        "id": "halo",
        "name": "HALO",
        "role_fr": "Gardien du Risque & Drawdown",
        "role_en": "Risk Guardian & Drawdown",
        "color": "#00ff9f",
        "description_fr": "Vérifie le risque maximal journalier (max 2% DD) et bloque les trades hors limites.",
        "description_en": "Monitors max daily risk (max 2% DD) and blocks out-of-bounds trades."
    },
    {
        "id": "ledger",
        "name": "LEDGER",
        "role_fr": "Analyste Marché & Macro",
        "role_en": "Market & Macro Analyst",
        "color": "#ffd700",
        "description_fr": "Analyse les structures de marché, l'OI, le Funding Rate et la liquidité.",
        "description_en": "Analyzes market structures, Open Interest, Funding Rates, and liquidity."
    },
    {
        "id": "quill",
        "name": "QUILL",
        "role_fr": "Rédacteur & Journaliste de Trade",
        "role_en": "Trade Writer & Journalist",
        "color": "#00bfff",
        "description_fr": "Rédige les rapports de trading post-session et enregistre les logs de performance.",
        "description_en": "Drafts post-session trading reports and records performance logs."
    },
    {
        "id": "penny",
        "name": "PENNY",
        "role_fr": "Gestionnaire PnL & Bilan",
        "role_en": "PnL & Balance Manager",
        "color": "#ff69b4",
        "description_fr": "Calcule le PnL réalisé, les frais de commissions et l'allocation des fonds.",
        "description_en": "Calculates realized PnL, commission fees, and capital allocation."
    },
    {
        "id": "vox",
        "name": "VOX",
        "role_fr": "Sentiment & Flux Sociaux",
        "role_en": "Sentiment & Social Streams",
        "color": "#bf00ff",
        "description_fr": "Scanne le sentiment social, Telegram, Twitter (X) et le Fear & Greed index.",
        "description_en": "Scans social sentiment, Telegram, Twitter (X), and the Fear & Greed index."
    },
    {
        "id": "sentry",
        "name": "SENTRY",
        "role_fr": "Surveillance 24/7 & Sécurité",
        "role_en": "24/7 Monitoring & Security",
        "color": "#00ffff",
        "description_fr": "Surveille la connectivité API OKX, la latence et les anomalies de réseau.",
        "description_en": "Monitors OKX API connectivity, latency, and network anomalies."
    },
    {
        "id": "groove",
        "name": "GROOVE",
        "role_fr": "Focus & Psychologie du Trader",
        "role_en": "Focus & Trader Psychology",
        "color": "#ff8c00",
        "description_fr": "Garde la discipline mentale du trader et applique les préceptes de la MojoCode Academy.",
        "description_en": "Maintains trader mental discipline and enforces MojoCode Academy rules."
    },
    {
        "id": "blues",
        "name": "BLUES",
        "role_fr": "Spécialiste Quant & Scalping",
        "role_en": "Quant & Scalping Specialist",
        "color": "#1e90ff",
        "description_fr": "Détecte les squeezes de volatilité et les signaux haute fréquence (Scalping/Intraday/Futures).",
        "description_en": "Detects volatility squeezes and high-frequency signals (Scalping/Intraday/Futures)."
    }
]

def get_all_agents() -> List[Dict]:
    return AGENTS

def agent_response(agent_id: str, question: str, lang: str = "fr") -> str:
    a = next((x for x in AGENTS if x["id"] == agent_id), AGENTS[0])
    role = a["role_fr"] if lang == "fr" else a["role_en"]
    if lang == "fr":
        return f"[{a['name']} - {role}] : Analyse de '{question}' terminée. Alignment MojoCode respecté : Discipline is the Edge."
    else:
        return f"[{a['name']} - {role}] : Analysis of '{question}' complete. MojoCode Alignment preserved: Discipline is the Edge."
