# Create your views here.
from rest_framework import generics

from .serializers import ShopReadSerializer, ShopSerializerBase, ShopDeleteSerializer, ShopCreateSerializer
from ..shop.models import Shop


# прочитать(get запрос) shop по pk, patch, put и delete запросы к shop
class ShopApiDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Shop.objects.all()

    # чтобы не показывать обычному пользователю владельца магаза надо узнать какой именно запрос он посылает
    def get_serializer_class(self):
        if self.request.method == "GET":
            return ShopReadSerializer
        elif self.request.method == "DELETE":
            return ShopDeleteSerializer
        return ShopSerializerBase


# get запрос на список всех магазинов, post запрос на создание магазина
class ShopApiList(generics.ListCreateAPIView):
    queryset = Shop.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ShopSerializerBase
        return ShopCreateSerializer


