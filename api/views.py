from rest_framework import generics, filters, mixins, viewsets, status

from .permissions import MethodPermissions
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth import get_user_model

from recipes.models import Recipe, Ingredients, ShoppingList, FavoriteRecipe
from users.models import Follow

from .serializers import IngredientsSerializer, \
    FollowSerializer, \
    FavoriteSerializer, \
    PurchaseSerializer

from django.db.utils import IntegrityError

from django.shortcuts import get_object_or_404

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


# class PurchaseViewSet(viewsets.ModelViewSet):
#     serializer_class = PurchaseSerializer
#     permission_classes = [MethodPermissions]
#
#     def get_queryset(self):
#         recipe_id = self.kwargs.get('recipe_id')
#         user = self.request.user
#         recipe = generics.get_object_or_404(Recipe, pk=recipe_id)
#         queryset = ShoppingList.objects.filter(recipe=recipe, user=user)
#         return queryset
