from django import forms
from django.contrib.auth.models import User
from cookhub.models import UserModel

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "password", "confirm_password")
        
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