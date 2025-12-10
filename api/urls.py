from django.urls import path
from . import views
from .password_reset_views import request_password_reset, verify_reset_token, reset_password

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('password-reset/request/', request_password_reset, name='password_reset_request'),
    path('password-reset/verify/', verify_reset_token, name='password_reset_verify'),
    path('password-reset/reset/', reset_password, name='password_reset'),
]
