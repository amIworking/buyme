# Create your views here.
from rest_framework import generics, viewsets
from rest_framework.decorators import action
from rest_framework.views import APIView

from .serializers import ShopReadSerializer, ShopSerializerBase, ShopDeleteSerializer, ShopCreateSerializer, BasketSerializerBase
from ..shop.models import Shop, Basket, Product, ProductInfo
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
        


class BasketViewSet(viewsets.ModelViewSet):
    queryset = ProductInfo.objects.all()
    serializer_class = BasketSerializerBase
    
    @action(methods='post', detail=False)
    def create_basket(self, request, pk):
        user = request.user
        if not ProductInfo.objects.filter(pk=pk).exists:
            error_message = "This product's item doesn't exist"
         # Придумать ответ на отсутсвие товара в бд
            pass
        elif ProductInfo.objects.get(pk=pk).quantity == 0:
            error_message = "Unfortunately, we're out of this product"
             # Придумать ответ на отсутсвие товара в магазине
            pass
        elif Basket.objects.filter(product__pk=pk, user=user).exists():
            self.update(request, pk)       
        else:
            product = ProductInfo.objects.get(pk=pk)
            basket = Basket.objects.create(
            product=product, 
            user=user, quantity=1)
            basket.recalculate_final_price()
            basket.save()
                   
    def update(self, request, pk):
        user = request.user
        print(Basket.objects.filter(
            product__pk=pk, 
            user=user))
        if Basket.objects.filter(
            product__pk=pk, 
            user=user):
            basket = Basket.objects.get(
            product__pk=pk, user=user)
            basket.quantity += 1
            basket.recalculate_final_price()
            basket.save()
            
    @action(methods='post', detail=False)
    def delete_basket_item(self, request, pk):
        user = request.user
        if not Basket.objects.filter(product__pk=pk, user=user).exists():
            error_message = "You have deleted all particular items"
            pass
            #Придумать ответ на отсутствие корзины
        else:
            basket = Basket.objects.get(product__pk=pk, user=user)
            if basket.quantity <= 1:
                basket.delete()
            else:
                basket.quantity -= 1
                basket.recalculate_final_price()
                basket.save()
        
