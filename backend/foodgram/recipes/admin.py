from django.contrib import admin
from .models import Recipe, Ingredient, RecipeIngredient, Tag, ShoppingCart, Favorites, Follow
from import_export import resources
from import_export.admin import ImportExportModelAdmin

class RecipeIngredientInLine(admin.TabularInline):
    model = RecipeIngredient
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = (RecipeIngredientInLine, )

class IngredientResource(resources.ModelResource):
    class Meta:
        model = Ingredient


# Вывод данных на странице
class IngredientAdmin(ImportExportModelAdmin):
    resource_classes = [IngredientResource]


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag)
# admin.site.register(Recipe)
admin.site.register(Favorites)
admin.site.register(ShoppingCart)
admin.site.register(Follow)

# # Register your models here.
# @admin.register(Recipe)
# class RecipeAdmin(admin.ModelAdmin):
#     list_display = ('name', 'author', 'image', 'text', 'ingredients', 'tag', 'time', 'pub_time', 'quantity', 'like')


# @admin.register(Ingredient)
# class IngredientAdmin(admin.ModelAdmin):
#     list_display = ('name', 'measure')
