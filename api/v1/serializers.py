from recipes.models import FavoriteRecipe, Ingredient, ShoppingTransfer
from rest_framework import serializers

from users.models import Follow


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'title', 'dimension')
        model = Ingredient


class PurchaseSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    recipe = serializers.StringRelatedField()

    class Meta:
        fields = '__all__'
        model = ShoppingTransfer

    def validate(self, data):
        super().validate(data)
        user = self.context.get('request_user')
        recipe = self.context.get('id')
        if ShoppingTransfer.objects.filter(user=user, recipe=recipe).exists():
            raise serializers.ValidationError('Already purchased')
        return data


class FavoriteSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    recipe = serializers.StringRelatedField()

    class Meta:
        fields = '__all__'
        model = FavoriteRecipe

    def validate(self, data):
        super().validate(data)
        user = self.context.get('request_user')
        recipe = self.context.get('id')
        if FavoriteRecipe.objects.filter(user=user, recipe=recipe).exists():
            raise serializers.ValidationError('Already added')
        return data


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    author = serializers.StringRelatedField()

    class Meta:
        fields = '__all__'
        model = Follow

    def validate(self, data):
        super().validate(data)
        user = self.context.get('request_user')
        author = self.context.get('author')
        if Follow.objects.filter(user=user, author=author).exists():
            raise serializers.ValidationError('subscriptions already created')
        return data
