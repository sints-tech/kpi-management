from django.urls import path
from django.views.generic import TemplateView
from django.http import HttpResponse
import logging

logger = logging.getLogger(__name__)

# Import dengan error handling untuk mencegah crash saat URL routing
try:
    from .views import DashboardsView
except Exception as e:
    logger.error(f"Error importing DashboardsView: {e}", exc_info=True)
    # Fallback view jika import gagal
    class DashboardsView(TemplateView):
        template_name = "dashboard_kpi.html"
        def get(self, request, *args, **kwargs):
            return HttpResponse("Dashboard view error. Please check logs.", status=500)

urlpatterns = [
    path(
        "",
        DashboardsView.as_view(template_name="dashboard_kpi.html"),
        name="index",
    ),
    path(
        "dashboard-analytics/",
        DashboardsView.as_view(template_name="dashboard_analytics.html"),
        name="dashboard-analytics",
    )
]
