# Create your views here.
from django.forms import model_to_dict
from rest_framework import generics, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *

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
    queryset = BasketItem.objects.all()
    serializer_class = BasketSerializerBase
    
    @action(methods='get', detail=True)
    def show_basket(self, request):
        user = request.user
        basket = Basket.objects.get_or_create(user=user)[0]
        basket_sr = BasketSerializerBase(basket).data
        basket_items_sr = BasketItemSerializerBase(basket.basket_items.all(), many=True).data
        products = {item.product for item in basket.basket_items.all()}
        products_sr = ProductInfoSerializerBase(products, many=True).data
        print('show ----')
        return Response({'basket': basket_sr.data.data,
                         'basket_items':basket_items_sr.data,
                        'products': products_sr.data})
    
    @action(methods='post', detail=False)
    def add_basket_item(self, request, pk):
        user = request.user
        basket = Basket.objects.get_or_create(user=user)[0]
        if not ProductInfo.objects.filter(pk=pk).exists:
            error_message = "This product's item doesn't exist"
            # Придумать ответ на отсутсвие товара в бд
            raise ValueError(error_message)
        elif ProductInfo.objects.get(pk=pk).quantity == 0:
            error_message = "Unfortunately, we're out of this product"
             # Придумать ответ на отсутсвие товара в магазине
            raise ValueError(error_message)
        product = ProductInfo.objects.get(pk=pk)
        basket_item, is_basket_item_new = BasketItem.objects.get_or_create(product=product, user=user)
        if not is_basket_item_new:
            return self.update_basket_item(request, pk)      
        else:
            basket_item.recalculate_price()
            basket.basket_items.add(basket_item)
            basket.calculate_final_price()
            basket_sr = BasketSerializerBase(basket)
            basket_items_sr = BasketItemSerializerBase(basket.basket_items.all(), many=True)
            products = {item.product for item in basket.basket_items.all()}
            products_sr = ProductInfoSerializerBase(products, many=True)
            print('add ----')
            return Response({'basket': basket_sr.data.data,
                         'basket_items':basket_items_sr.data,
                        'products': products_sr.data})
        
    @action(methods='put', detail=False)               
    def update_basket_item(self, request, pk):
        user = request.user
        basket = Basket.objects.get_or_create(user=user)[0]
        if not ProductInfo.objects.filter(pk=pk).exists:
            error_message = "This product's item doesn't exist"
            # Придумать ответ на отсутсвие товара в бд
            raise ValueError(error_message)
        elif ProductInfo.objects.get(pk=pk).quantity == 0:
            error_message = "Unfortunately, we're out of this product"
             # Придумать ответ на отсутсвие товара в магазине
            raise ValueError(error_message)
        product = ProductInfo.objects.get(pk=pk)
        basket_item, is_basket_item_new = BasketItem.objects.get_or_create(product=product, user=user)
        if not is_basket_item_new:
            return self.add_basket_item(request, pk)
        basket_item.increase_quantity_and_price()
        basket.calculate_final_price()
        basket_sr = BasketSerializerBase(basket)
        basket_items_sr = BasketItemSerializerBase(basket.basket_items.all(), many=True)
        products = {item.product for item in basket.basket_items.all()}
        products_sr = ProductInfoSerializerBase(products, many=True)
        print('update ----')
        return Response({'basket': basket_sr.data,
                         'basket_items':basket_items_sr.data,
                        'products': products_sr.data})

            
    @action(methods='delete', detail=False)
    def delete_basket_item(self, request, pk):
        user = request.user
        basket = Basket.objects.get_or_create(user=user)[0]
        if not BasketItem.objects.filter(product__pk=pk, user=user).exists():
            error_message = "You have deleted all particular items"
            raise ValueError(error_message)
            #Придумать ответ на отсутствие товара в корзине
        else:
            basket_item = BasketItem.objects.get(product__pk=pk, user=user)
            basket_item.decrease_quantity_and_price()
            basket.calculate_final_price()
            basket_sr = BasketSerializerBase(basket)
            basket_items_sr = BasketItemSerializerBase(basket.basket_items.all(), many=True)
            products = {item.product for item in basket.basket_items.all()}
            products_sr = ProductInfoSerializerBase(products, many=True)
            print('delete ----')
            return Response({'basket': basket_sr.data.data,
                         'basket_items':basket_items_sr.data,
                        'products': products_sr.data})

        
