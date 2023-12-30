from rest_framework import serializers
from .models import CustomUser, UserProfile
from rest_framework_simplejwt.tokens import RefreshToken


# REGISTER
################################################################
class UserProfileSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(
        source="user.phone_number", read_only=True)

    class Meta:
        model = UserProfile
        fields = ("id", "age", "fullname", "email", "username", "phone_number")
        read_only_fields = ("id", "phone_number")


class CustomUserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(required=False)
    phone_number = serializers.CharField()
    password = serializers.CharField(
        write_only=True, style={"input_type": "password"})
    password_confirm = serializers.CharField(
        write_only=True, style={"input_type": "password"}
    )

    class Meta:
        model = CustomUser
        fields = (
            "id",
            "phone_number",
            "password",
            "password_confirm",
            "profile",
            "is_admin",
        )
        read_only_fields = ("id",)

    def create(self, validated_data):
        profile_data = validated_data.pop("profile", None)
        phone_number = validated_data.pop("phone_number", None)
        password = validated_data.pop("password")
        password_confirm = validated_data.pop("password_confirm")

        if password != password_confirm:
            raise serializers.ValidationError("Passwords do not match.")

        user = CustomUser.objects.create(phone_number=phone_number)
        user.set_password(password)
        user.save()

        if profile_data:
            UserProfile.objects.create(user=user, **profile_data)

        return user


class UserLoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField(style={"input_type": "password"})

    def validate(self, data):
        phone_number = data.get("phone_number")
        password = data.get("password")

        if phone_number and password:
            user = CustomUser.objects.filter(phone_number=phone_number).first()

            if user and user.check_password(password):
                refresh = RefreshToken.for_user(user)
<<<<<<< HEAD

                # Get additional user info to include in the token payload
                additional_info = {
                    "user_id": user.id,
                    "phone_number": user.phone_number,
                    "is_admin": user.is_admin,  # Modify this based on your model
                    # Add other desired user info
                }

                # Update the token's payload with additional user info
=======
                additional_info = {
                    "user_id": user.id,
                    "phone_number": user.phone_number,
                    "is_admin": user.is_admin,
                }

>>>>>>> 3ca20dd1f5fac3575221ebc6627f2adf559bb98f
                refresh.payload.update(additional_info)

                data["tokens"] = {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }
            else:
                raise serializers.ValidationError(
                    "Incorrect phone number or password.")
        else:
            raise serializers.ValidationError(
                "Phone number and password are required.")

        return data


# USER LIST
# ----------------------------------------------------------------
class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserProfile
        fields = ("age", "fullname", "email", "username")


class UserDetailSerializer(serializers.HyperlinkedModelSerializer):
    profile = UserProfileSerializer(required=False)

    class Meta:
        model = CustomUser
        fields = (
            "id",
            "phone_number",
            "is_admin",
            "is_staff",
            "is_superuser",
            "profile",
        )
 
    def to_representation(self, instance):
        data = super().to_representation(instance)
        try:
            profile_instance = instance.userprofile
            data["profile"] = UserProfileSerializer(profile_instance).data
        except UserProfile.DoesNotExist:
            data["profile"] = None
        return data

<<<<<<< HEAD
    #------------------
    def update(self, instance, validated_data):
        # Update user profile data
=======
    # ------------------
    def update(self, instance, validated_data):
>>>>>>> 3ca20dd1f5fac3575221ebc6627f2adf559bb98f
        print("Update method called")
        print(f"Validated Data: {validated_data}")
        profile_data = validated_data.pop("profile", {})
        if instance.userprofile:
            instance.userprofile.age = profile_data.get("age", instance.userprofile.age)
<<<<<<< HEAD
            instance.userprofile.fullname = profile_data.get("fullname", instance.userprofile.fullname)
            instance.userprofile.email = profile_data.get("email", instance.userprofile.email)
            instance.userprofile.username = profile_data.get("username", instance.userprofile.username)
            instance.userprofile.save(force_update=True)

        # Update user data
        instance.phone_number = validated_data.get("phone_number", instance.phone_number)
        instance.is_staff = validated_data.get("is_staff", instance.is_staff)
        instance.is_superuser = validated_data.get("is_superuser", instance.is_superuser)
=======
            instance.userprofile.fullname = profile_data.get(
                "fullname", instance.userprofile.fullname
            )
            instance.userprofile.email = profile_data.get(
                "email", instance.userprofile.email
            )
            instance.userprofile.username = profile_data.get(
                "username", instance.userprofile.username
            )
            instance.userprofile.save(force_update=True)

        instance.phone_number = validated_data.get(
            "phone_number", instance.phone_number
        )
        instance.is_staff = validated_data.get("is_staff", instance.is_staff)
        instance.is_superuser = validated_data.get(
            "is_superuser", instance.is_superuser
        )
>>>>>>> 3ca20dd1f5fac3575221ebc6627f2adf559bb98f
        instance.is_admin = validated_data.get("is_admin", instance.is_admin)
        instance.save(force_update=True)

        return instance


# USER EDIT
################################################################
class UserProfileEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
<<<<<<< HEAD
        # Fields user can edit
        fields = ("age", "fullname", "email", "username")
=======
        fields = ("age", "fullname", "email", "username")


# RESET PASSWORD
# ----------------------------------------------------------------
class PasswordResetSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    age = serializers.IntegerField()
    username = serializers.CharField()

    def validate(self, data):
        return data


class NewPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(
        write_only=True, style={"input_type": "password"}
    )

    def validate(self, data):
        return data
>>>>>>> 3ca20dd1f5fac3575221ebc6627f2adf559bb98f
