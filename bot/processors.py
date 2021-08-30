from users.models import CustomUser
from restaurant.models import Dish, Category, Cart, CartItem


def tg_add_cart(m, dish, quantity):
    user = CustomUser.objects.get(telegram_id=m.chat.id)
    Cart.objects.get_or_create(user=user)
    user_cart = Cart.objects.get(user=user)
    try:
        item = CartItem.objects.get(product=dish)
    except CartItem.DoesNotExist:
        CartItem.objects.create(cart=user_cart, product=dish, quantity=quantity)
    else:
        item.quantity += quantity