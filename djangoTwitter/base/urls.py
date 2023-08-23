from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),

    path('register/', views.registerPage, name="register"),
    path('profile/', views.profile, name="profile"),
    path('editProfile', views.editProfile, name="editProfile"),

    path('profile/<str:pk>/', views.userProfile, name="user-profile"),
]