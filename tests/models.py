import sys
from django.db import models
from django.contrib.auth.models import User
from core.models import Auditable, Translatable


class Types(Translatable):
    image = models.ImageField(upload_to="tests/types/images", blank=True)

    class Meta:
        verbose_name = "Type"
        verbose_name_plural = "Types"
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
        verbose_name = "Group"
        verbose_name_plural = "Groups"
        ordering = ["number"]

    def __str__(self):
        return f"{self.name_uz_uz}"


class BookTypes(Translatable):
    code = models.TextField()
    description = models.TextField()
    image = models.ImageField(upload_to="tests/book_types/images", blank=True)

    class Meta:
        verbose_name = "BookType"
        verbose_name_plural = "BookTypes"
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
        verbose_name = "Book"
        verbose_name_plural = "Books"
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
        verbose_name = "Topic"
        verbose_name_plural = "Topics"
        ordering = ["number"]

    def __str__(self):
        return f"{self.name_uz_uz}"


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

    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"
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
        verbose_name = "Answer"
        verbose_name_plural = "Answers"
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
        verbose_name = "Road sign category"
        verbose_name_plural = "Road sign categories"
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
        verbose_name = "Road sign"
        verbose_name_plural = "Road signs"
        ordering = ["category__sort_order", "sort_order"]

    def __str__(self):
        return f"{self.number} {self.name_uz_uz}"
