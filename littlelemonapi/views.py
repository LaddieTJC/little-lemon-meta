from django.shortcuts import render
from .models import MenuItem, Category
from rest_framework import generics
from .serializers import MenuItemSerializer, CategorySerializer, ManagerSerializer
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django.contrib.auth.models import User, Group
from .permissions import ManagerOnlyPermission
# Create your views here.


class MenuItemsView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    def get_permissions(self):
        if self.request.method == 'POST' or self.request.method == 'PUT' or self.request.method == 'DELETE':
            # manager = Group.filter(name="Manager")
            return [ManagerOnlyPermission()]
        return [IsAuthenticated()]
    

class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    def get_permissions(self):
        if self.request.method == 'POST' or self.request.method == 'PUT' or self.request.method == 'DELETE':
            return [ManagerOnlyPermission()]
        return [IsAuthenticated()]
    

class ManagersView(generics.ListAPIView):
    queryset = User.objects.filter(groups__name='Manager')
    serializer_class = ManagerSerializer
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    permission_classes = [ManagerOnlyPermission,]

    