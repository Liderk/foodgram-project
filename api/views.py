from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from recipes.models import FavoriteRecipe, Ingredients, Recipe, ShoppingList
from rest_framework import filters, generics, mixins, status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from users.models import Follow
from .serializers import (FavoriteSerializer, FollowSerializer,
                          IngredientsSerializer, PurchaseSerializer)

User = get_user_model()


class IngredientListView(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer
    filter_backends = [filters.SearchFilter, ]
    search_fields = ['title', ]
    ordering_fields = ['title', ]


@api_view(['POST', 'DELETE'])
def api_purchase_detail(request, recipe_id):
    recipe = generics.get_object_or_404(Recipe, pk=recipe_id)
    if request.method == 'POST':
        serializer = PurchaseSerializer(data=request.data)

        if serializer.is_valid():
            try:
                serializer.save(user=request.user, recipe=recipe)
            except IntegrityError:  # если такая покупка уже есть
                Response({'success': False},
                         status=status.HTTP_400_BAD_REQUEST)
            return Response({'success': True}, status=status.HTTP_201_CREATED)
        return Response({'success': False}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        purchase = generics.get_object_or_404(
            ShoppingList, user=request.user, recipe=recipe)
        purchase.delete()
        return Response({'success': True})


@api_view(['POST', 'DELETE'])
def api_favorite_detail(request, recipe_id):
    recipe = generics.get_object_or_404(Recipe, pk=recipe_id)
    if request.method == 'POST':
        serializer = FavoriteSerializer(data=request.data)

        if serializer.is_valid():
            try:
                serializer.save(user=request.user, recipe=recipe)
            except IntegrityError:
                Response({'success': False},
                         status=status.HTTP_400_BAD_REQUEST)
            return Response({'success': True}, status=status.HTTP_201_CREATED)
        return Response({'success': False}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        favorite = generics.get_object_or_404(
            FavoriteRecipe, user=request.user, recipe=recipe)
        favorite.delete()
        return Response({'success': True})


@api_view(['POST', 'DELETE'])
def api_follow_detail(request, user_id):
    cook = generics.get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        serializer = FollowSerializer(data=request.data)

        if serializer.is_valid():
            try:
                serializer.save(user=request.user, author=cook)
            except IntegrityError:
                Response({'success': False},
                         status=status.HTTP_400_BAD_REQUEST)
            return Response({'success': True}, status=status.HTTP_201_CREATED)
        return Response({'success': False}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        follow = generics.get_object_or_404(
            Follow, user=request.user, author=cook)
        follow.delete()
        return Response({'success': True})
