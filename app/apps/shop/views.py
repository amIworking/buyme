# Create your views here.
from rest_framework import mixins, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.shop.serializers import (
    ShopSerializerBase, ShopCreateSerializer, ShopReadSerializer, ShopDeleteSerializer,
    BasketSerializerBase, ChangeItemSerializer, DeleteBasketItem,
    ProductSerializer, OrderSerializerBase, ChangeOrderSerializer,
    ContactSerializer
)

from apps.shop.models import Shop, Basket, ProductInfo, Order, OrderItem, Contact


class ShopView(mixins.ListModelMixin,
               mixins.RetrieveModelMixin,
               mixins.CreateModelMixin,
               mixins.DestroyModelMixin,
               viewsets.GenericViewSet):
    queryset = Shop.objects.all()

    serializers = {
        'list': ShopSerializerBase,
        'retrieve': ShopReadSerializer,
        'create': ShopCreateSerializer,
        'destroy': ShopDeleteSerializer,  # вы действительно хотите давать удалять магазины?)
    }
    permission_classes_map = {
        'list': (permissions.AllowAny,),
        'retrieve': (permissions.AllowAny,),
        'create': (permissions.IsAdminUser,),
        'destroy': (permissions.IsAdminUser,),
    }

    def get_serializer_class(self):
        return self.serializers.get(self.action)

    def get_permissions(self):
        return [permission() for permission in self.permission_classes_map.get(self.action)]


class ProductsView(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = ProductInfo.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (permissions.AllowAny,)


class BasketView(viewsets.ViewSet):

    queryset = Basket.objects.all()
    serializer_class = BasketSerializerBase
    permission_classes = (permissions.AllowAny,)

    def list(self, request, *args, **kwargs):
        """Корзина"""
        basket, is_created = Basket.objects.get_or_create(user=request.user)
        return Response(BasketSerializerBase(instance=basket).data)

    @action(methods=['post'], detail=False, serializer_class=ChangeItemSerializer)
    def add_basket_item(self, request):
        """Добавить продукт в корзину"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        basket = serializer.save()
        return Response(BasketSerializerBase(instance=basket).data)
        
    @action(methods=['post'], detail=False, serializer_class=ChangeItemSerializer)
    def update_basket_item(self, request):
        """Изменить количество продкута"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        basket = serializer.save()
        return Response(BasketSerializerBase(instance=basket).data)

    @action(methods=['post'], detail=False, serializer_class=DeleteBasketItem)
    def delete_basket_item(self, request):
        """Удалить продукт в корзине"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        basket = serializer.save()
        return Response(BasketSerializerBase(instance=basket).data)

    def get_serializer(self, *args, serializer_class=None, request=None, **kwargs):
        """
        Return instance of serializer with a request in context.
        """
        serializer_class = serializer_class or self.serializer_class
        if "context" not in kwargs:
            request = request or getattr(self, "request", None)
            assert request, "self.request is not set and is not passed in kwargs"
            kwargs["context"] = {"request": request}
        return serializer_class(**kwargs)

class ContactView(viewsets.ViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = (permissions.AllowAny,)

class OrderView(viewsets.ViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializerBase
    permission_classes = (permissions.AllowAny,)

    def list(self, request, *args, **kwargs):
        if Order.objects.filter(user=request.user).exists():
            orders = Order.objects.filter(user=request.user)
            return Response(OrderSerializerBase(instance=orders, many=True).data)
        else:
            return Response({"message":"You have no orders"})

    @action(methods=['post'], detail=False, serializer_class=ChangeOrderSerializer)
    def create_order(self, request, *args, **kwargs):
        serializer = ChangeOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        return Response(BasketSerializerBase(instance=order).data)
