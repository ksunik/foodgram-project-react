from rest_framework import serializers
# from rest_framework.relations import SlugRelatedField

from recipes.models import Recipe, Tag, Ingredient, RecipeIngredient,  Favorites, ShoppingCart, Follow
from users.models import User
from users.serializers import CustomUserSerializer


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'name', 'measurement_unit']
        model = Ingredient


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'name', 'color', 'slug']
        model = Tag


class RcipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(source='ingredient.measurement_unit')

    class Meta:
        fields = ['id', 'name', 'measurement_unit', 'amount']
        model = RecipeIngredient


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(read_only=True, many=True)
    ingredients = RcipeIngredientSerializer(read_only=True, many=True, source='recipeingredient_set')
    author = CustomUserSerializer(read_only=True)

    class Meta:
        fields = ['id',
                  'tags',
                  'author',
                  'ingredients',
                  'is_favorited',
                  'is_in_shopping_cart',
                  'name',
                  'image',
                  'text',
                  'cooking_time',
                  ]
        model = Recipe


class RecipeIngredientCreateSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        source='ingredient',
        queryset=Ingredient.objects.all()
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount')


class RecipeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['tags',
                  'ingredients',
                  'is_favorited',
                  'is_in_shopping_cart',
                  'name',
                  'image',
                  'text',
                  'cooking_time',
                  ]
        model = Recipe

    # def create(self, validated_data):
    #     ingredients = validated_data.pop('ingredients')
    #     instance = super().create(validated_data)

    #     for ingredient_data in ingredients:
    #         RecipeIngredient(
    #             recipe=instance,
    #             ingredient=ingredient_data['ingredient'],
    #             amount=ingredient_data['amount']
    #         ).save()


class ShoppingListSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['recipe', 'author', 'amount']
        model = ShoppingCart


class FavoritesSerializer(serializers.ModelSerializer):
    recipe = serializers.PrimaryKeyRelatedField(
        queryset=Recipe.objects.all()
    )
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )
    class Meta:
        fields = ['recipe', 'author']
        model = Favorites


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault())
    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all())

    class Meta:
        fields = '__all__'
        model = Follow
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'following'),
                message='Вы уже подписаны'
            )
        ]

    def validate_following(self, data_following):
        """Валидация полученных значений при сериализации."""
        if data_following == self.context['request'].user:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя')
        return data_following