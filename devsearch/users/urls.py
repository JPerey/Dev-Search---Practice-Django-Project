from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.loginUser, name="login"),
    path("logout/", views.logoutUser, name="logout"),
    path("register/", views.registerUser, name="register"),
    path("account/", views.userAccount, name="userAccount"),
    path("edit-account/", views.editAccount, name="edit-account"),
    path("inbox/", views.Inbox, name="inbox"),
    path("message/<str:pk>", views.viewMessage, name="message"),
    path("", views.profiles, name="profiles"),
    path("profile/<str:pk>/", views.userProfile, name="userProfile"),
    path("create-skill/", views.createSkill, name="create-skill"),
    path("update-skill/<str:pk>/", views.updateSkill, name="update-skill"),
    path("delete-skill/<str:pk>/", views.deleteSkill, name="delete-skill"),
]
