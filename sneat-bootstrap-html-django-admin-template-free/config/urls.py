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

# Try to include dashboards.urls with error handling
try:
    dashboard_urls = include("apps.dashboards.urls")
except Exception as e:
    logger.error(f"Error including dashboards.urls: {e}", exc_info=True)
    # Fallback: create a simple view directly
    from django.views.generic import TemplateView
    from django.http import HttpResponse
    def index_fallback(request):
        return HttpResponse("Dashboard routing error. Please check logs.", status=500)
    dashboard_urls = [path("", index_fallback, name="index")]

urlpatterns = [
    path("admin/", admin.site.urls),

    # Dashboard urls - IMPORTANT: This must be first to catch root URL
    path("", dashboard_urls),

    # layouts urls
    path("", include("apps.layouts.urls")),

    # Pages urls
    path("", include("apps.pages.urls")),

    # Auth urls
    path("", include("apps.authentication.urls")),

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

    # KPI Management urls
    path("kpi/", include("apps.kpi_management.urls")),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Error handlers - hanya untuk URL yang benar-benar tidak ditemukan
# Catatan: Handler ini hanya dipanggil jika URL tidak match dengan pattern apapun
# Jangan menangkap static files - WhiteNoise sudah menangani itu
handler404 = SystemView.as_view(template_name="pages_misc_error.html", status=404)
handler400 = SystemView.as_view(template_name="pages_misc_error.html", status=400)
handler500 = SystemView.as_view(template_name="pages_misc_error.html", status=500)
