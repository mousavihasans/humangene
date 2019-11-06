from django.utils.translation import get_language_from_request
from rest_framework.fields import get_attribute

import utils
from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from cms.models import Content, Slider, Tag, Category, Comment, SliderItem, Service, Feature, CustomerCompanies, \
    CompanyMembers, ContactMessage
from utils.date import TimestampField


class ContentSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    text = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    def get_title(self, instance):
        lang = get_language_from_request(self.context['request'], check_path=True)
        return getattr(instance, 'title_'+lang)

    def get_text(self, instance):
        lang = get_language_from_request(self.context['request'], check_path=True)
        return getattr(instance, 'text_' + lang)

    def get_comments(self, instance):
        comments = Comment.objects.filter(content_type=ContentType.objects.get_for_model(Content),
                                          object_id=instance.id,
                                          enabled=True,
                                          is_approved=True).order_by('-created_at')
        return CommentSerializer(comments, many=True).data

    class Meta:
        model = Content
        fields = ('id', 'title', 'text', 'image', 'category', 'published_date', 'comments')


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    timestamp = TimestampField(source='created_at', read_only=True)

    def get_user(self, instance):
        return instance.user.username

    class Meta:
        model = Comment
        fields = ('id', 'user', 'text', 'timestamp')
        read_only_fields = ('id', 'user', 'timestamp')


class SliderItemSerializer(serializers.ModelSerializer):
    text = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    def get_text(self, instance):
        lang = get_language_from_request(self.context['request'], check_path=True)
        return getattr(instance, 'text_' + lang)

    def get_description(self, instance):
        lang = get_language_from_request(self.context['request'], check_path=True)
        return getattr(instance, 'description_' + lang)

    class Meta:
        model = SliderItem
        fields = ('id', 'order', 'image', 'text', 'url', 'description')


class SliderSerializer(serializers.ModelSerializer):
    items = SliderItemSerializer(read_only=True, many=True)

    class Meta:
        model = Slider
        fields = ('id', 'name', 'items')


class TagSerializer(serializers.ModelSerializer):
    text = serializers.SerializerMethodField()

    def get_text(self, instance):
        lang = get_language_from_request(self.context['request'], check_path=True)
        return getattr(instance, 'text_' + lang)

    class Meta:
        model = Tag
        fields = ('id', 'text')


class CategorySerializer(serializers.ModelSerializer):
    text = serializers.SerializerMethodField()

    def get_text(self, instance):
        lang = get_language_from_request(self.context['request'], check_path=True)
        return getattr(instance, 'text_' + lang)

    class Meta:
        model = Category
        fields = ('id', 'text')


class ServiceSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    def get_title(self, instance):
        lang = get_language_from_request(self.context['request'], check_path=True)
        return getattr(instance, 'title_' + lang)

    def get_description(self, instance):
        lang = get_language_from_request(self.context['request'], check_path=True)
        return getattr(instance, 'description_' + lang)

    class Meta:
        model = Service
        fields = ('id', 'title', 'image', 'description', 'link')


class FeatureSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    def get_title(self, instance):
        lang = get_language_from_request(self.context['request'], check_path=True)
        return getattr(instance, 'title_' + lang)

    def get_description(self, instance):
        lang = get_language_from_request(self.context['request'], check_path=True)
        return getattr(instance, 'description_' + lang)

    class Meta:
        model = Feature
        fields = ('id', 'title', 'icon', 'description')


class CustomerCompaniesSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()

    def get_title(self, instance):
        lang = get_language_from_request(self.context['request'], check_path=True)
        return getattr(instance, 'title_' + lang)

    class Meta:
        model = CustomerCompanies
        fields = ('id', 'title', 'image', 'link')


class CompanyMembersSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    job = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    def get_name(self, instance):
        lang = get_language_from_request(self.context['request'], check_path=True)
        return getattr(instance, 'name_' + lang)

    def get_job(self, instance):
        lang = get_language_from_request(self.context['request'], check_path=True)
        return getattr(instance, 'job_' + lang)

    def get_description(self, instance):
        lang = get_language_from_request(self.context['request'], check_path=True)
        return getattr(instance, 'description_' + lang)

    class Meta:
        model = CompanyMembers
        fields = ('id', 'image', 'job', 'name', 'description', 'email')


class ContactMessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContactMessage
        fields = ('id', 'name', 'text', 'email')


