from django.db import models
import uuid
from django.conf import settings
from django.shortcuts import reverse
User = settings.AUTH_USER_MODEL


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, null=True)

    def __str__(self):
        return self.name


class Dish(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, related_name='dishes')
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150)
    description = models.TextField()
    image = models.ImageField(upload_to='dishes/')
    price = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'dishes'

    def __str__(self):
        return self.name[:50]

    def get_absolute_url(self):
        return reverse('restaurant:dish_detail', args=[self.slug])


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    def items_number(self):
        return self.cartitem_set.count()

    def total_price(self):
        return sum([i.product.price * i.quantity for i in self.cartitem_set.all()])


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Dish, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product.name} in {self.cart}"


class Order(models.Model):
    DELIVERY_METHODS = [('DLVR', 'Доставка'), ('SLFD', 'Самовызов')]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(default='cash', max_length=50)
    delivery_method = models.CharField(choices=DELIVERY_METHODS, max_length=50)

    def __str__(self):
        return self.user.username

    def get_total_price(self):
        return sum([item.product.price * item.quantity for item in self.orderitem_set.all()])

    def get_absolute_url(self):
        return reverse('restaurant:order_detail', args=[self.id])


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Dish, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.product.name