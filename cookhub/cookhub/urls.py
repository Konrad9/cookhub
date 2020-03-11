from django.urls import path
from cookhub import views
from cookhub.views import Homepage, EditProfileView, ProfileView

app_name = 'cookhub'

urlpatterns = [
    path('', Homepage.as_view(), name='homepage'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/<username>/edit', views.EditProfileView.as_view(), name='edit_profile'),
    path('profile/<username>/', views.ProfileView.as_view(), name='profile'),
]