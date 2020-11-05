from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path("recipe/<username>/", views.profile, name='profile'),
    path('new-recipe', views.new_recipe, name='new_recipe'),
    path('recipe/<int:recipe_id>/edit', views.recipe_edit, name='recipe_edit'),
    path('recipe/<int:recipe_id>/delete', views.recipe_delete, name='recipe_delete'),
    path('recipe/<username>/<int:recipe_id>/', views.recipe_view, name='recipe_view'),
    path("follow/<username>/", views.follow, name='follow'),
    path('followrecipe/<username>/', views.follow_recipe, name='followrecipe'),
    path('shopping-list/', views.shopping_list, name='shopping-list'),
    path('download', views.download, name='download'),
]