import os
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import EmailConfirmation, PasswordReset
from .utils import get_auth_response_data, send_password_reset_email, delete_existing_actions

class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login, handling email and password validation.
    """
    email = serializers.EmailField(max_length=63)
    password = serializers.CharField(max_length=63, write_only=True)
    
    def validate(self, attrs):
        try:
            username = User.objects.get(email=attrs['email']).username
        except User.DoesNotExist:
            raise serializers.ValidationError('Invalid credentials.')
        attrs.update(username=username)
        user = authenticate(**attrs)
        if not user:
            raise serializers.ValidationError('Invalid credentials.')            
        return attrs
    
    def create(self, validated_data):
        user = User.objects.get(email=validated_data['email'])
        token, created = Token.objects.get_or_create(user=user)
        return get_auth_response_data(user=user, token=token)              

class RegistrationSerializer(serializers.Serializer):
    """
    Serializer for user registration, handling email and password validation.
    """
    email = serializers.EmailField(max_length=63)
    password = serializers.CharField(max_length=63, write_only=True)
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('This email is already registered.')
        return value
    
    def validate_password(self, value):
        validate_password(value)
        return value
    
    def create(self, validated_data):
        created_user = User.objects.create_user(username='User', **validated_data)
        created_user.username += str(created_user.pk)
        created_user.save()
        token = Token.objects.create(user=created_user)
        return get_auth_response_data(user=created_user, token=token)
    
# class UserSerializer(serializers.HyperlinkedModelSerializer):
#     """
#     Serializer for basic user information.
#     """  
#     class Meta:
#         model = User
#         fields = ['pk', 'email']

class RequestPasswordResetSerializer(serializers.Serializer):
    """
    Serializer for password reset requests.
    """
    email = serializers.EmailField(write_only=True, required=True)
    
    def create(self, validated_data):
        email = validated_data['email']
        user = User.objects.filter(email__iexact=email).first()
        if user:
            delete_existing_actions(user=user, queryset=PasswordReset)
            token_generator = PasswordResetTokenGenerator()
            token = token_generator.make_token(user)
            new_reset_obj = PasswordReset(user=user, token=token)
            new_reset_obj.save()
            reset_url = os.environ['FRONTEND_BASE_URL'] + 'auth/pwReset/perform/' + token
            send_password_reset_email(email_address=email, reset_url=reset_url)
        return {'success': 'We have sent you a link to reset your password.'}
    
    
class PerformPasswordResetSerializer(serializers.Serializer):
    """
    Serializer for performing password resets.
    """
    new_password = serializers.CharField(max_length=63, write_only=True)
    token = serializers.CharField(write_only=True, required=True)
    
    def validate_new_password(self, value):
        validate_password(value)
        return value
    
    def validate_token(self, value):
        try:
            reset_obj = PasswordReset.objects.get(token=value)
        except PasswordReset.DoesNotExist:
            raise serializers.ValidationError('Invalid token.')
        if reset_obj.is_token_expired():
            reset_obj.delete()
            raise serializers.ValidationError('Your token is expired.')            
        return value
        
    def create(self, validated_data):
        new_password = validated_data['new_password']
        reset_obj = PasswordReset.objects.get(token=validated_data['token'])
        reset_obj.user.set_password(new_password)
        reset_obj.user.save()
        reset_obj.delete()
        return {'success':'Password updated'}