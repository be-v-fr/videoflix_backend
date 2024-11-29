from django.core.mail import send_mail

def get_auth_response_data(user, token):
    """
    Constructs an authentication response data dictionary.
    """
    return {
        'token': token.key,
        'email': user.email,
        'user_id': user.pk,
    }

def send_password_reset_email(email_address, reset_url):
    """
    Sends a password reset email.
    The reset URL links to the frontend and must contain a valid token.
    """
    send_mail(
        "Reset your password",
        f"Reset URL: {reset_url}",
        "noreply@join.bengt-fruechtenicht.de",
        [email_address],
        fail_silently=False,
    )
    
def delete_existing_actions(user, queryset):
    for existing_action in queryset.objects.filter(user=user):
        existing_action.delete()