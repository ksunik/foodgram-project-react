from rest_framework import serializers
# from rest_framework.relations import SlugRelatedField
from djoser.serializers import UserCreateSerializer, UserSerializer
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from rest_framework.validators import UniqueTogetherValidator
# from drf_extra_fields.fields import Base64ImageField
import base64
from django.core.files.base import ContentFile

from recipes.models import Recipe, Tag, Ingredient, RecipeIngredient, Favorites, ShoppingCart, Follow
from users.models import User


class CustomUserSerializer(UserCreateSerializer):
    # is_subscribed = FollowSerializer(many=True)

    class Meta:
        model = User
        fields = ['email', 'id', 'username', 'first_name', 'last_name', 'password']


class ShowUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name', 'is_subscribed')

    def get_is_subscribed(self, obj):
        if (self.context.get('request')
            and not self.context['request'].user.is_anonymous):
            return Follow.objects.filter(following=self.context['request'].user, user=obj).exists()
        return False


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

    def validate_amount(self, value):
        if value <= 0:
            raise ValidationError(
                'Ингредиенты должны обязательно присутствовать'
            )
        return value


class RecipeShortSerializer(CustomUserSerializer):
    class Meta:
        model = Recipe
        fields = ['id',
                  'name',
                  'image',
                  'cooking_time'
                 ]


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(read_only=True, many=True)
    ingredients = RcipeIngredientSerializer(read_only=True, many=True, source='recipeingredients')
    author = CustomUserSerializer(read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    # image = Base64ImageField(required=False)
    image = serializers.CharField(max_length=None, allow_blank=True)

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

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        return (request and request.user.is_authenticated
                and Favorites.objects.filter(
                    author=request.user, recipe=obj
                ).exists())
    
    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        return (request and request.user.is_authenticated
                and ShoppingCart.objects.filter(author=request.user, recipe=obj).exists())
    
    # def to_internal_value(self, data):
    #     if 'image' in data:
    #         image_data = data.pop('image')
    #         image_file = self.decode_image(image_data)
    #         data['image'] = image_file
    #     return super().to_internal_value(data)

    # def decode_image(self, image_data):
    #     try:
    #         decoded_image = base64.b64decode(image_data)
    #     except TypeError:
    #         raise serializers.ValidationError("Invalid image data")

    #     # Генерируем имя файла
    #     filename = 'recipe_image.png'  # или другое имя файла, если нужно
    #     # Создаем объект файла для сохранения
    #     image_file = ContentFile(decoded_image, name=filename)
    #     return image_file
    
    # def to_internal_value(self, data):
    #     if isinstance(data, str) and data.startswith('data:image'):
    #         format, imgstr = data.split(';base64,')
    #         ext = format.split('/')[-1]
    #         data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

    #     return super().to_internal_value(data)


class RecipeIngredientCreateSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        source='ingredient',
        queryset=Ingredient.objects.all()
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount')


class RecipeCreateSerializer(serializers.ModelSerializer):
    ingredients = RecipeIngredientCreateSerializer(many=True, source='recipeingredients')
    tags = serializers.PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all())
    # tags = TagSerializer(many=True)
    # image = Base64ImageField()
    # author = ShowUserSerializer(read_only=True)
    # is_favorited = serializers.SerializerMethodField()
    # is_in_shopping_cart = serializers.SerializerMethodField()
    # image = Base64ImageField(required=False)
    
    class Meta:
        fields = ['ingredients',
                  'tags',
                  'image',
                  'name',
                  'text',
                  'cooking_time'
                  ]
        model = Recipe

    def create(self, validated_data):
        ingredients = validated_data.pop("recipeingredients")
        instance = super().create(validated_data)
        for ingredient_data in ingredients:
            print('recipeeeeeeeeee')
            RecipeIngredient.objects.create(
                ingredient=ingredient_data['ingredient'], recipe=instance, amount=ingredient_data['amount']
            )
            return instance

    def update(self, instance, validated_data):
        instance.image = validated_data.get('image', instance.image)
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get('cooking_time', instance.cooking_time)
        tags = validated_data.pop('tags')
        instance.tags.set(tags)
        ingredients = validated_data.pop('recipeingredients')
    
        instance.ingredients.clear()
        for ingredient_data in ingredients:
            RecipeIngredient.objects.create(
                ingredient=ingredient_data['ingredient'], recipe=instance, amount=ingredient_data['amount']
            )
        return instance
    
    def to_representation(self, instance):
        return RecipeSerializer(instance).data
        

class ShoppingListSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['recipe', 'author']
        model = ShoppingCart
        validators = [
            UniqueTogetherValidator(
                queryset=ShoppingCart.objects.all(),
                fields=('user', 'recipe'),
                message='Рецепт уже добавлен в список покупок'
            )
        ]

    def to_representation(self, instance):
        request = self.context.get('request')
        return RecipeShortSerializer(
            instance.recipe,
            context={'request': request}
        ).data


class FavoritesSerializer(serializers.ModelSerializer):
    recipe = serializers.PrimaryKeyRelatedField(
        queryset=Recipe.objects.all()
    )
    author = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )

    class Meta:
        fields = ['recipe', 'author']
        model = Favorites

    def to_representation(self, instance):
        request = self.context.get('request')
        return RecipeSerializer(
            instance.recipe,
            context={'request': request}
        ).data

class ShowFollowSerializer(serializers.ModelSerializer):
    """"Сериализатор для предоставления информации
    о подписках пользователя.
    """
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField("get_recipes_count")

    class Meta:
        model = User
        fields = ['email',
                  'id',
                  'username',
                  'first_name',
                  'last_name',
                  'is_subscribed',
                  'recipes',
                  'recipes_count'
        ]
        read_only_fields = ['email',
                            'username',
                            'first_name',
                            'last_name',
                            'is_subscribed',
                            'recipes',
                            'recipes_count'
        ]

    def get_is_subscribed(self, obj):
        request = self.context.get("request")
        if request is None or request.user.is_anonymous:
            return False
        return Follow.objects.filter(user=request.user, following=obj).exists()

    def get_recipes(self, obj):
        request = self.context.get('request')
        recipes = obj.recipe_author.all()
        return RecipeShortSerializer(recipes, many=True, context={'request': request}).data
    
    def get_recipes_count(self, obj):
        return obj.recipe_author.count()
        

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

    def to_representation(self, instance):
        request = self.context.get('request')
        return ShowFollowSerializer(
            instance.author, context={'request': request}
        ).data


class ShoppingCartSerializer(serializers.ModelSerializer):
    """Сериализатор для работы со списком покупок."""
    class Meta:
        model = ShoppingCart
        fields = ['recipe', 'author']
        validators = [UniqueTogetherValidator(queryset=ShoppingCart.objects.all(),
                                              fields=('author', 'recipe'),
                                              message='Рецепт уже в списоке покупок')
        ]

    def to_representation(self, instance):
        request = self.context.get('request')
        return RecipeShortSerializer(
            instance.recipe,
            context={'request': request}
        ).data