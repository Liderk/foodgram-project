from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from recipes.models import FavoriteRecipe, Ingredient, Recipe, ShoppingTransfer
from rest_framework import filters, mixins, status, viewsets
from rest_framework.response import Response

from .serializers import (FavoriteSerializer, FollowSerializer,
                          IngredientSerializer, PurchaseSerializer)
from users.models import Follow

User = get_user_model()


class IngredientListView(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [filters.SearchFilter, ]
    search_fields = ['title', ]
    ordering_fields = ['title', ]


class PurchaseViewSet(viewsets.ModelViewSet):
    queryset = ShoppingTransfer.objects.all()
    serializer_class = PurchaseSerializer

    def perform_create(self, serializer):
        recipe = get_object_or_404(Recipe, pk=self.request.data.get('id'))
        serializer = PurchaseSerializer(data=self.request.data, context={
            'request_user': self.request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user, recipe=recipe)
        return Response({'success': True}, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        recipe = get_object_or_404(Recipe, pk=kwargs['pk'])
        shoppinglist = get_object_or_404(
            ShoppingTransfer,
            recipe=recipe,
            user=request.user)
        shoppinglist.delete()
        return Response({'success': True})


class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = FavoriteRecipe.objects.all()
    serializer_class = FavoriteSerializer

    def perform_create(self, serializer):
        recipe = get_object_or_404(Recipe, pk=self.request.data.get('id'))
        serializer = FavoriteSerializer(data=self.request.data, context={
            'request_user': self.request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user, recipe=recipe)
        return Response({'success': True}, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        recipe = get_object_or_404(Recipe, pk=kwargs['pk'])
        favoriterecipe = get_object_or_404(
            FavoriteRecipe,
            recipe=recipe,
            user=request.user)
        favoriterecipe.delete()
        return Response({'success': True})


class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer

    def perform_create(self, serializer):
        author = get_object_or_404(User, pk=self.request.data.get('id'))
        serializer = FollowSerializer(data=self.request.data, context={
            'request_user': self.request.user,
            'author': author
        })
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user, author=author)
        return Response({'success': True}, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        author = get_object_or_404(User, pk=kwargs['pk'])
        follow = get_object_or_404(
            Follow,
            author=author,
            user=request.user)
        follow.delete()
        return Response({'success': True})
