from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Club
from .serializers import ClubSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

class ClubList(APIView):

    def get(self, request, format=None):
        clubs = Club.objects.all()
        serializer = ClubSerializer(clubs, many = True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ClubSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)

        return Response(status = status.HTTP_400_BAD_REQUEST)






class ClubDetail(APIView):

    def get_object(self, pk):
        try:
            return Club.objects.get(pk=pk)
        except Club.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        club = self.get_object(pk)
        serializer = ClubSerializer(club)
        return Response(serializer.data)

    def put(self, request, pk, format = None):
        club = self.get_object(pk)
        serializer = ClubSerializer(club, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        club = self.get_object(pk)
        club.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

