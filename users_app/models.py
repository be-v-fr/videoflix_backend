from django.db import models
from django.contrib.auth.models import User

class UserAction(models.Model):
    """
    Abstract model connecting a user to a token.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        abstract = True
        
    def __str__(self):
        return f"{self.user.email} ({self.created_at})"   

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