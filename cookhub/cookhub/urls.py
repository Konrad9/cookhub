from django.urls import path
from cookhub import views
from cookhub.views import Homepage, EditProfileView, ProfileView, RecipeView, EditRecipeView

app_name = 'cookhub'

urlpatterns = [
    path('', Homepage.as_view(), name='homepage'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/<username>/edit', views.EditProfileView.as_view(), name='edit_profile'),
    path('profile/<username>/', views.ProfileView.as_view(), name='profile'),
    path('change_password/', views.change_password, name='change_password'),
    path('recipe/<recipe_id>/', RecipeView.as_view(),  name='recipe'),
    path('add_recipe/', views.create_recipe, name='create_recipe'),
    path('add_recipe/<recipe_id>/', views.add_recipe, name='add_recipe'),
    path('add_recipe/<recipe_id>/<ingredient_id>/', views.del_ingredient, name = 'del_ingredient'),
    path('recipe/<recipe_id>/edit/', EditRecipeView.as_view(), name='edit_recipe'),
    path('recipe/<recipe_id>/edit/<ingredient_id>/', views.del_editingredient, name='del_editingredient'),
]