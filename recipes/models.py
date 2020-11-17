from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(verbose_name='Tag name', max_length=150)
    slug = models.SlugField(unique=True)
    color = models.CharField(verbose_name='color', max_length=15, null=True)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    title = models.CharField(max_length=255)
    dimension = models.CharField(max_length=10, verbose_name='Количество')

    def __str__(self):
        return self.title


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    title = models.CharField(verbose_name='recipe name', max_length=255)
    description = models.TextField(verbose_name='description')
    tag = models.ManyToManyField(Tag, blank=True)
    pub_date = models.DateTimeField('date published', auto_now_add=True,
                                    db_index=True)
    image = models.ImageField(upload_to='recipes/', blank=True, null=True)
    cooking_time = models.IntegerField(verbose_name='cooking_time')
    ingredient = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        through_fields=('recipe', 'ingredient')
    )

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.title


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='recipeingredients')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE,
                                   related_name='recipeingredients')
    quantity = models.IntegerField()

    def __str__(self):
        return self.ingredient.dimension


class FavoriteRecipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='favorite_recipes')
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite_recipes'
    )

    def __str__(self):
        return self.recipe.title


class ShoppingTransfer(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shoppingtransfer'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shoppingtransfer'
    )

    def __str__(self):
        return self.recipe.title
