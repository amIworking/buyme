from django.db import models
# from ..users.models import User
from apps.users.models import User

STATE_CHOICES = (
    ('basket', 'Статус корзины'),
    ('new', 'Новый'),
    ('confirmed', 'Подтвержден'),
    ('assembled', 'Собран'),
    ('sent', 'Отправлен'),
    ('delivered', 'Доставлен'),
    ('canceled', 'Отменен')
)


class Shop(models.Model):
    name = models.CharField(max_length=30, verbose_name='Название')
    url = models.URLField(verbose_name='Ссылка', blank=True, help_text='<i>Введите URL сайта<\i>')
    owner = models.OneToOneField(User, verbose_name='Владелец', on_delete=models.CASCADE, blank=True)
    state = models.BooleanField(verbose_name='Статус получения заказа', blank=True, default=True)

    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = 'Список магазинов'
        ordering = ('-name', )

    def __str__(self):
        return f'{self.name} | {self.url} |{self.owner} | {self.state}'


class Category(models.Model):
    name = models.CharField(max_length=30, verbose_name='Название')
    shops = models.ManyToManyField(Shop, verbose_name='Магазины', related_name='categories', blank=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Список категорий'
        ordering = ('-name', )

    def __str__(self):
        return f'{self.name}'


class Product(models.Model):
    name = models.CharField(max_length=30, verbose_name='Название')
    category = models.ForeignKey(Category, verbose_name='Категория', related_name='products', blank=True,
                                 on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Список продуктов'
        ordering = ('-name', )

    def __str__(self):
        return f'{self.name} | {self.category}'


class ProductInfo(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')
    model = models.CharField(max_length=80, verbose_name='Модель', blank=True)
    product = models.ForeignKey(Product, verbose_name='Продукт', related_name='product_infos', blank=True,
                                on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, verbose_name='Магазин', related_name='product_infos', blank=True,
                             on_delete=models.CASCADE)
    quantity = models.IntegerField(verbose_name='Количество')
    price = models.FloatField(verbose_name='Цена')
    price_rrc = models.FloatField(verbose_name='Рекомендуемая розничная цена')
    parameters = models.JSONField(verbose_name='Параметры')

    class Meta:
        verbose_name = 'Информация о продукте'
        verbose_name_plural = 'Информационный список о продуктах'
        constraints = [
            models.UniqueConstraint(fields=['product', 'shop'], name='unique_product_info'),
        ]
        ordering = ('-name', )

    def __str__(self):
        return f'{self.name} | {self.model} | {self.product} | {self.shop} | {self.quantity} | {self.price} | {self.price_rrc} | {self.parameters}'


# не уверен на счёт логики создания отдельной модели для параметров товара

# class Parameter:
#     name = models.CharField(max_length=30, verbose_name='Название')
class Contact(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', related_name='contacts', on_delete=models.CASCADE)
    city = models.CharField(max_length=50, verbose_name='Город')
    street = models.CharField(max_length=100, verbose_name='Улица')
    house = models.CharField(max_length=15, verbose_name='Дом', blank=True)
    structure = models.CharField(max_length=15, verbose_name='Корпус', blank=True)
    building = models.CharField(max_length=15, verbose_name='Строение', blank=True)
    apartment = models.CharField(max_length=15, verbose_name='Квартира', blank=True)
    phone = models.CharField(max_length=20, verbose_name='Телефон')

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Список контактов'

    def __str__(self):
        return f'{self.user} {self.city} {self.street} {self.house}'


class Order(models.Model):
    user = models.ForeignKey(User, verbose_name='Покупатель', related_name='orders', on_delete=models.CASCADE)
    date = models.DateTimeField(verbose_name='Дата заказа', auto_now=True)
    state = models.CharField(max_length=20, verbose_name='Статус', choices=STATE_CHOICES)
    contact = models.ForeignKey(Contact, verbose_name='Контакт', related_name='orders', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Список заказов'
        ordering = ('-date', )

    def __str__(self):
        return f'{str(self.date)} | {self.user} | {self.state} | {self.contact}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, verbose_name='Заказ', related_name='order_items', on_delete=models.CASCADE)
    product_info = models.ForeignKey(ProductInfo, verbose_name='Информация о продукте', related_name='ordered_items',
                                     on_delete=models.CASCADE)
    quantity = models.IntegerField(verbose_name='Количество')

    class Meta:
        verbose_name = 'Заказанный товар'
        verbose_name_plural = 'Список заказанных товаров'
        constraints = [
            models.UniqueConstraint(fields=['order_id', 'product_info'], name='unique_order_item')
        ]

    def __str__(self):
        return f'{self.order} | {self.quantity}'