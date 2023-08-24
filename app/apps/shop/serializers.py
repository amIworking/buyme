from rest_framework import serializers

from ..shop.models import Shop, BasketItem




class ShopSerializerBase(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = '__all__'


# доработать чтобы возвращал что-то типо status: магазин "название" удалён
class ShopDeleteSerializer(ShopSerializerBase):
    class Meta:
        model = Shop
        fields = ("name", "url", "owner", "state")


class ShopCreateSerializer(ShopSerializerBase):
    class Meta:
        model = Shop
        fields = '__all__'


# выделение в отдельный сериализатор во избежание показа юзеру владельцев магазинов
class ShopReadSerializer(ShopSerializerBase):
    pass


class BasketSerializerBase(serializers.ModelSerializer):
    class Meta:
        model = BasketItem
        fields = ('user', 'product')
        
        
class BasketCreate(BasketSerializerBase):
    class Meta:
        model = BasketItem
        fields = ('user', 'product')
        
        
class BasketRemove(BasketSerializerBase):
    class Meta:
        model = BasketItem
        fields = ('user', 'product')