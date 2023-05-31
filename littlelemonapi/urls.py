from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
        path('menu-items', views.MenuItemsView.as_view()),
        path('menu-items/<int:pk>', views.SingleMenuItemView.as_view()),
        path('groups/manager/users', views.ManagersView.as_view()),
        path('groups/delivery-crew/users', views.DeliveryCrewView.as_view()),
        path('cart/menu-items', views.CartView.as_view()),
]