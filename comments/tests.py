from django.core.cache import cache
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


@override_settings(SECURE_SSL_REDIRECT=False)
class CommentModerationTestCase(TestCase):
    def setUp(self):
        cache.clear()  # IP böyiça rate-limit hisoblagiçi oldingi testlardan qolmasin

    def post(self, text, **extra):
        data = {"username": "Ali", "email": "ali@mail.uz", "text": text, "page_url": PAGE, **extra}
        return self.client.post("/add-comment/", data)

    def test_link_comment_goes_to_moderation(self):
        self.post("Zör sayt, mana bu yerda ham bor https://spam.example.com")
        comment = Comment.objects.get()
        self.assertEqual(comment.status, Comment.Status.PENDING)
        response = self.client.get("/comments/more/", {"offset": 0, "page_url": PAGE})
        self.assertNotIn("spam.example.com", response.content.decode())

    def test_plain_comment_is_published(self):
        self.post("Rahmat, juda foydali testlar ekan")
        self.assertEqual(Comment.objects.get().status, Comment.Status.APPROVED)

    def test_same_text_with_other_email_is_duplicate(self):
        self.post("Bir xil matnli izoh")
        self.post("Bir xil matnli izoh", email="boshqa@mail.uz")
        self.assertEqual(Comment.objects.count(), 1)

    def test_pii_is_masked_on_page(self):
        Comment.objects.create(
            username="Vali", email="v@mail.uz", page_url=PAGE,
            text="Pasportim AA1234567, tel +998 90 123 45 67, JŞŞIR 31234567890123",
        )
        html = self.client.get("/comments/more/", {"offset": 0, "page_url": PAGE}).content.decode()
        for secret in ("AA1234567", "123 45 67", "31234567890123"):
            self.assertNotIn(secret, html)
        self.assertIn("Pasportim", html)

    def test_hidden_reply_not_shown(self):
        parent = Comment.objects.create(username="A", email="a@b.uz", page_url=PAGE, text="Asosiy izoh")
        Comment.objects.create(
            username="B", email="b@b.uz", page_url=PAGE, text="yaşirin javob", parent=parent,
            status=Comment.Status.HIDDEN,
        )
        html = self.client.get("/comments/more/", {"offset": 0, "page_url": PAGE}).content.decode()
        self.assertIn("Asosiy izoh", html)
        self.assertNotIn("yaşirin javob", html)
