from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path("register", views.register),
    path("login", views.login),
    path("success", views.success),
    path("logout", views.logout),
    path("homepage", views.homepage),
    path("newitem", views.newitem),
    path("create", views.createItem),
    path("iteminfo/<itemid>", views.itemInfo),
    path("delete/<itemid>", views.delete),
    path("item/like/<itemid>", views.faved),
    path("item/unlike/<itemid>", views.unfaved),
    path("likeditem", views.likeditem)
]

