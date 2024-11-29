from django.contrib import admin
from .models import EmailConfirmation, PasswordReset 

admin.site.register(EmailConfirmation)
admin.site.register(PasswordReset)

