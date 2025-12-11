"""
URL configuration for web_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from web_project.views import SystemView
import logging

logger = logging.getLogger(__name__)

urlpatterns = [
    path("admin/", admin.site.urls),
]

# Debug endpoints (HAPUS setelah production stabil!)
try:
    from apps.dashboards.views_debug import HealthCheckView, RunMigrationsView
    urlpatterns += [
        path("health/", HealthCheckView.as_view(), name="health-check"),
        path("run-migrations/", RunMigrationsView.as_view(), name="run-migrations"),
    ]
except ImportError as e:
    # Jika views_debug tidak ada, skip debug endpoints
    import logging
    logger = logging.getLogger(__name__)
    logger.warning(f"Debug views not available: {e}")

# Import authentication URLs module to verify it loads correctly
try:
    from apps.authentication import urls as auth_urls
    logger.info("Successfully imported apps.authentication.urls")
    # Log the URL patterns from authentication app
    logger.info(f"Authentication URL patterns: {[str(p.pattern) for p in auth_urls.urlpatterns]}")
except Exception as e:
    logger.error(f"Failed to import apps.authentication.urls: {e}", exc_info=True)

# IMPORTANT: Order matters! More specific patterns should come first
urlpatterns += [
    # KPI Management urls - Most specific, must come first
    path("kpi/", include("apps.kpi_management.urls")),
    
    # Auth urls - Specific paths, must come before catch-all patterns
    path("", include("apps.authentication.urls")),

    # Dashboard urls - Has catch-all pattern "", so comes after specific patterns
    path("", include("apps.dashboards.urls")),

    # layouts urls
    path("", include("apps.layouts.urls")),

    # Pages urls
    path("", include("apps.pages.urls")),

    # Card urls
    path("", include("apps.cards.urls")),

    # UI urls
    path("", include("apps.ui.urls")),

    # Extended UI urls
    path("", include("apps.extended_ui.urls")),

    # Icons urls
    path("", include("apps.icons.urls")),

    # Forms urls
    path("", include("apps.forms.urls")),

    # FormLayouts urls
    path("", include("apps.form_layouts.urls")),

    # Tables urls
    path("", include("apps.tables.urls")),
]

logger.info(f"Total URL patterns registered: {len(urlpatterns)}")
# Log all URL patterns for debugging - use info level so it shows in production
for i, pattern in enumerate(urlpatterns):
    logger.info(f"URL pattern {i+1}: {pattern}")
    
# Specifically log authentication URLs
try:
    from apps.authentication import urls as auth_urls
    logger.info("=" * 50)
    logger.info("AUTHENTICATION URL PATTERNS:")
    for i, pattern in enumerate(auth_urls.urlpatterns):
        logger.info(f"  {i+1}. Pattern: {pattern.pattern}, View: {pattern.callback}, Name: {pattern.name}")
    logger.info("=" * 50)
except Exception as e:
    logger.error(f"Error logging authentication URLs: {e}", exc_info=True)

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Serve static files in development
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# CATATAN: Untuk production, WhiteNoise middleware akan menangani static files
# Jangan tambahkan static file serving di sini untuk production karena akan mengganggu WhiteNoise

handler404 = SystemView.as_view(template_name="pages_misc_error.html", status=404)
handler400 = SystemView.as_view(template_name="pages_misc_error.html", status=400)
handler500 = SystemView.as_view(template_name="pages_misc_error.html", status=500)
