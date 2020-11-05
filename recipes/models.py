from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(verbose_name='Tag name', max_length=50)
    slug = models.SlugField(unique=True)
    color = models.CharField(verbose_name='color', max_length=15, null=True)

    def __str__(self):
        return self.name


class Ingredients(models.Model):
    title = models.CharField(max_length=50)
    dimension = models.CharField(max_length=10, verbose_name='Количество')

    def __str__(self):
        return self.title


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipe_author'
    )
    title = models.CharField(verbose_name='recipe name', max_length=255)
    description = models.TextField(verbose_name='description')
    tag = models.ManyToManyField(Tag, blank=True)
    pub_date = models.DateTimeField("date published", auto_now_add=True,
                                    db_index=True)
    image = models.ImageField(upload_to='recipes/', blank=True, null=True)
    cooking_time = models.IntegerField(verbose_name='cooking_time')
    ingredients = models.ManyToManyField(
        Ingredients,
        through='RecipeIngredients',
        through_fields=('recipe', 'ingredients')
    )
    slug = models.SlugField()

    def __str__(self):
        # выводим текст рецепта
        return self.title

    class Meta:
        ordering = ['-pub_date']


class RecipeIngredients(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredients = models.ForeignKey(Ingredients, on_delete=models.CASCADE,
                                    related_name='Ingredient')
    quantity = models.IntegerField()

    def __str__(self):
        return self.ingredients.dimension


class FavoriteRecipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='favor_by')
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="favor"
    )

    def __str__(self):
        return self.recipe.title


class ShoppingList(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopper'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_list'
    )

    def __str__(self):
        return self.recipe.title
