from django.urls import path

from cms.views import PageList, NewsList, CategoryList, PageDetail, NewsCommentList, PageCommentList, NewsDetail

urlpatterns = [
    path('page', PageList.as_view(), name='page_list'),
    path('page/<int:pk>/', PageDetail.as_view(), name='page_detail'),
    path('page/<int:pk>/comment', PageCommentList.as_view(), name='page_comment_list'),
    path('news', NewsList.as_view(), name='news_list'),
    path('news/<int:pk>/comment', NewsDetail.as_view(), name='news_detail'),
    path('news/<int:pk>/comment', NewsCommentList.as_view(), name='news_comment_list'),
    # path('news', NewsList.as_view(), name='news_list'),

    path('category', CategoryList.as_view(), name='category_list'),
]
