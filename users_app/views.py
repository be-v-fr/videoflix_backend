from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import LoginSerializer, RegistrationSerializer

class LoginView(APIView):
    """
    API endpoint for user login.
    """
    # permission_classes = [permissions.AllowAny]

    def post(self, request):
        """
        Authenticates the user and returns a response with authentication data.
        """
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            response_data = serializer.save()
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegistrationView(APIView):
    """
    API endpoint for user registration.
    """
    # permission_classes = [permissions.AllowAny]

    def post(self, request):
        """
        Registers a new user, creating a profile and returning response data.
        """
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            response_data = serializer.save()
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    