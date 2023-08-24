# Create your views here.
from rest_framework import generics, viewsets
from rest_framework.decorators import action
from rest_framework.views import APIView

from .serializers import ShopReadSerializer, ShopSerializerBase, ShopDeleteSerializer, ShopCreateSerializer, BasketSerializerBase
from ..shop.models import Shop, BasketItem, Basket, Product, ProductInfo
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
        basket_items = BasketItem.objects.filter(user=user)
        return basket_items
        


class BasketViewSet(viewsets.ModelViewSet):
    queryset = ProductInfo.objects.all()
    serializer_class = BasketSerializerBase
    
    @action(methods='post', detail=False)
    def add_basket_item(self, request, pk):
        user = request.user
        basket = Basket.objects.get_or_create(user=user)[0]
        if not ProductInfo.objects.filter(pk=pk).exists:
            error_message = "This product's item doesn't exist"
            # Придумать ответ на отсутсвие товара в бд
            print(error_message)
            pass
        elif ProductInfo.objects.get(pk=pk).quantity == 0:
            error_message = "Unfortunately, we're out of this product"
             # Придумать ответ на отсутсвие товара в магазине
            print(error_message)
            pass
        product = ProductInfo.objects.get(pk=pk)
        basket_item = BasketItem.objects.get_or_create(product=product, user=user)[0]
        if Basket.objects.filter(basket_items=basket_item, user=user).exists():
            self.update_basket_item(request, pk)       
        else:
            basket.basket_items.add(basket_item)
            basket.calculate_final_price()
            basket.save()
        print(basket.final_price)
        
    @action(methods='post', detail=False)               
    def update_basket_item(self, request, pk):
        user = request.user
        basket = Basket.objects.get_or_create(user=user)[0]
        if BasketItem.objects.filter(
            product__pk=pk, user=user):
            basket_item = BasketItem.objects.get(
            product__pk=pk, user=user)
            basket_item.quantity += 1
            basket_item.save()
            basket.calculate_final_price()
            basket.save()
        else:
            self.create_basket_item(request, pk)
        print(basket.final_price)
            
    @action(methods='post', detail=False)
    def delete_basket_item(self, request, pk):
        user = request.user
        basket = Basket.objects.get_or_create(user=user)[0]
        if not BasketItem.objects.filter(product__pk=pk, user=user).exists():
            error_message = "You have deleted all particular items"
            print(error_message)
            pass
            #Придумать ответ на отсутствие корзины
        else:
            basket_item = BasketItem.objects.get(product__pk=pk, user=user)
            if basket_item.quantity <= 1:
                basket_item.delete()
            else:
                basket_item.quantity -= 1
                basket_item.save()
            basket.calculate_final_price()
            basket.save()
        print(basket.final_price)
        
