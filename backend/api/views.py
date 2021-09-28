from django.shortcuts import render
from rest_framework.request import Request
from rest_framework.views import APIView
from .serializers import UserCreateSerializer

# Create your views here.

class UserCreateView(APIView):

    def post(self, request):
        try:
            user = UserCreateSerializer(data=request.data)
        except:
            return Request(status=400)
        return Request(status=201)
