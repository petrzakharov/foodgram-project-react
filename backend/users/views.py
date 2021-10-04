from decimal import Context
from django.shortcuts import get_object_or_404, render
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import generics, status
from rest_framework.views import APIView
from .serializers import UserCreateSerializer
import requests
from .models import User
from api.models import Follow
from .serializers import FollowSerializer


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


# Follow
    # GET list
    # Возвращает авторов на которых подписан пользователь и их рецепты
    # query params: page(пагинация?), limit(количество объектов на странице), recipes_limit (количество объектов рецепта для каждого пользователя)

    # GET retrieve
    # Подписка на нового автора
    # id автора берется из url
    # query params: recipes_limit(сколько записей рецептов вернуть)
    # Если подписка уже существует или пользователь подписывается сам на себя - ошибка 400

    # DELETE
    # Отписаться от автора
    # id автора берется из url
    # Не был подписан на пользователя - ошибка 400
    
    
# class CatViewSet(viewsets.ModelViewSet):
#     queryset = Cat.objects.all()
#     serializer_class = CatSerializer
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
#     # Вот он наш собственный класс пагинации с page_size=20
#     pagination_class = CatsPagination


# Написать page pagination 
class FollowViewList(generics.ListAPIView):
    """Список подписок"""
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    
    # добавить пагинацию
    def get_queryset(self):
        # User.objects.filter(
        # following__user_id__in = (self.request.user,)
        # )
        
        qs = self.request.user.followings.all() # на кого я подписан, объекты Follow
        return [i.author for i in qs] # выяснить нормально ли передается список а не кверисет
        
        
        


class FollowView(APIView):
    """подписка на нового автора"""

    def get(self, request, pk):
        # recipes_limit = request.query_params.get('recipes_limit')
        # limit = request.query_params.get('limit')
        # page = request.query_params.get('page')
        if pk == request.user.id or (
            Follow.objects.filter(
                author_id=pk,
                user=request.user
            ).exists()
        ):
            return Response(
                {"errors": "Подписка уже существует"}, 
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
        author = get_object_or_404(User, pk=1)
        queryset = Follow.objects.filter(author__id=pk, user=request.user)
        if not queryset.exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
