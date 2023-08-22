from rest_framework import serializers

from ..shop.models import Shop, ShoppingCart


class ShopSerializerBase(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ("name", "url", "state")


# доработать чтобы возвращал что-то типо status: магазин "название" удалён
class ShopDeleteSerializer(ShopSerializerBase):
    class Meta:
        model = Shop
        fields = ("name", "url", "owner", "state")


class ShopCreateSerializer(ShopSerializerBase):
    class Meta:
        model = Shop
        fields = ("name", "url", "owner", "state")


# выделение в отдельный сериализатор во избежание показа юзеру владельцев магазинов
class ShopReadSerializer(ShopSerializerBase):
    pass


class ShoppingCartSerializerBase():
    class Meta:
        model = ShoppingCart
        fields = ('user', 'product', 'user_address')
        
        
class ShoppingCartAdd(ShoppingCartSerializerBase):
    class Meta:
        model = ShoppingCart
        fields = ('user', 'product', 'user_address')
        
        
class ShoppingCartRemove(ShoppingCartSerializerBase):
    class Meta:
        model = ShoppingCart
        fields = ('user', 'product', 'user_address')