from enum import IntEnum

from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation

from ckeditor.fields import RichTextField

from humangene import settings
from utils.intenum import IntEnumField


class Category(models.Model):
    text_fa = models.CharField(max_length=40, unique=True)
    text_en = models.CharField(max_length=40, unique=True, default='')

    def __str__(self):
        return self.text_fa


class Tag(models.Model):
    text_fa = models.CharField(max_length=40, unique=True)
    text_en = models.CharField(max_length=40, unique=True, default='')

    def __str__(self):
        return self.text_fa


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    created_at = models.DateTimeField(default=now)


class Dislike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    created_at = models.DateTimeField(default=now)


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    text = models.CharField(max_length=1000)
    is_approved = models.BooleanField(default=False)
    supervised_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name='supervised_by',
                                      on_delete=models.DO_NOTHING)
    supervised_date = models.DateTimeField(blank=True, null=True)

    enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return self.text


class ContentTypeChoices(IntEnum):
    page = 0
    news = 1


class Content(models.Model):
    type = IntEnumField(ContentTypeChoices, default=ContentTypeChoices.page)
    title_fa = models.CharField(max_length=500)
    title_en = models.CharField(max_length=500, default='')
    text_fa = RichTextField()
    text_en = RichTextField(default='')
    image = models.ImageField(upload_to='images/posts', blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True)
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.DO_NOTHING)
    created_date = models.DateTimeField(default=now)
    published_date = models.DateTimeField(default=now)

    comments = GenericRelation(Comment, related_query_name='news', blank=True, null=True, on_delete=models.CASCADE)
    likes = GenericRelation(Like, related_query_name='news', blank=True, null=True, on_delete=models.CASCADE)
    dislikes = GenericRelation(Dislike, related_query_name='news', blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.title_fa)


# class News(models.Model):
#     title_fa = models.CharField(max_length=500)
#     title_en = models.CharField(max_length=500, default='')
#     text_fa = RichTextField()
#     text_en = RichTextField(default='')
#     image = models.ImageField(upload_to='images/posts', blank=True, null=True)
#     tags = models.ManyToManyField(Tag, blank=True)
#     category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.DO_NOTHING)
#     created_date = models.DateTimeField(default=now)
#     published_date = models.DateTimeField(default=now)
#
#     comments = GenericRelation(Comment, related_query_name='news', blank=True, null=True, on_delete=models.CASCADE)
#     likes = GenericRelation(Like, related_query_name='news', blank=True, null=True, on_delete=models.CASCADE)
#     dislikes = GenericRelation(Dislike, related_query_name='news', blank=True, null=True, on_delete=models.CASCADE)
#
#     class Meta:
#         verbose_name_plural = 'News'
#
#     def __str__(self):
#         return str(self.title_en)


class SliderItem(models.Model):
    order = models.IntegerField(default=0)
    image = models.ImageField(upload_to='images/sliders')
    text_fa = models.CharField(max_length=300)
    text_en = models.CharField(max_length=300, default='')
    description_fa = models.CharField(max_length=500)
    description_en = models.CharField(max_length=500, default='')
    url = models.URLField()

    def __str__(self):
        return self.text_fa


class Slider(models.Model):
    name = models.CharField(max_length=200)
    items = models.ManyToManyField(SliderItem, blank=True)

    def __str__(self):
        return self.name


class CompanyMembers(models.Model):
    image = models.ImageField(upload_to='images/company_members')
    name_fa = models.CharField(max_length=200)
    name_en = models.CharField(max_length=200, default='')
    job_fa = models.CharField(max_length=200)
    job_en = models.CharField(max_length=200, default='')
    description_fa = models.CharField(max_length=500)
    description_en = models.CharField(max_length=500, default='')
    email = models.EmailField()

    def __str__(self):
        return self.name_fa


class CustomerCompanies(models.Model):
    title_fa = models.CharField(max_length=200)
    title_en = models.CharField(max_length=200, default='')
    image = models.ImageField(upload_to='images/customer_companies')
    link = models.URLField()

    def __str__(self):
        return self.title_fa


class Feature(models.Model):
    title_fa = models.CharField(max_length=200)
    title_en = models.CharField(max_length=200, default='')
    icon = models.CharField(max_length=100)
    description_fa = models.CharField(max_length=500)
    description_en = models.CharField(max_length=500, default='')

    def __str__(self):
        return self.title_fa


class Service(models.Model):
    title_fa = models.CharField(max_length=200)
    title_en = models.CharField(max_length=200, default='')
    image = models.ImageField(upload_to='images/services')
    description_fa = models.CharField(max_length=500)
    description_en = models.CharField(max_length=500, default='')
    link = models.URLField()

    def __str__(self):
        return self.title_fa


class ContactMessage(models.Model):
    name = models.CharField(max_length=200)
    text = models.CharField(max_length=500)
    email = models.EmailField()
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return self.name