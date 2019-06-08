from rest_framework import serializers

from cms.models import Page, News, Slider, Tag, Category


class PageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Page
        fields = ('id', 'title_fa', 'title_en', 'text_fa', 'text_en', 'image', 'category')


class NewsSerializer(serializers.ModelSerializer):

    class Meta:
        model = News
        fields = ('id', 'title_fa', 'title_en', 'text_fa', 'text_en', 'image')


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


