# from django.shortcuts import get_object_or_404
from rest_framework import filters, viewsets, mixins, status
# from rest_framework.pagination import LimitOffsetPagination
# from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view, action
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.views import APIView
# from rest_framework.permissions import (
#     AllowAny,
#     IsAuthenticatedOrReadOnly,
# )

# from permissions import IsOwnerOrReadOnly
from . import models, serializers
from api.serializers import (RecipeSerializer, IngredientSerializer,
                             TagSerializer, ShoppingListSerializer,
                             FavoritesSerializer, FollowSerializer)

from recipes.models import (Recipe, Tag, Ingredient,
                            Favorites, ShoppingCart)
                    #  Follow)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    # def dispatch(self, request, *args, **kwargs):
    #     res = super().dispatch(request, *args, **kwargs)
    #     return res

    # def get_queryset(self):
    #     recipes = Recipe.objects.prefetch_related(
    #         'recipe_ingredients_ingredient', 'tags'
    #     ).all()
    #     return recipes

    # def get_serializer_class(self):
    #     if self.action == 'create':
    #         return RecipeSerializer
    #     return RecipeSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    # permissions = [AllowAny, ]


class FavoritesViewSet(viewsets.ModelViewSet):
    queryset = Favorites.objects.all()
    serializer_class = FavoritesSerializer

    @action(methods=['post'], detail=True,)
    def post(self, request, recipe_id):
        user = request.user
        data = {
            "user": user.id,
            "recipe": recipe_id,
        }
        if Favorites.objects.filter(
            user=user, recipe__id=recipe_id
        ).exists():
            return Response(
                {"Ошибка": "Уже в избранном"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = serializers.FavoritesSerializer(
            data=data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['DELETE'], detail=True,)
    def delete(self, request, recipe_id):
        user = request.user
        recipe = get_object_or_404(models.Recipe, id=recipe_id)
        if not Favorites.objects.filter(
            user=user, recipe=recipe
        ).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        Favorites.objects.get(user=user, recipe=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ShoppingListViewSet(viewsets.ModelViewSet):
    queryset = ShoppingCart.objects.all()
    serializer_class = ShoppingListSerializer


class FollowViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    GenericViewSet):
    serializer_class = FollowSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        user = self.request.user
        return user.follower

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
