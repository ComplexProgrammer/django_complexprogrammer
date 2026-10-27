from django.db import models
from django.conf import settings
from django.utils import timezone


class Comment(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)  # Email manzili
    page_url = models.CharField(max_length=200)  # Qaysi sahifada qoldirilgani
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="replies"
    )

    class Meta:
        ordering = ["-created_at"]
        # Har bir sahifa o'z izohlarini page_url bo'yicha oladi (comments.pages.page_comments)
        indexes = [models.Index(fields=["page_url", "-created_at"], name="comment_page_idx")]

    def __str__(self):
        return f"{self.username} - {self.page_url} - {self.text}"

    @property
    def is_official(self):
        """Sayt ma'muriyatining javobi (bu email bilan faqat xodim yoza oladi — comments.views)."""
        return (self.email or "").lower() == settings.COMMENTS_OFFICIAL_EMAIL
