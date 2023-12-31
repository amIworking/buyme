"""
URL configuration for rest_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions, routers

from apps.shop.views import ShopView, BasketView, ProductsView

v1_router = routers.SimpleRouter()
v1_router.register(r'shops', ShopView, basename='shops')
v1_router.register(r'products', ProductsView, basename='products')
v1_router.register(r'basket', BasketView, basename='basket')


schema_view = get_schema_view(
    openapi.Info(title="Dominos API", default_version="v1", description="Routes of Dominos project"),
    public=False,
    permission_classes=(permissions.AllowAny,),
)

v1_api = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('', include(v1_router.urls)),
    path("swagger(<str:format>.json|.yaml)/", schema_view.without_ui(), name="schema-json"),
    path("swagger/", schema_view.with_ui("swagger"), name="schema-swagger-ui"),
    path("docs/", schema_view.with_ui("redoc"), name="schema-redoc"),
]


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(v1_api)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)