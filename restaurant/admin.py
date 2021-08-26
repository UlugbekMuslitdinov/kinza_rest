from django.contrib import admin
from .models import Dish, Cart, CartItem, Category, Order, OrderItem


class DishAdmin(admin.ModelAdmin):
    model = Dish
    list_display = ['name', 'price']
    prepopulated_fields = {'slug': ('name',)}


class CartItemInline(admin.TabularInline):
    model = CartItem


class CartAdmin(admin.ModelAdmin):
    model = Cart
    inlines = [CartItemInline, ]


class CategoryAdmin(admin.ModelAdmin):
    model = Category
    prepopulated_fields = {'slug': ('name',)}


class OrderItemInline(admin.StackedInline):
    model = OrderItem


class OrderAdmin(admin.ModelAdmin):
    model = Order
    list_display = ['id', 'user', 'created_at', 'delivery_method', 'payment_method']
    inlines = [OrderItemInline, ]


admin.site.register(Dish, DishAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Order, OrderAdmin)