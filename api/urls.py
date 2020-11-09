from django.urls import path
from . import views


urlpatterns = [
    path("ingredients", views.Ingredients.as_view(), name="ingredients"),
    path("favorites", views.Favorites.as_view(), name="add_favor"),
    path(
        "favorites/<int:recipe_id>",
        views.Favorites.as_view(),
        name="remove_favor"
    ),
    path("subscriptions", views.Subscription.as_view(), name="add_subs"),
    path(
        "subscriptions/<int:author_id>",
        views.Subscription.as_view(),
        name="remove_subs",
    ),
    path(
        "purchases",
        views.Purchases.as_view(),
        name="add_to_shop"
    ),
    path(
        "purchases/<int:recipe_id>",
        views.Purchases.as_view(),
        name="remove_from_shop"
    ),
]