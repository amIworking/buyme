from rest_framework import serializers

from apps.shop.models import Shop, BasketItem, Basket, ProductInfo


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


class ProductInfoSerializerBase(serializers.ModelSerializer):
    class Meta:
        model = ProductInfo
        fields = ('name', 'product', 'price')


class BasketItemSerializerBase(serializers.ModelSerializer):
    product = ProductInfoSerializerBase()

    class Meta:
        model = BasketItem
        fields = ('product', 'quantity')


class BasketSerializerBase(serializers.ModelSerializer):
    items = BasketItemSerializerBase(many=True, source='cart_product')

    class Meta:
        model = Basket
        fields = ('user', 'items', 'final_price')


class ChangeItemSerializer(serializers.Serializer):
    product = serializers.IntegerField(help_text='id продукта')
    quantity = serializers.IntegerField(min_value=1, help_text='количество продукта в корзине')

    def __init__(self, *args, **kwargs):
        self._product = None
        super().__init__(*args, **kwargs)

    def validate_product(self, value):
        self._product = ProductInfo.objects.filter(pk=value).first()
        if not self._product:
            error_message = "This product's item doesn't exist"
            raise serializers.ValidationError(error_message)
        return value

    def validate(self, attrs):
        if self._product.quantity < attrs['quantity']:
            error_message = "Unfortunately, we're do not have such amount of product"
            raise serializers.ValidationError(error_message)
        return attrs

    def save(self, **kwargs):
        request = self.context['request']
        quantity = self.validated_data["quantity"]
        item = (
            BasketItem.objects
            .filter(basket__user=request.user, product=self._product)
            .select_related('basket')
            .first()
        )
        if item:
            basket = item.basket
            item.set_quantity(quantity)
        else:
            basket, is_created = Basket.objects.get_or_create(user=request.user)
            BasketItem.objects.create(product=self._product, basket=basket, quantity=quantity)
        basket.calculate_final_price()
        return basket


class DeleteBasketItem(ChangeItemSerializer):
    quantity = None

    def validate(self, attrs):
        attrs['quantity'] = 0
        attrs = super().validate(attrs)
        return attrs


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductInfo
        fields = ('id', 'name', 'price', 'quantity', )