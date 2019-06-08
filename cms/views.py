from django.utils.timezone import now
from rest_framework import mixins, generics
from rest_framework.permissions import IsAuthenticated

from cms.models import Page, News, Category
from cms.serializers import PageSerializer, NewsSerializer, CategorySerializer


class PageList(generics.ListCreateAPIView):
    serializer_class = PageSerializer

    def get_queryset(self):
        return Page.objects.filter(published_date__lte=now())


class NewsList(generics.ListCreateAPIView):
    serializer_class = NewsSerializer

    def get_queryset(self):
        return News.objects.filter(published_date__lte=now())


class CategoryList(generics.ListCreateAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        return Category.objects.all()

