from rest_framework import serializers
# from rest_framework.relations import SlugRelatedField

from recipes.models import Recipe, Tag, Ingredient, Favorites, ShoppingList, Follow


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id',
                 'author',
                 'name',
                 'image',
                 'text',
                 'ingredients',
                 'tag',
                 'time',
                 'pub_date',
                 'quantity',
                 'like']
        model = Recipe


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'name', 'measurement_unit']
        model = Ingredient


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'name', 'color', 'slug']
        model = Tag


class ShoppingListSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['recipe', 'author', 'quantity']
        model = ShoppingList


class FavoritesSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['recipe', 'author']
        model = Favorites


class FollowSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Follow
