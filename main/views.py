from django.shortcuts import render
from rest_framework.decorators import api_view
from .serializer import UserSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import User
# Create your views here.

def get_user_or_404(user_id):
    return User.objects.filter(id=user_id).first()

@api_view(['POST'])
def create(request):
    serializer = UserSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status= status.HTTP_201_CREATED)
    return Response({"errors" :serializer.errors}, status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def read(request, user_id):
    user = get_user_or_404(user_id)
    if user:
        serializer = UserSerializer(user)
        return Response(serializer.data, status = status.HTTP_200_OK)
    return Response({"message" : "user doesn't exist"}, status = status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
def update(request, user_id):
    user = get_user_or_404(user_id)
    if user:
        serializer = UserSerializer(user, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_200_OK)
        return Response({"errors" :serializer.errors}, status = status.HTTP_400_BAD_REQUEST)
    return Response({"message" : "user doesn't exist"}, status = status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
def delete(request, user_id):
    user = get_user_or_404(user_id)
    if user:
        user.delete()
        return Response({"message" :"successfuly deleted"}, status = status.HTTP_200_OK)
    return Response({"message" : "user doesn't exist"}, status = status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def userlist(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many = True)
    return Response(serializer.data,status = status.HTTP_200_OK)