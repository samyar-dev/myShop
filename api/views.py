from django.shortcuts import render
from rest_framework import generics, views, viewsets
from rest_framework.response import Response
from shop.models import Product
from account.models import ShopUser
from .serializers import Productserializer, UserListSerializer, UserRegistrationSerializer
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import action


# class ProductListApiView(generics.ListAPIView):
#     authentication_classes = [BasicAuthentication]
#     permission_classes = [IsAuthenticated]
#     queryset = Product.objects.all()
#     serializer_class = Productserializer


# class ProductDetailApiView(generics.RetrieveAPIView):
#     authentication_classes = [BasicAuthentication]
#     permission_classes = [IsAuthenticated]
#     queryset = Product.objects.all()
#     serializer_class = Productserializer


class ProductViewSet(viewsets.ModelViewSet):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = Productserializer

    @action(detail=False, methods=['GET'])
    def discounted_products(self, requset):
        min_discount = requset.query_params.get('min_discount', 0)
        try:
            products = self.queryset.filter(discount__gte=min_discount)
            serializer = self.get_serializer(products, many=True)
            return Response(serializer.data)
        except ValueError:
            return Response({'error': 'Invalid discount number parameter'}, status=400)


class UserListApiView(generics.ListAPIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = ShopUser.objects.all().order_by('id')
    serializer_class = UserListSerializer

# class UserListApiView(views.APIView):
#     authentication_classes = [BasicAuthentication]
#     permission_classes = [IsAuthenticated]
#     def get(self, request, *args, **kwargs):
#         users = ShopUser.objects.all()
#         serializer = UserListSerializer(users, many=True)
#         return response.Response(serializer.data)
    

class UserRegistrationApiView(generics.CreateAPIView):
    queryset = ShopUser.objects.all()
    serializer_class = UserRegistrationSerializer