from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.db import connection


@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    """Auto log user login activity"""
    try:
        # Check if table exists
        with connection.cursor() as cursor:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='kpi_management_auditlog'")
            if not cursor.fetchone():
                return  # Table doesn't exist yet, skip logging

        from .models import AuditLog, get_client_ip

        AuditLog.objects.create(
            user=user,
            action='login',
            target_type='User',
            target_id=user.id,
            target_name=user.username,
            ip_address=get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
            description=f'User {user.username} logged in'
        )
    except Exception:
        # Silently fail if there's any error (table not created, etc)
        pass


