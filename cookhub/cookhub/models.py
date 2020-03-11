from django.db import models
from django.contrib.auth.models import User

class UserModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    picture = models.ImageField(upload_to="profile_images", blank=True, default="default.jpg")
    
    def __str__(self):
        return self.user.username