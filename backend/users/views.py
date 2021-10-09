import requests

from api.models import Follow, Recipe
from django.shortcuts import get_object_or_404, render
from rest_framework import generics, permissions, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .pagination import LargeResultsSetPagination
from .serializers import FollowSerializer, UserCreateSerializer

# class UserCreateView(APIView):
#     def post(self, request):
#         try:
#             user = UserCreateSerializer(data=request.data)
#         except:
#             return Response(status=status.HTTP_400_BAD_REQUEST)
#         return Response(status=status.HTTP_200_OK)


class UserLogout(APIView):
    """Разлогин пользователя"""
    def get(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


# при переходе юзера по ссылке активации, ловим гет запрос и отправляем пост запрос
class UserActivationView(APIView):
    """Отправка POST запроса при активации по ссылке"""
    def get(self, request, uid, token):
        protocol = 'https://' if request.is_secure() else 'http://'
        web_url = protocol + request.get_host()
        post_url = web_url + 'api/users/activation/'
        post_data = {'uid': uid, 'token': token}
        result = requests.post(post_url, data=post_data)
        content = result.text()
        return Response(content)


class FollowViewList(generics.ListAPIView):
    """Список подписок"""
    queryset = User.objects.all()
    serializer_class = FollowSerializer
    pagination_class = LargeResultsSetPagination
    permission_classes = [permissions.IsAuthenticated, ]

    def get_queryset(self):
        qs = User.objects.filter(following__user=self.request.user)
        return qs


class FollowView(APIView):
    """Подписка на нового автора"""
    def get(self, request, pk):
        if pk == request.user.id or (
            Follow.objects.filter(
                author_id=pk,
                user=request.user
            ).exists()
        ):
            return Response(
                {'errors': 'Подписка уже существует'},
                status=status.HTTP_400_BAD_REQUEST
            )
        author = User.objects.filter(id=pk).first()
        if author:
            Follow.objects.create(
                author_id=pk,
                user=request.user
            )
            serialized = FollowSerializer(author, context={'request': request})
            return Response(
                serialized.data,
                status=status.HTTP_201_CREATED
            )
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        """Отписка от автора"""

        queryset = Follow.objects.filter(author__id=pk, user=request.user)
        if not queryset.exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
