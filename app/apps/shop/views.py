# Create your views here.
from rest_framework import generics
from rest_framework.views import APIView

from .serializers import ShopReadSerializer, ShopSerializerBase, ShopDeleteSerializer, ShopCreateSerializer, BasketSerializerBase
from ..shop.models import Shop, Basket, Product
from ..users.models import User


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

class BasketShowApi(APIView):
    
    def get_queryset(self):
        user = self.request.user
        basket_items = Basket.objects.filter(user=user)
        return basket_items
        


class BasketAddApi(generics.CreateAPIView):
    
    def get_serializer(self, *args, **kwargs):
       kwargs['context'] = self.get_serializer_context
       
       if 'product_id' in self.kwargs:
           product_id = self.kwargs['product_id']
           user = self.request.user
           print(Basket.objects.filter(
               product__id=product_id, 
               user=user))
           if Basket.objects.filter(
               product__id=product_id, 
               user=user):
               basket = Basket.objects.get(
               product__id=product_id, user=user)
               basket.quantity += 1
               basket.save()
           else:
               if not Product.objects.filter(id=product_id).exists:
                # Придумать ответ на отсутсвие товара
                   pass
               else:
                   product = Product.objects.get(id=product_id)
                   basket = Basket.objects.create(
                   product=product, 
                   user=user)
                   basket.save()
            
