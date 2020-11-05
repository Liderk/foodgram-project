from django.shortcuts import render, get_object_or_404
from recipes.models import Tag, Ingredients, Recipe, RecipeIngredients, \
    FavoriteRecipe, ShoppingList, User
from users.models import Follow


def get_tag(request, recipe_list):
    all_tags = Tag.objects.all()
    noted_tags = request.GET.getlist('filters')
    if noted_tags:
        recipe_list = recipe_list.filter(tag__name__in=noted_tags).distinct()
    context = {'recipes': recipe_list, 'tags': all_tags}
    return context


def index(request):
    recipe_list = Recipe.objects.all()
    context = get_tag(request, recipe_list)
    return render(request, 'index.html', context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    recipe = Recipe.objects.filter(author=author).all()
    recipe_by_tag = get_tag(request, recipe)
    following = Follow.objects.filter(author=author, user=request.user.id)
    context = {'author': author, 'following': following, **recipe_by_tag}
    return render(request, 'profile.html', context)


def new_recipe():
    return None


def recipe_edit():
    return None


def recipe_delete():
    return None


def recipe_view(request, username, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    author = get_object_or_404(User, username=username)
    following = Follow.objects.filter(author=author, user=request.user.id)
    context = {'recipe': recipe, 'author': author, 'following': following}
    return render(request, 'single_recipe.html', context)


def follow():
    return None


def follow_recipe():
    return None


def shopping_list():
    return None


def download():
    return None
