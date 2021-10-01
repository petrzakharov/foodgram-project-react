from django.db.models import query
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from .models import Tag
from .serializers import TagSerializer


class TagListView(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    
class TagView(generics.RetrieveAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


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


