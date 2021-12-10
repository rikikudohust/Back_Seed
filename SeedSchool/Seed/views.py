from django.shortcuts import render
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from SeedSchool.Seed.models import Menu
from SeedSchool.Seed.serializers import MenuSerializer
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404


class MenuList(APIView):
    def get(self, request, format=None):
        menu = Menu.objects.all()
        serializer = MenuSerializer(menu, many = True)
        return Response(serializer.data) 
    def post(self, request, format=None):
        serializer = MenuSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
class MenuDetail(APIView):
    def get_object(self, pk):
            try:
                return Menu.objects.get(pk=pk)
            except Menu.DoesNotExist:
                raise Http404
    def get(self, request, pk, format=None):
        menu = self.get_object(pk)
        serializer = MenuSerializer(menu)
        return Response(serializer.data)
    def put(self, request, pk, format=None):
        menu = self.get_object(pk)
        serializer = MenuSerializer(menu, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    

