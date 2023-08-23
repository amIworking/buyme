from django.urls import path

from ..users.views import UserRegisterViewSet

urlpatterns = [
    path('register', UserRegisterViewSet.as_view({'post': 'register'})),
]