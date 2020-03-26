from django import forms
from django.contrib.auth.models import User
from cookhub.models import UserModel, Recipe, Comment, Rating, Category, Ingredient, IngredientArray
from django.utils import timezone

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "password", "confirm_password", )
        
    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password!=confirm_password:
            raise forms.ValidationError("Confirm password and password don't match")

        
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ("picture",)


class ChangePasswordForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        model = User
        fields = ("password", "confirm_password", )
        
    def clean(self):
        cleaned_data = super(ChangePasswordForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password!=confirm_password:
            raise forms.ValidationError("Confirm password and password don't match")


class RecipeForm(forms.ModelForm):
    title = forms.CharField(max_length=40, help_text="Name of your recipe:")
    description = forms.CharField(widget=forms.Textarea, max_length=4000, help_text="How to make your recipe:")
    photo = forms.ImageField(required=False, help_text="Upload a photo of your recipe:")
    time = forms.IntegerField(help_text="How long it takes to prepare your recipe:")
    averageRating = forms.FloatField(widget=forms.HiddenInput(), initial=0, required=False)
    servings = forms.IntegerField(help_text="The number of people your recipe serves:")
    creationDate = forms.DateTimeField(widget=forms.HiddenInput(), initial=timezone.now(), required=False)
    views = forms.IntegerField(required=False, widget=forms.HiddenInput(), initial=0)
    categories = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=Category.objects.all(), required=False, help_text="Categories your recipe belongs to:")
    
    class Meta:
        model = Recipe
        exclude = ('user',)
        
class CommentForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea, max_length = 400)
    creationDate = forms.DateTimeField(widget=forms.HiddenInput(), required=False)
    
    class Meta:
        model = Comment
        exclude = ('user', 'recipe',)

class RatingForm(forms.ModelForm):
    rating = forms.IntegerField()
    
    class Meta:
        model = Rating
        exclude = ('user', 'recipe',)

class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=20)
    
    class Meta:
        model = Category
        fields = ('name',)

class IngredientForm(forms.ModelForm):
    name = forms.CharField(max_length=20, help_text='Name of the ingredient:')
    quantity = forms.IntegerField(help_text='How many units of ingredient are there')
    unit = forms.CharField(max_length=20, help_text='Unit used for the ingredient (can be blank)', required=False)
    
    class Meta:
        model = Ingredient
        exclude = ('recipe',)

class IngredientArrayForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea, max_length = 2000)
    
    class Meta:
        model = IngredientArray
        fields = ('text',)
        

    
