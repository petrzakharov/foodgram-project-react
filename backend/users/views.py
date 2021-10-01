from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.views import APIView
from .serializers import UserCreateSerializer
import requests

# class UserCreateView(APIView):
#     def post(self, request):
#         try:
#             user = UserCreateSerializer(data=request.data)
#         except:
#             return Response(status=status.HTTP_400_BAD_REQUEST)
#         return Response(status=status.HTTP_200_OK)


class UserLogout(APIView):  # разлогин, проверить что у нас тоже происходит через гет запрос
    def get(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

#при переходе юзера по ссылке активации, ловим гет запрос и отправляем пост запрос
class UserActivationView(APIView):
    def get(self, request, uid, token):
        protocol = 'https://' if request.is_secure() else 'http://'
        web_url = protocol + request.get_host()
        post_url = web_url + "api/users/activation/"
        post_data = {'uid': uid, 'token': token}
        result = requests.post(post_url, data=post_data)
        content = result.text()
        print(content)
        return Response(content)
