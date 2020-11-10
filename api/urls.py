from django.urls import path, include
from .views import (IngredientListView, api_purchase_detail,
                    api_favorite_detail, api_follow_detail)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()


router.register(r'ingredients', IngredientListView)
# router.register(r'purchases', PurchaseViewSet, basename='purchases')

urlpatterns = [
    path('purchases/<recipe_id>', api_purchase_detail),
    path('favorites/<recipe_id>', api_favorite_detail),
    path('subscriptions/<user_id>', api_follow_detail),
    path("", include(router.urls)),
]
