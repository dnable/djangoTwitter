from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),

    path('/<str:pk>', views.home, name="homeFilter"),
    
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),

    path('register/', views.registerPage, name="register"),
    path('profile/', views.profile, name="profile"),
    path('editProfile/', views.editProfile, name="editProfile"),

    path('profile/<str:pk>/', views.userProfile, name="userProfile"),

    path('follow/<str:pk>/', views.follow, name="follow"),
    path('unfollow/<str:pk>/', views.unfollow, name="unfollow"),

    path('deleteTweet/<str:pk>/<str:path>/', views.deleteTweet, name="deleteTweet"),

    path('followers/<str:pk>/', views.followers, name="followers"),
    path('following/<str:pk>/', views.following, name="following"),
]