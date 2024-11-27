from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from users_app.utils import get_auth_response_data

class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login, handling email and password validation.
    """
    email = serializers.EmailField(max_length=63)
    password = serializers.CharField(max_length=63, write_only=True)
    
    def validate(self, attrs):
        try:
            username = User.objects.get(email=attrs['email']).username
        except:
            raise serializers.ValidationError('Invalid credentials.')
        auth_data = attrs.update(username=username)
        user = authenticate(**attrs)
        if not user:
            raise serializers.ValidationError('Invalid credentials.')            
        return attrs
    
    def create(self, validated_data):
        user = User.objects.get(email=validated_data['email'])
        token, created = Token.objects.get_or_create(user=user)
        return get_auth_response_data(user=user, token=token)              

class RegistrationSerializer(LoginSerializer):
    """
    Serializer for user registration, with password validation and email.
    """
    repeated_password = serializers.CharField(max_length=63, write_only=True)
    
    def validate(self, attrs):
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError('This email is already registered.')
        validate_password(attrs['password'])
        if attrs['repeated_password'] != attrs['password']:
            raise serializers.ValidationError('Passwords do not match.')
        attrs.pop('repeated_password')
        return attrs
    
    def create(self, validated_data):
        created_user = User.objects.create_user(username='User', **validated_data)
        created_user.username += str(created_user.pk)
        token = Token.objects.create(user=created_user)
        return get_auth_response_data(user=created_user, token=token) 
    
# class UserSerializer(serializers.HyperlinkedModelSerializer):
#     """
#     Serializer for basic user information.
#     """  
#     class Meta:
#         model = User
#         fields = ['pk', 'email']