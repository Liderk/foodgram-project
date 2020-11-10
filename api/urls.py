from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (IngredientListView, api_favorite_detail, api_follow_detail,
                    api_purchase_detail)

router = DefaultRouter()


router.register(r'ingredients', IngredientListView)

urlpatterns = [
    path('purchases/<recipe_id>', api_purchase_detail),
    path('favorites/<recipe_id>', api_favorite_detail),
    path('subscriptions/<user_id>', api_follow_detail),
    path("", include(router.urls)),
]
