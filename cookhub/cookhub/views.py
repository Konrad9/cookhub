from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from cookhub.forms import UserForm, UserProfileForm, RecipeForm, RatingForm, CommentForm, IngredientForm, CategoryForm, IngredientArrayForm, ChangePasswordForm
from cookhub.models import UserModel, Recipe, Rating, Comment, Ingredient, Category, IngredientArray
from django.utils import timezone


class Homepage(View):
    def get(self, request):
        context_dict = {}
        saved = []
        
        context_dict['newestRecipes'] = Recipe.objects.order_by('-creationDate')
        context_dict['popularRecipes'] = Recipe.objects.order_by('-views')
        n = len(Recipe.objects.order_by('-creationDate'))
        context_dict["NewestRecipePages"] = n//3
        if n//3!=n/3:
            context_dict["NewestRecipePages"] += 1
        n = len(Recipe.objects.order_by('-views'))
        context_dict["PopularRecipePages"] = n//3
        if n//3!=n/3:
            context_dict["PopularRecipePages"] += 1
        if request.user.is_authenticated:
            userProfile = UserModel.objects.get(user=request.user)
            savedRecipes = userProfile.saved_recipes.all()
            for recipe in context_dict['newestRecipes']:
                if recipe in savedRecipes:
                    saved += [recipe.id]
            for recipe in context_dict['popularRecipes']:
                if recipe in savedRecipes:
                    saved += [recipe.id]
        context_dict["saved"] = saved
        print("Newest pages: " + str(context_dict["NewestRecipePages"]))
        print("Popular pages: " + str(context_dict["PopularRecipePages"]))
        response = render(request, 'cookhub/homepage.html', context=context_dict)
        return response

def register(request):
    # A boolean telling the template whether the registration was succesful, 
    # set initially to false. Code changes it to true 
    # once the registration is complete.
    registered = False

    # If it is a HTTP post, we are interested in processing form data.
    if request.method == "POST":
        # Attempt to grap information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)

        # If the two forms are valid:
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserModel instance.
            # Since we need to set the user attribute ourselves,
            # we set commit=False, which delays saving the model 
            # until we are ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # If the user provided a profile picture, we need to 
            # get it from the input form and put it in the UserModel model.
            if "picture" in request.FILES:
                profile.picture = request.FILES["picture"]

            # Now save the UserModel model instance.
            profile.save()

            # Update our variable to indicate that the template
            # registration was successful.
            registered = True
            login(request, user)
            return redirect(reverse("cookhub:homepage"))
        else:
            # Invalid form(s): print problems to terminal.
            print(user_form.errors, profile_form.errors)

    else:
        # Not a HTTP post, so we render our form using two ModelForm instances.
        # These forms will be blank, ready for user input.
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render(request, "registration/register.html", context={"user_form": user_form,
                                                                  "profile_form": profile_form,
                                                                  "registered": registered})


def user_login(request):
    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':

        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        # We use request.POST.get('<variable>') as opposed
        # to request.POST['<variable>'], because the
        # request.POST.get('<variable>') returns None if the
        # value does not exist, while request.POST['<variable>']
        # will raise a KeyError exception.
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember = request.POST.get("rememberme")

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                if remember!="remember-me":
                    request.session.set_expiry(0)
                return redirect(reverse('cookhub:homepage'))
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your Cookhub account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP get.
    else:
        # No context variables to pass to the template system, hence the 
        # blank dictionary object.
        return render(request, "registration/login.html")


def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val

# Updated the function definition
def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request, 'visits', '1'))
    last_visit_cookie = get_server_side_cookie(request,'last_visit',str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')
    # If it's been more than a day since the last visit...
    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        # Update the last visit cookie now that we have updated the count
        request.session['last_visit'] = str(datetime.now())
    else:
        # Set the last visit cookie
        request.session['last_visit'] = last_visit_cookie
        # Update/set the visits cookie
        request.session['visits'] = visits


@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    # Take the user back to the homepage.
    return redirect(reverse('cookhub:homepage'))


class EditProfileView(View):
    def get_user_details(self, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None

        user_profile = UserModel.objects.get_or_create(user=user)[0]
        form = UserProfileForm({'picture': user_profile.picture})
        return (user, user_profile, form)

    @method_decorator(login_required)
    def get(self, request, username):
        print("here edit\n")
        try:
            (user, user_profile, form) = self.get_user_details(username)
        except TypeError:
            return redirect(reverse('cookhub:homepage'))

        context_dict = {'user_profile': user_profile,
                        'selected_user': user,
                        'form': form}
        return render(request, 'cookhub/edit_profile.html', context_dict)

    @method_decorator(login_required)
    def post(self, request, username):
        try:
            (user, user_profile, form) = self.get_user_details(username)
        except TypeError:
            return redirect(reverse('cookhub:homepage'))

        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save(commit=True)
            return redirect('cookhub:profile', user.username)
        else:
            print(form.errors)

        context_dict = {'user_profile': user_profile,
                        'selected_user': user,
                        'form': form}
        return render(request, 'cookhub/edit_profile.html', context_dict)


class ProfileView(View):

    def get_user_details(self, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None

        user_profile = UserModel.objects.get_or_create(user=user)[0]
        form = UserProfileForm({'picture': user_profile.picture})
        return (user, user_profile, form)

    def get(self, request, username):
        try:
            (user, user_profile, form) = self.get_user_details(username)
        except TypeError:
            return redirect(reverse('cookhub:homepage'))
        
        context_dict = {'user_profile': user_profile,
                        'selected_user': user, }
        
        MyRecipeList = Recipe.objects.filter(user=user).order_by('-creationDate')        
        n = len(MyRecipeList)
        context_dict["MyRecipePages"] = n//3
        if n//3!=n/3:
            context_dict["MyRecipePages"] += 1
        
        savedRecipeList = user_profile.saved_recipes.all()
        n = len(savedRecipeList)
        context_dict["SavedRecipePages"] = n//3
        if n//3!=n/3:
            context_dict["SavedRecipePages"] += 1
        print("saved recipes: " + str(3//3))
        
        return render(request, 'cookhub/profile.html', context_dict)


    @method_decorator(login_required)
    def post(self, request, username):
        try:
            (user, user_profile, form) = self.get_user_details(username)
        except TypeError:
            return redirect(reverse('cookhub:homepage'))

        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)

        if form.is_valid():
            newmail = request.POST.get("email")
            user.email = newmail
            user.save()
            form.save(commit=True)
            return redirect('cookhub:profile', user.username)
        else:
            print(form.errors)

        context_dict = {'user_profile': user_profile,
                        'selected_user': user,
                        'form': form}
        return render(request, 'cookhub/profile.html', context_dict)



@login_required
def change_password(request, username):

    if request.method == "POST":
        form = ChangePasswordForm(request.POST)

        if form.is_valid():
            # Hash the password with the set_password method.
            # Once hashed, we can update the user object.
            request.user.set_password(request.POST.get("password"))
            request.user.save()
            login(request, request.user)
            return redirect('cookhub:edit_profile', request.user.username)
        else:
            print(form.errors)

    else:
        # Not a HTTP post, so we render the form
        form = ChangePasswordForm()
    print("about to render change_password.html")
    return render(request, "registration/change_password.html", context = {"form":form})
  

class RecipeView(View):
    def get_recipe_details(self, recipe_id):
        try:
            recipe = Recipe.objects.get(id=recipe_id)
            ingredients = Ingredient.objects.filter(recipe=recipe)
            categories = recipe.categories.all()
            comments = Comment.objects.filter(recipe=recipe)
            ratings = Rating.objects.filter(recipe=recipe)
            creator = recipe.user
            user_profile = UserModel.objects.get(user=creator)
            rating_form = RatingForm()
            comment_form = CommentForm()
            
        except Recipe.DoesNotExist:
            return None
        
        context_dict = {}
        context_dict['ingredients'] = ingredients
        context_dict['categories'] = categories
        context_dict['comments'] = comments
        context_dict['ratings'] = ratings
        context_dict['creator'] = creator
        context_dict["profile_picture"] = user_profile.picture
        context_dict['recipe'] = recipe
        context_dict['rating_form'] = rating_form
        context_dict['comment_form'] = comment_form
        return context_dict
    
    def get (self, request, recipe_id):
        try: 
            context_dict = self.get_recipe_details(recipe_id=recipe_id)
        except TypeError:
            return redirect(reverse('cookhub:homepage'))
        if request.user!=context_dict['creator']:
            context_dict['recipe'].views+=1
            context_dict['rpresent'] = (request.user.is_authenticated and not context_dict['ratings'].filter(user=request.user))
        Recipe.objects.filter(id=recipe_id).update(views=context_dict['recipe'].views)
        if request.user.is_authenticated:
            userProfile = UserModel.objects.get(user=request.user)
            savedRecipes = userProfile.saved_recipes.all()
            if context_dict['recipe'] in savedRecipes:
                context_dict["saved"] = "yes"
        return render(request, 'cookhub/recipe.html', context=context_dict)
    
    @method_decorator(login_required)
    def post(self, request, recipe_id):
        print("post")
        try:
            context_dict = self.get_recipe_details(recipe_id=recipe_id)
        except TypeError:
            return redirect(reverse('cookhub:homepage'))
        
        context_dict['rpresent'] = not context_dict['ratings'].filter(user=request.user)
        rating_form = RatingForm(request.POST)
        comment_form = CommentForm(request.POST)
        
        if rating_form.is_valid():
            rating = rating_form.save(commit=False)
            user = request.user
            rating.user = user
            recipe = context_dict['recipe']
            rating.recipe = recipe
            print(str(rating_form))
            num = context_dict['recipe'].averageRating*len(context_dict['ratings']) + int(rating.rating)
            if len(context_dict['ratings']):
                rnum = ((num))/(len(context_dict['ratings']))
            else:
                rnum = num
            Recipe.objects.filter(id=recipe_id).update(averageRating=rnum)
            rating.save()
            context_dict = self.get_recipe_details(recipe_id=recipe_id)
            return redirect(reverse('cookhub:recipe', kwargs={'recipe_id':recipe_id}))
        
        if comment_form.is_valid():
            print(str(not context_dict['ratings'].filter(user=request.user)))
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.recipe = context_dict['recipe']
            comment.save()
            context_dict = self.get_recipe_details(recipe_id=recipe_id)
            return redirect(reverse('cookhub:recipe', kwargs={'recipe_id':recipe_id}))
        return render(request, 'cookhub/recipe.html', context=context_dict)

class EditRecipeView(View):
    def get_recipe_details(self, recipe_id):
        try:
            recipe = Recipe.objects.get(id=recipe_id)
            ingredients = Ingredient.objects.filter(recipe=recipe)
            creator = recipe.user
            ingredient_form = IngredientForm()
            recipe_form = RecipeForm(instance=recipe)
            category_form = CategoryForm()
            
        except Recipe.DoesNotExist:
            return None
        
        context_dict = {}
        context_dict['ingredients'] = ingredients
        context_dict['creator'] = creator
        context_dict['recipe'] = recipe
        context_dict['ingredient_form'] = ingredient_form
        context_dict['recipe_form'] = recipe_form
        context_dict['category_form'] = category_form
        return context_dict
    
    def get (self, request, recipe_id):
        try: 
            context_dict = self.get_recipe_details(recipe_id=recipe_id)
        except TypeError:
            return redirect(reverse('cookhub:homepage'))
        return render(request, 'cookhub/edit_recipe.html', context=context_dict)
    
    def post(self, request, recipe_id):
        try:
            context_dict = self.get_recipe_details(recipe_id=recipe_id)
        except TypeError:
            return redirect(reverse('cookhub:homepage'))
            
        if 'addIngredient' in request.POST:
            ingredient_form = IngredientForm(request.POST)
            if ingredient_form.is_valid():
                ingredient = ingredient_form.save(commit=False)
                ingredient.recipe = context_dict['recipe']
                ingredient.save()
            return redirect(reverse('cookhub:edit_recipe', kwargs={'recipe_id':recipe_id}))
        
        if 'editRecipe' in request.POST:
            recipe_form = RecipeForm(request.POST, request.FILES, instance=context_dict['recipe'])
            if recipe_form.is_valid():
                recipe = recipe_form.save(commit = False)
                recipe.save()
                recipe_form.save_m2m()
                return redirect(reverse('cookhub:recipe', kwargs={'recipe_id':recipe_id}))
        
        if 'addCategory' in request.POST:
            category_form = CategoryForm(request.POST)
            if category_form.is_valid():
                category_form.save()
            return redirect(reverse('cookhub:edit_recipe', kwargs={'recipe_id':recipe_id}))
        return render(request, 'cookhub/edit_recipe.html', context=context_dict)



@login_required
def create_recipe(request):
    recipe = Recipe(user=request.user)
    recipe.save()
    return redirect(reverse('cookhub:add_recipe', kwargs={'recipe_id':recipe.id}))


@login_required
def add_recipe(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)
    recipe_form = RecipeForm(instance=recipe)
    category_form = CategoryForm()
    ingredient_form = IngredientForm()
    if request.method == 'POST':
        if 'addCategory' in request.POST:
            category_form = CategoryForm(request.POST)
            if category_form.is_valid():
                category_form.save()
            return redirect(reverse('cookhub:add_recipe', kwargs={'recipe_id':recipe_id}))
            
        if 'addRecipe' in request.POST:
            recipe_form = RecipeForm(request.POST, request.FILES, instance=recipe)
            if recipe_form.is_valid():
                recipe = recipe_form.save(commit=False)
                recipe.save()
                recipe_form.save_m2m()
                return redirect(reverse('cookhub:recipe', kwargs={'recipe_id':recipe_id}))
            else:
                print(recipe_form.errors)
        
        if 'addIngredient' in request.POST:
            ingredient_form = IngredientForm(request.POST)
            if ingredient_form.is_valid():
                ingredient = ingredient_form.save(commit=False)
                ingredient.recipe = recipe
                ingredient.save()
            return redirect(reverse('cookhub:add_recipe', kwargs={'recipe_id':recipe_id}))
            
    return render(request, 'cookhub/add_recipe.html', context={'recipe_form':recipe_form, 'category_form':category_form, 'recipe':recipe, 'ingredient_form':ingredient_form, 'ingredients':Ingredient.objects.filter(recipe=recipe)})


class DeleteRecipeView(View):
    @method_decorator(login_required)
    def get(self, request, recipe_id):
        try:
            Recipe.objects.get(id=int(recipe_id)).delete()
            return redirect(reverse('cookhub:profile', kwargs={'username':request.user.username}))
        except Recipe.DoesNotExist:
            return HttpResponse("An error occurred and the recipe could not be found. <a href='/profile/"+request.user.username+"/'>Return to your profile page.</a>")


@login_required
def del_ingredient(request, recipe_id, ingredient_id):
    if request.method == 'POST':
        if ingredient_id:
            ingredient = Ingredient.objects.get(id=ingredient_id).delete()
        return redirect(reverse('cookhub:add_recipe', kwargs={'recipe_id':recipe_id}))
    return render(request, 'cookhub/del_ingredient.html', context={'recipe_id':recipe_id, 'ingredient':Ingredient.objects.get(id=ingredient_id)})

@login_required
def del_editingredient(request, recipe_id, ingredient_id):
    if request.method == 'POST':
        if ingredient_id:
            ingredient = Ingredient.objects.get(id=ingredient_id).delete()
        return redirect(reverse('cookhub:edit_recipe', kwargs={'recipe_id':recipe_id}))
    return render(request, 'cookhub/del_editingredient.html', context={'recipe_id':recipe_id, 'ingredient':Ingredient.objects.get(id=ingredient_id)})



class SavedRecipesView(View):
    @method_decorator(login_required)
    # saves a recipe
    def get(self, request):
        recipeID = request.GET["recipeID"]
        try:
            recipe = Recipe.objects.get(id=int(recipeID))
        except Recipe.DoesNotExist:
            return HttpResponse("Error - recipe not found.")
        except ValueError:
            return HttpResponse("Error - bad recipe ID.")
        
        userProfile = UserModel.objects.get(user=request.user)
        userProfile.saved_recipes.add(recipe)
        userProfile.save()
        return HttpResponse()
    
    @method_decorator(login_required)
    # removes a saved recipe
    def post(self, request):
        recipeID = request.POST["recipeID"]
        try:
            recipe = Recipe.objects.get(id=int(recipeID))
        except Recipe.DoesNotExist:
            return HttpResponse("Error - recipe not found.")
        except ValueError:
            return HttpResponse("Error - bad recipe ID.")
        
        userProfile = UserModel.objects.get(user=request.user)
        userProfile.saved_recipes.remove(recipe)
        userProfile.save()
        n = len(userProfile.saved_recipes.all())
        print("Saved recipes left: " + str(n))
        return HttpResponse("correct"+str(n))


class PaginationView(View):
    def get(self, request):
        RecipesPerPage = int(request.GET["RecipesPerPage"])
        author = request.GET["author"]
        which = request.GET["which"]
        page = int(request.GET["page"])
        print("Page to get: "+str(page))
        single = int(request.GET["single"])
        buttons = request.GET.get("buttons", None)
        # deal with the author
        if author!="#":
            try:
                user = User.objects.get(username=author)
                recipes = Recipe.objects.filter(user=user)
            except User.DoesNotExist:
                return HttpResponse("error: User does not exist")
            except Recipe.DoesNotExist:
                return HttpResponse("error: Recipe does not exist")
            except ValueError:
                return HttpResponse("error: value error")
        else:
            recipes = Recipe.objects.all()
        
        # deal with the which
        if which=="newest":
            recipes = recipes.order_by("-creationDate")
        elif which=="popular":
            recipes = recipes.order_by("-views")
        elif which=="my":
            pass # we already specified the author
        elif which=="saved":
            user_profile = UserModel.objects.get(user=user)
            recipes = user_profile.saved_recipes.all()
        else:
            return HttpResponse("error: Wrong 'which' parameter")
        
        # deal with the RecipesPerPage and pages
        n = len(recipes)-1 # end index of the number of queryset
        print("recipes: "+ str(n+1))
        if n<0:
            return HttpResponse("empty")
        if n<(page-1)*RecipesPerPage:
            return HttpResponse("error: not this many recipes exist for "+str(page) +" pages and "+str(RecipesPerPage)+" recipes per page")
        if n+1>page*RecipesPerPage:
            recipes = recipes[(page-1)*RecipesPerPage:page*RecipesPerPage] 
        else:
            recipes = recipes[(page-1)*RecipesPerPage:n+1]
        
        if single==0:
            pass
        elif single<0:
            return HttpResponse("error: single bellow 0")
        elif single>RecipesPerPage:
            return HttpResponse("error: single larger than RecipesPerPage")
        else:
            recipes = recipes[single-1]
        
        # pack the recipes into the format for the webpage
        responseString = ""
        
        if single!=0 or len(recipes)==1:
            if (n==0 or len(recipes)==1) and single==0:
                recipes = recipes[0]
            responseString += str(recipes.photo) + ";;"
            responseString += str(recipes.id) + ";;"
            responseString += recipes.title + ";;"
            responseString += str(recipes.averageRating)
            if buttons=="yes" and request.user.is_authenticated:
                userProfile = UserModel.objects.get(user=request.user)
                savedRecipes = userProfile.saved_recipes.all()
                if recipes in savedRecipes:
                    responseString += ";;" + "saved" + ";;"
                else:
                    responseString += ";;" + "save" + ";;"
            responseString += "||RCP||"
        elif n>0:
            for recipe in recipes:
                responseString += str(recipe.photo) + ";;"
                responseString += str(recipe.id) + ";;"
                responseString += recipe.title + ";;"
                responseString += str(recipe.averageRating)
                if buttons=="yes" and request.user.is_authenticated:
                    userProfile = UserModel.objects.get(user=request.user)
                    savedRecipes = userProfile.saved_recipes.all()
                    if recipe in savedRecipes:
                        responseString += ";;" + "saved" + ";;"
                    else:
                        responseString += ";;" + "save" + ";;"
                responseString += "||RCP||"
        else:
            return HttpResponse("error: no recipes returned")
        
        print("recipes: "+ str(n+1))
        responseString = responseString[:-7] # remove last ||RCP|| delimiter
        return HttpResponse(responseString)
        
def test(request):
    #recipe = Recipe.objects.get(id=1)
    return render(request, "cookhub/test.html", {"debuggingInformation":""})