from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from rest_framework.authtoken.models import Token

# from recipes.models import models
from recipes.models import Recipe, Follow
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


class ShowUserSerializer(CustomUserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name', 'is_subscribed')

    def get_is_subscribed(self, obj):
        if (self.context.get('request')
            and not self.context['request'].user.is_anonymous):
            return Follow.objects.filter(following=self.context['request'].user, user=obj).exists()
        return False
