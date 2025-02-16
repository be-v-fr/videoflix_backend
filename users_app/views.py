from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import LoginSerializer, RegistrationSerializer, UserSerializer
from .serializers import AccountActivationSerializer
from .serializers import RequestPasswordResetSerializer, PerformPasswordResetSerializer

class LoginView(APIView):
    """
    API endpoint for user login.
    """
    authentication_classes = []
    permission_classes = [AllowAny]

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
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Registers a new user, creating a profile and returning response data.
        """
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            response_data = serializer.save()
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserView(APIView):
    """
    API endpoint for user profile access.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Retrieves user profile.
        """
        serializer = UserSerializer(instance=request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class ActivateAccount(APIView):
    """
    Performs account activation and deletes the corresponding account activation object.
    """
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Executes the password reset logic.
        """
        serializer = AccountActivationSerializer(data=request.data)
        if serializer.is_valid():
            response_data = serializer.save()
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class RequestPasswordReset(APIView):
    """
    Handles password reset requests by creating a password reset object.
    """
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Executes the password reset request logic.
        """
        serializer = RequestPasswordResetSerializer(data=request.data) 
        if serializer.is_valid():
            response_data = serializer.save()
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class PerformPasswordReset(APIView):
    """
    Performs password reset and deletes the corresponding password reset object.
    """
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Executes the password reset logic.
        """
        serializer = PerformPasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            response_data = serializer.save()
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)