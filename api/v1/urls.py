from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (IngredientListView, FavoriteViewSet, FollowViewSet,
                    PurchaseViewSet)

router = DefaultRouter()


router.register(r'ingredients', IngredientListView)
router.register(r'purchases', PurchaseViewSet, basename='purchases')
router.register(r'favorites', FavoriteViewSet, basename='favorites')
router.register(r'subscriptions', FollowViewSet, basename='subscriptions')

urlpatterns = [
    path("", include(router.urls)),
]
