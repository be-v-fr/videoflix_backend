from django.urls import path
from .views import LoginView, RegistrationView, RequestPasswordReset, PerformPasswordReset

PW_RESET_URL = 'reset-pw/'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', RegistrationView.as_view(), name='signup'),
    path(PW_RESET_URL + 'request/', RequestPasswordReset.as_view(), name='request-pw-reset'),
    path(PW_RESET_URL + 'perform/', PerformPasswordReset.as_view(), name='perform-pw-reset'),
]