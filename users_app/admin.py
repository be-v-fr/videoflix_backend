from django.contrib import admin
from .models import AccountActivation, PasswordReset 

admin.site.register(AccountActivation)
admin.site.register(PasswordReset)

