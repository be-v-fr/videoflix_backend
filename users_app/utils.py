def get_auth_response_data(user, token):
    """
    Constructs an authentication response data dictionary.
    """
    return {
        'token': token.key,
        'email': user.email,
        'user_id': user.pk,
    }