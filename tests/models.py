import sys
from django.db import models
from django.contrib.auth.models import User
from core.models import Auditable, Translatable

class Types(Translatable):
    image = models.ImageField(upload_to='tests/types/images', blank=True)
    class Meta:
        verbose_name = "Type"
        verbose_name_plural = "Types"
        ordering=['sort_order']
    def __str__(self):
        return f"{self.name_uz_uz}"
class Groups(Translatable):
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='tests_groups')
    number = models.IntegerField()
    type = models.ForeignKey(Types,
                                null=True,
                                default=None,
                                related_name='groups',
                                on_delete=models.DO_NOTHING)
    image = models.ImageField(upload_to='tests/groups/images', blank=True)
    class Meta:
        verbose_name = "Group"
        verbose_name_plural = "Groups"
        ordering=['number']
    def __str__(self):
        return f"{self.name_uz_uz}"
    
class BookTypes(Translatable):
    code = models.TextField()
    description = models.TextField()
    image = models.ImageField(upload_to='tests/book_types/images', blank=True)
    class Meta:
        verbose_name = "BookType"
        verbose_name_plural = "BookTypes"
        ordering=['sort_order']
    def __str__(self):
        return f"{self.code}"

class Books(Auditable):
    book_type = models.ForeignKey(BookTypes,
                                null=True,
                                default=None,
                                related_name='books',
                                on_delete=models.DO_NOTHING)
    type = models.ForeignKey(Types,
                                null=True,
                                default=None,
                                related_name='books',
                                on_delete=models.DO_NOTHING)
    group = models.ForeignKey(Groups,
                                  related_name='books',
                                  on_delete=models.DO_NOTHING)
    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "Books"
        ordering=['sort_order']
    def __str__(self):
        return f"{self.book_type}"
    
class Topics(Translatable):
    number = models.IntegerField()
    type = models.ForeignKey(Types,
                                null=True,
                                default=None,
                                related_name='topics',
                                on_delete=models.DO_NOTHING)
    group = models.ForeignKey(Groups,
                              null=True,
                                default=None,
                                  related_name='topics',
                                  on_delete=models.DO_NOTHING)
    book = models.ForeignKey(Books,
                                  related_name='topics',
                                  on_delete=models.DO_NOTHING)
    image = models.ImageField(upload_to='tests/topics/images', blank=True)
    class Meta:
        verbose_name = "Topic"
        verbose_name_plural = "Topics"
        ordering=['number']
    def __str__(self):
        return f"{self.name_uz_uz}"

class Questions(Translatable):
    number = models.IntegerField()
    image = models.ImageField(upload_to='tests/questions/images', blank=True)
    type = models.ForeignKey(Types,
                                null=True,
                                default=None,
                                related_name='questions',
                                on_delete=models.DO_NOTHING)
    group = models.ForeignKey(Groups,
                              null=True,
                                default=None,
                                  related_name='questions',
                                  on_delete=models.DO_NOTHING)
    book = models.ForeignKey(Books,
                             null=True,
                                default=None,
                                  related_name='questions',
                                  on_delete=models.DO_NOTHING)
    topic = models.ForeignKey(Topics,
                                  related_name='questions',
                                  on_delete=models.DO_NOTHING)
    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"
        ordering=['number']
    def __str__(self):
        return f"{self.name_uz_uz}"

class Answers(Translatable):
    number = models.IntegerField()
    image = models.ImageField(upload_to='tests/answers/images', blank=True)
    right = models.BooleanField(default=False)
    type = models.ForeignKey(Types,
                                null=True,
                                default=None,
                                related_name='answers',
                                on_delete=models.DO_NOTHING)
    group = models.ForeignKey(Groups,
                              null=True,
                                default=None,
                                  related_name='answers',
                                  on_delete=models.DO_NOTHING)
    book = models.ForeignKey(Books,
                             null=True,
                                default=None,
                                  related_name='answers',
                                  on_delete=models.DO_NOTHING)
    topic = models.ForeignKey(Topics,
                              null=True,
                                default=None,
                                  related_name='answers',
                                  on_delete=models.DO_NOTHING)
    question = models.ForeignKey(Questions,
                                  related_name='answers',
                                  on_delete=models.DO_NOTHING)
    class Meta:
        verbose_name = "Answer"
        verbose_name_plural = "Answers"
        ordering=['number']
    def __str__(self):
        return f"{self.name_uz_uz}"
