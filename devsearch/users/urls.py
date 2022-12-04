from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.loginUser, name="login"),
    path("logout/", views.logoutUser, name="logout"),
    path("register/", views.registerUser, name="register"),
    path("account/", views.userAccount, name="userAccount"),
    path("edit-account/", views.editAccount, name="edit-account"),
    path("", views.profiles, name="profiles"),
    path("profile/<str:pk>/", views.userProfile, name="userProfile"),
    path("profile/<str:pk>/create-skill/", views.createSkill, name="create-skill"),
    path("profile/<str:pk>/update-skill/", views.updateSkill, name="update-skill"),
    path("profile/<str:pk>/delete-skill", views.deleteSkill, name="delete-skill"),
]
