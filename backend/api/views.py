from django.db.models import query
from django.shortcuts import render
from requests.api import request
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from .models import Tag, Favorite, Follow, Recipe
from users.models import User
from .serializers import TagSerializer, FavoriteSerializer
from rest_framework import permissions
from django.shortcuts import get_object_or_404
from rest_framework.response import Response


class TagListView(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    
class TagView(generics.RetrieveAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


# ошибка добавления в избранное не реализована
class FavoriteView(generics.RetrieveDestroyAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(id=request.user)


class FollowView(APIView):
    def get(self, request, pk):
        request.QUERY['recipes_limit']  # recipes_limit
        author = User.objects.get(id=pk)
        Follow.objects.create(
            author=author,
            user=request.user
        )
        paginations_limit = request.GET.get('recipes_limit', None)
        # author_receips = Recipe.objects.filter(author=author)
        

    def delete(self, request, pk):
        author = get_object_or_404(User, pk=1)
        queryset = Follow.objects.filter(author__id=pk, user=request.user)
        if not queryset.exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
        
        
        
class FollowViewList(generics.ListAPIView):
    pass
    


# class TagListView(APIView):
#     def get(self, request):
#         tags = Tag.objects.all()
#         serializer = TagSerializer(tags, many=True)
#         return Response(serializer.data)


# class TagView(APIView):
#     def get(self, request, pk):
#         tags = Tag.objects.get(id=pk)
#         serializer = TagSerializer(tags)
#         return Response(serializer.data)


