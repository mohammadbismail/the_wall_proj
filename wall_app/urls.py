from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path("register/", views.register_user),
    path("login/", views.check_login),
    path("wall/", views.user_wall_page),
    path("logout/", views.logout_user),
    path("wall/add_message/", views.add_message),
    path("wall/add_comment/", views.add_comment),
]
