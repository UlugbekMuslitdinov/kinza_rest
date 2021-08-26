from django.shortcuts import render, redirect, get_object_or_404
from .models import Dish, Category, Cart, CartItem, Order, OrderItem
from .forms import CartItemForm
from django.http import Http404

import uuid


def index(request):
    recent_dishes = Dish.objects.order_by('-created_at')[:5]
    categories = Category.objects.all()[:5]
    form = CartItemForm()
    context = {'recent_dishes': recent_dishes, 'form': form, 'categories': categories}
    return render(request, 'index.html', context)


def cart(request):
    Cart.objects.get_or_create(user=request.user, defaults={'id': uuid.uuid4})
    user_cart = Cart.objects.get(user=request.user)
    cart_items = CartItem.objects.filter(cart=user_cart)
    form = CartItemForm()
    context = {'cart': user_cart, 'items': cart_items, 'form': form}
    return render(request, 'cart.html', context)


def dish_detail(request, dish_slug):
    form = CartItemForm()
    dish = get_object_or_404(Dish, slug=dish_slug)
    context = {'dish': dish, 'form': form}
    return render(request, 'dish_detail.html', context)


def category_detail(request, category_slug):
    """Returns all dishes of specific category"""
    category = get_object_or_404(Category, slug=category_slug)
    dish_list = Dish.objects.filter(category=category)
    form = CartItemForm()
    context = {"dishes": dish_list, "form": form}
    return render(request, 'category_detail.html', context)


def add_cart(request, dish_slug):
    dish = Dish.objects.get(slug=dish_slug)
    Cart.objects.get_or_create(user=request.user)
    user_cart = Cart.objects.get(user=request.user)
    form = CartItemForm(data=request.POST)
    if form.is_valid():
        try:
            item = CartItem.objects.filter(cart=user_cart).get(product=dish)
        except CartItem.DoesNotExist:
            new_item = form.save(commit=False)
            new_item.cart = user_cart
            new_item.product = dish
            new_item.save()
        else:
            add = form.save(commit=False)
            item.quantity += add.quantity
            item.save()
    return redirect('restaurant:cart')


def cart_update(request, dish_slug):
    dish = Dish.objects.get(slug=dish_slug)
    user_cart = Cart.objects.get(user=request.user)
    item = CartItem.objects.filter(cart=user_cart).get(product=dish)
    form = CartItemForm(data=request.POST)
    if form.is_valid():
        add_num = form.save(commit=False)
        item.quantity = add_num.quantity
        item.save()
    return redirect('restaurant:cart')


def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if order.user != request.user:
        raise Http404
    context = {'order': order}
    return render(request, 'order_detail.html', context)


def create_order(request):
    user_cart = Cart.objects.get(user=request.user)
    order = Order(user=request.user, delivery_method='DLVR')
    order.save()
    for item in user_cart.cartitem_set.all():
        order_item = OrderItem(order=order, product=item.product, quantity=item.quantity)
        order_item.save()
    user_cart.cartitem_set.all().delete()
    return redirect('restaurant:cart')


def order_list(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'order_list.html', {'orders': orders})