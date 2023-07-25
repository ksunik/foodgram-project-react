from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from rest_framework.authtoken.models import Token

from . import models
from recipes.models import Recipe
# from api.serializers import FollowSerializer


User = get_user_model()


class CustomUserSerializer(serializers.ModelSerializer):
    # is_subscribed = FollowSerializer(many=True)

    class Meta:
        model = User
        fields = ['email', 'id', 'username', 'first_name', 'last_name']


class PasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True)
    current_password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = '__all__'


# class SpecialRecipeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Recipe
#         fields = (
#             "id",
#             "name",
#             "image",
#             "cooking_time",
#         )


class TokenSerializer(serializers.ModelSerializer):
    token = serializers.CharField(source='key')

    class Meta:
        model = Token
        fields = ('token',)