from rest_framework import serializers

from recipes.models import Ingredients, ShoppingList, FavoriteRecipe
from users.models import Follow


class IngredientsSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'title', 'dimension')
        model = Ingredients


class PurchaseSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    recipe = serializers.StringRelatedField()

    class Meta:
        fields = '__all__'
        model = ShoppingList


class FavoriteSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    recipe = serializers.StringRelatedField()

    class Meta:
        fields = '__all__'
        model = FavoriteRecipe


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    author = serializers.StringRelatedField()

    class Meta:
        fields = '__all__'
        model = Follow
