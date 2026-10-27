from django.test import TestCase, override_settings

from comments.models import Comment

PAGE = "https://complexprogrammer.uz/avtotest/1/"


@override_settings(SECURE_SSL_REDIRECT=False)
class CommentPaginationTestCase(TestCase):
    def setUp(self):
        Comment.objects.bulk_create(
            Comment(username=f"user{i}", email="a@b.uz", page_url=PAGE, text=f"izoh {i}") for i in range(25)
        )

    def test_more_comments_returns_next_batch(self):
        # /ru/ prefiksi va utm parametri bilan ham shu sahifaning izohlari olinadi
        response = self.client.get(
            "/comments/more/", {"offset": 20, "page_url": "https://complexprogrammer.uz/ru/avtotest/1/?utm_source=x"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode().count('class="card shadow-sm mb-3"'), 5)

    def test_more_comments_bad_offset(self):
        response = self.client.get("/comments/more/", {"offset": "abc", "page_url": PAGE})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode().count('class="card shadow-sm mb-3"'), 20)
