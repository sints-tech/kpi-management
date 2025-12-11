from django.contrib import admin
from .models import Story, DailyFeedReels, FYPPostValue, Campaign, CollabBrand, Profile, SocialMediaAccount, Company


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'phone', 'created_at']
    list_filter = ['role', 'created_at']
    search_fields = ['user__username', 'user__email', 'phone']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'platform', 'account_name', 'views', 'engagement_rate', 'story_date', 'status', 'created_by', 'created_at']
    list_filter = ['platform', 'status', 'story_date', 'created_at']
    search_fields = ['title', 'account_name', 'notes']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'story_date'


@admin.register(DailyFeedReels)
class DailyFeedReelsAdmin(admin.ModelAdmin):
    list_display = ['title', 'content_type', 'platform', 'account_name', 'views', 'engagement_rate', 'publish_date', 'status', 'created_by', 'created_at']
    list_filter = ['content_type', 'platform', 'status', 'publish_date', 'created_at']
    search_fields = ['title', 'account_name', 'caption', 'tags']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'publish_date'


@admin.register(FYPPostValue)
class FYPPostValueAdmin(admin.ModelAdmin):
    list_display = ['post_title', 'platform', 'account_name', 'fyp_views', 'total_views', 'fyp_percentage', 'viral_score', 'post_date', 'created_by', 'created_at']
    list_filter = ['platform', 'post_date', 'created_at']
    search_fields = ['post_title', 'account_name', 'notes']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'post_date'


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ['name', 'start_date', 'end_date', 'budget', 'spent', 'status', 'created_by', 'created_at']
    list_filter = ['status', 'start_date', 'created_at']
    search_fields = ['name', 'description', 'target_platforms']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'start_date'


@admin.register(CollabBrand)
class CollabBrandAdmin(admin.ModelAdmin):
    list_display = ['brand_name', 'contact_person', 'email', 'collaboration_type', 'contract_value', 'payment_status', 'status', 'start_date', 'created_by', 'created_at']
    list_filter = ['status', 'payment_status', 'start_date', 'created_at']
    search_fields = ['brand_name', 'contact_person', 'email', 'company']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'start_date'


@admin.register(SocialMediaAccount)
class SocialMediaAccountAdmin(admin.ModelAdmin):
    list_display = ['platform', 'account_name', 'company', 'owner', 'input_method', 'status', 'followers_count', 'engagement_rate', 'created_at']
    list_filter = ['platform', 'status', 'is_verified', 'is_business_account', 'input_method', 'company', 'auto_sync_enabled']
    search_fields = ['account_name', 'display_name', 'owner__username', 'profile__brand_name', 'company__name', 'notes', 'tags']
    readonly_fields = ['created_at', 'updated_at', 'connected_at', 'last_synced_at']
    fieldsets = (
        ('Informasi Perusahaan', {
            'fields': ('company',)
        }),
        ('Informasi Akun', {
            'fields': ('platform', 'account_name', 'display_name', 'profile_url', 'account_id', 'status', 'is_verified', 'is_business_account')
        }),
        ('Metode Input', {
            'fields': ('input_method', 'auto_sync_enabled', 'sync_schedule')
        }),
        ('Pemilik Akun', {
            'fields': ('owner', 'profile')
        }),
        ('Statistik', {
            'fields': ('followers_count', 'following_count', 'posts_count', 'engagement_rate')
        }),
        ('Kredensial & Akses API (Sensitif)', {
            'fields': ('api_key', 'api_secret', 'access_token', 'refresh_token'),
            'classes': ('collapse',),  # Collapsible for sensitive info
        }),
        ('Metadata & Timestamps', {
            'fields': ('notes', 'tags', 'connected_at', 'last_synced_at', 'created_by', 'created_at', 'updated_at')
        }),
    )

