"""Avtotest foydalanuvchilari: Telegram orqali kirish, natijalarni qurilmalar o'rtasida saqlash, imtihonlar va faollik."""

from django.contrib.auth.models import User
from django.db import models


class TelegramAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="telegram")
    telegram_id = models.BigIntegerField(unique=True)
    username = models.CharField(max_length=64, blank=True, default="")
    first_name = models.CharField(max_length=128, blank=True, default="")
    last_name = models.CharField(max_length=128, blank=True, default="")
    photo_url = models.URLField(max_length=500, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    last_login_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Telegram akkaunt"
        verbose_name_plural = "Telegram akkauntlar"

    def __str__(self):
        return self.display_name

    @property
    def display_name(self):
        """Reytingda ko'rinadigan ism: familiyaning faqat bosh harfi (maxfiylik uchun)."""
        name = self.first_name or self.username or f"#{self.telegram_id}"
        if self.last_name:
            name += f" {self.last_name[0]}."
        return name


class Progress(models.Model):
    """Brauzerdagi ``avtotestResults`` va ``avtotestMistakes`` ning server nusxasi."""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="avtotest_progress")
    results = models.JSONField(default=dict, blank=True)
    mistakes = models.JSONField(default=dict, blank=True)
    # Boshqa qurilmada tuzatilgan xatolar: {savol_id: o'chirilgan vaqt (ms)} — eski nusxa qayta tiklanmasligi uchun
    removed = models.JSONField(default=dict, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Natijalar"
        verbose_name_plural = "Natijalar"

    def __str__(self):
        return f"{self.user} — {len(self.results)} bilet"


class ExamResult(models.Model):
    """Imtihon simulyatori natijasi (20 savol, 25 daqiqa)."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="exam_results")
    correct = models.PositiveSmallIntegerField()
    total = models.PositiveSmallIntegerField()
    seconds = models.PositiveIntegerField(default=0)
    passed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = "Imtihon natijasi"
        verbose_name_plural = "Imtihon natijalari"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} {self.correct}/{self.total}"


class ActivityDay(models.Model):
    """Kunlik faollik: ketma-ket kunlar (streak) va haftalik reyting shundan hisoblanadi."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="activity_days")
    date = models.DateField(db_index=True)
    answered = models.PositiveIntegerField(default=0)
    correct = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Faollik kuni"
        verbose_name_plural = "Faollik kunlari"
        unique_together = ("user", "date")
        ordering = ["-date"]

    def __str__(self):
        return f"{self.user} {self.date}: {self.answered}"
