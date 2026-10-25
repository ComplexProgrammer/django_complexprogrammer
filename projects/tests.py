from unittest.mock import MagicMock, patch
from django.core.cache import cache
from django.test import TestCase, override_settings
from django.urls import reverse
import requests

from projects.views import (
    CBU_FALLBACK_FILE,
    CBU_RATES_URL,
    DEFAULT_REQUEST_HEADERS,
    fetch_json,
)


class ExchangeRatesTestCase(TestCase):
    def setUp(self):
        cache.clear()
        self.mock_rates = [
            {
                "id": 68,
                "Code": "840",
                "Ccy": "USD",
                "CcyNm_RU": "Доллар США",
                "CcyNm_UZ": "AQSH dollari",
                "CcyNm_UZC": "АҚШ доллари",
                "CcyNm_EN": "US Dollar",
                "Nominal": "1",
                "Rate": "12820.00",
                "Diff": "15.00",
                "Date": "25.10.2026",
            }
        ]

    def tearDown(self):
        cache.clear()

    @patch("projects.views.requests.get")
    def test_fetch_json_sends_browser_user_agent(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = self.mock_rates
        mock_get.return_value = mock_resp

        result = fetch_json("https://cbu.uz/test", "test:key")
        self.assertEqual(result, self.mock_rates)
        mock_get.assert_called_once()
        headers = mock_get.call_args[1].get("headers", {})
        self.assertIn("Mozilla/5.0", headers.get("User-Agent", ""))

    @patch("projects.views.requests.get")
    def test_fetch_json_falls_back_to_cache_on_error(self, mock_get):
        # 1. Success sets cache and fallback
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = self.mock_rates
        mock_get.return_value = mock_resp

        result = fetch_json("https://cbu.uz/test", "test:fallback_key", ttl=1)
        self.assertEqual(result, self.mock_rates)

        # Clear primary cache to simulate expiration
        cache.delete("test:fallback_key")
        self.assertIsNone(cache.get("test:fallback_key"))

        # 2. Network error occurs
        mock_get.side_effect = requests.RequestException("CBU timeout")

        fallback_result = fetch_json("https://cbu.uz/test", "test:fallback_key")
        self.assertEqual(fallback_result, self.mock_rates)

    @patch("projects.views.requests.get")
    def test_get_exchange_rates_endpoint_success(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = self.mock_rates
        mock_get.return_value = mock_resp

        url = reverse("GetExchangeRates")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("data", data)
        self.assertEqual(len(data["data"]), 1)
        self.assertEqual(data["data"][0]["Ccy"], "USD")

    @patch("projects.views.requests.get")
    def test_get_exchange_rates_fallback_on_cbu_failure(self, mock_get):
        # Simulate CBU being down (timeout or connection error)
        mock_get.side_effect = requests.RequestException("Central bank server unreachable")

        # CBU_FALLBACK_FILE exists on disk
        self.assertTrue(CBU_FALLBACK_FILE.exists())

        url = reverse("GetExchangeRates")
        response = self.client.get(url)
        # Should NOT return 503! Should return 200 with fallback data
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("data", data)
        self.assertGreater(len(data["data"]), 0)
        # Verify USD is present in fallback
        ccys = [item.get("Ccy") for item in data["data"]]
        self.assertIn("USD", ccys)
