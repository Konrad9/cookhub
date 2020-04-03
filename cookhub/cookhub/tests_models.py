from django.test import TestCase
from cookhub.models import *

# Create your tests here.

class CategoryTestCase(TestCase):
    def setUp(self):
        Category.objects.create(name="Meat")
    
    def test_name_label(self):
        category = Category.objects.get(id=1)
        field_label = category._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'name')
    
    def test_number_of_recipes_label(self):
        category = Category.objects.get(id=1)
        field_label = category._meta.get_field('number_of_recipes').verbose_name
        self.assertEquals(field_label, 'number of recipes')
    
    def test_name_max_length(self):
        category = Category.objects.get(id=1)
        max_length = category._meta.get_field('name').max_length
        self.assertEquals(max_length, 20)
    
    def test_object_name_is_name(self):
        category = Category.objects.get(id=1)
        expected_object_name = category.name
        self.assertEquals(expected_object_name, str(category))


class RecipeTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username="username")
        Recipe.objects.create(user=user)
    
    def test_title_label(self):
        recipe = Recipe.objects.get(id=1)
        field_label = recipe._meta.get_field('title').verbose_name
        self.assertEquals(field_label, 'title')
    
    def test_description_label(self):
        recipe = Recipe.objects.get(id=1)
        field_label = recipe._meta.get_field('description').verbose_name
        self.assertEquals(field_label, 'description')
    
    def test_photo_label(self):
        recipe = Recipe.objects.get(id=1)
        field_label = recipe._meta.get_field('photo').verbose_name
        self.assertEquals(field_label, 'photo')
    
    def test_time_label(self):
        recipe = Recipe.objects.get(id=1)
        field_label = recipe._meta.get_field('time').verbose_name
        self.assertEquals(field_label, 'time')
    
    def test_averageRating_label(self):
        recipe = Recipe.objects.get(id=1)
        field_label = recipe._meta.get_field('averageRating').verbose_name
        self.assertEquals(field_label, 'averageRating')
    
    def test_servings_label(self):
        recipe = Recipe.objects.get(id=1)
        field_label = recipe._meta.get_field('servings').verbose_name
        self.assertEquals(field_label, 'servings')
    
    def test_creationDate_label(self):
        recipe = Recipe.objects.get(id=1)
        field_label = recipe._meta.get_field('creationDate').verbose_name
        self.assertEquals(field_label, 'creationDate')
    
    def test_views_label(self):
        recipe = Recipe.objects.get(id=1)
        field_label = recipe._meta.get_field('views').verbose_name
        self.assertEquals(field_label, 'views')
    
    def test_user_label(self):
        recipe = Recipe.objects.get(id=1)
        field_label = recipe._meta.get_field('user').verbose_name
        self.assertEquals(field_label, 'user')
    
    def test_categories_label(self):
        recipe = Recipe.objects.get(id=1)
        field_label = recipe._meta.get_field('categories').verbose_name
        self.assertEquals(field_label, 'categories')
    
    def test_title_max_length(self):
        recipe = Recipe.objects.get(id=1)
        max_length = recipe._meta.get_field('title').max_length
        self.assertEquals(max_length, 40)
    
    def test_description_max_length(self):
        recipe = Recipe.objects.get(id=1)
        max_length = recipe._meta.get_field('description').max_length
        self.assertEquals(max_length, 4000)
    
    def test_user_relation(self):
        recipe = Recipe.objects.get(id=1)
        user = User.objects.get(username='username')
        self.assertEquals(User.objects.get(recipe=recipe), user)
    
    def test_categories_relation(self):
        recipe = Recipe.objects.get(id=1)
        category = Category.objects.create(name="Meat")
        recipe.categories.add(category)
        recipe.save()
        self.assertTrue(recipe.categories.exists())
    
    def test_object_name_is_title_id(self):
        recipe = Recipe.objects.get(id=1)
        expected_object_name = recipe.title + str(recipe.id)
        self.assertEquals(expected_object_name, str(recipe))


class UserModelTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username="username")
        UserModel.objects.create(user=user)
    
    def test_user_label(self):
        user = User.objects.get_or_create(username="username")[0]
        userModel = UserModel.objects.get(user=user)
        field_label = userModel._meta.get_field('user').verbose_name
        self.assertEquals(field_label, 'user')
    
    def test_picture_label(self):
        user = User.objects.get_or_create(username="username")[0]
        userModel = UserModel.objects.get(user=user)
        field_label = userModel._meta.get_field('picture').verbose_name
        self.assertEquals(field_label, 'picture')
    
    def test_saved_recipes_label(self):
        user = User.objects.get_or_create(username="username")[0]
        userModel = UserModel.objects.get(user=user)
        field_label = userModel._meta.get_field('saved_recipes').verbose_name
        self.assertEquals(field_label, 'saved recipes')
    
    def test_user_relation(self):
        user = User.objects.get_or_create(username="username")[0]
        userModel = UserModel.objects.get(user=user)
        self.assertEquals(userModel.user, user)
    
    def test_saved_recipes_relation_exists(self):
        user = User.objects.get_or_create(username="username")[0]
        userModel = UserModel.objects.get(user=user)
        recipe = Recipe.objects.create(user=user)
        userModel.saved_recipes.add(recipe)
        userModel.save()
        self.assertTrue(userModel.saved_recipes.exists())
    
    def test_saved_recipes_relation(self):
        user = User.objects.get_or_create(username="username")[0]
        userModel = UserModel.objects.get(user=user)
        recipe = Recipe.objects.create(user=user)
        userModel.saved_recipes.add(recipe)
        userModel.save()
        self.assertEquals(userModel.saved_recipes.get(id=recipe.id), recipe)
    
    def test_object_name_is_username(self):
        user = User.objects.get_or_create(username="username")[0]
        userModel = UserModel.objects.get(user=user)
        expected_object_name = user.username
        self.assertEquals(expected_object_name, str(userModel))


class IngredientTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username="username")
        recipe = Recipe.objects.create(user=user)
        Ingredient.objects.create(recipe=recipe)
    
    def test_name_label(self):
        ingredient = Ingredient.objects.get(id=1)
        field_label = ingredient._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'name')
    
    def test_quantity_label(self):
        ingredient = Ingredient.objects.get(id=1)
        field_label = ingredient._meta.get_field('quantity').verbose_name
        self.assertEquals(field_label, 'quantity')
    
    def test_unit_label(self):
        ingredient = Ingredient.objects.get(id=1)
        field_label = ingredient._meta.get_field('unit').verbose_name
        self.assertEquals(field_label, 'unit')
    
    def test_recipe_label(self):
        ingredient = Ingredient.objects.get(id=1)
        field_label = ingredient._meta.get_field('recipe').verbose_name
        self.assertEquals(field_label, 'recipe')
    
    def test_name_max_length(self):
        ingredient = Ingredient.objects.get(id=1)
        max_length = Ingredient._meta.get_field('name').max_length
        self.assertEquals(max_length, 40)
    
    def test_unit_max_length(self):
        ingredient = Ingredient.objects.get(id=1)
        max_length = Ingredient._meta.get_field('unit').max_length
        self.assertEquals(max_length, 20)
    
    def test_recipe_relation(self):
        recipe = Recipe.objects.get(id=1)
        ingredient = Ingredient.objects.get(id=1)
        self.assertEquals(Recipe.objects.get(ingredient=ingredient), recipe)
    
    def test_object_name_is_name(self):
        ingredient = Ingredient.objects.get(id=1)
        expected_object_name = ingredient.name
        self.assertEquals(expected_object_name, str(ingredient))


class RatingTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username="username")
        recipe = Recipe.objects.create(user=user)
        Rating.objects.create(user=user, recipe=recipe)
    
    def test_user_label(self):
        user = User.objects.get_or_create(username="username")[0]
        recipe = Recipe.objects.get(id=1)
        rating = Rating.objects.get(user=user, recipe=recipe)
        field_label = rating._meta.get_field('user').verbose_name
        self.assertEquals(field_label, 'user')
    
    def test_recipe_label(self):
        user = User.objects.get_or_create(username="username")[0]
        recipe = Recipe.objects.get(id=1)
        rating = Rating.objects.get(user=user, recipe=recipe)
        field_label = rating._meta.get_field('recipe').verbose_name
        self.assertEquals(field_label, 'recipe')
    
    def test_rating_label(self):
        user = User.objects.get_or_create(username="username")[0]
        recipe = Recipe.objects.get(id=1)
        rating = Rating.objects.get(user=user, recipe=recipe)
        field_label = rating._meta.get_field('rating').verbose_name
        self.assertEquals(field_label, 'rating')
    
    def test_user_relation(self):
        user = User.objects.get_or_create(username="username")[0]
        recipe = Recipe.objects.get(id=1)
        rating = Rating.objects.get(user=user, recipe=recipe)
        self.assertEquals(User.objects.get(rating=rating), user)
    
    def test_recipe_relation(self):
        user = User.objects.get_or_create(username="username")[0]
        recipe = Recipe.objects.get(id=1)
        rating = Rating.objects.get(user=user, recipe=recipe)
        self.assertEquals(Recipe.objects.get(rating=rating), recipe)
    
    def test_user_recipe_unique_together(self):
        user = User.objects.get_or_create(username="username")[0]
        recipe = Recipe.objects.get(id=1)
        rating = Rating.objects.get(user=user, recipe=recipe)
        with self.assertRaises(Exception):
            rating_clone = Rating.objects.create(user=user, recipe=recipe)
    
    def test_object_name_is_rating(self):
        user = User.objects.get_or_create(username="username")[0]
        recipe = Recipe.objects.get(id=1)
        rating = Rating.objects.get(user=user, recipe=recipe)
        expected_object_name = str(rating.rating)
        self.assertEquals(expected_object_name, str(rating))


class CommentTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username="username")
        recipe = Recipe.objects.create(user=user)
        Comment.objects.create(user=user, recipe=recipe)
    
    def test_user_label(self):
        user = User.objects.get_or_create(username="username")[0]
        recipe = Recipe.objects.get(id=1)
        comment = Comment.objects.get(user=user, recipe=recipe)
        field_label = comment._meta.get_field('user').verbose_name
        self.assertEquals(field_label, 'user')
    
    def test_recipe_label(self):
        user = User.objects.get_or_create(username="username")[0]
        recipe = Recipe.objects.get(id=1)
        comment = Comment.objects.get(user=user, recipe=recipe)
        field_label = comment._meta.get_field('recipe').verbose_name
        self.assertEquals(field_label, 'recipe')
    
    def test_text_label(self):
        user = User.objects.get_or_create(username="username")[0]
        recipe = Recipe.objects.get(id=1)
        comment = Comment.objects.get(user=user, recipe=recipe)
        field_label = comment._meta.get_field('text').verbose_name
        self.assertEquals(field_label, 'text')
    
    def test_creationDate_label(self):
        user = User.objects.get_or_create(username="username")[0]
        recipe = Recipe.objects.get(id=1)
        comment = Comment.objects.get(user=user, recipe=recipe)
        field_label = comment._meta.get_field('creationDate').verbose_name
        self.assertEquals(field_label, 'creationDate')
    
    def test_user_relation(self):
        user = User.objects.get_or_create(username="username")[0]
        recipe = Recipe.objects.get(id=1)
        comment = Comment.objects.get(user=user, recipe=recipe)
        self.assertEquals(User.objects.get(comment=comment), user)
    
    def test_recipe_relation(self):
        user = User.objects.get_or_create(username="username")[0]
        recipe = Recipe.objects.get(id=1)
        comment = Comment.objects.get(user=user, recipe=recipe)
        self.assertEquals(Recipe.objects.get(comment=comment), recipe)
    
    def test_object_name_is_comment_plus_id(self):
        user = User.objects.get_or_create(username="username")[0]
        recipe = Recipe.objects.get(id=1)
        comment = Comment.objects.get(user=user, recipe=recipe)
        expected_object_name = comment.text + str(comment.id)
        self.assertEquals(expected_object_name, str(comment))