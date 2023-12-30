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
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model


# REGISTER
################################################################
class CustomUserCreateView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        # UserProfile.objects.create(user=user)

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
        return self.request.user.userprofile

    def get_queryset(self):
        return UserProfile.objects.filter(
            user=self.request.user
        )


from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            user = self.user
            refresh = response.data.get("refresh")
            access = response.data.get("access")

            # Custom payload data to include in the tokens
            custom_payload = {
                "user_id": user.id,
                "phone_number": user.phone_number,
                "is_admin": user.is_admin,
            }

            # Update the tokens' payloads with custom data
            encoded_refresh = RefreshToken(refresh)
            encoded_access = RefreshToken(access)
            encoded_refresh.payload.update(custom_payload)
            encoded_access.payload.update(custom_payload)

            response.data["refresh"] = str(encoded_refresh)
            response.data["access"] = str(encoded_access)

        return response


@receiver(post_save, sender=get_user_model())
def create_user_profile(sender, instance, created, **kwargs):
    if created and not hasattr(instance, 'userprofile'):
        UserProfile.objects.create(user=instance)