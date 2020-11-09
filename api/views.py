import json
from django.http import JsonResponse
from django.views.generic import View
from django.shortcuts import get_object_or_404

from recipes.models import (
    User,
    Ingredients,
    Recipe,
    FavoriteRecipe,
    ShoppingList
    )

from users.models import Follow


class Ingredients(View):
    def get(self, request):
        text = request.GET.get("filters")
        ingredients = list(
            Ingredients.objects.filter(title__icontains=text).values(
                "title", "dimension"
            )
        )
        return JsonResponse(ingredients, safe=False)


class Favorites(View):
    def post(self, request):
        recipe_id = json.loads(request.body).get("id")
        recipe = get_object_or_404(Recipe, id=recipe_id)
        FavoriteRecipe.objects.get_or_create(user=request.user, recipe=recipe)
        return JsonResponse({"success": True})

    def delete(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, id=recipe_id)
        user = get_object_or_404(User, username=request.user.username)
        obj = get_object_or_404(FavoriteRecipe, user=user, recipe=recipe)
        obj.delete()
        return JsonResponse({"success": True})


class Purchases(View):
    def post(self, request):
        recipe_id = json.loads(request.body).get("id")
        recipe = get_object_or_404(Recipe, id=recipe_id)
        ShoppingList.objects.get_or_create(user=request.user, recipe=recipe)
        return JsonResponse({"success": True})

    def delete(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, id=recipe_id)
        user = get_object_or_404(User, username=request.user.username)
        obj = get_object_or_404(ShoppingList, user=user, recipe=recipe)
        obj.delete()
        return JsonResponse({"success": True})


class Subscription(View):
    def post(self, request):
        author_id = json.loads(request.body).get("id")
        author = get_object_or_404(User, id=author_id)
        Follow.objects.get_or_create(user=request.user, author=author)
        return JsonResponse({"success": True})

    def delete(self, request, author_id):
        user = get_object_or_404(User, username=request.user.username)
        author = get_object_or_404(User, id=author_id)
        obj = get_object_or_404(Follow, user=user, author=author)
        obj.delete()
        return JsonResponse({"success": True})
