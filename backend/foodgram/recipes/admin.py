# from django.contrib import admin
# from .models import Recipe, Ingredient, RecipeIngredient, Tag, ShoppingCart, Favorites, Follow
# from import_export import resources
# from import_export.admin import ImportExportModelAdmin

# class RecipeIngredientInLine(admin.TabularInline):
#     model = RecipeIngredient
#     extra = 1


# @admin.register(Recipe)
# class RecipeAdmin(admin.ModelAdmin):
#     inlines = (RecipeIngredientInLine, )

# class IngredientResource(resources.ModelResource):
#     class Meta:
#         model = Ingredient


# # Вывод данных на странице
# class IngredientAdmin(ImportExportModelAdmin):
#     resource_classes = [IngredientResource]


# admin.site.register(Ingredient, IngredientAdmin)
# admin.site.register(Tag)
# # admin.site.register(Recipe)
# admin.site.register(Favorites)
# admin.site.register(ShoppingCart)
# admin.site.register(Follow)

# # # Register your models here.
# # @admin.register(Recipe)
# # class RecipeAdmin(admin.ModelAdmin):
# #     list_display = ('name', 'author', 'image', 'text', 'ingredients', 'tag', 'time', 'pub_time', 'quantity', 'like')


# # @admin.register(Ingredient)
# # class IngredientAdmin(admin.ModelAdmin):
# #     list_display = ('name', 'measure')

from django.conf import settings
from django.contrib import admin

from recipes.models import (Favorites, Ingredient, Recipe,
                            RecipeIngredient, ShoppingCart, Tag)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'color', 'slug')
    search_fields = ('name', 'color', 'slug')
    list_filter = ('name', 'color', 'slug')
    empty_value_display = settings.EMPTY_VALUE


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'measurement_unit')
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = settings.EMPTY_VALUE


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'author', 'favorites_amount')
    search_fields = ('name', 'author')
    list_filter = ('name', 'author', 'tags')
    empty_value_display = settings.EMPTY_VALUE
    inlines = [
        RecipeIngredientInline,
    ]

    def favorites_amount(self, obj):
        return obj.is_favorited.count()


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'recipe', 'ingredient', 'amount')
    empty_value_display = settings.EMPTY_VALUE


@admin.register(Favorites)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'recipe')
    search_fields = ('author', 'recipe')
    empty_value_display = settings.EMPTY_VALUE


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'recipe')
    search_fields = ('author', 'recipe')
    empty_value_display = settings.EMPTY_VALUE