# from django.shortcuts import get_object_or_404
from django.db.models import Sum
import os
from rest_framework import filters, viewsets, mixins, status
# from rest_framework.pagination import LimitOffsetPagination
# from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, FileResponse
from rest_framework.decorators import api_view, action
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.permissions import (AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated)
# from rest_framework.permissions import IsOwnerOrReadOnly
from . import models, serializers
from foodgram.settings import MEDIA_ROOT
from api.serializers import (RecipeSerializer, IngredientSerializer, RecipeCreateSerializer,
                             TagSerializer, ShoppingCartSerializer, ShoppingListSerializer,
                             FavoritesSerializer, FollowSerializer, ShowFollowSerializer,
                             CustomUserSerializer)

from recipes.models import (Recipe, Tag, Ingredient, RecipeIngredient,
                            Favorites, ShoppingCart, Follow)
from users.models import User
                    #  Follow)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeSerializer
        return RecipeCreateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        detail=True,
        methods=['post', 'delete'],
        # permission_classes=[IsAuthenticated, ]
    )
    def favorite(self, request, pk):
        """Работа с избранными рецептами.
        Удаление/добавление в избранное.
        """
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == 'POST':
            serializer = FavoritesSerializer(
                data={'user': request.user.id, 'recipe': recipe.id, },
                context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            # return create_model_instance(request, recipe, FavoritesSerializer)

        if request.method == 'DELETE':
            error_message = 'У вас нет этого рецепта в избранном'
            if not Favorites.objects.filter(user=request.user, recipe=recipe).exists():
                return Response({'errors': error_message}, status=status.HTTP_400_BAD_REQUEST)
            Favorites.objects.filter(user=request.user, recipe=recipe).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
            # return delete_model_instance(request, Favorites, recipe, error_message)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated, ]
    )
    def shopping_cart(self, request, pk):
        """Работа со списком покупок.
        Удаление/добавление в список покупок.
        """
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == 'POST':
            serializer = ShoppingCartSerializer(data={'author': request.user.id, 'recipe': recipe.id, },)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if request.method == 'DELETE':
            error_message = 'У вас нет этого рецепта в списке покупок'
            if not ShoppingCart.objects.filter(author=request.user, recipe=recipe).exists():
                return Response({'errors': error_message}, status=status.HTTP_400_BAD_REQUEST)
            ShoppingCart.objects.filter(author=request.user, recipe=recipe).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    # @action(
    #     detail=False,
    #     methods=['get'],
    #     permission_classes=[IsAuthenticated, ]
    # )
    # def download_shopping_cart(self, request):
    #     """Отправка файла со списком покупок."""
    #     ingredients = RecipeIngredient.objects.filter(
    #         recipe__shopping_cart__author=request.user).values(
    #         'ingredient__name', 'ingredient__measurement_unit'
    #     ).annotate(ingredient_amount=Sum('amount'))
    #     shopping_list = ['Список покупок:\n']
    #     for ingredient in ingredients:
    #         name = ingredient['ingredient__name']
    #         unit = ingredient['ingredient__measurement_unit']
    #         amount = ingredient['ingredient_amount']
    #         shopping_list.append(f'\n{name} - {amount}, {unit}')
    #     response = HttpResponse(shopping_list, content_type='text/plain')
    #     response['Content-Disposition'] = \
    #         'attachment; filename="shopping_cart.txt"'
    #     return response

    # def download_shopping_cart(self, request):
    #     author = request.user
    #     shopping_cart = author.shopping_cart.all()
    #     buying_list = {}
    #     for record in shopping_cart:
    #         recipe = record.recipe
    #         ingredients = RecipeIngredient.objects.filter(recipe=recipe)
    #         for ingredient in ingredients:
    #             amount = ingredient.amount
    #             name = ingredient.ingredient.name
    #             measurement_unit = ingredient.ingredient.measurement_unit
    #             if name not in buying_list:
    #                 buying_list[name] = {
    #                     "measurement_unit": measurement_unit,
    #                     "amount": amount,
    #                 }
    #             else:
    #                 buying_list[name]["amount"] = (
    #                     buying_list[name]["amount"] + amount
    #                 )
    #     wishlist = []
    #     for name, data in buying_list.items():
    #         wishlist.append(
    #             f"\n{name} - {data['amount']} {data['measurement_unit']}\n"
    #         )
    #     response = HttpResponse(wishlist, content_type="text/plain")
    #     response['Content-Disposition'] = 'attachment; filename="shopping_cart.txt"'
    #     return response


    # def download_shopping_cart(self, request):
        # """Выгрузка списка покупок в формате txt. """
        # shopping_cart = ShoppingCart.objects.filter(author=request.user)
        # shopping_list = "\n".join([f"{item.recipe.name}: {item.recipe.ingredients}" for item in shopping_cart])
        # response = HttpResponse(content_type='text/plain')
        # response['Content-Disposition'] = 'attachment; filename="shopping_cart.txt"'
        # response.write(shopping_list)
        # return response

    # def download_shopping_cart(self, request):
    #     """Скачать список покупок в формате txt."""
    #     shopping_cart_items = ShoppingCart.objects.filter(author=request.user)
    #     filename = 'shopping_cart.txt'
    #     filepath = os.path.join(MEDIA_ROOT, filename)
        
    #     with open(filepath, 'w') as file:
    #         for item in shopping_cart_items:
    #             file.write(f"{item.recipe.name}\n")
        
    #     return FileResponse(open(filepath, 'rb'), as_attachment=True, filename=filename)


    @action(
        detail=False,
        methods=['get'],
        permission_classes=[IsAuthenticated, ]
    )
    def download_shopping_cart(self, request):
        author = request.user
        shopping_cart = author.shopping_cart.all()
        buying_list = {}
        for record in shopping_cart:
            recipe = record.recipe
            ingredients = RecipeIngredient.objects.filter(recipe=recipe)
            for ingredient in ingredients:
                amount = ingredient.amount
                name = ingredient.ingredient.name
                measurement_unit = ingredient.ingredient.measurement_unit
                if name not in buying_list:
                    buying_list[name] = {
                        "measurement_unit": measurement_unit,
                        "amount": amount,
                    }
                else:
                    buying_list[name]["amount"] = (
                        buying_list[name]["amount"] + amount
                    )
        wishlist = []
        for name, data in buying_list.items():
            wishlist.append(
                f"\n{name} ({data['measurement_unit']}) - {data['amount']}"
            )
        content = "".join(wishlist)
        
        # Создание файла shopping_cart.txt в папке media
        filename = 'shopping_cart.txt'
        filepath = os.path.join(MEDIA_ROOT, filename)
        with open(filepath, 'w') as file:
            file.write(content)
        
        return FileResponse(open(filepath, 'rb'), as_attachment=True, filename=filename)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
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
    pagination_class = None


class FollowViewSet(mixins.ListModelMixin,
                    GenericViewSet):
    """Получение списка всех подписок на пользователей."""
    serializer_class = ShowFollowSerializer
    # filter_backends = (filters.SearchFilter,)
    # search_fields = ('following__username',)


    def get_queryset(self):
        return User.objects.filter(following__user=self.request.user)

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)


class FollowView(APIView):
    """Создание/удаление подписки на пользователя."""
    def post(self, request, user_id):
        print('1111111111111111111')
        
        author = get_object_or_404(User, id=user_id)
        print(author)
        print(request.user.id)
        print(author.id)
        serializer = FollowSerializer(
            data={'user': request.user.id, 'author': author.id},
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, user_id):
        author = get_object_or_404(User, id=user_id)
        if not Follow.objects.filter(user=request.user,
                                     author=author).exists():
            return Response(
                {'errors': 'Вы не подписаны на этого пользователя'},
                status=status.HTTP_400_BAD_REQUEST
            )
        Follow.objects.get(user=request.user.id,
                           author=user_id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FollowViewSet2(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    pagination_class = None

    @action(methods=["get", "delete", "post"], detail=True, permission_classes=[AllowAny],)
    def subscribe(self, request, pk=None):
        if request.method == "GET" or request.method == "POST":
            user = request.user
            following = get_object_or_404(User, pk=pk)
            follow = Follow.objects.filter(user=user, following=following)
            data = {
                "user": user.id,
                "following": following.id,
            }
            # if request.method == "GET" or request.method == "POST":
            if follow.exists():
                return Response(
                    "Вы уже подписаны", status=status.HTTP_400_BAD_REQUEST
                )
            serializer = FollowSerializer(data=data, context=request)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif request.method == "DELETE":
            follow.delete()
            return Response("Удалено", status=status.HTTP_204_NO_CONTENT)
