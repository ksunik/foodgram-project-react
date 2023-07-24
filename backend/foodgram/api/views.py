# from django.shortcuts import get_object_or_404
from rest_framework import filters, viewsets, mixins
# from rest_framework.pagination import LimitOffsetPagination
# from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import GenericViewSet

# from permissions import IsOwnerOrReadOnly
from api.serializers import (RecipeSerializer, IngredientSerializer,
                             TagSerializer, ShoppingListSerializer,
                             FavoritesSerializer, FollowSerializer)

from recipes.models import (Recipe, Tag, Ingredient,
                            Favorites, ShoppingList)
                    #  Follow)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class FavoritesViewSet(viewsets.ModelViewSet):
    queryset = Favorites.objects.all()
    serializer_class = FavoritesSerializer


class ShoppingListViewSet(viewsets.ModelViewSet):
    queryset = ShoppingList.objects.all()
    serializer_class = ShoppingListSerializer


class FollowViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    GenericViewSet):
    serializer_class = FollowSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        follower = self.request.follower
        return follower.follower

    def perform_create(self, serializer):
        serializer.save(follower=self.request.follower)
