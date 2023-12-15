from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser, UserProfile
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.permissions import IsAuthenticated


# REGISTER
################################################################
class CustomUserCreateView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# LOGIN
################################################################
class UserLoginView(CreateAPIView):
    serializer_class = UserLoginSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            return Response(
                serializer.validated_data["tokens"], status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# USER LIST
################################################################
class AdminUserListView(ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = [IsAdminUser]


class AdminUserDetailView(RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = [IsAdminUser]


# USER EDIT
################################################################
class UserProfileEditView(RetrieveUpdateAPIView):
    serializer_class = UserProfileEditSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.userprofile  # Retrieve logged-in user's profile

    def get_queryset(self):
        return UserProfile.objects.filter(
            user=self.request.user
        )  # Filter queryset for the logged-in user
