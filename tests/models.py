import sys
from django.db import models
from django.contrib.auth.models import User
from core.models import Auditable, Translatable

EXPLANATION_STATUS = [("", "Yöq"), ("draft", "Qoralama"), ("approved", "Tasdiqlangan")]
EXPLANATION_FIELDS = ("explanation_en_us", "explanation_ru_ru", "explanation_uz_crl", "explanation_uz_uz")


class Types(Translatable):
    image = models.ImageField(upload_to="tests/types/images", blank=True)

    class Meta:
        verbose_name = "Test turi"
        verbose_name_plural = "Test turlari"
        ordering = ["sort_order"]

    def __str__(self):
        return f"{self.name_uz_uz}"


class Groups(Translatable):
    created_by = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name="tests_groups"
    )
    number = models.IntegerField()
    type = models.ForeignKey(
        Types,
        null=True,
        default=None,
        related_name="groups",
        on_delete=models.DO_NOTHING,
    )
    image = models.ImageField(upload_to="tests/groups/images", blank=True)

    class Meta:
        verbose_name = "Guruh"
        verbose_name_plural = "Guruhlar"
        ordering = ["number"]

    def __str__(self):
        return f"{self.name_uz_uz}"


class BookTypes(Translatable):
    code = models.TextField()
    description = models.TextField()
    image = models.ImageField(upload_to="tests/book_types/images", blank=True)

    class Meta:
        verbose_name = "Kitob turi"
        verbose_name_plural = "Kitob turlari"
        ordering = ["sort_order"]

    def __str__(self):
        return f"{self.code}"


class Books(Auditable):
    book_type = models.ForeignKey(
        BookTypes,
        null=True,
        default=None,
        related_name="books",
        on_delete=models.DO_NOTHING,
    )
    type = models.ForeignKey(
        Types,
        null=True,
        default=None,
        related_name="books",
        on_delete=models.DO_NOTHING,
    )
    group = models.ForeignKey(Groups, related_name="books", on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = "Kitob"
        verbose_name_plural = "Kitoblar"
        ordering = ["sort_order"]

    def __str__(self):
        return f"{self.book_type}"


class Topics(Translatable):
    number = models.IntegerField()
    type = models.ForeignKey(
        Types,
        null=True,
        default=None,
        related_name="topics",
        on_delete=models.DO_NOTHING,
    )
    group = models.ForeignKey(
        Groups,
        null=True,
        default=None,
        related_name="topics",
        on_delete=models.DO_NOTHING,
    )
    book = models.ForeignKey(Books, related_name="topics", on_delete=models.DO_NOTHING)
    image = models.ImageField(upload_to="tests/topics/images", blank=True)

    class Meta:
        verbose_name = "Bilet / mavzu"
        verbose_name_plural = "Biletlar / mavzular"
        ordering = ["number"]

    def __str__(self):
        # Kitob nomi bilan: "28-bilet" bir neçta kitobda bor, admin'dagi tanlovda adaşmaslik uçun
        return f"{self.name_uz_uz} · {self.book}" if self.book_id else f"{self.name_uz_uz}"


class Questions(Translatable):
    number = models.IntegerField()
    image = models.ImageField(upload_to="tests/questions/images", blank=True)
    type = models.ForeignKey(
        Types,
        null=True,
        default=None,
        related_name="questions",
        on_delete=models.DO_NOTHING,
    )
    group = models.ForeignKey(
        Groups,
        null=True,
        default=None,
        related_name="questions",
        on_delete=models.DO_NOTHING,
    )
    book = models.ForeignKey(
        Books,
        null=True,
        default=None,
        related_name="questions",
        on_delete=models.DO_NOTHING,
    )
    topic = models.ForeignKey(
        Topics, related_name="questions", on_delete=models.DO_NOTHING
    )
    # Javob izohi: nima uchun aynan shu javob to'g'ri (YHQ bandi va h.k.)
    explanation_en_us = models.TextField(blank=True, default="")
    explanation_ru_ru = models.TextField(blank=True, default="")
    explanation_uz_crl = models.TextField(blank=True, default="")
    explanation_uz_uz = models.TextField(blank=True, default="")
    # AI qoralamasi (manage.py draft_explanations submit --source tests) tasdiqlanmaguncha saytda ko'rinmaydi
    explanation_status = models.CharField(
        max_length=10, blank=True, default="", choices=EXPLANATION_STATUS, db_index=True,
        help_text="«Qoralama» izoh saytda körinmaydi. Qölda yozilgan izoh uçun böş yoki «Tasdiqlangan».",
    )
    explanation_confidence = models.CharField(
        max_length=10, blank=True, default="",
        help_text="AI qoralamaning öz bahosi (high/medium/low) — past bölsa diqqat bilan tekşiring.",
    )

    class Meta:
        verbose_name = "Savol"
        verbose_name_plural = "Savollar"
        ordering = ["number"]

    def __str__(self):
        return f"{self.name_uz_uz}"


class Answers(Translatable):
    number = models.IntegerField()
    image = models.ImageField(upload_to="tests/answers/images", blank=True)
    right = models.BooleanField(default=False)
    type = models.ForeignKey(
        Types,
        null=True,
        default=None,
        related_name="answers",
        on_delete=models.DO_NOTHING,
    )
    group = models.ForeignKey(
        Groups,
        null=True,
        default=None,
        related_name="answers",
        on_delete=models.DO_NOTHING,
    )
    book = models.ForeignKey(
        Books,
        null=True,
        default=None,
        related_name="answers",
        on_delete=models.DO_NOTHING,
    )
    topic = models.ForeignKey(
        Topics,
        null=True,
        default=None,
        related_name="answers",
        on_delete=models.DO_NOTHING,
    )
    question = models.ForeignKey(
        Questions, related_name="answers", on_delete=models.DO_NOTHING
    )

    class Meta:
        verbose_name = "Javob"
        verbose_name_plural = "Javoblar"
        ordering = ["number"]

    def __str__(self):
        return f"{self.name_uz_uz}"


class RoadSignCategories(models.Model):
    """Yo'l belgilari toifalari (ogohlantiruvchi, taqiqlovchi va h.k.)."""

    code = models.CharField(max_length=32, unique=True)
    name_en_us = models.TextField(blank=True, default="")
    name_ru_ru = models.TextField(blank=True, default="")
    name_uz_crl = models.TextField(blank=True, default="")
    name_uz_uz = models.TextField()
    image = models.ImageField(upload_to="tests/road_sign_categories/images", blank=True)
    sort_order = models.IntegerField(default=0)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Belgi kategoriyasi"
        verbose_name_plural = "Belgi kategoriyalari"
        ordering = ["sort_order"]

    def __str__(self):
        return f"{self.name_uz_uz}"


class RoadSigns(models.Model):
    """Yo'l belgisi: raqami (masalan 1.1), nomi, rasmi va ma'nosi."""

    category = models.ForeignKey(
        RoadSignCategories, related_name="signs", on_delete=models.CASCADE
    )
    number = models.CharField(max_length=16, blank=True, default="")
    name_en_us = models.TextField(blank=True, default="")
    name_ru_ru = models.TextField(blank=True, default="")
    name_uz_crl = models.TextField(blank=True, default="")
    name_uz_uz = models.TextField()
    description_en_us = models.TextField(blank=True, default="")
    description_ru_ru = models.TextField(blank=True, default="")
    description_uz_crl = models.TextField(blank=True, default="")
    description_uz_uz = models.TextField(blank=True, default="")
    image = models.ImageField(upload_to="tests/road_signs/images", blank=True)
    sort_order = models.IntegerField(default=0)
    is_deleted = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Yöl belgisi"
        verbose_name_plural = "Yöl belgilari"
        ordering = ["category__sort_order", "sort_order"]

    def __str__(self):
        return f"{self.number} {self.name_uz_uz}"
