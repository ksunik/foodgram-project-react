# from django.urls import include, path
# from api.views import RecipeViewSet, IngredientViewSet, TagViewSet, FavoritesViewSet, FollowViewSet
# from users.views import CustomUserViewSet, ShowUserViewSet
# # import api.views
# from rest_framework.routers import DefaultRouter

# # app_name = 'recipes'
# router = DefaultRouter()
# # router.register('recipes/(?P<recipe_id>\d+)/favorite/', FavoritesViewSet, basename='favorites')
# router.register('recipes', RecipeViewSet, basename='recipes')
# router.register('ingredients', IngredientViewSet, basename='ingredients')
# router.register('tags', TagViewSet, basename='tags')
# router.register('users/subscriptions/', FollowViewSet, basename='subscriptions')
# router.register('users', ShowUserViewSet, basename='users')

# # router.register('users/(?P<user_id>\d+)/subscriptions/', FavoritesViewSet, basename='id_subscriptions')


# urlpatterns = [
#     # Djoser создаст набор необходимых эндпоинтов.
#     # базовые, для управления пользователями в Django:
#     # path('auth/', include('djoser.urls')),
#     # # JWT-эндпоинты, для управления JWT-токенами:
#     # path('auth/', include('djoser.urls.jwt')),
#     path('auth/', include('users.urls')),
#     path('auth/', include('django.contrib.auth.urls')),

#     # path('recipes/download_shopping_cart/', download_shopping_cart, name='download'),
#     # path('recipes/<int:recipe_id>/favorite/', FavoritesViewSet.as_view(),),
#     path('', include(router.urls)),
#     # path('v1/', include('djoser.urls.jwt')),
    
# ]

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (IngredientViewSet, RecipeViewSet, TagViewSet,
                       FollowView, FollowViewSet, FollowViewSet2)


v1_router = DefaultRouter()

v1_router.register(r'tags', TagViewSet, basename='tags')
v1_router.register(r'ingredients', IngredientViewSet, basename='ingredients')
v1_router.register(r'recipes', RecipeViewSet, basename='recipes')


urlpatterns = [
    path('users/subscriptions/',
         FollowViewSet.as_view({'get': 'list'})),
    # path('users/<int:user_id>/subscribe/', FollowView.as_view()),
    path('users/<int:user_id>/subscribe/', FollowViewSet2.as_view({'get': 'list'})),
    path('', include(v1_router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]