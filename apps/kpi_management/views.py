from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator
import csv
import json
from web_project import TemplateLayout
from web_project.template_helpers.theme import TemplateHelper

from .models import (
    Story, DailyFeedReels, FeedReelsHistory, FYPPostValue, Campaign, CollabBrand,
    Profile, DashboardSettings, Report, AuditLog, SystemSettings, SocialMediaAccount, Company
)
from .forms import (
    StoryForm, DailyFeedReelsForm, FYPPostValueForm,
    CampaignForm, CollabBrandForm, ProfileForm, UserForm,
    DashboardSettingsForm, ReportForm, SystemSettingsForm, SocialMediaAccountForm
)
from django.utils import timezone
from django.http import JsonResponse, HttpResponse
from django.db.models import Count, Avg, Sum, Q
from django.core.paginator import Paginator


def get_companies_safe():
    """Get companies safely, return empty list if table doesn't exist"""
    try:
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='kpi_management_company'")
            if cursor.fetchone():
                return Company.objects.filter(is_active=True).order_by('company_type', 'name')
    except Exception:
        pass
    return []


def get_campaigns_safe():
    """Get campaigns safely, handling missing company_id column"""
    try:
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("PRAGMA table_info(kpi_management_campaign)")
            columns = [col[1] for col in cursor.fetchall()]
            if 'company_id' in columns:
                return Campaign.objects.all()
            else:
                # If company_id doesn't exist, defer it
                return Campaign.objects.defer('company')
    except Exception:
        return Campaign.objects.none()


def check_admin_permission(user):
    """Check if user is admin"""
    if not user or not user.is_authenticated:
        return False
    try:
        # Use select_related to avoid extra queries and handle missing fields gracefully
        profile = Profile.objects.select_related('user').filter(user=user).first()
        if profile:
            # Check if profile has is_admin property (handle case where field might not exist yet)
            try:
                return profile.is_admin
            except (AttributeError, Exception):
                # Fallback: check role field directly
                return getattr(profile, 'role', 'user') == 'admin'
        return False
    except (Profile.DoesNotExist, Exception):
        return False


class BaseKPIView(LoginRequiredMixin):
    """Base view class for KPI management"""
    login_url = '/auth/login/'
    redirect_field_name = 'next'

    def get_context_data(self, **kwargs):
        # A function to init the global layout. It is defined in web_project/__init__.py file
        # TemplateLayout.init already calls TemplateHelper.set_layout, so we don't need to call it again
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context


# ==================== STORY CRUD ====================

class StoryListView(BaseKPIView, ListView):
    model = Story
    template_name = 'kpi_management/story_list.html'
    context_object_name = 'stories'  # Tetap tersedia untuk backward compatibility
    paginate_by = 20

    def get_queryset(self):
        # Hanya gunakan select_related untuk field yang pasti ada
        queryset = Story.objects.select_related('campaign', 'collab_brand', 'created_by').all()
        search = self.request.GET.get('search', '')
        platform = self.request.GET.get('platform', '')
        status = self.request.GET.get('status', '')
        campaign = self.request.GET.get('campaign', '')
        user = self.request.GET.get('user', '')
        company = self.request.GET.get('company', '')
        account_name = self.request.GET.get('account_name', '')

        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(account_name__icontains=search)
            )
        if platform:
            queryset = queryset.filter(platform=platform)
        if status:
            queryset = queryset.filter(status=status)
        if campaign:
            queryset = queryset.filter(campaign_id=campaign)
        if user:
            queryset = queryset.filter(created_by_id=user)
        if company:
            try:
                queryset = queryset.filter(company_id=company)
            except Exception:
                # Jika field company belum ada, skip filter ini
                pass
        if account_name:
            queryset = queryset.filter(account_name=account_name)

        return queryset.order_by('-story_date', '-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_admin'] = check_admin_permission(self.request.user)
        try:
            context['campaigns'] = get_campaigns_safe().order_by('-start_date')[:50]
        except Exception:
            context['campaigns'] = []

        context['companies'] = get_companies_safe()
        
        # Get social media accounts for filter
        try:
            context['social_media_accounts'] = SocialMediaAccount.objects.filter(status='active').order_by('platform', 'account_name')
        except Exception:
            context['social_media_accounts'] = []

        # Analytics data untuk Story Management
        from django.db.models import Avg, Count, Sum
        from django.utils import timezone
        from datetime import timedelta

        # Performance Trend - 30 hari terakhir (separate try-except)
        try:
            date_range = [timezone.now().date() - timedelta(days=x) for x in range(29, -1, -1)]
            trend_data = {
                'dates': [d.strftime('%d %b') for d in date_range],
                'views': [],
                'engagement': [],
                'reach': []
            }
            for date in date_range:
                try:
                    story_views = Story.objects.filter(story_date=date).aggregate(Sum('views'))['views__sum'] or 0
                    trend_data['views'].append(int(story_views))
                except Exception:
                    trend_data['views'].append(0)

                try:
                    story_eng = Story.objects.filter(story_date=date).aggregate(Avg('engagement_rate'))['engagement_rate__avg'] or 0
                    trend_data['engagement'].append(round(story_eng, 2))
                except Exception:
                    trend_data['engagement'].append(0)

                try:
                    story_reach = Story.objects.filter(story_date=date).aggregate(Sum('reach'))['reach__sum'] or 0
                    trend_data['reach'].append(int(story_reach))
                except Exception:
                    trend_data['reach'].append(0)

            context['story_trend_data'] = json.dumps(trend_data)
        except Exception as e:
            context['story_trend_data'] = json.dumps({'dates': [], 'views': [], 'engagement': [], 'reach': []})

        # Platform Comparison (separate try-except)
        try:
            platform_data = {
                'labels': ['Instagram', 'TikTok', 'Facebook', 'YouTube'],
                'avg_engagement': [],
                'total_views': [],
                'count': []
            }
            platform_mapping = {
                'instagram': ['instagram'],
                'tiktok': ['tiktok'],
                'facebook': ['facebook'],
                'youtube': ['youtube', 'youtube_long']
            }
            
            for platform_key in ['instagram', 'tiktok', 'facebook', 'youtube']:
                try:
                    platform_values = platform_mapping.get(platform_key, [platform_key])
                    platform_filter = Q()
                    for pv in platform_values:
                        platform_filter |= Q(platform__iexact=pv)
                    
                    stories = Story.objects.filter(platform_filter)
                    platform_data['avg_engagement'].append(
                        round(stories.aggregate(Avg('engagement_rate'))['engagement_rate__avg'] or 0, 2)
                    )
                    platform_data['total_views'].append(
                        int(stories.aggregate(Sum('views'))['views__sum'] or 0)
                    )
                    platform_data['count'].append(stories.count())
                except Exception:
                    platform_data['avg_engagement'].append(0)
                    platform_data['total_views'].append(0)
                    platform_data['count'].append(0)

            context['story_platform_data'] = json.dumps(platform_data)
        except Exception as e:
            context['story_platform_data'] = json.dumps({'labels': ['Instagram', 'TikTok', 'Facebook', 'YouTube'], 'avg_engagement': [0, 0, 0, 0], 'total_views': [0, 0, 0, 0], 'count': [0, 0, 0, 0]})

        # Best Performing Stories (top 5)
        try:
            best_stories = Story.objects.filter(status='published').order_by('-performance_rating')[:5]
            context['best_stories'] = best_stories
        except Exception:
            context['best_stories'] = []

        return context


class StoryCreateView(BaseKPIView, CreateView):
    model = Story
    form_class = StoryForm
    template_name = 'kpi_management/story_form.html'
    success_url = reverse_lazy('kpi_management:story-list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        response = super().form_valid(form)
        # Auto calculate performance rating
        self.object.calculate_performance_rating()
        # Log activity
        try:
            AuditLog.objects.create(
                user=self.request.user,
                action='create',
                target_type='Story',
                target_id=self.object.id,
                target_name=self.object.title,
                ip_address=self.get_client_ip(),
                user_agent=self.request.META.get('HTTP_USER_AGENT', ''),
                description=f'Created story: {self.object.title}'
            )
        except Exception:
            pass  # Skip if AuditLog table doesn't exist
        messages.success(self.request, 'Story berhasil dibuat!')
        return response

    def get_client_ip(self):
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        return ip

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Tambah Story'
        context['is_admin'] = check_admin_permission(self.request.user)
        return context


class StoryUpdateView(BaseKPIView, UpdateView):
    model = Story
    form_class = StoryForm
    template_name = 'kpi_management/story_form.html'
    success_url = reverse_lazy('kpi_management:story-list')

    def form_valid(self, form):
        old_data = {
            'title': self.object.title,
            'views': self.object.views,
            'engagement_rate': self.object.engagement_rate,
        }
        response = super().form_valid(form)
        # Auto calculate performance rating
        self.object.calculate_performance_rating()
        # Log activity
        AuditLog.objects.create(
            user=self.request.user,
            action='update',
            target_type='Story',
            target_id=self.object.id,
            target_name=self.object.title,
            old_data=old_data,
            new_data={
                'title': self.object.title,
                'views': self.object.views,
                'engagement_rate': self.object.engagement_rate,
            },
            ip_address=self.get_client_ip(),
            user_agent=self.request.META.get('HTTP_USER_AGENT', ''),
            description=f'Updated story: {self.object.title}'
        )
        messages.success(self.request, 'Story berhasil diperbarui!')
        return response

    def get_client_ip(self):
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        return ip

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Story'
        context['is_admin'] = check_admin_permission(self.request.user)
        return context


class StoryDeleteView(BaseKPIView, DeleteView):
    model = Story
    template_name = 'kpi_management/story_confirm_delete.html'
    success_url = reverse_lazy('kpi_management:story-list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        title = self.object.title
        target_id = self.object.id
        # Log activity before deletion
        try:
            AuditLog.objects.create(
                user=request.user,
                action='delete',
                target_type='Story',
                target_id=target_id,
                target_name=title,
                ip_address=self.get_client_ip(),
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
                description=f'Deleted story: {title}'
            )
        except Exception:
            pass  # Skip if AuditLog table doesn't exist
        messages.success(self.request, 'Story berhasil dihapus!')
        return super().delete(request, *args, **kwargs)

    def get_client_ip(self):
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        return ip

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_admin'] = check_admin_permission(self.request.user)
        return context


class StoryDetailView(BaseKPIView, DetailView):
    model = Story
    template_name = 'kpi_management/story_detail.html'
    context_object_name = 'story'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_admin'] = check_admin_permission(self.request.user)
        return context


@login_required
def story_export_csv(request):
    """Export Story data to CSV"""
    try:
        stories = Story.objects.all().order_by('-story_date')

        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = 'attachment; filename="stories_export.csv"'

        writer = csv.writer(response)
        writer.writerow([
            'Title', 'Platform', 'Account Name', 'Story Date', 'Views', 'Reach',
            'Impressions', 'Engagement Rate', 'Swipe Up', 'Saves', 'Shares',
            'Status', 'Performance Rating'
        ])

        for story in stories:
            writer.writerow([
                story.title, story.get_platform_display(), story.account_name,
                story.story_date, story.views, story.reach, story.impressions,
                story.engagement_rate, story.swipe_up, story.saves, story.shares,
                story.get_status_display(), story.performance_rating
            ])

        return response
    except Exception as e:
        messages.error(request, f'Error exporting data: {str(e)}')
        return redirect('kpi_management:story-list')


@login_required
def story_bulk_action(request):
    """Handle bulk actions for Story"""
    if request.method == 'POST' and check_admin_permission(request.user):
        action = request.POST.get('action')
        story_ids = request.POST.getlist('story_ids')

        if not story_ids:
            messages.warning(request, 'Pilih minimal satu story!')
            return redirect('kpi_management:story-list')

        try:
            stories = Story.objects.filter(id__in=story_ids)

            if action == 'delete':
                count = stories.count()
                stories.delete()
                messages.success(request, f'{count} story berhasil dihapus!')
            elif action == 'update_status':
                new_status = request.POST.get('new_status')
                if new_status:
                    count = stories.update(status=new_status)
                    messages.success(request, f'{count} story berhasil diupdate status!')
            elif action == 'assign_campaign':
                campaign_id = request.POST.get('campaign_id')
                if campaign_id:
                    try:
                        campaign = Campaign.objects.get(id=campaign_id)
                        count = stories.update(campaign=campaign)
                        messages.success(request, f'{count} story berhasil diassign ke campaign!')
                    except Campaign.DoesNotExist:
                        messages.error(request, 'Campaign tidak ditemukan!')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    else:
        messages.error(request, 'Akses ditolak!')

    return redirect('kpi_management:story-list')


@login_required
def dailyfeedreels_export_csv(request):
    """Export Daily Feed/Reels data to CSV"""
    try:
        feeds = DailyFeedReels.objects.all().order_by('-publish_date')

        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = 'attachment; filename="feeds_reels_export.csv"'

        writer = csv.writer(response)
        writer.writerow([
            'Title', 'Content Type', 'Platform', 'Account Name', 'Publish Date',
            'Views', 'Likes', 'Comments', 'Shares', 'Saves', 'Engagement Rate', 'Status'
        ])

        for feed in feeds:
            writer.writerow([
                feed.title, feed.get_content_type_display(), feed.get_platform_display(),
                feed.account_name, feed.publish_date, feed.views, feed.likes,
                feed.comments, feed.shares, feed.saves, feed.engagement_rate,
                feed.get_status_display()
            ])

        return response
    except Exception as e:
        messages.error(request, f'Error exporting data: {str(e)}')
        return redirect('kpi_management:dailyfeedreels-list')


@login_required
def dailyfeedreels_bulk_action(request):
    """Handle bulk actions for Daily Feed/Reels"""
    if request.method == 'POST' and check_admin_permission(request.user):
        action = request.POST.get('action')
        feed_ids = request.POST.getlist('feed_ids')

        if not feed_ids:
            messages.warning(request, 'Pilih minimal satu feed/reel!')
            return redirect('kpi_management:dailyfeedreels-list')

        try:
            feeds = DailyFeedReels.objects.filter(id__in=feed_ids)

            if action == 'delete':
                count = feeds.count()
                feeds.delete()
                messages.success(request, f'{count} feed/reel berhasil dihapus!')
            elif action == 'update_status':
                new_status = request.POST.get('new_status')
                if new_status:
                    count = feeds.update(status=new_status)
                    messages.success(request, f'{count} feed/reel berhasil diupdate status!')
            elif action == 'assign_campaign':
                campaign_id = request.POST.get('campaign_id')
                if campaign_id:
                    try:
                        campaign = Campaign.objects.get(id=campaign_id)
                        count = feeds.update(campaign=campaign)
                        messages.success(request, f'{count} feed/reel berhasil diassign ke campaign!')
                    except Campaign.DoesNotExist:
                        messages.error(request, 'Campaign tidak ditemukan!')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    else:
        messages.error(request, 'Akses ditolak!')

    return redirect('kpi_management:dailyfeedreels-list')


@login_required
def campaign_export_csv(request):
    """Export Campaign data to CSV"""
    try:
        campaigns = get_campaigns_safe().order_by('-start_date')

        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = 'attachment; filename="campaigns_export.csv"'

        writer = csv.writer(response)
        writer.writerow([
            'Name', 'Objective', 'Start Date', 'End Date', 'Budget', 'Spent',
            'Remaining', 'Progress (%)', 'Status', 'Owner'
        ])

        for campaign in campaigns:
            writer.writerow([
                campaign.name, campaign.get_objective_display(),
                campaign.start_date, campaign.end_date,
                campaign.budget, campaign.spent, campaign.budget_remaining,
                campaign.progress_percentage, campaign.get_status_display(),
                campaign.owner.username if campaign.owner else '-'
            ])

        return response
    except Exception as e:
        messages.error(request, f'Error exporting data: {str(e)}')
        return redirect('kpi_management:campaign-list')


@login_required
def fyppostvalue_export_csv(request):
    """Export FYP Post Value data to CSV"""
    try:
        fyp_posts = FYPPostValue.objects.all().order_by('-post_date')

        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = 'attachment; filename="fyp_posts_export.csv"'

        writer = csv.writer(response)
        writer.writerow([
            'Post Title', 'Platform', 'Account Name', 'Post Date',
            'FYP Views', 'Total Views', 'FYP Percentage', 'Reach',
            'Engagement Rate', 'Viral Score'
        ])

        for post in fyp_posts:
            writer.writerow([
                post.post_title, post.get_platform_display(), post.account_name,
                post.post_date, post.fyp_views, post.total_views,
                post.fyp_percentage, post.reach, post.engagement_rate,
                post.viral_score
            ])

        return response
    except Exception as e:
        messages.error(request, f'Error exporting data: {str(e)}')
        return redirect('kpi_management:fyppostvalue-list')


@login_required
def collabbrand_export_csv(request):
    """Export Collab Brand data to CSV"""
    try:
        collabs = CollabBrand.objects.all().order_by('-start_date')

        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = 'attachment; filename="collab_brands_export.csv"'

        writer = csv.writer(response)
        writer.writerow([
            'Brand Name', 'Contact Person', 'Email', 'Collaboration Type',
            'Start Date', 'End Date', 'Contract Value', 'Payment Status', 'Status'
        ])

        for collab in collabs:
            writer.writerow([
                collab.brand_name, collab.contact_person, collab.email,
                collab.collaboration_type, collab.start_date, collab.end_date,
                collab.contract_value, collab.get_payment_status_display(),
                collab.get_status_display()
            ])

        return response
    except Exception as e:
        messages.error(request, f'Error exporting data: {str(e)}')
        return redirect('kpi_management:collabbrand-list')


# ==================== DAILY FEED/REELS CRUD ====================

class DailyFeedReelsListView(BaseKPIView, ListView):
    model = DailyFeedReels
    template_name = 'kpi_management/dailyfeedreels_list.html'
    context_object_name = 'feeds'
    paginate_by = 20

    def get_queryset(self):
        # Hanya gunakan select_related untuk field yang pasti ada
        queryset = DailyFeedReels.objects.select_related('campaign', 'collab_brand', 'created_by').all()
        search = self.request.GET.get('search', '')
        content_type = self.request.GET.get('content_type', '')
        platform = self.request.GET.get('platform', '')
        company = self.request.GET.get('company', '')
        account_name = self.request.GET.get('account_name', '')

        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(account_name__icontains=search)
            )
        if content_type:
            queryset = queryset.filter(content_type=content_type)
        if platform:
            queryset = queryset.filter(platform=platform)
        if company:
            try:
                queryset = queryset.filter(company_id=company)
            except Exception:
                # Jika field company belum ada, skip filter ini
                pass
        if account_name:
            queryset = queryset.filter(account_name=account_name)

        return queryset.order_by('-publish_date', '-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_admin'] = check_admin_permission(self.request.user)
        
        # Get social media accounts for filter
        try:
            context['social_media_accounts'] = SocialMediaAccount.objects.filter(status='active').order_by('platform', 'account_name')
        except Exception:
            context['social_media_accounts'] = []

        # Data untuk grafik Daily Feed/Reels
        try:
            from django.db.models import Avg, Sum, Count
            from datetime import datetime, timedelta
            import json

            # Daily Performance Graph (30 hari terakhir)
            date_range = [timezone.now().date() - timedelta(days=x) for x in range(29, -1, -1)]
            feed_daily_perf = {
                'dates': [d.strftime('%d %b') for d in date_range],
                'views': [],
                'likes': [],
                'engagement': []
            }

            for date in date_range:
                try:
                    feeds = DailyFeedReels.objects.filter(publish_date__date=date)
                    feed_daily_perf['views'].append(int(feeds.aggregate(Sum('views'))['views__sum'] or 0))
                    feed_daily_perf['likes'].append(int(feeds.aggregate(Sum('likes'))['likes__sum'] or 0))
                    avg_eng = feeds.aggregate(Avg('engagement_rate'))['engagement_rate__avg'] or 0
                    feed_daily_perf['engagement'].append(round(float(avg_eng), 2))
                except Exception as e:
                    feed_daily_perf['views'].append(0)
                    feed_daily_perf['likes'].append(0)
                    feed_daily_perf['engagement'].append(0.0)

            context['feed_daily_perf_data'] = json.dumps(feed_daily_perf)

            # Content Performance Comparison (Feed vs Reels)
            feed_comparison = {
                'labels': ['Feed', 'Reels'],
                'avg_views': [],
                'avg_engagement': []
            }

            try:
                feeds = DailyFeedReels.objects.filter(content_type='feed')
                reels = DailyFeedReels.objects.filter(content_type='reels')

                feed_comparison['avg_views'].append(float(feeds.aggregate(Avg('views'))['views__avg'] or 0))
                feed_comparison['avg_views'].append(float(reels.aggregate(Avg('views'))['views__avg'] or 0))
                feed_comparison['avg_engagement'].append(float(feeds.aggregate(Avg('engagement_rate'))['engagement_rate__avg'] or 0))
                feed_comparison['avg_engagement'].append(float(reels.aggregate(Avg('engagement_rate'))['engagement_rate__avg'] or 0))
            except Exception as e:
                feed_comparison['avg_views'] = [0.0, 0.0]
                feed_comparison['avg_engagement'] = [0.0, 0.0]

            context['feed_content_comparison'] = json.dumps(feed_comparison)
            context['companies'] = get_companies_safe()
            # Add campaigns for bulk action
            try:
                context['campaigns'] = get_campaigns_safe().order_by('-start_date')[:50]
            except Exception:
                context['campaigns'] = []
        except Exception as e:
            import json
            context['feed_daily_perf_data'] = json.dumps({'dates': [], 'views': [], 'likes': [], 'engagement': []})
            context['feed_content_comparison'] = json.dumps({'labels': [], 'avg_views': [], 'avg_engagement': []})
            try:
                context['companies'] = get_companies_safe()
            except Exception:
                context['companies'] = []
            try:
                context['campaigns'] = get_campaigns_safe().order_by('-start_date')[:50]
            except Exception:
                context['campaigns'] = []

        return context


class DailyFeedReelsCreateView(BaseKPIView, CreateView):
    model = DailyFeedReels
    form_class = DailyFeedReelsForm
    template_name = 'kpi_management/dailyfeedreels_form.html'
    success_url = reverse_lazy('kpi_management:dailyfeedreels-list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        response = super().form_valid(form)
        # Log activity
        try:
            AuditLog.objects.create(
                user=self.request.user,
                action='create',
                target_type='DailyFeedReels',
                target_id=self.object.id,
                target_name=self.object.title,
                ip_address=self.get_client_ip(),
                user_agent=self.request.META.get('HTTP_USER_AGENT', ''),
                description=f'Created Daily Feed/Reels: {self.object.title}'
            )
        except Exception:
            pass  # Skip if AuditLog table doesn't exist
        messages.success(self.request, 'Daily Feed/Reels berhasil dibuat!')
        return response

    def get_client_ip(self):
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        return ip

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Tambah Daily Feed/Reels'
        context['is_admin'] = check_admin_permission(self.request.user)
        return context


class DailyFeedReelsUpdateView(BaseKPIView, UpdateView):
    model = DailyFeedReels
    form_class = DailyFeedReelsForm
    template_name = 'kpi_management/dailyfeedreels_form.html'
    success_url = reverse_lazy('kpi_management:dailyfeedreels-list')

    def form_valid(self, form):
        old_data = {
            'title': self.object.title,
            'views': self.object.views,
            'engagement_rate': self.object.engagement_rate,
        }
        response = super().form_valid(form)
        # Log activity
        try:
            AuditLog.objects.create(
                user=self.request.user,
                action='update',
                target_type='DailyFeedReels',
                target_id=self.object.id,
                target_name=self.object.title,
                old_data=old_data,
                new_data={
                    'title': self.object.title,
                    'views': self.object.views,
                    'engagement_rate': self.object.engagement_rate,
                },
                ip_address=self.get_client_ip(),
                user_agent=self.request.META.get('HTTP_USER_AGENT', ''),
                description=f'Updated Daily Feed/Reels: {self.object.title}'
            )
        except Exception:
            pass  # Skip if AuditLog table doesn't exist
        messages.success(self.request, 'Daily Feed/Reels berhasil diperbarui!')
        return response

    def get_client_ip(self):
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        return ip

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Daily Feed/Reels'
        context['is_admin'] = check_admin_permission(self.request.user)
        return context


class DailyFeedReelsDeleteView(BaseKPIView, DeleteView):
    model = DailyFeedReels
    template_name = 'kpi_management/dailyfeedreels_confirm_delete.html'
    success_url = reverse_lazy('kpi_management:dailyfeedreels-list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        title = self.object.title
        target_id = self.object.id
        # Log activity before deletion
        try:
            AuditLog.objects.create(
                user=request.user,
                action='delete',
                target_type='DailyFeedReels',
                target_id=target_id,
                target_name=title,
                ip_address=self.get_client_ip(),
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
                description=f'Deleted Daily Feed/Reels: {title}'
            )
        except Exception:
            pass  # Skip if AuditLog table doesn't exist
        messages.success(self.request, 'Daily Feed/Reels berhasil dihapus!')
        return super().delete(request, *args, **kwargs)

    def get_client_ip(self):
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        return ip

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_admin'] = check_admin_permission(self.request.user)
        return context


class DailyFeedReelsDetailView(BaseKPIView, DetailView):
    model = DailyFeedReels
    template_name = 'kpi_management/dailyfeedreels_detail.html'
    context_object_name = 'feed'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_admin'] = check_admin_permission(self.request.user)
        return context


# ==================== FYP POST VALUE CRUD ====================

class FYPPostValueListView(BaseKPIView, ListView):
    model = FYPPostValue
    template_name = 'kpi_management/fyppostvalue_list.html'
    context_object_name = 'fyp_posts'
    paginate_by = 20

    def get_queryset(self):
        queryset = FYPPostValue.objects.all()
        search = self.request.GET.get('search', '')
        platform = self.request.GET.get('platform', '')
        account_name = self.request.GET.get('account_name', '')

        if search:
            queryset = queryset.filter(
                Q(post_title__icontains=search) |
                Q(account_name__icontains=search)
            )
        if platform:
            queryset = queryset.filter(platform=platform)
        if account_name:
            queryset = queryset.filter(account_name=account_name)

        return queryset.order_by('-viral_score', '-post_date', '-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_admin'] = check_admin_permission(self.request.user)
        
        # Get social media accounts for filter
        try:
            context['social_media_accounts'] = SocialMediaAccount.objects.filter(status='active').order_by('platform', 'account_name')
        except Exception:
            context['social_media_accounts'] = []

        # Analytics data untuk FYP Post Value Management
        try:
            from django.db.models import Avg, Count, Sum, Max
            from django.utils import timezone
            from datetime import timedelta
            import json

            # Viral Score Trend - 30 hari terakhir
            date_range = [timezone.now().date() - timedelta(days=x) for x in range(29, -1, -1)]
            viral_trend_data = {
                'dates': [d.strftime('%d %b') for d in date_range],
                'viral_scores': [],
                'fyp_views': [],
                'total_views': []
            }
            for date in date_range:
                try:
                    posts = FYPPostValue.objects.filter(post_date=date)
                    viral_trend_data['viral_scores'].append(
                        round(posts.aggregate(Avg('viral_score'))['viral_score__avg'] or 0, 2)
                    )
                    viral_trend_data['fyp_views'].append(
                        int(posts.aggregate(Sum('fyp_views'))['fyp_views__sum'] or 0)
                    )
                    viral_trend_data['total_views'].append(
                        int(posts.aggregate(Sum('total_views'))['total_views__sum'] or 0)
                    )
                except Exception:
                    viral_trend_data['viral_scores'].append(0)
                    viral_trend_data['fyp_views'].append(0)
                    viral_trend_data['total_views'].append(0)

            context['fyp_trend_data'] = json.dumps(viral_trend_data)

            # Platform Distribution
            platform_data = {
                'labels': ['TikTok', 'Instagram'],
                'viral_scores': [],
                'fyp_percentages': [],
                'count': []
            }
            for platform in ['tiktok', 'instagram']:
                try:
                    posts = FYPPostValue.objects.filter(platform=platform)
                    platform_data['viral_scores'].append(
                        round(posts.aggregate(Avg('viral_score'))['viral_score__avg'] or 0, 2)
                    )
                    platform_data['fyp_percentages'].append(
                        round(posts.aggregate(Avg('fyp_percentage'))['fyp_percentage__avg'] or 0, 2)
                    )
                    platform_data['count'].append(posts.count())
                except Exception:
                    platform_data['viral_scores'].append(0)
                    platform_data['fyp_percentages'].append(0)
                    platform_data['count'].append(0)

            context['fyp_platform_data'] = json.dumps(platform_data)

            # Top Viral Posts
            try:
                top_viral = FYPPostValue.objects.all().order_by('-viral_score')[:5]
                context['top_viral_posts'] = top_viral
            except Exception:
                context['top_viral_posts'] = []

        except Exception as e:
            context['fyp_trend_data'] = json.dumps({'dates': [], 'viral_scores': [], 'fyp_views': [], 'total_views': []})
            context['fyp_platform_data'] = json.dumps({'labels': [], 'viral_scores': [], 'fyp_percentages': [], 'count': []})
            context['top_viral_posts'] = []

        return context


class FYPPostValueCreateView(BaseKPIView, CreateView):
    model = FYPPostValue
    form_class = FYPPostValueForm
    template_name = 'kpi_management/fyppostvalue_form.html'
    success_url = reverse_lazy('fyppostvalue-list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        response = super().form_valid(form)
        # Auto calculate viral score
        self.object.calculate_viral_score()
        # Log activity
        AuditLog.objects.create(
            user=self.request.user,
            action='create',
            target_type='FYPPostValue',
            target_id=self.object.id,
            target_name=self.object.post_title,
            ip_address=self.get_client_ip(),
            user_agent=self.request.META.get('HTTP_USER_AGENT', ''),
            description=f'Created FYP Post: {self.object.post_title}'
        )
        messages.success(self.request, 'FYP Post Value berhasil dibuat!')
        return response

    def get_client_ip(self):
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        return ip

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Tambah FYP Post Value'
        context['is_admin'] = check_admin_permission(self.request.user)
        return context


class FYPPostValueUpdateView(BaseKPIView, UpdateView):
    model = FYPPostValue
    form_class = FYPPostValueForm
    template_name = 'kpi_management/fyppostvalue_form.html'
    success_url = reverse_lazy('fyppostvalue-list')

    def form_valid(self, form):
        old_data = {
            'post_title': self.object.post_title,
            'viral_score': self.object.viral_score,
        }
        response = super().form_valid(form)
        # Auto calculate viral score
        self.object.calculate_viral_score()
        # Log activity
        AuditLog.objects.create(
            user=self.request.user,
            action='update',
            target_type='FYPPostValue',
            target_id=self.object.id,
            target_name=self.object.post_title,
            old_data=old_data,
            new_data={
                'post_title': self.object.post_title,
                'viral_score': self.object.viral_score,
            },
            ip_address=self.get_client_ip(),
            user_agent=self.request.META.get('HTTP_USER_AGENT', ''),
            description=f'Updated FYP Post: {self.object.post_title}'
        )
        messages.success(self.request, 'FYP Post Value berhasil diperbarui!')
        return response

    def get_client_ip(self):
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        return ip

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit FYP Post Value'
        context['is_admin'] = check_admin_permission(self.request.user)
        return context


class FYPPostValueDeleteView(BaseKPIView, DeleteView):
    model = FYPPostValue
    template_name = 'kpi_management/fyppostvalue_confirm_delete.html'
    success_url = reverse_lazy('fyppostvalue-list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        title = self.object.post_title
        target_id = self.object.id
        # Log activity before deletion
        try:
            AuditLog.objects.create(
                user=request.user,
                action='delete',
                target_type='FYPPostValue',
                target_id=target_id,
                target_name=title,
                ip_address=self.get_client_ip(),
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
                description=f'Deleted FYP Post: {title}'
            )
        except Exception:
            pass  # Skip if AuditLog table doesn't exist
        messages.success(self.request, 'FYP Post Value berhasil dihapus!')
        return super().delete(request, *args, **kwargs)

    def get_client_ip(self):
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        return ip

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_admin'] = check_admin_permission(self.request.user)
        return context


class FYPPostValueDetailView(BaseKPIView, DetailView):
    model = FYPPostValue
    template_name = 'kpi_management/fyppostvalue_detail.html'
    context_object_name = 'fyp_post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_admin'] = check_admin_permission(self.request.user)
        return context


# ==================== CAMPAIGN CRUD ====================

class CampaignListView(BaseKPIView, ListView):
    model = Campaign
    template_name = 'kpi_management/campaign_list.html'
    context_object_name = 'campaigns'
    paginate_by = 20

    def get_queryset(self):
        # Hanya gunakan select_related untuk field yang pasti ada
        try:
            queryset = get_campaigns_safe()
            # Coba select_related untuk field yang mungkin ada
            try:
                queryset = queryset.select_related('owner', 'created_by')
            except Exception:
                # Jika select_related gagal, gunakan tanpa select_related
                pass
            queryset = queryset.all()
        except Exception:
            queryset = Campaign.objects.none()

        search = self.request.GET.get('search', '')
        status = self.request.GET.get('status', '')
        company = self.request.GET.get('company', '')

        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(description__icontains=search)
            )
        if status:
            queryset = queryset.filter(status=status)
        if company:
            try:
                queryset = queryset.filter(company_id=company)
            except Exception:
                # Jika field company belum ada, skip filter ini
                pass

        return queryset.order_by('-start_date', '-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_admin'] = check_admin_permission(self.request.user)

        # Analytics data untuk Campaign Management
        try:
            from django.db.models import Avg, Count, Sum
            from decimal import Decimal
            import json

            # Budget vs Spent Chart
            campaigns_queryset = get_campaigns_safe()
            budget_vs_spent = {
                'labels': [],
                'budget': [],
                'spent': [],
                'remaining': []
            }
            # Ambil top 10 campaigns sebagai list untuk iterasi
            top_campaigns = list(campaigns_queryset[:10])
            for campaign in top_campaigns:
                try:
                    budget_vs_spent['labels'].append(campaign.name[:20] + '...' if len(campaign.name) > 20 else campaign.name)
                    budget_vs_spent['budget'].append(float(campaign.budget or 0))
                    budget_vs_spent['spent'].append(float(campaign.spent or 0))
                    budget_vs_spent['remaining'].append(float(campaign.budget_remaining or 0))
                except Exception:
                    # Skip campaign jika ada error
                    continue

            context['campaign_budget_data'] = json.dumps(budget_vs_spent)

            # ROI Analysis
            roi_data = {
                'labels': [],
                'roi': []
            }
            for campaign in top_campaigns:
                try:
                    # Simple ROI calculation: (achieved KPI / target KPI) * 100
                    if campaign.kpi_target and campaign.kpi_achieved:
                        total_target = sum(campaign.kpi_target.values()) if isinstance(campaign.kpi_target, dict) else 0
                        total_achieved = sum(campaign.kpi_achieved.values()) if isinstance(campaign.kpi_achieved, dict) else 0
                        roi = (total_achieved / total_target * 100) if total_target > 0 else 0
                    else:
                        roi = getattr(campaign, 'progress_percentage', 0) or 0
                    roi_data['labels'].append(campaign.name[:20] + '...' if len(campaign.name) > 20 else campaign.name)
                    roi_data['roi'].append(round(float(roi), 2))
                except Exception:
                    try:
                        roi_data['labels'].append(campaign.name[:20] + '...' if len(campaign.name) > 20 else campaign.name)
                        roi_data['roi'].append(0)
                    except Exception:
                        # Skip campaign jika ada error
                        continue

            context['campaign_roi_data'] = json.dumps(roi_data)

            # Campaign Performance Summary
            # Gunakan queryset asli untuk filter, bukan list yang sudah di-slice
            try:
                active_campaigns = campaigns_queryset.filter(status='active')
                completed_campaigns = campaigns_queryset.filter(status='completed')
                context['active_campaigns_count'] = active_campaigns.count()
                context['completed_campaigns_count'] = completed_campaigns.count()
                # Untuk sum, gunakan list dari queryset
                all_campaigns_list = list(campaigns_queryset)
                context['total_budget'] = sum([float(c.budget or 0) for c in all_campaigns_list])
                context['total_spent'] = sum([float(c.spent or 0) for c in all_campaigns_list])
            except Exception:
                context['active_campaigns_count'] = 0
                context['completed_campaigns_count'] = 0
                context['total_budget'] = 0
                context['total_spent'] = 0

        except Exception as e:
            context['campaign_budget_data'] = json.dumps({'labels': [], 'budget': [], 'spent': [], 'remaining': []})
            context['campaign_roi_data'] = json.dumps({'labels': [], 'roi': []})
            context['active_campaigns_count'] = 0
            context['completed_campaigns_count'] = 0
            context['total_budget'] = 0
            context['total_spent'] = 0

        # Add companies untuk filter
        try:
            context['companies'] = get_companies_safe()
        except Exception:
            context['companies'] = []

        return context


class CampaignCreateView(BaseKPIView, CreateView):
    model = Campaign
    form_class = CampaignForm
    template_name = 'kpi_management/campaign_form.html'
    success_url = reverse_lazy('kpi_management:campaign-list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        response = super().form_valid(form)
        # Log activity
        try:
            AuditLog.objects.create(
                user=self.request.user,
                action='create',
                target_type='Campaign',
                target_id=self.object.id,
                target_name=self.object.name,
                ip_address=self.get_client_ip(),
                user_agent=self.request.META.get('HTTP_USER_AGENT', ''),
                description=f'Created campaign: {self.object.name}'
            )
        except Exception:
            pass  # Skip if AuditLog table doesn't exist
        messages.success(self.request, 'Campaign berhasil dibuat!')
        return response

    def get_client_ip(self):
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        return ip

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Tambah Campaign'
        context['is_admin'] = check_admin_permission(self.request.user)
        return context


class CampaignUpdateView(BaseKPIView, UpdateView):
    model = Campaign
    form_class = CampaignForm
    template_name = 'kpi_management/campaign_form.html'
    success_url = reverse_lazy('kpi_management:campaign-list')

    def get_queryset(self):
        """Get queryset safely"""
        return get_campaigns_safe()

    def form_valid(self, form):
        old_data = {
            'name': self.object.name,
            'status': self.object.status,
        }
        response = super().form_valid(form)
        # Log activity
        try:
            AuditLog.objects.create(
                user=self.request.user,
                action='update',
                target_type='Campaign',
                target_id=self.object.id,
                target_name=self.object.name,
                old_data=old_data,
                new_data={
                    'name': self.object.name,
                    'status': self.object.status,
                },
                ip_address=self.get_client_ip(),
                user_agent=self.request.META.get('HTTP_USER_AGENT', ''),
                description=f'Updated campaign: {self.object.name}'
            )
        except Exception:
            pass  # Skip if AuditLog table doesn't exist
        messages.success(self.request, 'Campaign berhasil diperbarui!')
        return response

    def get_client_ip(self):
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        return ip

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Campaign'
        context['is_admin'] = check_admin_permission(self.request.user)
        return context


class CampaignDeleteView(BaseKPIView, DeleteView):
    model = Campaign
    template_name = 'kpi_management/campaign_confirm_delete.html'
    success_url = reverse_lazy('kpi_management:campaign-list')

    def get_queryset(self):
        """Get queryset safely"""
        return get_campaigns_safe()

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        title = self.object.name
        target_id = self.object.id
        # Log activity before deletion
        try:
            AuditLog.objects.create(
                user=request.user,
                action='delete',
                target_type='Campaign',
                target_id=target_id,
                target_name=title,
                ip_address=self.get_client_ip(),
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
                description=f'Deleted campaign: {title}'
            )
        except Exception:
            pass  # Skip if AuditLog table doesn't exist
        messages.success(self.request, 'Campaign berhasil dihapus!')
        return super().delete(request, *args, **kwargs)

    def get_client_ip(self):
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        return ip

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_admin'] = check_admin_permission(self.request.user)
        return context


class CampaignDetailView(BaseKPIView, DetailView):
    model = Campaign
    template_name = 'kpi_management/campaign_detail.html'
    context_object_name = 'campaign'

    def get_queryset(self):
        """Get queryset safely"""
        return get_campaigns_safe()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_admin'] = check_admin_permission(self.request.user)
        return context


# ==================== COLLAB BRAND CRUD ====================

class CollabBrandListView(BaseKPIView, ListView):
    model = CollabBrand
    template_name = 'kpi_management/collabbrand_list.html'
    context_object_name = 'collabs'
    paginate_by = 20

    def get_queryset(self):
        queryset = CollabBrand.objects.all()
        search = self.request.GET.get('search', '')
        status = self.request.GET.get('status', '')

        if search:
            queryset = queryset.filter(
                Q(brand_name__icontains=search) |
                Q(contact_person__icontains=search) |
                Q(company__icontains=search)
            )
        if status:
            queryset = queryset.filter(status=status)

        return queryset.order_by('-start_date', '-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_admin'] = check_admin_permission(self.request.user)
        return context


class CollabBrandCreateView(BaseKPIView, CreateView):
    model = CollabBrand
    form_class = CollabBrandForm
    template_name = 'kpi_management/collabbrand_form.html'
    success_url = reverse_lazy('collabbrand-list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        response = super().form_valid(form)
        # Log activity
        try:
            AuditLog.objects.create(
                user=self.request.user,
                action='create',
                target_type='CollabBrand',
                target_id=self.object.id,
                target_name=self.object.brand_name,
                ip_address=self.get_client_ip(),
                user_agent=self.request.META.get('HTTP_USER_AGENT', ''),
                description=f'Created collab brand: {self.object.brand_name}'
            )
        except Exception:
            pass  # Skip if AuditLog table doesn't exist
        messages.success(self.request, 'Collab Brand berhasil dibuat!')
        return response

    def get_client_ip(self):
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        return ip

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Tambah Collab Brand'
        context['is_admin'] = check_admin_permission(self.request.user)
        return context


class CollabBrandUpdateView(BaseKPIView, UpdateView):
    model = CollabBrand
    form_class = CollabBrandForm
    template_name = 'kpi_management/collabbrand_form.html'
    success_url = reverse_lazy('collabbrand-list')

    def form_valid(self, form):
        old_data = {
            'brand_name': self.object.brand_name,
            'status': self.object.status,
        }
        response = super().form_valid(form)
        # Log activity
        try:
            AuditLog.objects.create(
                user=self.request.user,
                action='update',
                target_type='CollabBrand',
                target_id=self.object.id,
                target_name=self.object.brand_name,
                old_data=old_data,
                new_data={
                    'brand_name': self.object.brand_name,
                    'status': self.object.status,
                },
                ip_address=self.get_client_ip(),
                user_agent=self.request.META.get('HTTP_USER_AGENT', ''),
                description=f'Updated collab brand: {self.object.brand_name}'
            )
        except Exception:
            pass  # Skip if AuditLog table doesn't exist
        messages.success(self.request, 'Collab Brand berhasil diperbarui!')
        return response

    def get_client_ip(self):
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        return ip

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Collab Brand'
        context['is_admin'] = check_admin_permission(self.request.user)
        return context


class CollabBrandDeleteView(BaseKPIView, DeleteView):
    model = CollabBrand
    template_name = 'kpi_management/collabbrand_confirm_delete.html'
    success_url = reverse_lazy('collabbrand-list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        title = self.object.brand_name
        target_id = self.object.id
        # Log activity before deletion
        try:
            AuditLog.objects.create(
                user=request.user,
                action='delete',
                target_type='CollabBrand',
                target_id=target_id,
                target_name=title,
                ip_address=self.get_client_ip(),
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
                description=f'Deleted collab brand: {title}'
            )
        except Exception:
            pass  # Skip if AuditLog table doesn't exist
        messages.success(self.request, 'Collab Brand berhasil dihapus!')
        return super().delete(request, *args, **kwargs)

    def get_client_ip(self):
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        return ip

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_admin'] = check_admin_permission(self.request.user)
        return context


class CollabBrandDetailView(BaseKPIView, DetailView):
    model = CollabBrand
    template_name = 'kpi_management/collabbrand_detail.html'
    context_object_name = 'collab'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_admin'] = check_admin_permission(self.request.user)
        return context


# ==================== USER MANAGEMENT CRUD ====================

class UserListView(BaseKPIView, ListView):
    model = User
    template_name = 'kpi_management/user_list.html'
    context_object_name = 'users'
    paginate_by = 20

    def get_queryset(self):
        queryset = User.objects.all()
        search = self.request.GET.get('search', '')

        if search:
            queryset = queryset.filter(
                Q(username__icontains=search) |
                Q(email__icontains=search) |
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search)
            )

        return queryset.order_by('-date_joined')

    def dispatch(self, request, *args, **kwargs):
        if not check_admin_permission(request.user):
            messages.error(request, 'Anda tidak memiliki akses untuk melihat daftar user!')
            return redirect('index')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_admin'] = True
        return context


class UserCreateView(BaseKPIView, CreateView):
    model = User
    form_class = UserForm
    template_name = 'kpi_management/user_form.html'
    success_url = reverse_lazy('kpi_management:user-list')

    def dispatch(self, request, *args, **kwargs):
        if not check_admin_permission(request.user):
            messages.error(request, 'Anda tidak memiliki akses untuk membuat user!')
            return redirect('index')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save(commit=False)
        password = self.request.POST.get('password', '')
        if password:
            user.set_password(password)
        user.save()

        # Create profile
        Profile.objects.get_or_create(
            user=user,
            defaults={'role': 'user'}
        )

        messages.success(self.request, 'User berhasil dibuat!')
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Tambah User'
        context['is_admin'] = True
        return context


class UserUpdateView(BaseKPIView, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'kpi_management/user_form.html'
    success_url = reverse_lazy('kpi_management:user-list')

    def dispatch(self, request, *args, **kwargs):
        if not check_admin_permission(request.user):
            messages.error(request, 'Anda tidak memiliki akses untuk mengedit user!')
            return redirect('index')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save(commit=False)
        password = self.request.POST.get('password', '')
        if password:
            user.set_password(password)
        user.save()
        messages.success(self.request, 'User berhasil diperbarui!')
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit User'
        context['is_admin'] = True
        return context


class UserDeleteView(BaseKPIView, DeleteView):
    model = User
    template_name = 'kpi_management/user_confirm_delete.html'
    success_url = reverse_lazy('kpi_management:user-list')

    def dispatch(self, request, *args, **kwargs):
        if not check_admin_permission(request.user):
            messages.error(request, 'Anda tidak memiliki akses untuk menghapus user!')
            return redirect('index')
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'User berhasil dihapus!')
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_admin'] = True
        return context


# ==================== PROFILE MANAGEMENT ====================

@login_required
def profile_view(request):
    """View untuk melihat dan mengedit profile sendiri"""
    profile = None
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        # Create profile dengan field minimal
        try:
            profile = Profile.objects.create(user=request.user, role='user')
        except Exception as e:
            # Jika masih error, tampilkan form kosong dengan pesan warning
            messages.warning(request, 'Profile belum tersedia. Silakan isi form di bawah untuk membuat profile.')
            profile = None
    except Exception as e:
        # Jika ada error lain (misalnya kolom belum ada), handle gracefully
        try:
            # Coba buat profile baru
            profile = Profile.objects.create(user=request.user, role='user')
        except Exception:
            # Jika masih error, tampilkan form kosong
            messages.warning(request, 'Beberapa field profile belum tersedia. Silakan hubungi administrator.')
            profile = None

    if request.method == 'POST':
        try:
            if profile:
                form = ProfileForm(request.POST, request.FILES, instance=profile)
            else:
                form = ProfileForm(request.POST, request.FILES)
                form.instance.user = request.user
            if form.is_valid():
                if not profile:
                    form.instance.user = request.user
                profile = form.save()
                messages.success(request, 'Profile berhasil diperbarui!')
                return redirect('kpi_management:profile-view')
            else:
                messages.error(request, 'Terdapat error pada form. Silakan periksa kembali.')
        except Exception as e:
            messages.error(request, f'Terjadi error saat menyimpan profile: {str(e)}')
            if profile:
                form = ProfileForm(instance=profile)
            else:
                form = ProfileForm()
    else:
        try:
            if profile:
                form = ProfileForm(instance=profile)
            else:
                form = ProfileForm(initial={'user': request.user})
        except Exception as e:
            # If form initialization fails, create empty form
            messages.warning(request, 'Beberapa field profile belum tersedia.')
            form = ProfileForm()

    context = TemplateLayout.init(request, {})
    context.update({
        "layout_path": TemplateHelper.set_layout("layout_vertical.html", context),
        "form": form,
        "profile": profile,
        "is_admin": check_admin_permission(request.user),
    })

    try:
        return render(request, 'kpi_management/profile_form.html', context)
    except Exception as e:
        # If template rendering fails, return simple response
        messages.error(request, f'Error rendering template: {str(e)}')
        return redirect('index')


@login_required
def profile_edit(request, user_id):
    """View untuk admin mengedit profile user lain"""
    if not check_admin_permission(request.user):
        messages.error(request, 'Anda tidak memiliki akses!')
        return redirect('dashboard-analytics')

    user = get_object_or_404(User, id=user_id)
    try:
        profile = user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=user, role='user')

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile berhasil diperbarui!')
            return redirect('user-list')
    else:
        form = ProfileForm(instance=profile)

    context = TemplateLayout.init(request, {})
    context.update({
        "layout_path": TemplateHelper.set_layout("layout_vertical.html", context),
        "form": form,
        "profile": profile,
        "user_obj": user,
        "is_admin": True,
    })

    return render(request, 'kpi_management/profile_edit.html', context)


# ==================== DASHBOARD MANAGEMENT ====================

@login_required
def dashboard_management(request):
    """Dashboard Management - Overview kinerja platform & operasional"""
    from django.db.models import Avg, Sum, Count
    from django.utils import timezone
    from datetime import timedelta
    import json

    # Check permission - skip if DashboardSettings table doesn't exist
    try:
        if hasattr(request.user, 'profile') and request.user.profile:
            try:
                dashboard_settings = DashboardSettings.objects.filter(
                    Q(user=request.user) | Q(role=request.user.profile.role) | Q(allowed_users=request.user)
                ).first()
                if dashboard_settings and not dashboard_settings.can_view_dashboard:
                    messages.error(request, 'Anda tidak memiliki akses untuk melihat dashboard!')
                    return redirect('index')
            except Exception:
                # If DashboardSettings table doesn't exist, skip permission check
                pass
    except Exception:
        pass

    # Define querysets
    try:
        campaign_queryset = get_campaigns_safe()
    except Exception:
        campaign_queryset = Campaign.objects.none()

    try:
        story_queryset = Story.objects.all()
    except Exception:
        story_queryset = Story.objects.none()

    try:
        fyp_queryset = FYPPostValue.objects.all()
    except Exception:
        fyp_queryset = FYPPostValue.objects.none()

    try:
        feed_queryset = DailyFeedReels.objects.all()
    except Exception:
        feed_queryset = DailyFeedReels.objects.none()

    # Filter by company jika ada
    company_filter = request.GET.get('company', '')
    if company_filter:
        try:
            campaign_queryset = campaign_queryset.filter(company_id=company_filter)
        except Exception:
            pass
        try:
            story_queryset = story_queryset.filter(company_id=company_filter)
        except Exception:
            pass
        try:
            feed_queryset = feed_queryset.filter(company_id=company_filter)
        except Exception:
            pass
    
    # Filter by social media account jika ada
    account_name_filter = request.GET.get('account_name', '')
    if account_name_filter:
        try:
            story_queryset = story_queryset.filter(account_name=account_name_filter)
        except Exception:
            pass
        try:
            feed_queryset = feed_queryset.filter(account_name=account_name_filter)
        except Exception:
            pass

    # Get statistics
    try:
        total_campaigns = campaign_queryset.count()
    except Exception:
        total_campaigns = 0

    try:
        total_stories = story_queryset.count()
    except Exception:
        total_stories = 0

    try:
        total_fyp_posts = fyp_queryset.count()
    except Exception:
        total_fyp_posts = 0

    try:
        total_feeds = feed_queryset.count()
    except Exception:
        total_feeds = 0

    # Engagement rata-rata
    try:
        avg_engagement_story = story_queryset.aggregate(Avg('engagement_rate'))['engagement_rate__avg'] or 0
    except Exception:
        avg_engagement_story = 0

    try:
        avg_engagement_feed = feed_queryset.aggregate(Avg('engagement_rate'))['engagement_rate__avg'] or 0
    except Exception:
        avg_engagement_feed = 0

    engagement_avg = (avg_engagement_story + avg_engagement_feed) / 2 if (avg_engagement_story or avg_engagement_feed) else 0

    # Revenue / KPI collab brand
    try:
        total_revenue = CollabBrand.objects.filter(payment_status='paid').aggregate(Sum('contract_value'))['contract_value__sum'] or 0
        if total_revenue is None:
            total_revenue = 0
    except Exception:
        total_revenue = 0

    try:
        pending_revenue = CollabBrand.objects.filter(payment_status__in=['pending', 'partial']).aggregate(Sum('contract_value'))['contract_value__sum'] or 0
        if pending_revenue is None:
            pending_revenue = 0
    except Exception:
        pending_revenue = 0

    # Aktivitas user terbaru
    try:
        recent_activities = list(AuditLog.objects.all()[:10])
    except Exception:
        recent_activities = []

    # Notification status approval
    try:
        pending_campaigns = get_campaigns_safe().filter(status='planning').count()
    except Exception:
        pending_campaigns = 0

    try:
        pending_collabs = CollabBrand.objects.filter(status='negotiating').count()
    except Exception:
        pending_collabs = 0

    try:
        under_review_feeds = DailyFeedReels.objects.filter(status='under_review').count()
    except Exception:
        under_review_feeds = 0

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
                story_views = story_queryset.filter(story_date=date).aggregate(Sum('views'))['views__sum'] or 0
                feed_views = feed_queryset.filter(publish_date__date=date).aggregate(Sum('views'))['views__sum'] or 0
                trend_data['views'].append(int(story_views + feed_views))
            except Exception as e:
                trend_data['views'].append(0)

            try:
                story_eng = story_queryset.filter(story_date=date).aggregate(Avg('engagement_rate'))['engagement_rate__avg'] or 0
                feed_eng = feed_queryset.filter(publish_date__date=date).aggregate(Avg('engagement_rate'))['engagement_rate__avg'] or 0
                avg_eng = (story_eng + feed_eng) / 2 if (story_eng or feed_eng) else 0
                trend_data['engagement'].append(round(avg_eng, 2))
            except Exception as e:
                trend_data['engagement'].append(0)

            try:
                story_reach = story_queryset.filter(story_date=date).aggregate(Sum('reach'))['reach__sum'] or 0
                trend_data['reach'].append(int(story_reach))
            except Exception as e:
                trend_data['reach'].append(0)
    except Exception:
        trend_data = {
            'dates': [],
            'views': [],
            'engagement': [],
            'reach': []
        }

    # Data untuk Bar Chart - Perbandingan platform
    try:
        platform_data = {
            'labels': ['Instagram', 'TikTok', 'Facebook', 'YouTube'],
            'story_count': [],
            'feed_count': []
        }
        for platform in ['instagram', 'tiktok', 'facebook', 'youtube']:
            try:
                story_count = story_queryset.filter(platform=platform).count()
                platform_data['story_count'].append(story_count)
            except Exception as e:
                platform_data['story_count'].append(0)

            try:
                feed_count = feed_queryset.filter(platform=platform).count()
                platform_data['feed_count'].append(feed_count)
            except Exception as e:
                platform_data['feed_count'].append(0)
    except Exception:
        platform_data = {
            'labels': ['Instagram', 'TikTok', 'Facebook', 'YouTube'],
            'story_count': [0, 0, 0, 0],
            'feed_count': [0, 0, 0, 0]
        }

    # Data untuk Pie Chart - Distribusi konten berdasarkan status
    try:
        try:
            story_status_count = {
                'draft': story_queryset.filter(status='draft').count(),
                'published': story_queryset.filter(status__in=['live', 'published']).count(),
                'archived': story_queryset.filter(status='archived').count(),
            }
        except Exception:
            story_status_count = {'draft': 0, 'published': 0, 'archived': 0}

        try:
            feed_status_count = {
                'draft': feed_queryset.filter(status='draft').count(),
                'published': feed_queryset.filter(status='published').count(),
                'scheduled': feed_queryset.filter(status='scheduled').count(),
            }
        except Exception:
            feed_status_count = {'draft': 0, 'published': 0, 'scheduled': 0}
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

    # Get companies untuk filter
    try:
        companies = get_companies_safe()
    except Exception:
        companies = []
    
    # Get social media accounts untuk filter
    try:
        social_media_accounts = SocialMediaAccount.objects.filter(status='active').order_by('platform', 'account_name')
    except Exception:
        social_media_accounts = []

    context = TemplateLayout.init(request, {})
    context.update({
        "layout_path": TemplateHelper.set_layout("layout_vertical.html", context),
        "total_campaigns": total_campaigns,
        "total_stories": total_stories,
        "total_fyp_posts": total_fyp_posts,
        "total_feeds": total_feeds,
        "engagement_avg": round(engagement_avg, 2) if engagement_avg else 0.0,
        "total_revenue": float(total_revenue) if total_revenue else 0.0,
        "pending_revenue": float(pending_revenue) if pending_revenue else 0.0,
        "recent_activities": recent_activities,
        "pending_campaigns": pending_campaigns,
        "pending_collabs": pending_collabs,
        "under_review_feeds": under_review_feeds,
        "trend_data": json.dumps(trend_data),
        "platform_data": json.dumps(platform_data),
        "status_data": json.dumps(status_data),
        "companies": companies,
        "social_media_accounts": social_media_accounts,
        "is_admin": check_admin_permission(request.user),
    })

    return render(request, 'kpi_management/dashboard_management.html', context)


@login_required
def dashboard_settings_view(request):
    """Dashboard Settings - Setting layout widget dan permission"""
    if not check_admin_permission(request.user):
        messages.error(request, 'Anda tidak memiliki akses!')
        return redirect('dashboard-analytics')

    settings_obj = DashboardSettings.objects.first()
    if not settings_obj:
        settings_obj = DashboardSettings.objects.create()

    if request.method == 'POST':
        form = DashboardSettingsForm(request.POST, instance=settings_obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Dashboard settings berhasil diperbarui!')
            return redirect('dashboard-settings')
    else:
        form = DashboardSettingsForm(instance=settings_obj)

    context = TemplateLayout.init(request, {})
    context.update({
        "layout_path": TemplateHelper.set_layout("layout_vertical.html", context),
        "form": form,
        "settings": settings_obj,
        "is_admin": True,
    })

    return render(request, 'kpi_management/dashboard_settings.html', context)


# ==================== REPORT / LAPORAN ====================

class ReportListView(BaseKPIView, ListView):
    model = Report
    template_name = 'kpi_management/report_list.html'
    context_object_name = 'reports'
    paginate_by = 20

    def get_queryset(self):
        try:
            queryset = Report.objects.all()
        except Exception:
            # If table doesn't exist, return empty queryset immediately
            return Report.objects.none()

        try:
            search = self.request.GET.get('search', '')
            report_type = self.request.GET.get('report_type', '')
            period = self.request.GET.get('period', '')

            if search:
                queryset = queryset.filter(Q(title__icontains=search))
            if report_type:
                queryset = queryset.filter(report_type=report_type)
            if period:
                queryset = queryset.filter(period=period)

            return queryset.order_by('-created_at')
        except Exception:
            # If any error occurs during filtering, return empty queryset
            return Report.objects.none()

    def get_context_data(self, **kwargs):
        try:
            context = super().get_context_data(**kwargs)
        except Exception as e:
            # If pagination fails due to table not existing, create empty context
            # Create empty paginator object manually
            from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

            # Create empty list and paginate it
            empty_list = []
            paginator = Paginator(empty_list, self.paginate_by)
            page = self.request.GET.get('page', 1)
            try:
                page_obj = paginator.page(page)
            except (PageNotAnInteger, EmptyPage):
                page_obj = paginator.page(1)

            # Initialize context with TemplateLayout to ensure layout_path is set
            context = TemplateLayout.init(self, {
                'reports': page_obj,
                'is_paginated': False,
                'page_obj': page_obj,
            })
            context.update({
                "layout_path": TemplateHelper.set_layout("layout_vertical.html", context),
            })
        context['is_admin'] = check_admin_permission(self.request.user)
        return context


class ReportCreateView(BaseKPIView, CreateView):
    model = Report
    form_class = ReportForm
    template_name = 'kpi_management/report_form.html'
    success_url = reverse_lazy('kpi_management:report-list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        # Generate report data
        report = form.save()
        report.generate_report_data()
        # Log activity
        try:
            AuditLog.objects.create(
                user=self.request.user,
                action='create',
                target_type='Report',
                target_id=report.id,
                target_name=report.title,
                ip_address=self.get_client_ip(),
                user_agent=self.request.META.get('HTTP_USER_AGENT', ''),
                description=f'Created report: {report.title}'
            )
        except Exception:
            pass  # Skip if AuditLog table doesn't exist
        messages.success(self.request, 'Report berhasil dibuat!')
        return redirect('report-detail', pk=report.pk)

    def get_client_ip(self):
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        return ip

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Buat Report'
        context['is_admin'] = check_admin_permission(self.request.user)
        return context


class ReportDetailView(BaseKPIView, DetailView):
    model = Report
    template_name = 'kpi_management/report_detail.html'
    context_object_name = 'report'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_admin'] = check_admin_permission(self.request.user)
        return context


@login_required
def report_export_pdf(request, pk):
    """Export report to PDF"""
    report = get_object_or_404(Report, pk=pk)
    # TODO: Implement PDF export using reportlab or weasyprint
    messages.info(request, 'Fitur export PDF sedang dalam pengembangan')
    return redirect('kpi_management:report-detail', pk=pk)


@login_required
def report_export_excel(request, pk):
    """Export report to Excel"""
    report = get_object_or_404(Report, pk=pk)
    # TODO: Implement Excel export using openpyxl
    messages.info(request, 'Fitur export Excel sedang dalam pengembangan')
    return redirect('kpi_management:report-detail', pk=pk)


# ==================== AUDIT LOG ====================

class AuditLogListView(BaseKPIView, ListView):
    model = AuditLog
    template_name = 'kpi_management/auditlog_list.html'
    context_object_name = 'audit_logs'
    paginate_by = 50

    def get_queryset(self):
        try:
            queryset = AuditLog.objects.all()
        except Exception:
            # If table doesn't exist, return empty queryset
            return AuditLog.objects.none()

        user_filter = self.request.GET.get('user', '')
        action_filter = self.request.GET.get('action', '')
        target_type = self.request.GET.get('target_type', '')

        try:
            if user_filter:
                queryset = queryset.filter(user_id=user_filter)
            if action_filter:
                queryset = queryset.filter(action=action_filter)
            if target_type:
                queryset = queryset.filter(target_type=target_type)

            return queryset.order_by('-created_at')
        except Exception:
            # If any error occurs during filtering, return empty queryset
            return AuditLog.objects.none()

    def get_context_data(self, **kwargs):
        try:
            context = super().get_context_data(**kwargs)
        except Exception as e:
            # If pagination fails due to table not existing, create empty context
            # Create empty paginator object manually
            from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

            # Create empty list and paginate it
            empty_list = []
            paginator = Paginator(empty_list, self.paginate_by)
            page = self.request.GET.get('page', 1)
            try:
                page_obj = paginator.page(page)
            except (PageNotAnInteger, EmptyPage):
                page_obj = paginator.page(1)

            # Initialize context with TemplateLayout to ensure layout_path is set
            context = TemplateLayout.init(self, {
                'audit_logs': page_obj,
                'is_paginated': False,
                'page_obj': page_obj,
            })
            context.update({
                "layout_path": TemplateHelper.set_layout("layout_vertical.html", context),
            })
        context['is_admin'] = check_admin_permission(self.request.user)
        try:
            context['users'] = User.objects.filter(is_active=True)
        except Exception:
            context['users'] = []

        # Data untuk grafik Audit Log
        try:
            from django.db.models import Count
            from datetime import datetime, timedelta
            import json

            # Activity Timeline Chart (7 hari terakhir)
            date_range = [timezone.now().date() - timedelta(days=x) for x in range(6, -1, -1)]
            activity_timeline = {
                'dates': [d.strftime('%d %b') for d in date_range],
                'create': [],
                'update': [],
                'delete': [],
                'login': []
            }

            for date in date_range:
                logs = AuditLog.objects.filter(created_at__date=date)
                activity_timeline['create'].append(logs.filter(action='create').count())
                activity_timeline['update'].append(logs.filter(action='update').count())
                activity_timeline['delete'].append(logs.filter(action='delete').count())
                activity_timeline['login'].append(logs.filter(action='login').count())

            context['activity_timeline_data'] = json.dumps(activity_timeline)

            # Action Distribution Pie Chart
            action_dist = {
                'labels': ['Create', 'Update', 'Delete', 'Login', 'Other'],
                'values': []
            }
            action_dist['values'].append(AuditLog.objects.filter(action='create').count())
            action_dist['values'].append(AuditLog.objects.filter(action='update').count())
            action_dist['values'].append(AuditLog.objects.filter(action='delete').count())
            action_dist['values'].append(AuditLog.objects.filter(action='login').count())
            action_dist['values'].append(AuditLog.objects.exclude(action__in=['create', 'update', 'delete', 'login']).count())

            context['action_distribution_data'] = json.dumps(action_dist)

            # Top Users Activity
            top_users = AuditLog.objects.values('user__username').annotate(
                count=Count('id')
            ).order_by('-count')[:10]

            top_users_data = {
                'labels': [u['user__username'] or 'System' for u in top_users],
                'values': [u['count'] for u in top_users]
            }
            context['top_users_data'] = json.dumps(top_users_data)

        except Exception as e:
            import json
            context['activity_timeline_data'] = json.dumps({'dates': [], 'create': [], 'update': [], 'delete': [], 'login': []})
            context['action_distribution_data'] = json.dumps({'labels': [], 'values': []})
            context['top_users_data'] = json.dumps({'labels': [], 'values': []})

        return context


@login_required
def audit_log_charts_api(request):
    """API endpoint untuk real-time update grafik Audit Log"""
    try:
        from django.db.models import Count
        from datetime import timedelta
        import json

        # Activity Timeline Chart (7 hari terakhir)
        date_range = [timezone.now().date() - timedelta(days=x) for x in range(6, -1, -1)]
        activity_timeline = {
            'dates': [d.strftime('%d %b') for d in date_range],
            'create': [],
            'update': [],
            'delete': [],
            'login': []
        }

        for date in date_range:
            logs = AuditLog.objects.filter(created_at__date=date)
            activity_timeline['create'].append(logs.filter(action='create').count())
            activity_timeline['update'].append(logs.filter(action='update').count())
            activity_timeline['delete'].append(logs.filter(action='delete').count())
            activity_timeline['login'].append(logs.filter(action='login').count())

        # Action Distribution Pie Chart
        action_dist = {
            'labels': ['Create', 'Update', 'Delete', 'Login', 'Other'],
            'values': []
        }
        action_dist['values'].append(AuditLog.objects.filter(action='create').count())
        action_dist['values'].append(AuditLog.objects.filter(action='update').count())
        action_dist['values'].append(AuditLog.objects.filter(action='delete').count())
        action_dist['values'].append(AuditLog.objects.filter(action='login').count())
        action_dist['values'].append(AuditLog.objects.exclude(action__in=['create', 'update', 'delete', 'login']).count())

        # Top Users Activity
        top_users = AuditLog.objects.values('user__username').annotate(
            count=Count('id')
        ).order_by('-count')[:10]

        top_users_data = {
            'labels': [u['user__username'] or 'System' for u in top_users],
            'values': [u['count'] for u in top_users]
        }

        return JsonResponse({
            'success': True,
            'activity_timeline': activity_timeline,
            'action_distribution': action_dist,
            'top_users': top_users_data
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e),
            'activity_timeline': {'dates': [], 'create': [], 'update': [], 'delete': [], 'login': []},
            'action_distribution': {'labels': [], 'values': []},
            'top_users': {'labels': [], 'values': []}
        })


@login_required
def dashboard_charts_api(request):
    """API endpoint untuk real-time update grafik Dashboard Management"""
    try:
        from django.db.models import Avg, Sum, Count
        from datetime import timedelta
        import json

        # Filter by company jika ada
        company_filter = request.GET.get('company', '')
        account_name_filter = request.GET.get('account_name', '')

        try:
            story_queryset = Story.objects.all()
            feed_queryset = DailyFeedReels.objects.all()
        except Exception:
            story_queryset = Story.objects.none()
            feed_queryset = DailyFeedReels.objects.none()

        if company_filter:
            try:
                story_queryset = story_queryset.filter(company_id=company_filter)
                feed_queryset = feed_queryset.filter(company_id=company_filter)
            except Exception:
                pass

        if account_name_filter:
            try:
                story_queryset = story_queryset.filter(account_name=account_name_filter)
                feed_queryset = feed_queryset.filter(account_name=account_name_filter)
            except Exception:
                pass

        # Trend Performa 7 Hari Terakhir
        date_range = [timezone.now().date() - timedelta(days=x) for x in range(6, -1, -1)]
        trend_data = {
            'dates': [d.strftime('%d %b') for d in date_range],
            'views': [],
            'engagement': [],
            'reach': []
        }

        for date in date_range:
            try:
                # Story views dan reach
                try:
                    story_views = story_queryset.filter(story_date=date).aggregate(Sum('views'))['views__sum'] or 0
                except Exception:
                    story_views = 0
                
                try:
                    story_reach = story_queryset.filter(story_date=date).aggregate(Sum('reach'))['reach__sum'] or 0
                except Exception:
                    story_reach = 0
                
                try:
                    story_eng = story_queryset.filter(story_date=date).aggregate(Avg('engagement_rate'))['engagement_rate__avg'] or 0
                except Exception:
                    story_eng = 0

                # Feed views dan engagement
                try:
                    feed_views = feed_queryset.filter(publish_date__date=date).aggregate(Sum('views'))['views__sum'] or 0
                except Exception:
                    feed_views = 0
                
                try:
                    feed_eng = feed_queryset.filter(publish_date__date=date).aggregate(Avg('engagement_rate'))['engagement_rate__avg'] or 0
                except Exception:
                    feed_eng = 0

                # Combine data
                total_views = int(story_views + feed_views)
                total_reach = int(story_reach)
                avg_engagement = (story_eng + feed_eng) / 2 if (story_eng or feed_eng) else 0

                trend_data['views'].append(total_views)
                trend_data['reach'].append(total_reach)
                trend_data['engagement'].append(round(avg_engagement, 2))
            except Exception as e:
                trend_data['views'].append(0)
                trend_data['reach'].append(0)
                trend_data['engagement'].append(0)

        # Platform Distribution
        platform_data = {
            'labels': ['Instagram', 'TikTok', 'Facebook', 'YouTube'],
            'story_count': [0, 0, 0, 0],
            'feed_count': [0, 0, 0, 0]
        }

        try:
            for idx, platform in enumerate(['instagram', 'tiktok', 'facebook', 'youtube']):
                platform_data['story_count'][idx] = story_queryset.filter(platform__iexact=platform).count() if hasattr(story_queryset.model, 'platform') else 0
                platform_data['feed_count'][idx] = feed_queryset.filter(platform__iexact=platform).count() if hasattr(feed_queryset.model, 'platform') else 0
        except Exception:
            pass

        # Status Distribution
        status_data = {
            'labels': ['Draft', 'Published', 'Scheduled', 'Archived'],
            'values': [0, 0, 0, 0]
        }

        try:
            if hasattr(story_queryset.model, 'status'):
                status_data['values'][0] = story_queryset.filter(status='draft').count()
                status_data['values'][1] = story_queryset.filter(status='published').count()
                status_data['values'][2] = story_queryset.filter(status='scheduled').count()
                status_data['values'][3] = story_queryset.filter(status='archived').count()
        except Exception:
            pass

        return JsonResponse({
            'success': True,
            'trend_data': trend_data,
            'platform_data': platform_data,
            'status_data': status_data
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e),
            'trend_data': {'dates': [], 'views': [], 'engagement': [], 'reach': []},
            'platform_data': {'labels': [], 'story_count': [], 'feed_count': []},
            'status_data': {'labels': [], 'values': []}
        })


# ==================== FYP LEADERBOARD ====================

@login_required
def fyp_leaderboard(request):
    """FYP Leaderboard - Insight analytic & leaderboard FYP content"""
    try:
        # Try to get leaderboard, but handle if columns don't exist
        # Use only() to select specific fields that should exist
        try:
            leaderboard = FYPPostValue.objects.all().order_by('-viral_score')[:20]
            # Convert to list to avoid lazy evaluation issues
            leaderboard = list(leaderboard)
        except Exception:
            # If viral_score column doesn't exist, try ordering by post_date
            try:
                leaderboard = list(FYPPostValue.objects.all().order_by('-post_date')[:20])
            except Exception:
                # If table doesn't exist, return empty list
                leaderboard = []
    except Exception as e:
        # If table or columns don't exist, return empty list
        leaderboard = []

    context = TemplateLayout.init(request, {})
    context.update({
        "layout_path": TemplateHelper.set_layout("layout_vertical.html", context),
        "leaderboard": leaderboard,
        "is_admin": check_admin_permission(request.user),
    })

    return render(request, 'kpi_management/fyp_leaderboard.html', context)


# ==================== CALENDAR SCHEDULING ====================

@login_required
def calendar_scheduling(request):
    """Calendar scheduling view untuk Daily Feed/Reels"""
    # Get feeds with target_post_date, handle if column doesn't exist
    try:
        # Try to get feeds with target_post_date
        feeds = DailyFeedReels.objects.filter(status__in=['draft', 'scheduled']).exclude(target_post_date__isnull=True).order_by('target_post_date')
        # Convert to list to evaluate query and catch any column errors
        feeds = list(feeds)
    except Exception:
        # If target_post_date or format_type column doesn't exist, get all feeds without filtering by target_post_date
        try:
            feeds = list(DailyFeedReels.objects.filter(status__in=['draft', 'scheduled']).order_by('-created_at'))
        except Exception:
            # If table doesn't exist or other error, return empty list
            feeds = []

    # Format untuk calendar
    calendar_events = []
    for feed in feeds:
        try:
            # Check if target_post_date exists and has value
            target_date = None
            if hasattr(feed, 'target_post_date'):
                target_date = feed.target_post_date

            # If no target_post_date, use created_at as fallback
            if not target_date and hasattr(feed, 'created_at'):
                target_date = feed.created_at

            if target_date:
                if hasattr(target_date, 'isoformat'):
                    start_date = target_date.isoformat()
                elif hasattr(target_date, 'strftime'):
                    start_date = target_date.strftime('%Y-%m-%d')
                else:
                    start_date = str(target_date)

                calendar_events.append({
                    'title': getattr(feed, 'title', 'Untitled'),
                    'start': start_date,
                    'status': getattr(feed, 'status', 'draft'),
                    'platform': getattr(feed, 'platform', ''),
                    'url': f"/kpi/daily-feeds/{feed.pk}/"
                })
        except Exception:
            continue

    context = TemplateLayout.init(request, {})
    context.update({
        "layout_path": TemplateHelper.set_layout("layout_vertical.html", context),
        "feeds": feeds,
        "calendar_events": json.dumps(calendar_events) if calendar_events else json.dumps([]),
        "is_admin": check_admin_permission(request.user),
    })

    return render(request, 'kpi_management/calendar_scheduling.html', context)


# ==================== SYSTEM SETTINGS / PENGATURAN ====================

class SystemSettingsListView(BaseKPIView, ListView):
    model = SystemSettings
    template_name = 'kpi_management/settings_list.html'
    context_object_name = 'settings_list'
    paginate_by = 20

    def get_queryset(self):
        try:
            queryset = SystemSettings.objects.all()
        except Exception:
            # If table doesn't exist, return empty queryset
            return SystemSettings.objects.none()

        search = self.request.GET.get('search', '')
        setting_type = self.request.GET.get('type', '')

        if search:
            try:
                queryset = queryset.filter(
                    Q(name__icontains=search) |
                    Q(label__icontains=search) |
                    Q(description__icontains=search)
                )
            except Exception:
                return SystemSettings.objects.none()

        if setting_type:
            try:
                queryset = queryset.filter(setting_type=setting_type)
            except Exception:
                return SystemSettings.objects.none()

        try:
            return queryset.order_by('setting_type', 'name')
        except Exception:
            return SystemSettings.objects.none()

    def dispatch(self, request, *args, **kwargs):
        if not check_admin_permission(request.user):
            messages.error(request, 'Anda tidak memiliki akses untuk melihat pengaturan!')
            return redirect('index')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        try:
            context = super().get_context_data(**kwargs)
        except Exception as e:
            # If pagination fails due to table not existing, create empty context
            from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

            empty_list = []
            paginator = Paginator(empty_list, self.paginate_by)
            page = self.request.GET.get('page', 1)
            try:
                page_obj = paginator.page(page)
            except (PageNotAnInteger, EmptyPage):
                page_obj = paginator.page(1)

            # Initialize context with TemplateLayout to ensure layout_path is set
            context = TemplateLayout.init(self, {
                'settings_list': page_obj,
                'is_paginated': False,
                'page_obj': page_obj,
            })
            context.update({
                "layout_path": TemplateHelper.set_layout("layout_vertical.html", context),
            })

        context['is_admin'] = True
        try:
            context['setting_types'] = SystemSettings.SETTING_TYPE_CHOICES
        except Exception:
            context['setting_types'] = []
        return context


class SystemSettingsCreateView(BaseKPIView, CreateView):
    model = SystemSettings
    form_class = SystemSettingsForm
    template_name = 'kpi_management/settings_form.html'
    success_url = reverse_lazy('kpi_management:settings-list')

    def dispatch(self, request, *args, **kwargs):
        if not check_admin_permission(request.user):
            messages.error(request, 'Anda tidak memiliki akses untuk membuat pengaturan!')
            return redirect('index')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        setting = form.save(commit=False)
        setting.created_by = self.request.user
        setting.save()
        # Log activity
        try:
            AuditLog.objects.create(
                user=self.request.user,
                action='create',
                target_type='SystemSettings',
                target_id=setting.id,
                target_name=setting.name,
                ip_address=self.get_client_ip(),
                user_agent=self.request.META.get('HTTP_USER_AGENT', ''),
                description=f'Created setting: {setting.name}'
            )
        except Exception:
            pass  # Skip if AuditLog table doesn't exist
        messages.success(self.request, 'Pengaturan berhasil dibuat!')
        return redirect(self.success_url)

    def get_client_ip(self):
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        return ip

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Tambah Pengaturan'
        context['is_admin'] = True
        return context


class SystemSettingsUpdateView(BaseKPIView, UpdateView):
    model = SystemSettings
    form_class = SystemSettingsForm
    template_name = 'kpi_management/settings_form.html'
    success_url = reverse_lazy('kpi_management:settings-list')

    def dispatch(self, request, *args, **kwargs):
        if not check_admin_permission(request.user):
            messages.error(request, 'Anda tidak memiliki akses untuk mengedit pengaturan!')
            return redirect('index')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        old_name = self.object.name
        response = super().form_valid(form)
        # Log activity
        try:
            AuditLog.objects.create(
                user=self.request.user,
                action='update',
                target_type='SystemSettings',
                target_id=self.object.id,
                target_name=self.object.name,
                old_data={'name': old_name},
                new_data={'name': self.object.name},
                ip_address=self.get_client_ip(),
                user_agent=self.request.META.get('HTTP_USER_AGENT', ''),
                description=f'Updated setting: {self.object.name}'
            )
        except Exception:
            pass  # Skip if AuditLog table doesn't exist
        messages.success(self.request, 'Pengaturan berhasil diperbarui!')
        return response

    def get_client_ip(self):
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        return ip

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Pengaturan'
        context['is_admin'] = True
        return context


class SystemSettingsDeleteView(BaseKPIView, DeleteView):
    model = SystemSettings
    template_name = 'kpi_management/settings_confirm_delete.html'
    success_url = reverse_lazy('kpi_management:settings-list')

    def dispatch(self, request, *args, **kwargs):
        if not check_admin_permission(request.user):
            messages.error(request, 'Anda tidak memiliki akses untuk menghapus pengaturan!')
            return redirect('index')
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        name = self.object.name
        target_id = self.object.id
        # Log activity before deletion
        try:
            AuditLog.objects.create(
                user=request.user,
                action='delete',
                target_type='SystemSettings',
                target_id=target_id,
                target_name=name,
                ip_address=self.get_client_ip(),
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
                description=f'Deleted setting: {name}'
            )
        except Exception:
            pass  # Skip if AuditLog table doesn't exist
        messages.success(self.request, 'Pengaturan berhasil dihapus!')
        return super().delete(request, *args, **kwargs)

    def get_client_ip(self):
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        return ip

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_admin'] = True
        return context


# ==================== SOCIAL MEDIA ACCOUNT CRUD ====================

class SocialMediaAccountListView(BaseKPIView, ListView):
    model = SocialMediaAccount
    template_name = 'kpi_management/socialmediaaccount_list.html'
    context_object_name = 'accounts'
    paginate_by = 20

    def get_queryset(self):
        # Hanya gunakan select_related untuk field yang pasti ada
        queryset = SocialMediaAccount.objects.select_related('owner', 'profile').all()
        search = self.request.GET.get('search', '')
        platform = self.request.GET.get('platform', '')
        status = self.request.GET.get('status', '')
        company = self.request.GET.get('company', '')

        if search:
            queryset = queryset.filter(
                Q(account_name__icontains=search) |
                Q(display_name__icontains=search) |
                Q(owner__username__icontains=search) |
                Q(profile__brand_name__icontains=search)
            )
        if platform:
            queryset = queryset.filter(platform=platform)
        if status:
            queryset = queryset.filter(status=status)
        if company:
            try:
                queryset = queryset.filter(company_id=company)
            except Exception:
                # Jika field company belum ada, skip filter ini
                pass

        return queryset.order_by('-created_at')

    def dispatch(self, request, *args, **kwargs):
        if not check_admin_permission(request.user):
            messages.error(request, 'Anda tidak memiliki akses untuk melihat daftar akun sosial media!')
            return redirect('index')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_admin'] = True
        context['platforms'] = SocialMediaAccount.PLATFORM_CHOICES
        context['statuses'] = SocialMediaAccount.STATUS_CHOICES
        context['companies'] = get_companies_safe()

        # Convert tags from list to comma-separated string for display
        # Use page_obj.object_list if paginated, otherwise use accounts
        accounts_list = context.get('page_obj', None)
        if accounts_list:
            accounts_list = accounts_list.object_list
        else:
            accounts_list = context.get('accounts', [])

        for account in accounts_list:
            if hasattr(account, 'tags') and isinstance(account.tags, list):
                account.tags_display = ', '.join(account.tags)
            else:
                account.tags_display = ''

        return context


class SocialMediaAccountCreateView(BaseKPIView, CreateView):
    model = SocialMediaAccount
    form_class = SocialMediaAccountForm
    template_name = 'kpi_management/socialmediaaccount_form.html'
    success_url = reverse_lazy('kpi_management:socialmediaaccount-list')

    def dispatch(self, request, *args, **kwargs):
        if not check_admin_permission(request.user):
            messages.error(request, 'Anda tidak memiliki akses untuk membuat akun sosial media!')
            return redirect('index')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # Save form first to get instance
        account = form.save(commit=False)
        account.created_by = self.request.user
        if not account.connected_at:
            from django.utils import timezone
            account.connected_at = timezone.now()

        # Tags conversion is handled in form.save() method
        account.save()
        # Log activity
        try:
            AuditLog.objects.create(
                user=self.request.user,
                action='create',
                target_type='SocialMediaAccount',
                target_id=account.id,
                target_name=account.account_name,
                ip_address=self.get_client_ip(),
                user_agent=self.request.META.get('HTTP_USER_AGENT', ''),
                description=f'Created social media account: {account.account_name} ({account.get_platform_display()})'
            )
        except Exception:
            pass  # Skip if AuditLog table doesn't exist
        messages.success(self.request, 'Akun sosial media berhasil dibuat!')
        return redirect('kpi_management:socialmediaaccount-list')

    def get_client_ip(self):
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        return ip

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Tambah Akun Sosial Media'
        context['is_admin'] = True

        # Initialize tags field if instance exists
        if self.object and hasattr(self.object, 'tags') and isinstance(self.object.tags, list):
            context['form'].fields['tags'].initial = ', '.join(self.object.tags)

        return context


class SocialMediaAccountUpdateView(BaseKPIView, UpdateView):
    model = SocialMediaAccount
    form_class = SocialMediaAccountForm
    template_name = 'kpi_management/socialmediaaccount_form.html'
    success_url = reverse_lazy('kpi_management:socialmediaaccount-list')

    def dispatch(self, request, *args, **kwargs):
        if not check_admin_permission(request.user):
            messages.error(request, 'Anda tidak memiliki akses untuk mengedit akun sosial media!')
            return redirect('index')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # Save form first to get instance
        account = form.save(commit=False)

        # Tags conversion is handled in form.save() method
        old_account_name = self.object.account_name
        account.save()
        # Log activity
        try:
            AuditLog.objects.create(
                user=self.request.user,
                action='update',
                target_type='SocialMediaAccount',
                target_id=account.id,
                target_name=account.account_name,
                old_data={'account_name': old_account_name},
                new_data={'account_name': account.account_name},
                ip_address=self.get_client_ip(),
                user_agent=self.request.META.get('HTTP_USER_AGENT', ''),
                description=f'Updated social media account: {account.account_name} ({account.get_platform_display()})'
            )
        except Exception:
            pass  # Skip if AuditLog table doesn't exist
        messages.success(self.request, 'Akun sosial media berhasil diperbarui!')
        return redirect('kpi_management:socialmediaaccount-list')

    def get_client_ip(self):
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        return ip

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Akun Sosial Media'
        context['is_admin'] = True

        # Initialize tags field from list to comma-separated string
        if self.object and hasattr(self.object, 'tags'):
            if isinstance(self.object.tags, list):
                context['form'].fields['tags'].initial = ', '.join(self.object.tags)
            elif self.object.tags:
                context['form'].fields['tags'].initial = str(self.object.tags)

        return context


class SocialMediaAccountDeleteView(BaseKPIView, DeleteView):
    model = SocialMediaAccount
    template_name = 'kpi_management/socialmediaaccount_confirm_delete.html'
    success_url = reverse_lazy('kpi_management:socialmediaaccount-list')

    def dispatch(self, request, *args, **kwargs):
        if not check_admin_permission(request.user):
            messages.error(request, 'Anda tidak memiliki akses untuk menghapus akun sosial media!')
            return redirect('index')
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        name = self.object.account_name
        target_id = self.object.id
        # Log activity before deletion
        try:
            AuditLog.objects.create(
                user=request.user,
                action='delete',
                target_type='SocialMediaAccount',
                target_id=target_id,
                target_name=name,
                ip_address=self.get_client_ip(),
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
                description=f'Deleted social media account: {name}'
            )
        except Exception:
            pass  # Skip if AuditLog table doesn't exist
        messages.success(self.request, 'Akun sosial media berhasil dihapus!')
        return super().delete(request, *args, **kwargs)

    def get_client_ip(self):
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        return ip

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_admin'] = True
        return context


class SocialMediaAccountDetailView(BaseKPIView, DetailView):
    model = SocialMediaAccount
    template_name = 'kpi_management/socialmediaaccount_detail.html'
    context_object_name = 'account'

    def dispatch(self, request, *args, **kwargs):
        if not check_admin_permission(request.user):
            messages.error(request, 'Anda tidak memiliki akses untuk melihat detail akun sosial media!')
            return redirect('index')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_admin'] = True
        return context


@login_required
def sync_social_media_account(request, pk):
    """Sync data dari API untuk Social Media Account"""
    if not check_admin_permission(request.user):
        messages.error(request, 'Anda tidak memiliki akses!')
        return redirect('index')

    try:
        account = get_object_or_404(SocialMediaAccount, pk=pk)
        result = account.sync_from_api()

        if result.get('success'):
            messages.success(request, result.get('message', 'Data berhasil di-sync!'))
        else:
            messages.error(request, result.get('message', 'Gagal sync data!'))
    except Exception as e:
        messages.error(request, f'Error: {str(e)}')

    return redirect('kpi_management:socialmediaaccount-detail', pk=pk)


@login_required
def sync_insights_social_media_account(request, pk):
    """Sync insight data dari API untuk Social Media Account"""
    if not check_admin_permission(request.user):
        messages.error(request, 'Anda tidak memiliki akses!')
        return redirect('index')

    try:
        account = get_object_or_404(SocialMediaAccount, pk=pk)
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        result = account.sync_insights_from_api(start_date, end_date)

        if result.get('success'):
            messages.success(request, result.get('message', 'Insight data berhasil di-sync!'))
        else:
            messages.error(request, result.get('message', 'Gagal sync insight data!'))
    except Exception as e:
        messages.error(request, f'Error: {str(e)}')

    return redirect('kpi_management:socialmediaaccount-detail', pk=pk)


# ==================== THEME & LANGUAGE SETTINGS ====================

@login_required
def theme_settings_view(request):
    """View untuk pengaturan tema (dark/light mode)"""
    if not check_admin_permission(request.user):
        messages.error(request, 'Anda tidak memiliki akses!')
        return redirect('index')

    # Get current theme from session or default to 'light'
    current_theme = request.session.get('theme', 'light')

    if request.method == 'POST':
        theme = request.POST.get('theme', 'light')
        if theme in ['light', 'dark']:
            request.session['theme'] = theme
            # Also save to SystemSettings
            try:
                theme_setting, created = SystemSettings.objects.get_or_create(
                    name='theme_mode',
                    defaults={
                        'label': 'Theme Mode',
                        'setting_type': 'general',
                        'value': theme,
                        'value_type': 'text',
                        'description': 'Tema aplikasi: light atau dark',
                        'is_active': True,
                        'is_public': True,
                        'created_by': request.user
                    }
                )
                if not created:
                    theme_setting.value = theme
                    theme_setting.save()
            except Exception:
                pass

            messages.success(request, f'Tema berhasil diubah ke {theme}!')
            return redirect('kpi_management:settings-theme')
        else:
            messages.error(request, 'Tema tidak valid!')

    context = TemplateLayout.init(request, {})
    context.update({
        "layout_path": TemplateHelper.set_layout("layout_vertical.html", context),
        "current_theme": current_theme,
        "is_admin": True,
    })

    return render(request, 'kpi_management/settings_theme.html', context)


@login_required
def language_settings_view(request):
    """View untuk pengaturan bahasa"""
    if not check_admin_permission(request.user):
        messages.error(request, 'Anda tidak memiliki akses!')
        return redirect('index')

    # Get current language from session or default
    current_language = request.session.get('language', 'id')

    # Try to get from SystemSettings
    try:
        lang_setting = SystemSettings.objects.filter(name='system_language', is_active=True).first()
        if lang_setting:
            current_language = lang_setting.value or 'id'
            request.session['language'] = current_language
    except Exception:
        pass

    # Available languages - hanya Indonesia dan Inggris
    available_languages = [
        ('id', 'Bahasa Indonesia'),
        ('en', 'English'),
    ]

    if request.method == 'POST':
        from django.utils import translation
        language = request.POST.get('language', 'id')
        if language in [lang[0] for lang in available_languages]:
            request.session['language'] = language
            # Aktifkan bahasa di Django
            translation.activate(language)
            # Also save to SystemSettings
            try:
                lang_setting, created = SystemSettings.objects.get_or_create(
                    name='system_language',
                    defaults={
                        'label': 'System Language',
                        'setting_type': 'general',
                        'value': language,
                        'value_type': 'text',
                        'description': 'Bahasa sistem aplikasi',
                        'is_active': True,
                        'is_public': True,
                        'created_by': request.user
                    }
                )
                if not created:
                    lang_setting.value = language
                    lang_setting.save()
            except Exception:
                pass

            messages.success(request, f'Bahasa berhasil diubah!' if language == 'id' else 'Language changed successfully!')
            return redirect('kpi_management:settings-language')
        else:
            messages.error(request, 'Bahasa tidak valid!')

    context = TemplateLayout.init(request, {})
    context.update({
        "layout_path": TemplateHelper.set_layout("layout_vertical.html", context),
        "current_language": current_language,
        "available_languages": available_languages,
        "is_admin": True,
    })

    return render(request, 'kpi_management/settings_language.html', context)


@login_required
def toggle_theme(request):
    """AJAX endpoint untuk toggle theme"""
    if request.method == 'POST':
        current_theme = request.session.get('theme', 'light')
        new_theme = 'dark' if current_theme == 'light' else 'light'
        request.session['theme'] = new_theme

        # Save to SystemSettings
        try:
            theme_setting, created = SystemSettings.objects.get_or_create(
                name='theme_mode',
                defaults={
                    'label': 'Theme Mode',
                    'setting_type': 'general',
                    'value': new_theme,
                    'value_type': 'text',
                    'description': 'Tema aplikasi: light atau dark',
                    'is_active': True,
                    'is_public': True,
                    'created_by': request.user
                }
            )
            if not created:
                theme_setting.value = new_theme
                theme_setting.save()
        except Exception:
            pass

        from django.http import JsonResponse
        return JsonResponse({'success': True, 'theme': new_theme})

    from django.http import JsonResponse
    return JsonResponse({'success': False, 'error': 'Invalid method'})


@login_required
def set_language(request):
    """AJAX endpoint untuk set language"""
    if request.method == 'POST':
        language = request.POST.get('language', 'id')
        # Hanya support Indonesia dan Inggris
        available_languages = ['id', 'en']

        if language in available_languages:
            request.session['language'] = language

            # Save to SystemSettings
            try:
                lang_setting, created = SystemSettings.objects.get_or_create(
                    name='system_language',
                    defaults={
                        'label': 'System Language',
                        'setting_type': 'general',
                        'value': language,
                        'value_type': 'text',
                        'description': 'Bahasa sistem aplikasi',
                        'is_active': True,
                        'is_public': True,
                        'created_by': request.user
                    }
                )
                if not created:
                    lang_setting.value = language
                    lang_setting.save()
            except Exception:
                pass

            from django.http import JsonResponse
            return JsonResponse({'success': True, 'language': language})

    from django.http import JsonResponse
    return JsonResponse({'success': False, 'error': 'Invalid method'})


class SystemSettingsDetailView(BaseKPIView, DetailView):
    model = SystemSettings
    template_name = 'kpi_management/settings_detail.html'
    context_object_name = 'setting'

    def dispatch(self, request, *args, **kwargs):
        if not check_admin_permission(request.user):
            messages.error(request, 'Anda tidak memiliki akses untuk melihat detail pengaturan!')
            return redirect('index')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_admin'] = True
        return context

