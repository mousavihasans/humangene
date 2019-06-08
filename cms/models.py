from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation


class Category(models.Model):
    text_fa = models.CharField(max_length=40, unique=True)
    text_en = models.CharField(max_length=40, unique=True)

    def __str__(self):
        return self.text_fa


class Tag(models.Model):
    text_fa = models.CharField(max_length=40, unique=True)
    text_en = models.CharField(max_length=40, unique=True)

    def __str__(self):
        return self.text_fa


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    created_at = models.DateTimeField(default=now)


class Dislike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    created_at = models.DateTimeField(default=now)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    text = models.CharField(max_length=1000)
    is_approved = models.BooleanField(default=False)
    supervised_by = models.ForeignKey(User, blank=True, null=True, related_name='supervised_by',
                                      on_delete=models.DO_NOTHING)
    supervised_date = models.DateTimeField(blank=True, null=True)

    enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return self.text


class Page(models.Model):
    title_fa = models.CharField(max_length=500)
    title_en = models.CharField(max_length=500)
    text_fa = models.TextField()
    text_en = models.TextField()
    image = models.ImageField(upload_to="images/posts", blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True)
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.DO_NOTHING, 
    help_text="مقاله در این منو نشان داده خواهد شد.")
    created_date = models.DateTimeField(default=now)
    published_date = models.DateTimeField(default=now)

    comments = GenericRelation(Comment, related_query_name='news', blank=True, null=True, on_delete=models.CASCADE)
    likes = GenericRelation(Like, related_query_name='news', blank=True, null=True, on_delete=models.CASCADE)
    dislikes = GenericRelation(Dislike, related_query_name='news', blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.title_fa)


class News(models.Model):
    title_fa = models.CharField(max_length=500)
    title_en = models.CharField(max_length=500)
    text_fa = models.TextField()
    text_en = models.TextField()
    image = models.ImageField(upload_to="images/posts", blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True)
    created_date = models.DateTimeField(default=now)
    published_date = models.DateTimeField(default=now)

    comments = GenericRelation(Comment, related_query_name='news', blank=True, null=True, on_delete=models.CASCADE)
    likes = GenericRelation(Like, related_query_name='news', blank=True, null=True, on_delete=models.CASCADE)
    dislikes = GenericRelation(Dislike, related_query_name='news', blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.title_fa)


class SliderItem(models.Model):
    order = models.IntegerField(default=0)
    image = models.ImageField(upload_to="images/sliders")
    text_fa = models.CharField(max_length=300)
    text_en = models.CharField(max_length=300)
    url = models.URLField()

    def __str__(self):
        return str(self.id)


class Slider(models.Model):
    name = models.CharField(max_length=200)
    items = models.ManyToManyField(SliderItem, blank=True)

    def __str__(self):
        return self.name


