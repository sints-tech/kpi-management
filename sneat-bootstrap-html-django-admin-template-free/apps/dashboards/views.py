from django.views.generic import TemplateView
from web_project import TemplateLayout
from web_project.template_helpers.theme import TemplateHelper


"""
This file is a view controller for multiple pages as a module.
Here you can override the page view layout.
Refer to dashboards/urls.py file for more pages.
"""


class DashboardsView(TemplateView):
    # Predefined function
    def get_context_data(self, **kwargs):
        # A function to init the global layout. It is defined in web_project/__init__.py file
        try:
            context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        except Exception as e:
            # Fallback jika TemplateLayout.init gagal
            context = super().get_context_data(**kwargs)

        # Add KPI statistics dengan error handling
        from apps.kpi_management.models import Story, DailyFeedReels, Campaign, CollabBrand, FYPPostValue
        from django.db.models import Sum, Avg, Count
        from django.utils import timezone
        from datetime import timedelta
        import json

        try:
            total_stories = Story.objects.count()
        except Exception:
            total_stories = 0

        try:
            total_feeds = DailyFeedReels.objects.count()
        except Exception:
            total_feeds = 0

        try:
            total_campaigns = Campaign.objects.count()
        except Exception:
            total_campaigns = 0

        try:
            total_collabs = CollabBrand.objects.count()
        except Exception:
            total_collabs = 0

        try:
            total_fyp_posts = FYPPostValue.objects.count()
        except Exception:
            total_fyp_posts = 0

        # Revenue & Engagement Statistics
        try:
            total_revenue = CollabBrand.objects.filter(payment_status='paid').aggregate(Sum('contract_value'))['contract_value__sum'] or 0
            total_revenue = float(total_revenue) if total_revenue else 0.0
        except Exception:
            total_revenue = 0.0

        try:
            pending_revenue = CollabBrand.objects.filter(payment_status__in=['pending', 'partial']).aggregate(Sum('contract_value'))['contract_value__sum'] or 0
            pending_revenue = float(pending_revenue) if pending_revenue else 0.0
        except Exception:
            pending_revenue = 0.0

        try:
            avg_engagement_story = Story.objects.aggregate(Avg('engagement_rate'))['engagement_rate__avg'] or 0
        except Exception:
            avg_engagement_story = 0

        try:
            avg_engagement_feed = DailyFeedReels.objects.aggregate(Avg('engagement_rate'))['engagement_rate__avg'] or 0
        except Exception:
            avg_engagement_feed = 0

        engagement_avg = (avg_engagement_story + avg_engagement_feed) / 2 if (avg_engagement_story or avg_engagement_feed) else 0

        # Total Views & Reach
        try:
            total_views = (Story.objects.aggregate(Sum('views'))['views__sum'] or 0) + (DailyFeedReels.objects.aggregate(Sum('views'))['views__sum'] or 0)
        except Exception:
            total_views = 0

        try:
            total_reach = Story.objects.aggregate(Sum('reach'))['reach__sum'] or 0
        except Exception:
            total_reach = 0

        # Data untuk grafik - Trend performa 7 hari terakhir
        try:
            date_range = [timezone.now().date() - timedelta(days=x) for x in range(6, -1, -1)]
            trend_data = {
                'dates': [d.strftime('%d %b') for d in date_range],
                'views': [],
                'engagement': [],
                'reach': []
            }
            for date in date_range:
                try:
                    story_views = Story.objects.filter(story_date=date).aggregate(Sum('views'))['views__sum'] or 0
                    feed_views = DailyFeedReels.objects.filter(publish_date__date=date).aggregate(Sum('views'))['views__sum'] or 0
                    trend_data['views'].append(int(story_views + feed_views))
                except Exception:
                    trend_data['views'].append(0)

                try:
                    story_eng = Story.objects.filter(story_date=date).aggregate(Avg('engagement_rate'))['engagement_rate__avg'] or 0
                    feed_eng = DailyFeedReels.objects.filter(publish_date__date=date).aggregate(Avg('engagement_rate'))['engagement_rate__avg'] or 0
                    avg_eng = (story_eng + feed_eng) / 2 if (story_eng or feed_eng) else 0
                    trend_data['engagement'].append(round(avg_eng, 2))
                except Exception:
                    trend_data['engagement'].append(0)

                try:
                    story_reach = Story.objects.filter(story_date=date).aggregate(Sum('reach'))['reach__sum'] or 0
                    trend_data['reach'].append(int(story_reach))
                except Exception:
                    trend_data['reach'].append(0)
        except Exception:
            trend_data = {
                'dates': [],
                'views': [],
                'engagement': [],
                'reach': []
            }

        # Data untuk Platform Comparison
        try:
            platform_data = {
                'labels': ['Instagram', 'TikTok', 'Facebook', 'YouTube'],
                'story_count': [],
                'feed_count': []
            }
            for platform in ['instagram', 'tiktok', 'facebook', 'youtube']:
                try:
                    story_count = Story.objects.filter(platform=platform).count()
                    platform_data['story_count'].append(story_count)
                except Exception:
                    platform_data['story_count'].append(0)

                try:
                    feed_count = DailyFeedReels.objects.filter(platform=platform).count()
                    platform_data['feed_count'].append(feed_count)
                except Exception:
                    platform_data['feed_count'].append(0)
        except Exception:
            platform_data = {
                'labels': ['Instagram', 'TikTok', 'Facebook', 'YouTube'],
                'story_count': [0, 0, 0, 0],
                'feed_count': [0, 0, 0, 0]
            }

        # Data untuk Status Distribution
        try:
            story_status_count = {
                'draft': Story.objects.filter(status='draft').count(),
                'published': Story.objects.filter(status__in=['live', 'published']).count(),
                'archived': Story.objects.filter(status='archived').count(),
            }
            feed_status_count = {
                'draft': DailyFeedReels.objects.filter(status='draft').count(),
                'published': DailyFeedReels.objects.filter(status='published').count(),
                'scheduled': DailyFeedReels.objects.filter(status='scheduled').count(),
            }
            status_data = {
                'labels': ['Draft', 'Published', 'Scheduled', 'Archived'],
                'values': [
                    story_status_count.get('draft', 0) + feed_status_count.get('draft', 0),
                    story_status_count.get('published', 0) + feed_status_count.get('published', 0),
                    feed_status_count.get('scheduled', 0),
                    story_status_count.get('archived', 0),
                ]
            }
        except Exception:
            status_data = {
                'labels': ['Draft', 'Published', 'Scheduled', 'Archived'],
                'values': [0, 0, 0, 0]
            }

        # Data untuk Content Statistics Chart (Donut Chart)
        # Menggunakan data dari Stories, Feeds, Campaigns, Collabs
        try:
            total_content = total_stories + total_feeds + total_campaigns + total_collabs
            content_stats_data = {
                'labels': ['Stories', 'Feed/Reels', 'Campaigns', 'Collabs'],
                'series': [
                    total_stories if total_content > 0 else 0,
                    total_feeds if total_content > 0 else 0,
                    total_campaigns if total_content > 0 else 0,
                    total_collabs if total_content > 0 else 0,
                ]
            }
            # Jika semua 0, set default values untuk chart
            if total_content == 0:
                content_stats_data['series'] = [1, 1, 1, 1]  # Default untuk visualisasi
        except Exception:
            content_stats_data = {
                'labels': ['Stories', 'Feed/Reels', 'Campaigns', 'Collabs'],
                'series': [1, 1, 1, 1]
            }

        # Check admin permission
        try:
            from apps.kpi_management.views import check_admin_permission
            is_admin = check_admin_permission(self.request.user)
        except Exception:
            is_admin = False

        try:
            layout_path = TemplateHelper.set_layout("layout_vertical.html", context)
        except Exception:
            # Fallback jika TemplateHelper gagal
            layout_path = "layout/layout_vertical.html"

        context.update({
            "layout_path": layout_path,
            "total_stories": total_stories,
            "total_feeds": total_feeds,
            "total_campaigns": total_campaigns,
            "total_collabs": total_collabs,
            "total_fyp_posts": total_fyp_posts,
            "total_revenue": total_revenue,
            "pending_revenue": pending_revenue,
            "engagement_avg": round(engagement_avg, 2) if engagement_avg else 0.0,
            "total_views": total_views,
            "total_reach": total_reach,
            "trend_data": json.dumps(trend_data),
            "platform_data": json.dumps(platform_data),
            "status_data": json.dumps(status_data),
            "content_stats_data": json.dumps(content_stats_data),
            "is_admin": is_admin,
        })

        return context
