from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from cookhub.forms import UserForm, UserProfileForm
from cookhub.models import UserModel

class Homepage(View):
    def get(self, request):
        return render(request, "cookhub/homepage.html", {"content":"Cookhub Homepage"})
    
def register(request):
    # A boolean telling the template whether the registration was succesful, 
    # set initially to false. Code changes it to true 
    # once the registration is complete.
    registered = False
    
    #If it is a HTTP post, we are interested in processing form data.
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
            profile = profile_form.save(commit = False)
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
            
            return redirect(reverse('cookhub:homepage'))
        else:
            # Invalid form(s): print problems to terminal.
            print(user_form.errors, profile_form.errors)
            
    else:
        # Not a HTTP post, so we render our form using two ModelForm instances.
        # These forms will be blank, ready for user input.
        user_form = UserForm()
        profile_form = UserProfileForm()
        
    # Render the template depending on the context.
    return render(request, "registration/register.html", context = {"user_form":user_form,
                                                             "profile_form":profile_form,
                                                             "registered":registered})
    
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
                return redirect(reverse('cookhub:homepage')) # reverse obtains the URL named index from views.py
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
    
    @method_decorator(login_required)
    def get(self, request, username):
        try:
            (user, user_profile, form) = self.get_user_details(username)
        except TypeError:
            return redirect(reverse('cookhub:homepage'))
        
        context_dict = {'user_profile': user_profile,
                        'selected_user': user,
                        'form': form}
        return render(request, 'cookhub/profile.html', context_dict)
 
    @method_decorator(login_required)
    def post(self, request, username):
        print("post")
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