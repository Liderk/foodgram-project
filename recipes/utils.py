from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from .models import Tag

User = get_user_model()


def gen_shopping_list(request):
    shopper = get_object_or_404(User, username=request.user.username)
    shopping_list = shopper.shopper.all()
    ingredients = {}
    for item in shopping_list:
        for j in item.recipe.recipeingredients_set.all():
            name = j.ingredients.title
            amount = {}
            if name in ingredients.keys():
                ingredients[name][j.ingredients.dimension] += j.quantity
                continue
            else:
                amount[j.ingredients.dimension] = j.quantity
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


def get_recipe(request, recipe_list):
    all_tags = Tag.objects.all()
    noted_tags = request.GET.getlist('filters')
    if noted_tags:
        recipe_list = recipe_list.filter(tag__name__in=noted_tags).distinct()
    context = {'recipes': recipe_list, 'tags': all_tags}
    return context
