from django.shortcuts import render, get_object_or_404, redirect
from recipes.models import Tag, Ingredients, Recipe, RecipeIngredients, \
    FavoriteRecipe, ShoppingList, User
from users.models import Follow
from .forms import RecipeForm
from .utils import gen_shopping_list, get_ingredients


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


def new_recipe(request):
    user = User.objects.get(username=request.user)
    if request.method == 'POST':
        form = RecipeForm(request.POST or None, files=request.FILES or None)
        ingredients = get_ingredients(request)
        if not ingredients:
            form.add_error(None, 'Добавьте ингредиенты')
        elif form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = user
            recipe.save()
            for ing_name, quantity in ingredients.items():
                ingredient = get_object_or_404(Ingredients, title=ing_name)
                recipe_ing = RecipeIngredients(
                    recipe=recipe,
                    ingredients=ingredient,
                    quantity=quantity
                )
                recipe_ing.save()
            form.save_m2m()
            return redirect('index')
    else:
        form = RecipeForm()
    return render(request, 'new_recipe.html', {'form': form})


def recipe_edit(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    ing = RecipeIngredients.objects.filter(recipe=recipe_id).all()
    if request.user != recipe.author:
        return redirect('recipe', recipe_id=recipe.id)
    if request.method == "POST":
        form = RecipeForm(
            request.POST or None,
            files=request.FILES or None,
            instance=recipe
        )
        ingredients = get_ingredients(request)
        if form.is_valid():
            RecipeIngredients.objects.filter(recipe=recipe).delete()
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            recipe.ingredients.all().delete()
            for ing_name, quantity in ingredients.items():
                ingredient = get_object_or_404(Ingredients, title=ing_name)
                recipe_ing = RecipeIngredients(
                    recipe=recipe,
                    ingredients=ingredient,
                    quantity=quantity
                )
                recipe_ing.save()
            form.save_m2m()
            return redirect('index')
    form = RecipeForm(
        request.POST or None,
        files=request.FILES or None,
        instance=recipe
    )
    return render(
        request,
        'recipe-edit.html',
        {'form': form, 'recipe': recipe, 'edit': 'True', 'ingredients': ing}
    )


def recipe_delete(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.user == recipe.author:
        recipe.delete()
    return redirect('index')


def recipe_view(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    author = get_object_or_404(User, username=recipe.author)
    following = Follow.objects.filter(author=author, user=request.user.id)
    context = {'recipe': recipe, 'author': author, 'following': following}
    return render(request, 'single_recipe.html', context)


def follow(request):
    author_list = Follow.objects.filter(user=request.user).all()
    return render(
        request,
        'follow.html',
        {'authors': author_list}
    )


def favorites_recipe(request):
    recipe_list = Recipe.objects.filter(favor__user__id=request.user.id).all()
    context = get_tag(request, recipe_list)
    return render(request, 'index.html', context)


def shopping_list(request):
    shopping_list = ShoppingList.objects.select_related('recipe').filter(
        user=request.user.id
    )
    context = {'shopping_list': shopping_list}
    return render(request, 'shoplist.html',  context)



def download():
    return None
