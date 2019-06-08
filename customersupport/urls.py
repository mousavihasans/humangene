from django.urls import path

from cms.views import PageList, NewsList, CategoryList
from customersupport.views import TaskList

urlpatterns = [
    path('', TaskList.as_view(), name='page_list'),
]
