from django.db import models

class Auditable(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    # created_by = models.IntegerField()
    updated_at = models.DateTimeField(auto_now=True)
    # updated_by = models.IntegerField()
    is_deleted = models.BooleanField(default=False)
    sort_order = models.IntegerField(default=0)
    class Meta:
        abstract = True

class Translatable(Auditable):
    name_en_us = models.TextField()
    name_ru_ru = models.TextField()
    name_uz_crl = models.TextField()
    name_uz_uz = models.TextField()
    class Meta:
        abstract = True

class Types(Translatable):
    image = models.ImageField(upload_to='tests/types/images', blank=True)
    class Meta:
        verbose_name = "Type"
        verbose_name_plural = "Types"
        ordering=['sort_order']
    def __str__(self):
        return f"{self.name_en_us}"
class Groups(Translatable):
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
        return f"{self.name_en_us}"
    
class BookTypes(Auditable):
    code = models.TextField()
    description = models.TextField()
    image = models.ImageField(upload_to='tests/book_types/images', blank=True)
    class Meta:
        verbose_name = "BookType"
        verbose_name_plural = "BookTypes"
        ordering=['sort_order']
    def __str__(self):
        return f"{self.description}"

class Books(Translatable):
    type = models.ForeignKey(BookTypes,
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
        return f"{self.name_en_us}"
    
class Topics(Translatable):
    number = models.IntegerField()
    book = models.ForeignKey(Books,
                                  related_name='topics',
                                  on_delete=models.DO_NOTHING)
    image = models.ImageField(upload_to='tests/topics/images', blank=True)
    class Meta:
        verbose_name = "Topic"
        verbose_name_plural = "Topics"
        ordering=['number']
    def __str__(self):
        return f"{self.name_en_us}"

class Questions(Translatable):
    number = models.IntegerField()
    image = models.ImageField(upload_to='tests/questions/images', blank=True)
    topic = models.ForeignKey(Topics,
                                  related_name='questions',
                                  on_delete=models.DO_NOTHING)
    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"
        ordering=['number']
    def __str__(self):
        return f"{self.name_en_us}"

class Answers(Translatable):
    number = models.IntegerField()
    image = models.ImageField(upload_to='tests/answers/images', blank=True)
    right = models.BooleanField(default=False)
    question = models.ForeignKey(Questions,
                                  related_name='answers',
                                  on_delete=models.DO_NOTHING)
    class Meta:
        verbose_name = "Answer"
        verbose_name_plural = "Answers"
        ordering=['number']
    def __str__(self):
        return f"{self.name_en_us}"
