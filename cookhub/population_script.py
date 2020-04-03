#import cookhub_project.settings as settings
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
'cookhub_project.settings')

import django 
django.setup()
from django.core.files import File
from cookhub_project.settings import STATIC_DIR

from cookhub.models import UserModel, Recipe, Ingredient, Comment, Category, Rating
from django.contrib.auth.models import User
import random

def populate():
    
    # create a new superuser
    superUsername = "cookhubSuperUser"
    superPassword = "Cookhub-app"
    print("Creating new superuser...\n")
    superUser = User.objects.get_or_create(username=superUsername)[0]
    superUser.set_password(superPassword)
    superUser.is_superuser = True
    superUser.is_staff = True
    superUser.save()
    UserModel.objects.get_or_create(user=superUser)[0].save()
    
    photoFiles = {
        "users": ["user1DEMO.jpg", "user2DEMO.jpg", "user3DEMO.jpg", "user4DEMO.jpg", "user5DEMO.jpg"],
        "recipes": ["bakedchickenDEMO.jpg", "bbqDEMO.jpg", "fastfoodDEMO.jpg", "fruitbasketDEMO.jpg", "greeksaladDEMO.jpg",
                 "paellaDEMO.jpg", "quicheDEMO.jpg", "seafoodsoupDEMO.jpg", "tanzaniantakeoutDEMO.jpg", "tomatosaladDEMO.jpg"]
        }
    
    users = [
        {"first_name": "Steve", "last_name": "Imbil", "email": "a@b.cd", "password": "Aa111111"},
        {"first_name": "Peter", "last_name": "Style", "email": "a@b.ef", "password": "Aa111112"},
        {"first_name": "Hanna", "last_name": "Glass", "email": "a@b.gh", "password": "Aa111113"},
        {"first_name": "Richy", "last_name": "Cooks", "email": "a@b.ij", "password": "Aa111114"},
        {"first_name": "Magda", "last_name": "Longe", "email": "a@b.kl", "password": "Aa111115"},
        ]
    
    categoriesNamesList = ["Lunch", "Takeout", "Fruity", "Salad", "Greek", "Spanish", "African", "Vegetables", "Healthy", "Dessert",
                  "Brunch", "Breakfast", "Vegan", "Vegetarian", "Fish", "English", "Soup", "Summery", "Child friendly", "Easy"]
    
    recipes = ["Baked chicken", "BBQ", "Fast food", "Fruit basket", "Greek salad",
               "Paella", "Quiche", "Seafood soup", "Tanzanian takout", "Tomato salad"]
    
    ingredientsList = [
        {"name": "Chicken", "quantity": 1, "unit": "kg"}, 
        {"name": "Meat", "quantity": 300, "unit": "g"}, 
        {"name": "Prawns", "quantity": 5, "unit": ""}, 
        {"name": "Fruit", "quantity": 4, "unit": "lb"}, 
        {"name": "Rice", "quantity": 1, "unit": "pack"}, 
        {"name": "Egg", "quantity": 8, "unit": ""}, 
        {"name": "Broth", "quantity": 1, "unit": "litre"}, 
        {"name": "Tomato", "quantity": 8, "unit": ""},
        {"name": "Onion", "quantity": 3, "unit": ""}, 
        ]
    
    commentsList = ["Great", "Good", "Tasty", "can recommend!", "Would do it again, very tasty"]
    
    populationPath = os.path.join(STATIC_DIR, "population")
    
    # get the lorem ipsum recipe descriptions
    recipeDescriptions = []
    with open(os.path.join(populationPath, "loremipsum.txt"), "r") as f:
        recipeDescriptions = f.read().split("\n\n")
    
    print("\nAdding users:")
    # create the users and their UserModels
    userList = []
    for i in range(len(users)):
        username = "user"+str(i+1)
        first_name = users[i].get("first_name")
        last_name = users[i].get("last_name")
        email = users[i].get("email")
        password = users[i].get("password")
        user, exists = User.objects.get_or_create(username=username,
                                        first_name=first_name,
                                        last_name=last_name,
                                        email=email)
        user.set_password(password)
        if not exists: # if the user already exists (since the script has been run already), resume with next user
            continue
        user.save()
        userList += [user]
        usrMdl = UserModel.objects.get_or_create(user=user)[0]
        photoSource = photoFiles.get("users")[i]
        photo = open(os.path.join(populationPath, photoSource), "rb")
        usrMdl.picture.save(photoSource, File(photo), save=True)
        photo.close()
        print("- "+username)
        
    if not userList:
        print("The script has been run already, since all sample users already exist.\nDelete database and migrate again to redo.\nExiting the population script.")
        return 
    
    random.seed(1)
    
    print("\nCreating categories:")
    # create the categories
    categoriesList = []
    for name in categoriesNamesList:
        cat = Category.objects.get_or_create(name=name)[0]
        cat.save()
        categoriesList += [cat]
        print("- "+name)
        
    recipeList = []
    # create the recipes
    print("\nCreating Recipes:")
    for i in range(len(recipes)):
        title = recipes[i]
        description = recipeDescriptions[random.randrange(0, len(recipeDescriptions))]
        photoSource = photoFiles.get("recipes")[i]
        photoFile = open(os.path.join(populationPath, photoSource), "rb")
        photo = File(photoFile)
        time = random.randrange(1,100)
        averageRating = float("{:.1f}".format(random.uniform(0.0, 5.0)))
        servings = random.randrange(1, 10)
        views = random.randrange(1, 1000)
        userListIndex = random.randrange(0, len(userList))
        user = userList[userListIndex]
        length = len(categoriesList)
        categories = [categoriesList[random.randrange(0, length)%(length-1)], 
                      categoriesList[random.randrange(0, length)%(length-1)-1]
                      ]
        recipe, exists = Recipe.objects.get_or_create(user=user,
                        title=title,
                        time=time,
                        description=description,
                        servings=servings,
                        views=views)
        if not exists: # if the recipe already exists (since the script has been run already), resume with next recipe
            continue
        rating = Rating.objects.get_or_create(user=userList[userListIndex-1],
                                              recipe=recipe,
                                              rating=averageRating)[0]
        rating.save()
        recipe.averageRating = averageRating
        # add the to categories
        for cat in categories:
            if not recipe.categories.filter(name=cat.name).exists():
                recipe.categories.add(cat)
                cat.number_of_recipes += 1
                cat.save()
        recipe.photo.save(photoSource, photoFile, save=True)
        recipeList += [recipe]
        
        # add it to a saved list of a random user
        usrMdl = UserModel.objects.get(user=random.choice(userList))
        usrMdl.saved_recipes.add(recipe)
        usrMdl.save()
        
        # add an ingredient 
        length = len(ingredientsList)
        ingredientDict = random.choice(ingredientsList)
        ingredient = Ingredient.objects.get_or_create(recipe=recipe,
                                name=ingredientDict.get("name"),
                                quantity=ingredientDict.get("quantity"),
                                unit = ingredientDict.get("unit"))[0]
        ingredient.save()
        
        # add a comment
        comment = Comment.objects.get_or_create(text=random.choice(commentsList),
                user=random.choice(userList),
                recipe=recipe)[0]
        comment.save()
        
        print("- "+title)
        
    print("\nPopulation successfully executed.")


if __name__ == '__main__':
    print('Starting Cookhub population script...')
    populate()