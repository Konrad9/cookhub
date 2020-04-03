from django.urls import path
from cookhub import views

app_name = 'cookhub'

urlpatterns = [
    path('', views.Homepage.as_view(), name='homepage'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/<username>/', views.ProfileView.as_view(), name='profile'),
    path('profile/<username>/edit/', views.EditProfileView.as_view(), name='edit_profile'),
    path('profile/<username>/edit/change_password/', views.change_password, name='change_password'),
    path("getRecipesPagination/", views.PaginationView.as_view(), name="recipe_pagination"),
    path('recipe/<recipe_id>/', views.RecipeView.as_view(),  name='recipe'),
    path("save_recipe/", views.SavedRecipesView.as_view(), name="save_recipe"),
    path("remove_saved_recipe/", views.RemoveSavedRecipesView.as_view(), name="remove_saved_recipe"),
    path('add_recipe/', views.CreateRecipeView.as_view(), name='create_recipe'),
    path("add_category/", views.AddCategoryView.as_view(), name="add_category"),
    path('add_ingredient/', views.AddIngredientView.as_view(), name = "add_ingredient"),
    path('remove_ingredient/', views.RemoveIngredientView.as_view(), name = "remove_ingredient"),
    path('add_recipe/<recipe_id>/', views.add_recipe, name='add_recipe'),
    path('recipe/<recipe_id>/edit/', views.EditRecipeView.as_view(), name='edit_recipe'),
    path('recipe/<recipe_id>/edit/<ingredient_id>/', views.del_editingredient, name='del_editingredient'),
    path("recipe/<recipe_id>/delete/", views.DeleteRecipeView.as_view(), name="deleteRecipe"),
    path("categories/", views.CategoriesView.as_view(), name="all_categories"),
    path("search/", views.SearchView.as_view(), name="search"),
    path("search_query/", views.SearchQueryView.as_view(), name="search_query"),
    path("get_all_categories/", views.GetAllCategoriesView.as_view(), name="getAllCategories"),
    path("category/<category_id>/", views.CategoryView.as_view(), name="category"),
    path("recipes/<what>/", views.ViewAllRecipes.as_view(), name="view_all"),
]