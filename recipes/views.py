from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.base import View
from foodgram.settings import PAGES
from wkhtmltopdf.views import PDFTemplateResponse

from .forms import RecipeForm
from recipes.models import (Ingredient, Recipe, RecipeIngredient,
                            ShoppingTransfer, User)
from users.models import Follow
from .utils import gen_shopping_roster, get_ingredients, get_recipe


def index(request):
    recipe_roster = Recipe.objects.all()
    recipe_by_tag = get_recipe(request, recipe_roster)
    paginator = Paginator(recipe_by_tag.get('recipes'), PAGES)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {'page': page, 'paginator': paginator, **recipe_by_tag}
    return render(request, 'index.html', context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    recipe = Recipe.objects.filter(author=author)
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
    user = get_object_or_404(User, username=request.user)
    form = RecipeForm(request.POST or None, files=request.FILES or None)

    if request.method == 'POST':
        ingredients = get_ingredients(request)
        if not ingredients:
            form.add_error(None, 'Добавьте ингредиенты')

        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = user
            recipe.save()
            for ing_name, quantity in ingredients.items():
                ingredient = get_object_or_404(Ingredient, title=ing_name)
                recipe_ing = RecipeIngredient(
                    recipe=recipe,
                    ingredient=ingredient,
                    quantity=quantity
                )
                recipe_ing.save()
            form.save_m2m()
            return redirect('index')
    return render(request, 'new_recipe.html', {'form': form})


@login_required
def recipe_edit(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    ing = RecipeIngredient.objects.filter(recipe=recipe_id)
    form = RecipeForm(
        request.POST or None,
        files=request.FILES or None,
        instance=recipe
    )
    if request.user != recipe.author:
        return redirect('recipe', recipe_id=recipe.id)

    if request.method == 'POST':
        ingredients = get_ingredients(request)

        if form.is_valid():
            RecipeIngredient.objects.filter(recipe=recipe).delete()
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            recipe.ingredient.all().delete()
            for ing_name, quantity in ingredients.items():
                ingredient = get_object_or_404(Ingredient, title=ing_name)
                recipe_ing = RecipeIngredient(
                    recipe=recipe,
                    ingredient=ingredient,
                    quantity=quantity
                )
                recipe_ing.save()
            form.save_m2m()
            return redirect('index')
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
    author_list = Follow.objects.filter(user=request.user)
    paginator = Paginator(author_list, PAGES)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {'page': page, 'paginator': paginator, 'authors': author_list}
    return render(request, 'follow.html', context)


def favorites_recipe(request):
    recipe_roster = Recipe.objects.filter(
        favorite_recipes__user__id=request.user.id)
    recipe_by_tag = get_recipe(request, recipe_roster)
    paginator = Paginator(recipe_by_tag.get('recipes'), PAGES)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {'page': page, 'paginator': paginator, **recipe_by_tag}
    return render(request, 'favorites.html', context)


def shopping_roster(request):
    shopping_roster = ShoppingTransfer.objects.select_related('recipe').filter(
        user=request.user.id
    )
    context = {'shopping_roster': shopping_roster}
    return render(request, 'shoplist.html', context)


class Download(View):
    template = 'shop-list-to-pdf.html'

    def get(self, request):
        result = gen_shopping_roster(request)
        context = {'data': result}
        return PDFTemplateResponse(
            request=request,
            template=self.template,
            filename='my_purchases.pdf',
            context=context,
            show_content_in_browser=False,
        )
