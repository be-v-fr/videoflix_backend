from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils.timezone import now
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .utils import send_password_reset_email
import os
import six

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
    def delete_all_for_user(cls, user):
        instances = cls.objects.filter(user=user)
        instances.delete()

class AccountActivation(UserAction):
    """
    Email confirmation object including user emal and token.
    """
    pass

class PasswordReset(UserAction):
    """
    Password reset object including user email and token.
    """
    @classmethod
    def create_with_email(cls, user, token):
        instance = cls(user=user, token=token)
        instance.save()
        reset_url = os.environ['FRONTEND_BASE_URL'] + 'auth/pwReset/perform/' + instance.token
        send_password_reset_email(email_address=instance.user.email, reset_url=reset_url)
        return instance

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    """
    Custom token generator for account activation for better stability and code readability.
    """
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.is_active)
        )