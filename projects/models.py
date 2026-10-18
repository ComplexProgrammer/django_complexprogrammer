from django.utils import timezone
from django.db import models
from core.models import Auditable, Translatable


class IsService(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_service=True)


class IsActive(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=1)


class Project(models.Model):
    class Status(models.IntegerChoices):
        Draft = 0, "Draft"
        Active = 1, "Active"

    category = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    sub_title = models.CharField(max_length=255)
    url = models.CharField(max_length=255, blank=True)
    application_id = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to="projects/images")
    publish_time = models.DateTimeField(default=timezone.now)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    status = models.BooleanField(
        choices=Status.choices,  # type: ignore
        default=Status.Draft,  # type: ignore
    )
    is_service = models.BooleanField(default=False)
    order = models.IntegerField()
    objects = models.Manager()
    services = IsService()
    actives = IsActive()

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title


EXPLANATION_STATUS = [("", "Yo'q"), ("draft", "Qoralama"), ("approved", "Tasdiqlangan")]


class AvtoTest(models.Model):
    savol = models.TextField()
    savol_en = models.TextField()
    savol_ru = models.TextField()
    javob_a = models.TextField()
    javob_a_en = models.TextField()
    javob_a_ru = models.TextField()
    javob_b = models.TextField()
    javob_b_en = models.TextField()
    javob_b_ru = models.TextField()
    javob_c = models.TextField()
    javob_c_en = models.TextField()
    javob_c_ru = models.TextField()
    javob_d = models.TextField()
    javob_d_en = models.TextField()
    javob_d_ru = models.TextField()
    javob = models.CharField(max_length=1)
    bilet = models.IntegerField()
    raqam = models.IntegerField()
    rasm = models.CharField(max_length=255, blank=True)
    # "Nima uchun bu javob to'g'ri?" izohi. AI qoralama yozadi (manage.py draft_explanations),
    # saytda faqat admin tasdiqlagani ko'rinadi.
    izoh = models.TextField(blank=True, default="")
    izoh_ru = models.TextField(blank=True, default="")
    izoh_en = models.TextField(blank=True, default="")
    izoh_holati = models.CharField(
        max_length=10, blank=True, default="", choices=EXPLANATION_STATUS, db_index=True,
        help_text="Saytda faqat «Tasdiqlangan» izoh ko'rsatiladi.",
    )
    izoh_ishonch = models.CharField(
        max_length=10, blank=True, default="",
        help_text="AI qoralamaning o'z bahosi (high/medium/low) — past bo'lsa diqqat bilan tekshiring.",
    )
    objects = models.Manager()

    class Meta:
        ordering = ["raqam"]

    def __str__(self):
        return f"{self.bilet} {self.savol}"
