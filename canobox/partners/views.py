
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from permissions import IsAdminOrSuperUser
from .models import Company
from .serializers import CompanySerializer

# Create your views here.
class CompanyAdminAPI(APIView):

    permission_classes = [IsAdminOrSuperUser]

    def get(self, request):
        id = request.query_params.get('id')
        if not id:
            return Response({"error":"id 쿼리가 필요합니다"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            company = Company.objects.get(pk=id)
        except Company.DoesNotExist:
            return Response({"error":"거래처 정보가 없습니다"},status=status.HTTP_404_NOT_FOUND)
        
        serializer = CompanySerializer(company)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        if 'id' in request.data:
            return Response({"error":"이미 존재하는 id입니다"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = CompanySerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request):
        id = request.data.get('id')
        if not id:
            return Response({"error":"id가 필요합니다"},status=status.HTTP_400_BAD_REQUEST)
        try:
            company = Company.objects.get(pk=id)
        except Company.DoesNotExist:
            return Response({"error": "존재하지 않는 id입니다"},status=status.HTTP_404_NOT_FOUND)
        
        serializer = CompanySerializer(company, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class CompaniesAdminAPI(APIView):

    permission_classes = [IsAdminOrSuperUser]

    def get(self, request):

        limit = int(request.query_params.get('limit') or 20)
        page = int(request.query_params.get('page') or 1)

        companies = Company.objects.all()[limit * (page-1) : limit * page]
        serializer = CompanySerializer(companies, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)