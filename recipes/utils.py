from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from .models import Tag

User = get_user_model()


def gen_shopping_roster(request):
    shopper = get_object_or_404(User, username=request.user.username)
    shopping_list = shopper.shoppingtransfer.all()
    ingredients = {}
    for item in shopping_list:
        for obj in item.recipe.recipeingredients.all():
            name = obj.ingredient.title
            amount = {}
            if name in ingredients:
                ingredients[name][obj.ingredient.dimension] += obj.quantity
                continue
            else:
                amount[obj.ingredient.dimension] = obj.quantity
            ingredients[name] = amount.copy()
    return ingredients


def get_ingredients(request):
    ingredients = {}
    for key, ingredient_name in request.POST.items():
        if 'nameIngredient' in key:
            _ = key.split('_')
            ingredients[ingredient_name] = int(request.POST[
                                                   f'valueIngredient_{_[1]}']
                                               )
    return ingredients


def get_recipe(request, recipes):
    all_tags = Tag.objects.all()
    noted_tags = request.GET.getlist('filters')
    if noted_tags:
        recipes = recipes.filter(tag__name__in=noted_tags).distinct()
    context = {'recipes': recipes, 'tags': all_tags}
    return context
