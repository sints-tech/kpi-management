from django.urls import path
from .views import DashboardsView



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
