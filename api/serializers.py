from rest_framework import serializers
from restaurant.models import Dish, Category


class DishSerializer(serializers.ModelSerializer):

    class Meta:
        model = Dish
        fields = ('id', 'name', 'category', 'slug', 'description', 'image', 'price', 'created_at',)


class CategorySerializer(serializers.ModelSerializer):
    dishes = DishSerializer(many=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'slug', 'dishes')