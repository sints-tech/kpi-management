from django.urls import path
from .views import AuthView
import logging

logger = logging.getLogger(__name__)

# Log to ensure this file is loaded
logger.info("Loading apps.authentication.urls - AuthView should be available")

urlpatterns = [
    path(
        "auth/login/",
        AuthView.as_view(template_name="auth_login_basic.html"),
        name="auth-login-basic",
    ),
    path(
        "auth/register/",
        AuthView.as_view(template_name="auth_register_basic.html"),
        name="auth-register-basic",
    ),
    path(
        "auth/forgot_password/",
        AuthView.as_view(template_name="auth_forgot_password_basic.html"),
        name="auth-forgot-password-basic",
    ),
]

logger.info(f"Authentication URLs loaded: {len(urlpatterns)} patterns registered")
