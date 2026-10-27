from unittest.mock import MagicMock, patch
from django.core.cache import cache, caches
from django.test import TestCase, override_settings
from django.urls import reverse
import requests

from projects.views import (
    CBU_FALLBACK_FILE,
    CBU_RATES_URL,
    DEFAULT_REQUEST_HEADERS,
    fetch_json,
)


class SyncThread:
    """Fon yangilanishi testlarda darhol (sinxron) bajariladi — natija aniq bo'lsin."""

    def __init__(self, target, args=(), daemon=None):
        self.target, self.args = target, args

    def start(self):
        self.target(*self.args)


class ExchangeRatesTestCase(TestCase):
    def setUp(self):
        cache.clear()
        caches["durable"].clear()
        thread_patcher = patch("projects.views.threading.Thread", SyncThread)
        thread_patcher.start()
        self.addCleanup(thread_patcher.stop)
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
    def test_fetch_json_returns_stale_data_and_refreshes(self, mock_get):
        # Kesh muddati tugagan, lekin eski ma'lumot bor: darhol eski ma'lumot qaytadi, kesh fonda yangilanadi
        caches["durable"].set("test:stale_key:fallback", [{"Ccy": "OLD"}])
        mock_resp = MagicMock()
        mock_resp.json.return_value = self.mock_rates
        mock_get.return_value = mock_resp

        result = fetch_json("https://cbu.uz/test", "test:stale_key")
        self.assertEqual(result, [{"Ccy": "OLD"}])
        self.assertEqual(cache.get("test:stale_key"), self.mock_rates)
        self.assertIsNone(cache.get("test:stale_key:refreshing"))

    @patch("projects.views._save_disk_fallback")
    @patch("projects.views.requests.get")
    def test_get_exchange_rates_endpoint_success(self, mock_get, mock_save):
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


@override_settings(SECURE_SSL_REDIRECT=False)
class IpPageTestCase(TestCase):
    def setUp(self):
        cache.clear()

    def tearDown(self):
        cache.clear()

    @patch("projects.views.requests.get")
    def test_page_does_not_wait_for_ipapi(self, mock_get):
        # Keshda yo'q IP: sahifa ipapi.co'ga so'rov yubormasdan ochiladi, jadval keyin to'ldiriladi
        response = self.client.get("/ip/", {"ip": "8.8.8.8"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'data-pending="1"')
        mock_get.assert_not_called()

    @patch("projects.views.requests.get")
    def test_get_ip_data_and_cached_page(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.json.return_value = {"ip": "8.8.8.8", "city": "Mountain View", "country_code": "US"}
        mock_get.return_value = mock_resp

        data = self.client.get("/GetIpData/", {"ip": "8.8.8.8"}).json()
        self.assertEqual(data["city"], "Mountain View")
        # Endi keshda bor — sahifa ma'lumot bilan darhol chiqadi
        response = self.client.get("/ip/", {"ip": "8.8.8.8"})
        self.assertNotContains(response, 'data-pending="1"')
        self.assertContains(response, "Mountain View")
        self.assertEqual(mock_get.call_count, 1)

    def test_private_ip(self):
        data = self.client.get("/GetIpData/", {"ip": "192.168.1.1"}).json()
        self.assertTrue(data["error"])


@override_settings(SECURE_SSL_REDIRECT=False)
class YoutubeJobTestCase(TestCase):
    def setUp(self):
        cache.clear()
        thread_patcher = patch("projects.views.threading.Thread", SyncThread)
        thread_patcher.start()
        self.addCleanup(thread_patcher.stop)

    def tearDown(self):
        cache.clear()

    def post(self, **extra):
        body = {"choice": 1, "quality": "low", "link": "https://youtu.be/abc", **extra}
        return self.client.post("/youtube_downloader/", body, content_type="application/json")

    @patch("projects.views.youtube_downloader.download_video", return_value="abc_video.mp4")
    def test_async_job(self, mock_download):
        job = self.post(**{"async": True}).json()["job"]
        status = self.client.get("/youtube_downloader/status/", {"job": job}).json()
        self.assertEqual(status, {"status": "done", "result": "abc_video.mp4"})

    @patch("projects.views.youtube_downloader.download_video", return_value="abc_video.mp4")
    def test_sync_request_keeps_old_format(self, mock_download):
        # Mobil ilova "async"siz yuboradi va natijani shu javobda kutadi
        self.assertEqual(self.post().json(), {"result": "abc_video.mp4"})

    def test_unknown_job(self):
        response = self.client.get("/youtube_downloader/status/", {"job": "nope"})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["result"], "0")


class RateRowsTestCase(TestCase):
    def test_trend_is_numeric_not_string(self):
        from projects.views import _rate_rows

        rows = _rate_rows([
            {"Ccy": "USD", "Code": "840", "CcyNm_UZ": "AQSH dollari", "Nominal": "1", "Rate": "11861.96", "Diff": "23.04"},
            {"Ccy": "JPY", "Code": "392", "CcyNm_UZ": "Yaponiya iyenasi", "Nominal": "10", "Rate": "753.5", "Diff": "-1.10"},
            # Satr sifatida "0.00" > "0" — avval nol o'zgarish yashil "+" bilan chiqardi
            {"Ccy": "XDR", "Code": "960", "CcyNm_UZ": "SDR", "Nominal": "1", "Rate": "16000", "Diff": "0.00"},
            {"Ccy": "BAD", "Rate": "n/a"},
        ], "uz")
        self.assertEqual([r["trend"] for r in rows], ["up", "down", "flat"])
        self.assertEqual(rows[0]["rate_fmt"], "11\u00a0861.96")
        self.assertEqual(rows[0]["diff_fmt"], "+23.04")
        self.assertEqual(rows[1]["nominal"], 10)
        self.assertIn("dollari", rows[0]["search"])


@override_settings(SECURE_SSL_REDIRECT=False)
class YoutubeInfoTestCase(TestCase):
    def setUp(self):
        cache.clear()

    def tearDown(self):
        cache.clear()

    @patch("projects.views.youtube_downloader.video_info", return_value={"title": "Me at the zoo", "heights": [144, 240]})
    def test_info_is_cached(self, mock_info):
        for _ in range(2):
            data = self.client.get("/youtube_downloader/info/", {"url": "https://youtu.be/jNQXAC9IVRw"}).json()
        self.assertEqual(data["title"], "Me at the zoo")
        mock_info.assert_called_once()

    def test_info_rejects_non_youtube(self):
        response = self.client.get("/youtube_downloader/info/", {"url": "https://example.com/video"})
        self.assertEqual(response.status_code, 400)

    @patch("projects.views.youtube_downloader.video_info")
    def test_info_explains_errors(self, mock_info):
        from projects.youtube_downloader import DownloadError

        mock_info.side_effect = DownloadError("Video topilmadi yoki o'chirilgan")
        response = self.client.get("/youtube_downloader/info/", {"url": "https://youtu.be/xxxxxxxxxxx"})
        self.assertEqual(response.status_code, 422)
        self.assertIn("topilmadi", response.json()["error"])
