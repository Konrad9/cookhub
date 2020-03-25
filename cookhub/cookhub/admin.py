from django.contrib import admin
from cookhub.models import UserModel, Recipe, Comment, Rating, Category, Ingredient

admin.site.register(UserModel)
admin.site.register(Recipe)
admin.site.register(Comment)
admin.site.register(Rating)
admin.site.register(Category)
admin.site.register(Ingredient)
