from django.contrib import admin
from .models import Recipe, Ingredient, Tag, ShoppingList, Favorites
from import_export import resources
from import_export.admin import ImportExportModelAdmin


# класс обработки данных
class IngredientResource(resources.ModelResource):

    class Meta:
        model = Ingredient


# Вывод данных на странице
class IngredientAdmin(ImportExportModelAdmin):
    resource_classes = [IngredientResource]

admin.site.register(Ingredient, IngredientAdmin)

# # Register your models here.
# @admin.register(Recipe)
# class RecipeAdmin(admin.ModelAdmin):
#     list_display = ('name', 'author', 'image', 'text', 'ingredients', 'tag', 'time', 'pub_time', 'quantity', 'like')


# @admin.register(Ingredient)
# class IngredientAdmin(admin.ModelAdmin):
#     list_display = ('name', 'measure')
