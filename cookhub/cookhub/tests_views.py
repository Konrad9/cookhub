from django.test import TestCase
from django.urls import reverse
from cookhub.models import *
import os
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
import re

def add_category(name):
    category = Category.objects.get_or_create(name=name)[0]
    return category

def add_user(username, email, first_name, last_name, password):
    user = User.objects.get_or_create(username=username, first_name=first_name, last_name=last_name, password=password)[0]
    return user

def add_recipe(title, description, time, servings, user):
    recipe = Recipe.objects.get_or_create(title=title, description=description, time = time, servings=servings, user=user)[0]
    return recipe

def add_userModel(user):
    userModel = UserModel.objects.get_or_create(user=user)[0]
    return userModel

def add_ingredient(name, quantity, unit, recipe):
    ingredient = Ingredient.objects.get_or_create(name=name, quantity=quantity, unit=unit, recipe=recipe)[0]
    return ingredient

def add_rating(rating, recipe, user):
    rating = Rating.objects.get_or_create(rating=rating, recipe=recipe, user=user)[0]
    return rating

def add_comment(text, recipe, user):
    comment = Comment.objects.get_or_create(text=text, recipe=recipe, user=user)[0]
    return comment

class HomepageViewTestCase(TestCase):
    def test_homepage_view_with_no_categories(self):
        response = self.client.get(reverse('cookhub:homepage'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'There are no categories present')
        self.assertQuerysetEqual(response.context['categories'], [])
    
    def test_homepage_view_with_no_recipes(self):
        response = self.client.get(reverse('cookhub:homepage'))
        
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['popularRecipes'], [])
        self.assertQuerysetEqual(response.context['newestRecipes'], [])
    
    def test_homepage_view_with_anonymous_user(self):
        response = self.client.get(reverse('cookhub:homepage'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'You are not logged in')
        self.assertContains(response, 'Register')
        self.assertContains(response, 'Login')
    
    def test_homepage_view_with_categories(self):
        add_category('Beef')
        add_category('Vegan')
        add_category('Fish')
        
        response = self.client.get(reverse('cookhub:homepage'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Beef')
        self.assertContains(response, 'Vegan')
        self.assertContains(response, 'Fish')
        num_categories = len(response.context['categories'])
        self.assertEquals(num_categories, 3)
    
    def test_homepage_view_with_recipes(self):
        user = add_user('username', 'bob@gmail.com', 'Bob', 'Bobbington', 'g00gl315b4d')
        add_recipe('Meatballs', 'Make a bunch of Meatballs', 10, 1, user)
        add_recipe('Vegeballs', 'Make a bunch of Vegeballs', 10, 1, user)
        add_recipe('Fishballs', 'Make a bunch of Fishballs', 10, 1, user)
        
        response = self.client.get(reverse('cookhub:homepage'))
        self.assertEqual(response.status_code, 200)
        num_popularRecipes = len(response.context['popularRecipes'])
        num_newestRecipes = len(response.context['newestRecipes'])
        self.assertEquals(num_popularRecipes, 3)
        self.assertEquals(num_newestRecipes, 3)
    
    def test_homepage_view_with_logged_in_user(self):
        user = add_user('username', 'bob@gmail.com', 'Bob', 'Bobbington', 'g00gl315b4d')
        add_userModel(user)
        self.client.force_login(user)
        
        response = self.client.get(reverse('cookhub:homepage'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Welcome back, '+user.username)
        self.assertContains(response, 'New Recipe')
        self.assertContains(response, 'My Profile')
        self.assertContains(response, 'Logout')
        

class RecipeViewTestCase(TestCase):
    def test_recipe_view_no_categories(self):
        user = add_user('username', 'bob@gmail.com', 'Bob', 'Bobbington', 'g00gl315b4d')
        recipe = add_recipe('Meatballs', 'Make a bunch of Meatballs', 10, 1, user)
        add_userModel(user)
        
        response = self.client.get(reverse('cookhub:recipe', kwargs={'recipe_id':recipe.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This recipe is not part of any categories')
        self.assertQuerysetEqual(response.context['categories'], [])
    
    def test_recipe_view_no_ingredients(self):
        user = add_user('username', 'bob@gmail.com', 'Bob', 'Bobbington', 'g00gl315b4d')
        recipe = add_recipe('Meatballs', 'Make a bunch of Meatballs', 10, 1, user)
        add_userModel(user)
        
        response = self.client.get(reverse('cookhub:recipe', kwargs={'recipe_id':recipe.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No ingredients in this recipe')
        self.assertQuerysetEqual(response.context['ingredients'], [])
    
    def test_recipe_view_no_comments(self):
        user = add_user('username', 'bob@gmail.com', 'Bob', 'Bobbington', 'g00gl315b4d')
        recipe = add_recipe('Meatballs', 'Make a bunch of Meatballs', 10, 1, user)
        add_userModel(user)
        
        response = self.client.get(reverse('cookhub:recipe', kwargs={'recipe_id':recipe.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'There are no comments on this recipe')
        self.assertQuerysetEqual(response.context['comments'], [])
    
    def test_recipe_view_no_ratings(self):
        user = add_user('username', 'bob@gmail.com', 'Bob', 'Bobbington', 'g00gl315b4d')
        recipe = add_recipe('Meatballs', 'Make a bunch of Meatballs', 10, 1, user)
        add_userModel(user)
        
        response = self.client.get(reverse('cookhub:recipe', kwargs={'recipe_id':recipe.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Rating: 0.0')
        self.assertQuerysetEqual(response.context['ratings'], [])
    
    def test_recipe_view_with_anonymous_user(self):
        user = add_user('username', 'bob@gmail.com', 'Bob', 'Bobbington', 'g00gl315b4d')
        recipe = add_recipe('Meatballs', 'Make a bunch of Meatballs', 10, 1, user)
        add_userModel(user)
        
        response = self.client.get(reverse('cookhub:recipe', kwargs={'recipe_id':recipe.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'You are not logged in')
        self.assertContains(response, 'Register')
        self.assertContains(response, 'Login')
    
    def test_recipe_view_with_categories(self):
        user = add_user('username', 'bob@gmail.com', 'Bob', 'Bobbington', 'g00gl315b4d')
        recipe = add_recipe('Meatballs', 'Make a bunch of Meatballs', 10, 1, user)
        add_userModel(user)
        category = add_category('Meatballs')
        recipe.categories.add(category)
        category2 = add_category('Beef')
        recipe.categories.add(category2)
        recipe.save()
        
        response = self.client.get(reverse('cookhub:recipe', kwargs={'recipe_id':recipe.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Meatballs')
        self.assertContains(response, 'Beef')
        num_categories = len(response.context['categories'])
        self.assertEquals(num_categories, 2)
    
    def test_recipe_view_with_ingredients(self):
        user = add_user('username', 'bob@gmail.com', 'Bob', 'Bobbington', 'g00gl315b4d')
        recipe = add_recipe('Meatballs', 'Make a bunch of Meatballs', 10, 1, user)
        add_userModel(user)
        ingredient1 = add_ingredient('Minced Beef', 200, 'g', recipe)
        ingredient2 = add_ingredient('Herbs', 5, 'g', recipe)
        
        response = self.client.get(reverse('cookhub:recipe', kwargs={'recipe_id':recipe.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, str(ingredient1.quantity)+' '+ingredient1.unit+' '+ingredient1.name)
        self.assertContains(response, str(ingredient2.quantity)+' '+ingredient2.unit+' '+ingredient2.name)
        num_ingredients = len(response.context['ingredients'])
        self.assertEquals(num_ingredients, 2)
    
    def test_recipe_view_with_comments(self):
        user = add_user('username', 'bob@gmail.com', 'Bob', 'Bobbington', 'g00gl315b4d')
        recipe = add_recipe('Meatballs', 'Make a bunch of Meatballs', 10, 1, user)
        add_userModel(user)
        comment1 = add_comment('This is awesome', recipe, user)
        comment2 = add_comment('MEATBALLS', recipe, user)
        
        response = self.client.get(reverse('cookhub:recipe', kwargs={'recipe_id':recipe.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, comment1.text)
        self.assertContains(response, comment2.text)
        num_comments = len(response.context['comments'])
        self.assertEquals(num_comments, 2)
    
    def test_recipe_view_with_ratings(self):
        user = add_user('username', 'bob@gmail.com', 'Bob', 'Bobbington', 'g00gl315b4d')
        recipe = add_recipe('Meatballs', 'Make a bunch of Meatballs', 10, 1, user)
        add_userModel(user)
        user2 = add_user('username2', 'bob@gmail.com', 'Bob', 'Bobbington', 'g00gl315b4d')
        user3 = add_user('username3', 'bob@gmail.com', 'Bob', 'Bobbington', 'g00gl315b4d')
        add_userModel(user2)
        rating1 = add_rating(5, recipe, user3)
        rating2 = add_rating(4, recipe, user2)
        
        response = self.client.get(reverse('cookhub:recipe', kwargs={'recipe_id':recipe.id}))
        self.assertEqual(response.status_code, 200)
        num_ratings = len(response.context['ratings'])
        self.assertEquals(num_ratings, 2)
    
    def test_recipe_view_with_logged_in_user(self):
        user = add_user('username', 'bob@gmail.com', 'Bob', 'Bobbington', 'g00gl315b4d')
        recipe = add_recipe('Meatballs', 'Make a bunch of Meatballs', 10, 1, user)
        add_userModel(user)
        self.client.force_login(user)
        
        response = self.client.get(reverse('cookhub:recipe', kwargs={'recipe_id':recipe.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Welcome back, '+user.username)
        self.assertContains(response, 'New Recipe')
        self.assertContains(response, 'My Profile')
        self.assertContains(response, 'Logout')
        self.assertContains(response, 'Save Recipe')
    
    def test_recipe_view_with_logged_in_creator(self):
        user = add_user('username', 'bob@gmail.com', 'Bob', 'Bobbington', 'g00gl315b4d')
        recipe = add_recipe('Meatballs', 'Make a bunch of Meatballs', 10, 1, user)
        add_userModel(user)
        self.client.force_login(user)
        
        response = self.client.get(reverse('cookhub:recipe', kwargs={'recipe_id':recipe.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Welcome back, '+user.username)
        self.assertContains(response, 'New Recipe')
        self.assertContains(response, 'My Profile')
        self.assertContains(response, 'Logout')
        self.assertContains(response, 'Save Recipe')
        self.assertContains(response, 'Delete Recipe')

class ViewAllRecipesNewestTestCase(TestCase):
    def test_viewAllRecipesNewest_view_no_recipes(self):
        response = self.client.get(reverse('cookhub:view_all', kwargs={'what':'newest'}))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No recipes present')
        self.assertQuerysetEqual(response.context['recipes'], [])
    
    def test_viewAllRecipesNewest_view_with_recipes(self):
        user = add_user('username', 'bob@gmail.com', 'Bob', 'Bobbington', 'g00gl315b4d')
        add_recipe('Meatballs', 'Make a bunch of Meatballs', 10, 1, user)
        add_recipe('Vegeballs', 'Make a bunch of Vegeballs', 10, 1, user)
        add_recipe('Fishballs', 'Make a bunch of Fishballs', 10, 1, user)
        
        response = self.client.get(reverse('cookhub:view_all', kwargs={'what':'newest'}))
        self.assertEqual(response.status_code, 200)
        num_newestRecipes = len(response.context['recipes'])
        self.assertEquals(num_newestRecipes, 3)
    
    def test_viewAllRecipesNewest_view_with_anonymous_user(self):
        response = self.client.get(reverse('cookhub:view_all', kwargs={'what':'newest'}))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'You are not logged in')
        self.assertContains(response, 'Register')
        self.assertContains(response, 'Login')
    
    def test_viewAllRecipesNewest_view_with_logged_in_user(self):
        user = add_user('username', 'bob@gmail.com', 'Bob', 'Bobbington', 'g00gl315b4d')
        add_userModel(user)
        self.client.force_login(user)
        
        response = self.client.get(reverse('cookhub:view_all', kwargs={'what':'newest'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Welcome back, '+user.username)
        self.assertContains(response, 'New Recipe')
        self.assertContains(response, 'My Profile')
        self.assertContains(response, 'Logout')

class ViewAllRecipesMostPopularTestCase(TestCase):
    def test_viewAllRecipesMostPopular_view_no_recipes(self):
        response = self.client.get(reverse('cookhub:view_all', kwargs={'what':'popular'}))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No recipes present')
        self.assertQuerysetEqual(response.context['recipes'], [])
    
    def test_viewAllRecipesMostPopular_view_with_recipes(self):
        user = add_user('username', 'bob@gmail.com', 'Bob', 'Bobbington', 'g00gl315b4d')
        add_recipe('Meatballs', 'Make a bunch of Meatballs', 10, 1, user)
        add_recipe('Vegeballs', 'Make a bunch of Vegeballs', 10, 1, user)
        add_recipe('Fishballs', 'Make a bunch of Fishballs', 10, 1, user)
        
        response = self.client.get(reverse('cookhub:view_all', kwargs={'what':'popular'}))
        self.assertEqual(response.status_code, 200)
        num_popularRecipes = len(response.context['recipes'])
        self.assertEquals(num_popularRecipes, 3)
    
    def test_viewAllRecipesMostPopular_view_with_anonymous_user(self):
        response = self.client.get(reverse('cookhub:view_all', kwargs={'what':'popular'}))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'You are not logged in')
        self.assertContains(response, 'Register')
        self.assertContains(response, 'Login')
    
    def test_viewAllRecipesMostPopular_view_with_logged_in_user(self):
        user = add_user('username', 'bob@gmail.com', 'Bob', 'Bobbington', 'g00gl315b4d')
        add_userModel(user)
        self.client.force_login(user)
        
        response = self.client.get(reverse('cookhub:view_all', kwargs={'what':'popular'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Welcome back, '+user.username)
        self.assertContains(response, 'New Recipe')
        self.assertContains(response, 'My Profile')
        self.assertContains(response, 'Logout')

class CategoriesViewTestCase(TestCase):
    def test_category_view_no_recipes(self):
        category = add_category('Meatball')
        response = self.client.get(reverse('cookhub:category', kwargs={'category_id':category.id}))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No recipes present!')
        self.assertQuerysetEqual(response.context['recipes'], [])
    
    def test_category_view_with_anonymous_user(self):
        category = add_category('Meatball')
        response = self.client.get(reverse('cookhub:category', kwargs={'category_id':category.id}))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'You are not logged in')
        self.assertContains(response, 'Register')
        self.assertContains(response, 'Login')
    
    def test_category_view_with_recipes(self):
        category = add_category('Meatball')
        user = add_user('username', 'bob@gmail.com', 'Bob', 'Bobbington', 'g00gl315b4d')
        recipe = add_recipe('Meatballs', 'Make a bunch of Meatballs', 10, 1, user)
        recipe.categories.add(category)
        recipe.save()
        response = self.client.get(reverse('cookhub:category', kwargs={'category_id':category.id}))
        
        self.assertEqual(response.status_code, 200)
        num_recipes = len(response.context['recipes'])
        self.assertEquals(num_recipes, 1)
    
    def test_category_view_with_logged_in_user(self):
        user = add_user('username', 'bob@gmail.com', 'Bob', 'Bobbington', 'g00gl315b4d')
        add_userModel(user)
        self.client.force_login(user)
        category = add_category('Meatball')
        
        response = self.client.get(reverse('cookhub:category', kwargs={'category_id':category.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Welcome back, '+user.username)
        self.assertContains(response, 'New Recipe')
        self.assertContains(response, 'My Profile')
        self.assertContains(response, 'Logout')

class CategoriesViewTestCase(TestCase):
    def test_categories_view_no_categories(self):
        response = self.client.get(reverse('cookhub:all_categories'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['categories'], [])
    
    def test_categories_view_with_anonymous_user(self):
        response = self.client.get(reverse('cookhub:all_categories'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'You are not logged in')
        self.assertContains(response, 'Register')
        self.assertContains(response, 'Login')
    
    def test_categories_view_with_categories(self):
        category1 = add_category('Meatball')
        category2 = add_category('Fishball')
        category3 = add_category('Vegeball')
        response = self.client.get(reverse('cookhub:all_categories'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Meatball')
        self.assertContains(response, 'Fishball')
        self.assertContains(response, 'Vegeball')
        num_categories = len(response.context['categories'])
        self.assertEquals(num_categories, 3)
    
    def test_category_view_with_logged_in_user(self):
        user = add_user('username', 'bob@gmail.com', 'Bob', 'Bobbington', 'g00gl315b4d')
        add_userModel(user)
        self.client.force_login(user)
        
        response = self.client.get(reverse('cookhub:all_categories'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Welcome back, '+user.username)
        self.assertContains(response, 'New Recipe')
        self.assertContains(response, 'My Profile')
        self.assertContains(response, 'Logout')

'''
class SearchQueryViewTestCase(TestCase):
    def test_searchQueryViewTestCase_view_no_recipes(self):
        response = self.client.get(reverse('cookhub:search_query'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No recipes present')
        self.assertEquals(response.context['NumberOfPages'], 0)
'''





