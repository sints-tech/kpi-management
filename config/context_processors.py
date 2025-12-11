from django.conf import settings
from apps.kpi_management.translations import TRANSLATIONS, get_translation


def my_setting(request):
    return {'MY_SETTING': settings}


# Add the 'ENVIRONMENT' setting to the template context
def environment(request):
    return {'ENVIRONMENT': settings.ENVIRONMENT}


# Add is_admin to context for menu
def kpi_context(request):
    is_admin = False
    # Check if user attribute exists and is authenticated
    if hasattr(request, 'user') and request.user.is_authenticated:
        try:
            from apps.kpi_management.models import Profile
            # Use select_related to avoid extra queries
            profile = Profile.objects.select_related('user').filter(user=request.user).first()
            if profile:
                # Check if profile has is_admin property
                try:
                    is_admin = profile.is_admin
                except (AttributeError, Exception):
                    # Fallback: check role field directly
                    is_admin = getattr(profile, 'role', 'user') == 'admin'
        except Exception as e:
            # Log error but don't break the page
            import logging
            logger = logging.getLogger(__name__)
            logger.debug(f"Error in kpi_context: {e}")
            pass

    # Get theme from session
    theme = request.session.get('theme', 'light')

    # Get language from session
    language = request.session.get('language', 'id')
    
    # Get translation dictionary for current language
    translations = TRANSLATIONS.get(language, TRANSLATIONS['id'])

    def translate(key):
        """Helper function untuk translation di template"""
        return translations.get(key, key)
    
    return {
        'is_admin': is_admin,
        'theme': theme,
        'language': language,
        'trans': translations,  # Translation dictionary
        'translate': translate,  # Translation function
    }
