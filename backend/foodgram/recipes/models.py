from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(max_length=200, verbose_name='Наименование')
    # quantity = models.IntegerField(verbose_name='Количество')
    measurement_unit = models.CharField(max_length=200, verbose_name='Единицы измерения')

    # def __str__(self):
    #     return self.name


class Tag(models.Model):
    name = models.CharField(max_length=200, verbose_name='тэг')
    color = models.CharField(max_length=200, verbose_name='Цвет тэга')
    slug = models.SlugField(unique=True, verbose_name='Ссылка')


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
        # through="IngredientInRecipe",
        # related_name="recipes",
        blank=True,
        verbose_name='Ингредиенты',
        help_text='Введите необходимые ингредиенты'
    )
    tag = models.ManyToManyField(
        Tag,
        # through="TagsInRecipe",
        # related_name="recipes",
        verbose_name='Тэг',
        help_text='Введите необходимые тэги'
    )
    time = models.IntegerField(
        verbose_name='Время приготовления в минутах'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата'
    )
    quantity = models.IntegerField(
        verbose_name='Количество'
    )
    like = models.ManyToManyField(
        User,
        through="Favorites",
        through_fields=('recipe', 'author'),
        blank=True,
        related_name='rname_liked_recipes'
    )

    class Meta:
        ordering = ['-pub_date']
        # default_related_name = 'posts_rname'

    # def __str__(self):
    #     return self.name


# class TagsInRecipe(models.Model):
#     tag = models.ForeignKey(
#         Tag,
#         on_delete=models.CASCADE
#     )
#     recipe = models.ForeignKey(
#         Recipe,
#         on_delete=models.CASCADE
#     )


# class IngredientInRecipe(models.Model):
#     ingredient = models.ForeignKey(
#         Ingredient,
#         on_delete=models.CASCADE
#     )
#     recipe = models.ForeignKey(
#         Recipe,
#         on_delete=models.CASCADE
#     )
#     quantity = models.IntegerField(
#         verbose_name='Количество'
#     )


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

    # def __str__(self):
    #     return self.recipe


class ShoppingList(models.Model):
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
    quantity = models.IntegerField(
        verbose_name='Количество'
    )


    # def __str__(self):
    #     return self.recipe

class Follow(models.Model):
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='following')
    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Подписчик',
        related_name='follower')

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['following', 'follower'],
            name='unique subs')
        ]