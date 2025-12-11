"""
Debug views untuk membantu troubleshoot di production
HAPUS file ini setelah production stabil!
"""

from django.http import JsonResponse
from django.views import View
from django.db import connection
from django.conf import settings
import traceback


class HealthCheckView(View):
    """Health check endpoint untuk cek status aplikasi"""
    
    def get(self, request):
        data = {
            'status': 'ok',
            'debug': settings.DEBUG,
            'database': {
                'connected': False,
                'tables': []
            }
        }
        
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                data['database']['connected'] = True
                
                # Cek tables
                if 'postgresql' in settings.DATABASES['default']['ENGINE']:
                    cursor.execute("""
                        SELECT table_name 
                        FROM information_schema.tables 
                        WHERE table_schema = 'public'
                        ORDER BY table_name
                    """)
                    data['database']['tables'] = [row[0] for row in cursor.fetchall()]
        except Exception as e:
            data['database']['error'] = str(e)
        
        return JsonResponse(data)


class RunMigrationsView(View):
    """
    Endpoint untuk run migrations via HTTP
    PERINGATAN: Hanya untuk development/free tier!
    HAPUS setelah production!
    """
    
    def post(self, request):
        # Simple security: cek secret key di request
        secret = request.POST.get('secret') or request.GET.get('secret')
        if secret != 'run_migrations_2025':
            return JsonResponse({'error': 'Unauthorized'}, status=403)
        
        try:
            from django.core.management import call_command
            from io import StringIO
            
            output = StringIO()
            call_command('migrate', verbosity=2, stdout=output, interactive=False)
            
            return JsonResponse({
                'status': 'success',
                'output': output.getvalue()
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'error': str(e),
                'traceback': traceback.format_exc()
            }, status=500)

