from django.urls import include, path
from api.views import RecipeViewSet, IngredientViewSet, TagViewSet
# import api.views
from rest_framework.routers import DefaultRouter

# app_name = 'recipes'
router = DefaultRouter()
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('tags', TagViewSet, basename='tags')


urlpatterns = [
    path('', include(router.urls)),
    # path('v1/', include('djoser.urls.jwt')),
]