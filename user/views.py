from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from django.contrib.auth.models import User
from user.serializers import UserSerializer, UserRegisterSerializer, ProfileSerializer, ProfileUpdateSerializer
from user.models import Profile
from user.permissions import IsOwnerOrReadOnly
from rest_framework import permissions


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = ()

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method in ['POST']:
            return UserRegisterSerializer
        else:
            return UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            User.objects.create_user(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password'],
            )
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProfileList(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class ProfileDetail(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method in ['PUT', 'PATCH']:
            return ProfileUpdateSerializer
        else:
            return ProfileSerializer

    # def update(self, request, *args, **kwargs):
    #     serializer = ProfileUpdateSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(, status=status.HTTP_200_OK)
    #     else:
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





