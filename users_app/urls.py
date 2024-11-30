from django.urls import path
from .views import LoginView, RegistrationView, ActivateAccount, RequestPasswordReset, PerformPasswordReset

SIGNUP_URL = 'signup/'
PW_RESET_URL = 'reset-pw/'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path(SIGNUP_URL, RegistrationView.as_view(), name='signup'),
    path(SIGNUP_URL + 'activate/', ActivateAccount.as_view(), name='activate-account'),
    path(PW_RESET_URL + 'request/', RequestPasswordReset.as_view(), name='request-pw-reset'),
    path(PW_RESET_URL + 'perform/', PerformPasswordReset.as_view(), name='perform-pw-reset'),
]