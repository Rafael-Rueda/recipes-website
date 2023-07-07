from django.urls import path

from apps.authors import views

app_name = 'authors'

urlpatterns = [
    path(route = 'register/', view=views.register, name='register'),
    path('register/create/', views.register_create , name='create'),
    path('login/', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('authors/admin', views.authors_admin, name='authors-admin'),
    path('authors/admin/save', views.authors_admin_save, name='authors-admin-save'),
    path('authors/admin/recipe/<int:recipe_id>', views.authors_admin_recipe, name="authors-admin-recipe"),
    path('dashboard', views.dashboard, name='dashboard'),
    path('dashboard-update/<int:recipe_id>', views.dashboard_update, name='dashboard-update'),
    path('dashboard/create', views.dashboard_create, name='dashboard-create'),
    path('dashboard/delete/<int:recipe_id>', views.dashboard_delete, name='dashboard-delete'),
]