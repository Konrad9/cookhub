from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=20)
    
    class Meta:
        verbose_name_plural = 'categories'
    
    def __str__(self):
        return self.name


class Recipe(models.Model):
    title = models.CharField(max_length=40, blank=True, default='')
    description = models.TextField(max_length=4000, blank=True, default='')
    photo = models.ImageField(upload_to="recipe_images/", blank=True, default='default.jpg')
    time = models.IntegerField(blank=True, default=1)
    averageRating = models.FloatField(blank=True, default=0)
    servings = models.IntegerField(blank=True, default=1)
    creationDate = models.DateTimeField(blank=True, default=timezone.now)
    views = models.IntegerField(blank=True, default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category, blank=True, default=None)
    
    def __str__ (self):
        return self.title + str(self.id)
    
class UserModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    picture = models.ImageField(upload_to="profile_images/", blank=True, default="default.jpg")
    saved_recipes = models.ManyToManyField(Recipe, blank=True)
    
    def __str__(self):
        return self.user.username
    

class Ingredient(models.Model):
    name = models.CharField(max_length=40)
    quantity = models.IntegerField(default=0)
    unit = models.CharField(max_length=20, blank=True)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    
    class Meta:
        unique_together = ('user', 'recipe',)
    
    def __str__(self):
        return str(self.rating)

class Comment(models.Model):
    text = models.TextField(max_length=500)
    creationDate = models.DateField(blank=True, default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.text + str(self.id)

