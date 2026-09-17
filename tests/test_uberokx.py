import unittest
import os
from backend.config import settings
from backend.auth import hash_password, verify_password, create_access_token
from backend.services.agents import get_all_agents, agent_response
from backend.services.quant import quant_core, _detect_squeeze_and_reversal

class TestUbergestaltCore(unittest.TestCase):

    def test_config_and_auth(self):
        self.assertEqual(settings.MIN_ORDER_USDT, 1.0)
        h = hash_password("Ubergestalt2026!")
        self.assertTrue(verify_password("Ubergestalt2026!", h))
        self.assertFalse(verify_password("WrongPass", h))

        token = create_access_token({"sub": "admin@ubergestalt.local"})
        self.assertIsInstance(token, str)

    def test_ai_agents(self):
        agents = get_all_agents()
        self.assertEqual(len(agents), 10)
        agent_ids = [a["id"] for a in agents]
        self.assertIn("jarvis", agent_ids)
        self.assertIn("blues", agent_ids)

        resp_fr = agent_response("jarvis", "BTC target?", "fr")
        resp_en = agent_response("jarvis", "BTC target?", "en")
        self.assertIn("JARVIS", resp_fr)
        self.assertIn("Discipline is the Edge", resp_en)

    def test_quant_squeeze_detection(self):
        # Generate dummy candles: time, open, high, low, close, volume
        candles = []
        for i in range(40):
            candles.append([1000 * i, 100.0, 102.0, 98.0, 100.0 + (i % 2), 1000.0])

        res = _detect_squeeze_and_reversal(candles)
        self.assertIn("squeeze", res)
        self.assertIn("reversal", res)
        self.assertIsInstance(res["squeeze"], bool)

    def test_quant_status(self):
        st = quant_core.status()
        self.assertIn("radar", st)
        self.assertEqual(st["radar"], "TOP 50 Cryptos mondial")

if __name__ == '__main__':
    unittest.main()
