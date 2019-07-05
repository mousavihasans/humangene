from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from cms.models import Page, News, Slider, Tag, Category, Comment
from utils.date import TimestampField


class PageSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()

    def get_comments(self, instance):
        comments = Comment.objects.filter(content_type=ContentType.objects.get_for_model(Page),
                                          object_id=instance.id,
                                          enabled=True,
                                          is_approved=True).order_by('-created_at')
        return CommentSerializer(comments, many=True).data

    class Meta:
        model = Page
        fields = ('id', 'title_fa', 'title_en', 'text_fa', 'text_en', 'image', 'category', 'comments')


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    timestamp = TimestampField(source='created_at', read_only=True)

    def get_user(self, instance):
        return instance.user.username

    class Meta:
        model = Comment
        fields = ('id', 'user', 'text', 'timestamp')
        read_only_fields = ('id', 'user', 'timestamp')


class NewsSerializer(serializers.ModelSerializer):

    comments = serializers.SerializerMethodField()

    def get_comments(self, instance):
        comments = Comment.objects.filter(content_type=ContentType.objects.get_for_model(News),
                                          object_id=instance.id,
                                          enabled=True,
                                          is_approved=True).order_by('-created_at')
        return CommentSerializer(comments, many=True).data

    class Meta:
        model = News
        fields = ('id', 'title_fa', 'title_en', 'text_fa', 'text_en', 'image', 'comments')


class SliderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Slider
        fields = ('id', 'name', 'items')


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'text_fa', 'text_en')


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'text_fa', 'text_en')


