from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Club
from .serializers import ClubSerializer

# Create your views here.

@api_view(['GET', 'POST'])
def club_list(request, format=None):
    if request.method == "GET":
        clubs = Club.objects.all()
        serializer = ClubSerializer(clubs, many = True)

        return Response(serializer.data)

    elif request.method == "POST":
        serializer = ClubSerializer(data=request.data)

        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','DELETE','PUT'])
def club_detail(request, pk, format=None):
    try:
        club = Club.objects.get(pk = pk)

    except Club.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = ClubSerializer(club)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = ClubSerializer(club, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        club.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



