from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(max_length=200, verbose_name='Наименование')
    measurement_unit = models.CharField(max_length=200, verbose_name='Единицы измерения')

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Tag(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название')
    color = models.CharField(max_length=7, verbose_name='Цвет в HEX')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='Уникальный слаг')

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        help_text='Укажите автора'
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название рецепта',
        help_text='Укажите название рецепта'
    )
    image = models.ImageField(
        'Картинка',
        # upload_to='posts/',
        blank=True,
        null=True,
        help_text='Выберите изображение'
    )
    text = models.TextField(
        'Текст рецепта',
        help_text='Введите текст рецепта'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        through_fields=('recipe', 'ingredient'),
        # related_name="recipes",
        blank=True,
        verbose_name='Ингредиенты',
        help_text='Введите необходимые ингредиенты'
    )
    # amount = models.PositiveIntegerField(
    #     verbose_name='Количество'
    # )
    tags = models.ManyToManyField(
        Tag,
        # through="TagsInRecipe",
        # related_name="recipes",
        verbose_name='Тэг',
        help_text='Введите необходимые тэги'
    )
    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготовления в минутах'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата'
    )
    is_favorited = models.ManyToManyField(
        User,
        through="Favorites",
        through_fields=('recipe', 'author'),
        blank=True,
        related_name='rname_liked_recipes'
    )
    is_in_shopping_cart = models.ManyToManyField(
        'ShoppingCart',
        # through="Shopping_cart",
        # through_fields=('recipe', 'author'),
        blank=True,
        related_name='rname_liked_recipes'
    )

    class Meta:
        ordering = ['-pub_date']
        # default_related_name = 'posts_rname'

    def __str__(self):
        return self.name


# class TagsInRecipe(models.Model):
#     tag = models.ForeignKey(
#         Tag,
#         on_delete=models.CASCADE
#     )
#     recipe = models.ForeignKey(
#         Recipe,
#         on_delete=models.CASCADE
#     )


class RecipeIngredient(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE
    )
    amount = models.PositiveIntegerField(
        verbose_name='Количество'
    )


class Favorites(models.Model):
    recipe = models.ForeignKey(
        'Recipe',
        # related_name="favorite",
        on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        # related_name="favorite",
        verbose_name='Автор'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['recipe', 'author'],
                                    name='unique_like')
        ]
        # unique_together = ("author", "recipe")

    # def __str__(self):
    #     return self.recipe


class ShoppingCart(models.Model):
    recipe = models.ForeignKey(
        'Recipe',
        # related_name="shopping_cart",
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        # related_name="shopping_cart",
        verbose_name='Автор'
    )
    # amount = models.IntegerField(
    #     verbose_name='Количество'
    # )


    # def __str__(self):
    #     return self.recipe

class Follow(models.Model):
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='following')
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Подписчик',
        related_name='follower')

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['following', 'user'],
            name='unique subs')
        ]