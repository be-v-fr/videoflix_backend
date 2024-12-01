from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils.timezone import now
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .utils import send_account_activation_email, send_password_reset_email
import os
import six

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    """
    Custom token generator for account activation for better stability and code readability.
    """
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.is_active)
        )

class UserAction(models.Model):
    """
    Abstract model connecting a user to a token.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        abstract = True
        unique_together = ('token', 'user')
        
    def __str__(self):
        return f"{self.user.email} ({self.created_at})"

    def is_token_expired(self):
        expiration_time = self.created_at + timedelta(hours=24)
        return now() > expiration_time

    @classmethod
    def create_with_token(cls, user, token_generator_class):
        token = token_generator_class().make_token(user)
        instance = cls(user=user, token=token)
        instance.save()
        return instance        

    @classmethod
    def delete_all_for_user(cls, user):
        instances = cls.objects.filter(user=user)
        instances.delete()

class AccountActivation(UserAction):
    """
    Account activation model including user email and token.
    """
    @classmethod
    def create_with_email(cls, user):
        instance = cls.create_with_token(user, AccountActivationTokenGenerator)
        activation_url = os.environ['FRONTEND_BASE_URL'] + 'auth/signup/activate/' + instance.token
        send_account_activation_email(email_address=instance.user.email, activation_url=activation_url)
        return instance

class PasswordReset(UserAction):
    """
    Password reset model including user email and token.
    """
    @classmethod
    def create_with_email(cls, user):
        instance = cls.create_with_token(user, PasswordResetTokenGenerator)
        reset_url = os.environ['FRONTEND_BASE_URL'] + 'auth/pwReset/perform/' + instance.token
        send_password_reset_email(email_address=instance.user.email, reset_url=reset_url)
        return instance