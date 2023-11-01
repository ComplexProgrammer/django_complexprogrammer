from django.db import models

class Auditable(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    # created_by = models.IntegerField()
    updated_at = models.DateTimeField(auto_now=True)
    # updated_by = models.IntegerField()
    is_deleted = models.BooleanField(default=False)
    class Meta:
        abstract = True

class Translatable(Auditable):
    name_en_us = models.TextField()
    name_ru_ru = models.TextField()
    name_uz_crl = models.TextField()
    name_uz_uz = models.TextField()
    class Meta:
        abstract = True

class Groups(Translatable):
    number = models.IntegerField()
    class Meta:
        verbose_name = "Group"
        verbose_name_plural = "Groups"
        ordering=['number']
    def __str__(self):
        return f"{self.name_en_us}"

class Books(Translatable):
    class BookType(models.TextChoices):
        # none = 'none'
        # uzb_avto_test = 'uzb_avto_test'
        usa_avto_test= 'usa_avto_test'
    book_type = models.CharField(
        max_length=20,
        choices=BookType.choices,
        default=BookType.usa_avto_test,
    )
    group = models.ForeignKey(Groups,
                                  related_name='books',
                                  on_delete=models.CASCADE)
    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "Books"
        ordering=['id']
    def __str__(self):
        return f"{self.name_en_us}"
    
class Topics(Translatable):
    number = models.IntegerField()
    book = models.ForeignKey(Books,
                                  related_name='topics',
                                  on_delete=models.CASCADE)
    class Meta:
        verbose_name = "Topic"
        verbose_name_plural = "Topics"
        ordering=['number']
    def __str__(self):
        return f"{self.name_en_us}"

class Questions(Translatable):
    number = models.IntegerField()
    image = models.ImageField(upload_to='projects/tests/questions/images', blank=True)
    topic = models.ForeignKey(Topics,
                                  related_name='questions',
                                  on_delete=models.CASCADE)
    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"
        ordering=['number']
    def __str__(self):
        return f"{self.name_en_us}"

class Answers(Translatable):
    number = models.IntegerField()
    image = models.ImageField(upload_to='projects/tests/answers/images', blank=True)
    right = models.BooleanField(default=False)
    question = models.ForeignKey(Questions,
                                  related_name='answers',
                                  on_delete=models.CASCADE)
    class Meta:
        verbose_name = "Answer"
        verbose_name_plural = "Answers"
        ordering=['number']
    def __str__(self):
        return f"{self.name_en_us}"
