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
    
def send_account_activation_email(email_address, activation_url):
    """
    Sends an account activation email.
    The activation URL links to the frontend and must contain a valid token.
    """
    send_mail(
        "Activate your account by clicking the link below. The link will be valid for 24 hours.",
        f"Activation URL: {activation_url}",
        "noreply@videoflix.bengt-fruechtenicht.de",
        [email_address],
        fail_silently=False,
    )

def send_password_reset_email(email_address, reset_url):
    """
    Sends a password reset email.
    The reset URL links to the frontend and must contain a valid token.
    """
    send_mail(
        "Reset your password by clicking the link below. The link will be valid for 24 hours.",
        f"Reset URL: {reset_url}",
        "noreply@videoflix.bengt-fruechtenicht.de",
        [email_address],
        fail_silently=False,
    )