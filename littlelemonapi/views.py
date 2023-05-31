from django.shortcuts import render, get_object_or_404
from .models import MenuItem, Category
from rest_framework import generics, status
from .serializers import MenuItemSerializer, CategorySerializer, UserSerializer
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django.contrib.auth.models import User, Group
from .permissions import ManagerOnlyPermission
from rest_framework.response import Response
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
    

class ManagersView(generics.GenericAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    permission_classes = [ManagerOnlyPermission,]
    
    def get(self, request):
        users = User.objects.filter(groups__name='Manager')
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        username = request.data['username']
        if username:
            user = get_object_or_404(User, username=username)
            managers = Group.objects.get(name="Manager")
            managers.user_set.add(user)
            return Response({"Message":"Added to the Manager Group"})
        
        return Response({"Message":"Error"}, status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        username = request.data['username']
        if username:
            user = get_object_or_404(User, username=username) 
            managers = Group.objects.get(name="Manager")
            managers.user_set.remove(user)
            return Response({"Message": "Removed from Manager"})
        
        return Response({"Message":"Error"}, status.HTTP_400_BAD_REQUEST)
    

class DeliveryCrewView(generics.GenericAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    permission_classes = [ManagerOnlyPermission,]
    
    def get(self, request):
        users = User.objects.filter(groups__name='Delivery Crew')
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        username = request.data['username']
        if username:
            user = get_object_or_404(User, username=username)
            managers = Group.objects.get(name="Delivery Crew")
            managers.user_set.add(user)
            return Response({"Message":"Added to the Delivery Group"})
        
        return Response({"Message":"Error"}, status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        username = request.data['username']
        if username:
            user = get_object_or_404(User, username=username) 
            managers = Group.objects.get(name="Delivery Crew")
            managers.user_set.remove(user)
            return Response({"Message": "Removed from Delivery"})
        
        return Response({"Message":"Error"}, status.HTTP_400_BAD_REQUEST)







    