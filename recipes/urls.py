from django.urls import path
from .views import Download

from . import views


urlpatterns = [
    path('recipe/<int:recipe_id>/', views.recipe_view, name='recipe_view'),
    path('recipe/new', views.new_recipe, name='new_recipe'),
    path('recipe/<int:recipe_id>/edit', views.recipe_edit, name='recipe_edit'),
    path('recipe/<int:recipe_id>/delete',
         views.recipe_delete, name='recipe_delete'),
    path('recipe/favorites/', views.favorites_recipe, name='favorites'),
    path("followings/", views.follow, name='follow'),
    path('shopping-list/download', Download.as_view(), name='download'),
    path('shopping-list/', views.shopping_list, name='shopping-list'),
    path("<username>/", views.profile, name='profile'),
    path('', views.index, name='index'),
]
