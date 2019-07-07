from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from cms.models import Page, News, Slider, Tag, Category, Comment, SliderItem, Service, Feature, CustomerCompanies, \
    CompanyMembers
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
        fields = ('id', 'title_fa', 'title_en', 'text_fa', 'text_en', 'image', 'category', 'published_date', 'comments')


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
        fields = ('id', 'title_fa', 'title_en', 'text_fa', 'text_en', 'image', 'category', 'published_date', 'comments')


class SliderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = SliderItem
        fields = ('id', 'order', 'image', 'text_fa', 'text_en', 'url')


class SliderSerializer(serializers.ModelSerializer):
    items = SliderItemSerializer(read_only=True, many=True)

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


class ServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Service
        fields = ('id', 'title', 'image', 'description', 'link')


class FeatureSerializer(serializers.ModelSerializer):

    class Meta:
        model = Feature
        fields = ('id', 'title', 'icon', 'description')


class CustomerCompaniesSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomerCompanies
        fields = ('id', 'title', 'image', 'link')


class CompanyMembersSerializer(serializers.ModelSerializer):

    class Meta:
        model = CompanyMembers
        fields = ('id', 'image', 'job', 'name', 'description', 'email')


