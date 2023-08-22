from django.urls import path

from apps.users.views import UserRegisterApi

urlpatterns = [
    path('register', UserRegisterApi.as_view()),
]