from django.contrib import admin

# Register your models here.
from ..shop.models import Shop, Category, Product, ProductInfo, Contact, Order, OrderItem, ShoppingCart


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ['name', 'url', 'owner', 'state']
    list_filter = ['owner']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_category']
    list_filter = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
    list_filter = ['name', 'category']


@admin.register(ProductInfo)
class ProductInfoAdmin(admin.ModelAdmin):
    list_display = ['name', 'model', 'product', 'shop', 'quantity', 'price', 'price_rrc', 'parameters']
    list_filter = ['product', 'shop']


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['user', 'city', 'street', 'house', 'structure', 'building', 'apartment', 'phone']
    list_filter = ['city']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'state', 'contact']
    list_filter = ['user', 'date', 'state', 'contact']


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product_info', 'quantity']
    list_filter = ['order']
    
@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'user_address']
    list_filter = ['product']