from rest_framework import serializers
from .models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.password_validation import validate_password


class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )
    password2 = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )

    class Meta:
        model = CustomUser
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "password",
            "password2",
            "is_active",
            "is_staff",
        )

    def validate(self, data):
        """
        Ensure the two password fields match.
        """
        if data["password"] != data["password2"]:
            raise serializers.ValidationError("Passwords do not match.")
        validate_password(data["password"])
        return data

    def create(self, validated_data):
        """
        Create and return a new user instance, given the validated data.
        """
        validated_data.pop("password2")  # Remove password2 from the validated_data
        password = validated_data.pop("password")
        user = CustomUser(**validated_data)
        user.set_password(password)  # Hash the password
        user.save()
        return user

    def update(self, instance, validated_data):
        """
        Update and return an existing user instance, given the validated data.
        """
        validated_data.pop(
            "password2", None
        )  # Remove password2 from validated_data if present
        password = validated_data.pop("password", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(
                password
            )  # If password is updated, hash the new password

        instance.save()
        return instance

    def get_tokens(self, user):
        """
        Generate JWT tokens for the user
        """
        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

