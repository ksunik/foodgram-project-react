# Generated by Django 3.2 on 2023-08-10 11:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('recipes', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='shoppingcart',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shopping_cart', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AddField(
            model_name='recipeingredient',
            name='ingredient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rname_recipe_ingredients', to='recipes.ingredient', verbose_name='Название ингредиента'),
        ),
        migrations.AddField(
            model_name='recipeingredient',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rname_recipe_ingredients', to='recipes.recipe', verbose_name='Название рецепта'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rname_recipe_author', to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(related_name='rname_recipes', through='recipes.RecipeIngredient', to='recipes.Ingredient', verbose_name='Список ингредиентов'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='is_favorited',
            field=models.ManyToManyField(blank=True, related_name='rname_recipes_is_favorited', through='recipes.Favorite', to=settings.AUTH_USER_MODEL, verbose_name='В списке избранного'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='is_in_shopping_cart',
            field=models.ManyToManyField(related_name='rname_recipes_is_in_shopping_cart', through='recipes.ShoppingCart', to=settings.AUTH_USER_MODEL, verbose_name='В списке покупок'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(to='recipes.Tag', verbose_name='Список id тегов'),
        ),
        migrations.AddConstraint(
            model_name='ingredient',
            constraint=models.UniqueConstraint(fields=('name', 'measurement_unit'), name='unique_name_measurement_unit_ingredient'),
        ),
        migrations.AddField(
            model_name='favorite',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.recipe', verbose_name='Название рецепта'),
        ),
        migrations.AddField(
            model_name='favorite',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AddConstraint(
            model_name='favorite',
            constraint=models.UniqueConstraint(fields=('recipe', 'user'), name='unique_like'),
        ),
    ]
