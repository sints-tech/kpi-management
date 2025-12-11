from django.utils import translation
from django.conf import settings


class LanguageMiddleware:
    """
    Middleware untuk mengaktifkan bahasa berdasarkan session user
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get language from session, default to 'id' (Bahasa Indonesia)
        language = request.session.get('language', 'id')
        
        # Validasi bahasa (hanya id dan en yang diizinkan)
        if language not in ['id', 'en']:
            language = 'id'
        
        # Aktifkan bahasa di Django
        translation.activate(language)
        request.LANGUAGE_CODE = language
        
        response = self.get_response(request)
        
        # Deactivate setelah response
        translation.deactivate()
        
        return response

