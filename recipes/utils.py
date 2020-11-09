from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404


User = get_user_model()


def gen_shopping_list(request):
    shopper = get_object_or_404(User, username=request.user.username)
    shopping_list = shopper.shopper.all()
    ingredients = {}
    for item in shopping_list:
        for j in item.recipe.recipeingredients_set.all():
            name = j.ingredients.title
            quantity = f'{j.quantity} ({j.ingredients.dimension})'
            if name in ingredients.keys():
                ingredients[name] += quantity
            else:
                ingredients[name] = quantity
    # result = []
    # for key, quantity in ingredients.items():
    #     result.append(f'{key} - {quantity}')
    return ingredients


def get_ingredients(request):
    ingredients = {}
    for key, ingredient_name in request.POST.items():
        if 'nameIngredient' in key:
            _ = key.split('_')
            ingredients[ingredient_name] = int(request.POST[f'valueIngredient_{_[1]}'])
    return ingredients
