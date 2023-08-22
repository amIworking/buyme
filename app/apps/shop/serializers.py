from rest_framework import serializers

from ..shop.models import Shop, Basket


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


class BasketSerializerBase():
    class Meta:
        model = Basket
        fields = ('user', 'product')
        
        
class BasketAdd(BasketSerializerBase):
    class Meta:
        model = Basket
        fields = ('user', 'product')
        
        
class BasketRemove(BasketSerializerBase):
    class Meta:
        model = Basket
        fields = ('user', 'product')