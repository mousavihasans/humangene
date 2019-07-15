# from rest_framework.authtoken import views

# urlpatterns += [
#     url(r'^api-token-auth/', views.obtain_auth_token)
# ]

# url(r'^my_profile$', UserProfileViewSet.as_view()),
from django.urls import path

from members.views import RegisterView, LoginView, UserProfileView

urlpatterns = [
    path('register', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('profile', UserProfileView.as_view()),
]