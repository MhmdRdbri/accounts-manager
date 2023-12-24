from django.shortcuts import redirect
from django.urls import reverse
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser, UserProfile
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.generics import RetrieveAPIView, UpdateAPIView


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


# RESET PASSWORD
# ----------------------------------------------------------------
class PasswordResetRequestView(GenericAPIView):
    serializer_class = PasswordResetSerializer  # Use your serializer here

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data.get("phone_number")
        age = serializer.validated_data.get("age")
        username = serializer.validated_data.get("username")

        # Verify the user based on provided details
        try:
            user_profile = UserProfile.objects.get(
                user__phone_number=phone_number, age=age, username=username
            )
        except UserProfile.DoesNotExist:
            return Response(
                "User not found or details are incorrect.",
                status=status.HTTP_400_BAD_REQUEST,
            )

        reset_password_url = reverse(
            "accounts:set-new-password", kwargs={"user_id": user_profile.user_id}
        )
        return redirect(reset_password_url)


class SetNewPasswordView(UpdateAPIView):
    serializer_class = NewPasswordSerializer  # Replace with your actual serializer

    def update(self, request, *args, **kwargs):
        user_id = kwargs.get("user_id")
        new_password = request.data.get("new_password")

        try:
            user = CustomUser.objects.set_new_password(user_id, new_password)
            if not user:
                return Response("User not found.", status=status.HTTP_400_BAD_REQUEST)

            return Response("Password updated successfully.", status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
