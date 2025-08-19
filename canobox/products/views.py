
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework import status
from .models import PhoneModel, Product, ProductImages, ProductOption, ProductTag
from .serializers import ProductSerializer, PhoneModelSerializer, PhoneModelSerializerAdmin
from django.db.models import Case, When, Value, IntegerField

# Create your views here.
class ProductListAdmin(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class PhoneModels(ListAPIView):

    serializer_class = PhoneModelSerializer

    def get_queryset(self):
        return PhoneModel.objects.order_by('-model_type', '-model_name')
    
    
class PhoneModelsAdmin(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request):
        phoneModels = PhoneModel.objects.all()
        serializer = PhoneModelSerializerAdmin(phoneModels, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = PhoneModelSerializerAdmin(data=request.data, many=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)