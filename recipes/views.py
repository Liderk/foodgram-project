from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views.generic.base import View

from .forms import RecipeForm
from recipes.models import Ingredients, Recipe, RecipeIngredients, \
    ShoppingList, User
from users.models import Follow
from .utils import gen_shopping_list, get_ingredients, get_recipe

from wkhtmltopdf.views import PDFTemplateResponse

# Количество рецептов на странице
PAGES = 6


def index(request):
    recipe_list = Recipe.objects.all()
    recipe_by_tag = get_recipe(request, recipe_list)
    paginator = Paginator(recipe_by_tag.get('recipes'), PAGES)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {'page': page, 'paginator': paginator, **recipe_by_tag}
    return render(request, 'index.html', context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    recipe = Recipe.objects.filter(author=author).all()
    following = Follow.objects.filter(author=author, user=request.user.id)
    recipe_by_tag = get_recipe(request, recipe)
    paginator = Paginator(recipe_by_tag.get('recipes'), PAGES)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {
        'author': author,
        'following': following,
        **recipe_by_tag,
        'page': page,
        'paginator': paginator
    }
    return render(request, 'profile.html', context)


@login_required
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


@login_required
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


@login_required
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


@login_required
def follow(request):
    author_list = Follow.objects.filter(user=request.user).all()
    paginator = Paginator(author_list, PAGES)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {'page': page, 'paginator': paginator, 'authors': author_list}
    return render(request, 'follow.html', context)


def favorites_recipe(request):
    recipe_list = Recipe.objects.filter(favor__user__id=request.user.id).all()
    recipe_by_tag = get_recipe(request, recipe_list)
    paginator = Paginator(recipe_by_tag.get('recipes'), PAGES)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {'page': page, 'paginator': paginator, **recipe_by_tag}
    return render(request, 'favorites.html', context)


def shopping_list(request):
    shopping_list = ShoppingList.objects.select_related('recipe').filter(
        user=request.user.id
    )
    context = {'shopping_list': shopping_list}
    return render(request, 'shoplist.html', context)


class Download(View):
    template = 'shop-list-to-pdf.html'

    def get(self, request):
        result = gen_shopping_list(request)
        context = {'data': result}
        return PDFTemplateResponse(
            request=request,
            template=self.template,
            filename="my_purchases.pdf",
            context=context,
            show_content_in_browser=False,
        )


def page_not_found(request, exception=None):
    return render(request, '404.html', status=404)


def server_error(request):
    return render(request, "misc/500.html", status=500)
