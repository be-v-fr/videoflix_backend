from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils.timezone import now

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

class PasswordReset(UserAction):
    """
    Password reset object including user email and token.
    """
    pass

class EmailConfirmation(UserAction):
    """
    Email confirmation object including user emal and token.
    """
    pass