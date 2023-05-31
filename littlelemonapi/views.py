from django.shortcuts import render, get_object_or_404
from .models import MenuItem, Category, Cart
from rest_framework import generics, status
from .serializers import MenuItemSerializer, CategorySerializer, UserSerializer, CartSerializer
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
    


class CartView(generics.ListCreateAPIView):
    serializer_class = CartSerializer
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    permission_classes = [IsAuthenticated,]
    
    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        menuitem = self.request.data.get('menuitem')
        quantity = self.request.data.get('quantity')
        unit_price = MenuItem.objects.get(pk=menuitem).price
        price = int(quantity) * unit_price
        serializer.save(user=self.request.user, price=price)

    def delete(self, serializer):
        Cart.objects.filter(user=self.request.user).delete()
        return Response(status=204)
    








    