
import json
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework import status

from permissions import IsAdminOrSuperUser
from .models import PhoneModel, Product, ProductImages, ProductOption, ProductTag
from .serializers import ProductSerializer, PhoneModelSerializer, PhoneModelSerializerAdmin
from rest_framework.viewsets import ModelViewSet
from django.db import transaction

from djangorestframework_camel_case.util import underscoreize

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
    
class ProductDetailAdmin(APIView):

    permission_classes = [IsAdminOrSuperUser]

    def get(self, request):
        id = request.query_params.get('id')
        if not id: return Response({"error":"유효하지 않은 요청입니다"},status=status.HTTP_400_BAD_REQUEST)

        try: product = Product.objects.get(pk=id)
        except Product.DoesNotExist: Response({"error":"상품을 찾을 수 없습니다"},status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class ProductViewSet(ModelViewSet):

    permission_classes = {IsAdminOrSuperUser}

    queryset = Product.objects.all().prefetch_related(
        "tags", "additional_images", "options", "phone_model_options"
    )
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):

        # print("👉 request.data:", request.data)
        # print("👉 request.FILES:", request.FILES)

        data = request.data.get("data")
        json_data = {}
        try:
            json_data = json.loads(data)
        except json.JSONDecodeError:
            return Response({"error":"잘못된 데이터입니다"},status=status.HTTP_400_BAD_REQUEST)
            
        parsed_data = underscoreize(json_data)
        parsed_data["thumbnail"] = request.FILES.get("thumbnail")
        parsed_data["thumbnail_hover"] = request.FILES.get("thumbnail_hover")

        serializer = self.get_serializer(data=parsed_data, context={"request": request})
        if not serializer.is_valid():
            print("❌ serializer errors:", serializer.errors)  # 에러 출력
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @transaction.atomic
    def perform_create(self, serializer):
        serializer.save()

    @transaction.atomic
    def perform_update(self, serializer):
        serializer.save()


    
class PhoneModels(ListAPIView):

    serializer_class = PhoneModelSerializer

    def get_queryset(self):
        return PhoneModel.objects.order_by('-model_type', 'order')
    
    
class PhoneModelsAdmin(APIView):

    permission_classes = [IsAdminOrSuperUser]

    def get(self, request):
        phoneModels = PhoneModel.objects.order_by('-model_type', 'order')
        serializer = PhoneModelSerializerAdmin(phoneModels, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        try:
            data = request.data.get("data", [])
            dels = request.data.get("dels", [])

            if dels:
                PhoneModel.objects.filter(id__in=dels).delete()

            saved_instances = []

            for item in data:

                print(item)

                if "id" in item and item["id"]:
                    instance = PhoneModel.objects.get(id=item["id"])
                    serializer = PhoneModelSerializerAdmin(instance, data=item, partial=True)
                else:
                    serializer = PhoneModelSerializerAdmin(data=item)
                
                serializer.is_valid(raise_exception=True)
                saved = serializer.save()
                saved_instances.append(saved)

            response_serializer = PhoneModelSerializerAdmin(PhoneModel.objects.all().order_by("-model_type","order"),many=True)
            
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        
        except Exception as e:
            print(e)
            return Response({"success": False, "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)