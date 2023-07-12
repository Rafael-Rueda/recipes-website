from django.urls import path

from apps.recipes import views

app_name = 'recipes'

urlpatterns = [
    path(route = '', view = views.home, name='home'),
    path('recipes/search', views.search, name='search' ),
    path('recipes/<int:id>', views.recipe, name='recipe'),
    path('recipes/category/<int:category_id>', views.category, name='category'),
    path('recipes/api/v1', views.recipesAPIv1, name='recipes-api-v1'),
    path('recipes/api/v1/<int:id>', views.recipeAPIv1, name='recipe-api-v1'),
]
