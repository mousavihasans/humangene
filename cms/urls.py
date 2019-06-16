from django.urls import path

from cms.views import PageList, NewsList, CategoryList, PageDetail, NewsCommentList, PageCommentList

urlpatterns = [
    path('page', PageList.as_view(), name='page_list'),
    path('page/<int:pk>/', PageCommentList.as_view()),
    path('news', NewsList.as_view(), name='news_list'),
    path('news/<int:pk>/', NewsCommentList.as_view()),
    # path('news', NewsList.as_view(), name='news_list'),

    path('category', CategoryList.as_view(), name='category_list'),
]
