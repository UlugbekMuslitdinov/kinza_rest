from django.urls import path
from .views import (index, cart, dish_detail, add_cart, category_detail,
                    cart_update, order_detail, create_order, order_list)

app_name = 'restaurant'

urlpatterns = [
    path('', index, name='index'),
    path('cart/', cart, name='cart'),
    path('order/create/', create_order, name='create_order'),
    path('order/list/', order_list, name='order_list'),
    path('<str:dish_slug>/', dish_detail, name='dish_detail'),
    path('<str:dish_slug>/add_cart/', add_cart, name='cart_add'),
    path('category/<str:category_slug>/', category_detail, name='category_detail'),
    path('<str:dish_slug>/update/', cart_update, name='cart_update'),
    path('order/<str:order_id>/', order_detail, name='order_detail'),
    ]