from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CustomUserSerializer
from django.contrib.auth.models import update_last_login
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import CustomUser
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.password_validation import validate_password
from rest_framework.permissions import AllowAny


class RegisterAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Handle POST request for user registration.
        """
        serializer = CustomUserSerializer(data=request.data)

        if serializer.is_valid():
            # Save the user and get the instance
            user = serializer.save()

            # Update the last login field
            update_last_login(None, user)

            # Get JWT tokens for the registered user
            tokens = serializer.get_tokens(user)

            # Return the user data and tokens
            return Response(
                {
                    "user": {
                        "email": user.email,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                    },
                    "tokens": tokens,
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    """
    Handle POST request for user login.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        # Authenticate the user
        user = authenticate(request, email=email, password=password)

        if user is not None:
            # Update the last login field
            update_last_login(None, user)

            # Use the serializer's get_tokens method
            serializer = CustomUserSerializer()
            tokens = serializer.get_tokens(user)

            # Return the user data and tokens
            return Response(
                {
                    "user": {
                        "email": user.email,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                    },
                    "tokens": tokens,
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )


class LogoutAPIView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()  # Invalidate the token
            return Response(
                {"message": "logout successfully"}, status=status.HTTP_205_RESET_CONTENT
            )
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class PasswordResetRequestAPIView(APIView):
    def post(self, request):
        email = request.data.get("email")
        user = CustomUser.objects.filter(email=email).first()

        if user:
            token = PasswordResetTokenGenerator().make_token(user)
            # Generate a password reset link with token (e.g., frontend link)
            reset_link = f"http://frontend.com/reset-password/{token}"
            send_mail(
                "Password Reset Request",
                f"Use this link to reset your password: {reset_link}",
                "admin@yourapp.com",
                [email],
                fail_silently=False,
            )
            return Response(
                {"detail": "Password reset email sent"}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"detail": "User with this email not found"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class PasswordResetConfirmAPIView(APIView):
    def post(self, request, token):
        password = request.data.get("password")
        user = CustomUser.objects.filter(email=request.data.get("email")).first()

        if user and PasswordResetTokenGenerator().check_token(user, token):
            user.set_password(password)
            user.save()
            return Response(
                {"detail": "Password successfully reset"}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"detail": "Invalid token or user"}, status=status.HTTP_400_BAD_REQUEST
            )


class ChangePasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")

        if not user.check_password(old_password):
            return Response(
                {"detail": "Old password is incorrect"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        validate_password(new_password, user=user)
        user.set_password(new_password)
        user.save()
        return Response(
            {"detail": "Password successfully changed"}, status=status.HTTP_200_OK
        )


class ProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)

    def put(self, request):
        user = request.user
        serializer = CustomUserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
