from django.urls import path
from .views import DashboardsView
import logging

logger = logging.getLogger(__name__)

# Log untuk memastikan file ini ter-load
logger.info("Loading dashboards.urls - DashboardsView should be available")

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
