from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
        path('menu-items', views.MenuItemsView.as_view()),
]