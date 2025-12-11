from django.urls import path
from . import views

app_name = 'kpi_management'

urlpatterns = [
    # Story URLs
    path('stories/', views.StoryListView.as_view(), name='story-list'),
    path('stories/create/', views.StoryCreateView.as_view(), name='story-create'),
    path('stories/<int:pk>/', views.StoryDetailView.as_view(), name='story-detail'),
    path('stories/<int:pk>/edit/', views.StoryUpdateView.as_view(), name='story-update'),
    path('stories/<int:pk>/delete/', views.StoryDeleteView.as_view(), name='story-delete'),
    path('stories/export-csv/', views.story_export_csv, name='story-export-csv'),
    path('stories/bulk-action/', views.story_bulk_action, name='story-bulk-action'),

    # Daily Feed/Reels URLs
    path('daily-feeds/', views.DailyFeedReelsListView.as_view(), name='dailyfeedreels-list'),
    path('daily-feeds/create/', views.DailyFeedReelsCreateView.as_view(), name='dailyfeedreels-create'),
    path('daily-feeds/<int:pk>/', views.DailyFeedReelsDetailView.as_view(), name='dailyfeedreels-detail'),
    path('daily-feeds/<int:pk>/edit/', views.DailyFeedReelsUpdateView.as_view(), name='dailyfeedreels-update'),
    path('daily-feeds/<int:pk>/delete/', views.DailyFeedReelsDeleteView.as_view(), name='dailyfeedreels-delete'),
    path('daily-feeds/export-csv/', views.dailyfeedreels_export_csv, name='dailyfeedreels-export-csv'),
    path('daily-feeds/bulk-action/', views.dailyfeedreels_bulk_action, name='dailyfeedreels-bulk-action'),

    # FYP Post Value URLs
    path('fyp-posts/', views.FYPPostValueListView.as_view(), name='fyppostvalue-list'),
    path('fyp-posts/create/', views.FYPPostValueCreateView.as_view(), name='fyppostvalue-create'),
    path('fyp-posts/<int:pk>/', views.FYPPostValueDetailView.as_view(), name='fyppostvalue-detail'),
    path('fyp-posts/<int:pk>/edit/', views.FYPPostValueUpdateView.as_view(), name='fyppostvalue-update'),
    path('fyp-posts/<int:pk>/delete/', views.FYPPostValueDeleteView.as_view(), name='fyppostvalue-delete'),
    path('fyp-posts/export-csv/', views.fyppostvalue_export_csv, name='fyppostvalue-export-csv'),

    # Campaign URLs
    path('campaigns/', views.CampaignListView.as_view(), name='campaign-list'),
    path('campaigns/create/', views.CampaignCreateView.as_view(), name='campaign-create'),
    path('campaigns/<int:pk>/', views.CampaignDetailView.as_view(), name='campaign-detail'),
    path('campaigns/<int:pk>/edit/', views.CampaignUpdateView.as_view(), name='campaign-update'),
    path('campaigns/<int:pk>/delete/', views.CampaignDeleteView.as_view(), name='campaign-delete'),
    path('campaigns/export-csv/', views.campaign_export_csv, name='campaign-export-csv'),

    # Collab Brand URLs
    path('collab-brands/', views.CollabBrandListView.as_view(), name='collabbrand-list'),
    path('collab-brands/create/', views.CollabBrandCreateView.as_view(), name='collabbrand-create'),
    path('collab-brands/<int:pk>/', views.CollabBrandDetailView.as_view(), name='collabbrand-detail'),
    path('collab-brands/<int:pk>/edit/', views.CollabBrandUpdateView.as_view(), name='collabbrand-update'),
    path('collab-brands/<int:pk>/delete/', views.CollabBrandDeleteView.as_view(), name='collabbrand-delete'),
    path('collab-brands/export-csv/', views.collabbrand_export_csv, name='collabbrand-export-csv'),

    # User Management URLs
    path('users/', views.UserListView.as_view(), name='user-list'),
    path('users/create/', views.UserCreateView.as_view(), name='user-create'),
    path('users/<int:pk>/edit/', views.UserUpdateView.as_view(), name='user-update'),
    path('users/<int:pk>/delete/', views.UserDeleteView.as_view(), name='user-delete'),

    # Social Media Account URLs
    path('social-media-accounts/', views.SocialMediaAccountListView.as_view(), name='socialmediaaccount-list'),
    path('social-media-accounts/create/', views.SocialMediaAccountCreateView.as_view(), name='socialmediaaccount-create'),
    path('social-media-accounts/<int:pk>/', views.SocialMediaAccountDetailView.as_view(), name='socialmediaaccount-detail'),
    path('social-media-accounts/<int:pk>/edit/', views.SocialMediaAccountUpdateView.as_view(), name='socialmediaaccount-update'),
    path('social-media-accounts/<int:pk>/delete/', views.SocialMediaAccountDeleteView.as_view(), name='socialmediaaccount-delete'),
    path('social-media-accounts/<int:pk>/sync/', views.sync_social_media_account, name='socialmediaaccount-sync'),
    path('social-media-accounts/<int:pk>/sync-insights/', views.sync_insights_social_media_account, name='socialmediaaccount-sync-insights'),

    # Profile URLs
    path('profile/', views.profile_view, name='profile-view'),
    path('profile/<int:user_id>/edit/', views.profile_edit, name='profile-edit'),

    # Dashboard Management URLs
    path('dashboard/', views.dashboard_management, name='dashboard-management'),
    path('dashboard/settings/', views.dashboard_settings_view, name='dashboard-settings'),
    path('dashboard/api/charts/', views.dashboard_charts_api, name='dashboard-charts-api'),

    # Report URLs
    path('reports/', views.ReportListView.as_view(), name='report-list'),
    path('reports/create/', views.ReportCreateView.as_view(), name='report-create'),
    path('reports/<int:pk>/', views.ReportDetailView.as_view(), name='report-detail'),
    path('reports/<int:pk>/export-pdf/', views.report_export_pdf, name='report-export-pdf'),
    path('reports/<int:pk>/export-excel/', views.report_export_excel, name='report-export-excel'),

    # Audit Log URLs
    path('audit-logs/', views.AuditLogListView.as_view(), name='auditlog-list'),
    path('audit-logs/api/charts/', views.audit_log_charts_api, name='auditlog-charts-api'),

    # FYP Leaderboard
    path('fyp-leaderboard/', views.fyp_leaderboard, name='fyp-leaderboard'),

    # Calendar Scheduling
    path('calendar/', views.calendar_scheduling, name='calendar-scheduling'),

    # System Settings / Pengaturan URLs
    path('settings/', views.SystemSettingsListView.as_view(), name='settings-list'),
    path('settings/create/', views.SystemSettingsCreateView.as_view(), name='settings-create'),
    path('settings/<int:pk>/', views.SystemSettingsDetailView.as_view(), name='settings-detail'),
    path('settings/<int:pk>/edit/', views.SystemSettingsUpdateView.as_view(), name='settings-update'),
    path('settings/<int:pk>/delete/', views.SystemSettingsDeleteView.as_view(), name='settings-delete'),
    path('settings/theme/', views.theme_settings_view, name='settings-theme'),
    path('settings/language/', views.language_settings_view, name='settings-language'),
    path('settings/toggle-theme/', views.toggle_theme, name='toggle-theme'),
    path('settings/set-language/', views.set_language, name='set-language'),
]

