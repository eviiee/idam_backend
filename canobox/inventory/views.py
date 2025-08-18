from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse
from common import is_admin

# Create your views here.
@user_passes_test(is_admin)
def inbound_history_admin(request):
    data = {"message" : "관리자만 접근할 수 있는 API"}
    return JsonResponse(data)