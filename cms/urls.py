from django.urls import path

from cms.views import PageList, NewsList, CategoryList

urlpatterns = [
    path('page', PageList.as_view(), name='page_list'),
    path('news', NewsList.as_view(), name='news_list'),
    path('category', CategoryList.as_view(), name='category_list'),
]