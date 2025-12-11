from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
import json


class Company(models.Model):
    """Model untuk mengelola perusahaan pusat dan cabang"""
    TYPE_CHOICES = [
        ('pusat', 'Pusat'),
        ('cabang', 'Cabang'),
    ]

    name = models.CharField(max_length=200, help_text="Nama perusahaan")
    company_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='pusat', help_text="Tipe: Pusat atau Cabang")
    code = models.CharField(max_length=50, unique=True, help_text="Kode perusahaan (unique)")
    address = models.TextField(blank=True, null=True, help_text="Alamat perusahaan")
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    parent_company = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='branches', help_text="Perusahaan induk (untuk cabang)")
    is_active = models.BooleanField(default=True, help_text="Status aktif")
    notes = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"
        ordering = ['company_type', 'name']
        indexes = [
            models.Index(fields=['company_type', 'is_active']),
            models.Index(fields=['code']),
        ]

    def __str__(self):
        return f"{self.name} ({self.get_company_type_display()})"

    @property
    def is_pusat(self):
        return self.company_type == 'pusat'

    @property
    def is_cabang(self):
        return self.company_type == 'cabang'


class Profile(models.Model):
    """Model untuk mengelola profil user / influencer account profile"""
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('editor', 'Editor'),
        ('analyst', 'Analyst'),
        ('client', 'Client'),
        ('viewer', 'Viewer'),
        ('user', 'User'),
    ]

    CATEGORY_CHOICES = [
        ('fashion', 'Fashion'),
        ('beauty', 'Beauty'),
        ('food', 'Food'),
        ('travel', 'Travel'),
        ('lifestyle', 'Lifestyle'),
        ('tech', 'Technology'),
        ('fitness', 'Fitness'),
        ('education', 'Education'),
        ('business', 'Business'),
        ('entertainment', 'Entertainment'),
        ('other', 'Other'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    # Field baru untuk branding profile
    brand_name = models.CharField(max_length=200, blank=True, null=True, help_text="Nama brand / Influencer name")
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    platform_linked = models.JSONField(default=dict, blank=True, help_text="Platform linked (IG, FB, TikTok) dengan username")
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, blank=True, null=True, help_text="Category/niche")
    audience_segment = models.TextField(blank=True, null=True, help_text="Audience segment description")
    performance_rating = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(10.0)], help_text="Auto average insight")
    contact_info = models.JSONField(default=dict, blank=True, help_text="Contact & payment info")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.role}"

    @property
    def is_admin(self):
        return self.role == 'admin'

    def calculate_performance_rating(self):
        """Auto calculate performance rating dari semua insight terkait"""
        from django.db.models import Avg
        # Hitung rata-rata engagement rate dari story, feed, dan fyp post
        story_avg = Story.objects.filter(created_by=self.user).aggregate(Avg('engagement_rate'))['engagement_rate__avg'] or 0
        feed_avg = DailyFeedReels.objects.filter(created_by=self.user).aggregate(Avg('engagement_rate'))['engagement_rate__avg'] or 0
        fyp_avg = FYPPostValue.objects.filter(created_by=self.user).aggregate(Avg('viral_score'))['viral_score__avg'] or 0

        # Normalisasi ke skala 0-10
        rating = ((story_avg + feed_avg + (fyp_avg * 10)) / 3) / 10
        self.performance_rating = min(10.0, max(0.0, rating))
        self.save(update_fields=['performance_rating'])
        return self.performance_rating


class Story(models.Model):
    """Model untuk mengelola Insight Story di sosial media"""
    # Relasi ke Company
    company = models.ForeignKey('Company', on_delete=models.SET_NULL, null=True, blank=True, related_name='stories', help_text="Perusahaan/Cabang")

    PLATFORM_CHOICES = [
        ('instagram', 'Instagram'),
        ('facebook', 'Facebook'),
        ('tiktok', 'TikTok'),
        ('twitter', 'Twitter'),
        ('youtube', 'YouTube Short'),
        ('youtube_long', 'YouTube'),
    ]

    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('scheduled', 'Scheduled'),
        ('live', 'Live'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]

    title = models.CharField(max_length=200)
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    account_name = models.CharField(max_length=100)

    # Field baru: Konten upload
    content_file = models.FileField(upload_to='story_content/', blank=True, null=True, help_text="Gambar/video upload")
    content_image = models.ImageField(upload_to='story_images/', blank=True, null=True, help_text="Gambar story")
    content_url = models.URLField(blank=True, null=True, help_text="URL tautan konten story")

    # Field insight yang sudah ada
    views = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    impressions = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    reach = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    engagement_rate = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(100.0)])
    link_clicks = models.IntegerField(default=0, validators=[MinValueValidator(0)], help_text="CTR link / Swipe Up")

    # Field insight baru
    swipe_up = models.IntegerField(default=0, validators=[MinValueValidator(0)], help_text="Swipe Up count")
    reaction_rate = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(100.0)], help_text="Reaction rate percentage")
    saves = models.IntegerField(default=0, validators=[MinValueValidator(0)], help_text="Save count")
    shares = models.IntegerField(default=0, validators=[MinValueValidator(0)], help_text="Share count")
    replays = models.IntegerField(default=0, validators=[MinValueValidator(0)], help_text="Replay count")

    story_date = models.DateField(help_text="Tanggal Publish")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    notes = models.TextField(blank=True, null=True)

    # Relasi ke Campaign dan Brand Collab
    campaign = models.ForeignKey('Campaign', on_delete=models.SET_NULL, null=True, blank=True, related_name='stories')
    collab_brand = models.ForeignKey('CollabBrand', on_delete=models.SET_NULL, null=True, blank=True, related_name='stories')

    # Performance rating (auto calculated)
    performance_rating = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(10.0)], help_text="Auto calculated performance rating")

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='stories_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Story"
        verbose_name_plural = "Stories"
        ordering = ['-story_date', '-created_at']

    def __str__(self):
        return f"{self.title} - {self.platform}"

    def calculate_performance_rating(self):
        """Auto calculate performance rating berdasarkan insight"""
        if self.views == 0:
            self.performance_rating = 0.0
        else:
            # Formula: (engagement_rate * 0.4) + (reach/views * 100 * 0.3) + (saves/views * 100 * 0.2) + (shares/views * 100 * 0.1)
            engagement_score = self.engagement_rate * 0.4
            reach_score = (self.reach / self.views * 100) * 0.3 if self.views > 0 else 0
            save_score = (self.saves / self.views * 100) * 0.2 if self.views > 0 else 0
            share_score = (self.shares / self.views * 100) * 0.1 if self.views > 0 else 0

            total_score = engagement_score + reach_score + save_score + share_score
            # Normalisasi ke skala 0-10
            self.performance_rating = min(10.0, max(0.0, total_score / 10))

        self.save(update_fields=['performance_rating'])
        return self.performance_rating


class DailyFeedReels(models.Model):
    """Model untuk management konten setiap hari (Feed/Reels)"""
    # Relasi ke Company
    company = models.ForeignKey('Company', on_delete=models.SET_NULL, null=True, blank=True, related_name='feeds_reels', help_text="Perusahaan/Cabang")

    CONTENT_TYPE_CHOICES = [
        ('feed', 'Feed'),
        ('reels', 'Reels'),
    ]

    FORMAT_CHOICES = [
        ('image', 'Image'),
        ('video', 'Video'),
    ]

    PLATFORM_CHOICES = [
        ('instagram', 'Instagram'),
        ('facebook', 'Facebook'),
        ('tiktok', 'TikTok'),
        ('youtube', 'YouTube'),
    ]

    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('scheduled', 'Scheduled'),
        ('published', 'Published'),
        ('under_review', 'Under Review'),
        ('archived', 'Archived'),
    ]

    title = models.CharField(max_length=200)
    content_type = models.CharField(max_length=10, choices=CONTENT_TYPE_CHOICES)
    format_type = models.CharField(max_length=10, choices=FORMAT_CHOICES, default='image', help_text="Format (image/video)")
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    account_name = models.CharField(max_length=100)
    caption = models.TextField()
    content_url = models.URLField(blank=True, null=True)
    thumbnail = models.ImageField(upload_to='content_thumbnails/', blank=True, null=True)
    content_file = models.FileField(upload_to='feed_reels_content/', blank=True, null=True, help_text="Upload gambar/video")

    # Hashtag/Tag
    tags = models.CharField(max_length=500, blank=True, null=True, help_text="Comma-separated tags/hashtag")
    hashtags = models.CharField(max_length=500, blank=True, null=True, help_text="Comma-separated hashtags")

    # Insight
    likes = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    comments = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    shares = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    views = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    saves = models.IntegerField(default=0, validators=[MinValueValidator(0)], help_text="Saves count")
    engagement_rate = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(100.0)])

    # Scheduling
    target_post_date = models.DateTimeField(help_text="Target post date untuk scheduling")
    publish_date = models.DateTimeField(blank=True, null=True, help_text="Tanggal actual publish")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')

    # Relasi
    campaign = models.ForeignKey('Campaign', on_delete=models.SET_NULL, null=True, blank=True, related_name='feeds')
    collab_brand = models.ForeignKey('CollabBrand', on_delete=models.SET_NULL, null=True, blank=True, related_name='feeds')

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='feeds_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Daily Feed/Reels"
        verbose_name_plural = "Daily Feeds/Reels"
        ordering = ['-target_post_date', '-created_at']

    def __str__(self):
        return f"{self.title} - {self.content_type} ({self.platform})"


class FeedReelsHistory(models.Model):
    """Model untuk history update log Daily Feed/Reels"""
    feed_reels = models.ForeignKey(DailyFeedReels, on_delete=models.CASCADE, related_name='history_logs')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    update_type = models.CharField(max_length=50, help_text="Type of update (insight, status, content, etc)")
    old_value = models.TextField(blank=True, null=True)
    new_value = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Feed/Reels History"
        verbose_name_plural = "Feed/Reels Histories"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.feed_reels.title} - {self.update_type} - {self.created_at}"


class FYPPostValue(models.Model):
    """Model untuk Management FYP Post Value (Tracking nilai konten yang berhasil FYP/trending)"""
    PLATFORM_CHOICES = [
        ('tiktok', 'TikTok'),
        ('instagram', 'Instagram'),
        ('youtube', 'YouTube'),
    ]

    MILESTONE_CHOICES = [
        ('50k', '50K'),
        ('100k', '100K'),
        ('500k', '500K'),
        ('1m', '1M'),
        ('5m', '5M'),
        ('10m', '10M+'),
    ]

    post_title = models.CharField(max_length=200, help_text="Judul konten viral")
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    account_name = models.CharField(max_length=100)
    post_url = models.URLField()

    # View metrics
    fyp_views = models.IntegerField(default=0, validators=[MinValueValidator(0)], help_text="Views from FYP")
    total_views = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    fyp_percentage = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(100.0)], help_text="Percentage of views from FYP")
    view_milestone = models.CharField(max_length=10, choices=MILESTONE_CHOICES, blank=True, null=True, help_text="View milestone (50K, 100K, 1M, etc)")

    # Engagement metrics
    reach = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    engagement_rate = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(100.0)])
    engagement_value = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    estimated_reach = models.IntegerField(default=0, validators=[MinValueValidator(0)])

    # Viral score (auto calculated)
    viral_score = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(100.0)], help_text="Auto calculated viral score")

    # Faktor pendukung
    hashtags_used = models.CharField(max_length=500, blank=True, null=True, help_text="Hashtag yang digunakan")
    audio_trending = models.CharField(max_length=200, blank=True, null=True, help_text="Audio trending yang digunakan")
    niche = models.CharField(max_length=100, blank=True, null=True, help_text="Niche konten")
    timing = models.CharField(max_length=100, blank=True, null=True, help_text="Timing posting (best practice)")
    best_practice_note = models.TextField(blank=True, null=True, help_text="Best practice note dari konten ini")

    post_date = models.DateField(help_text="Tanggal viral")
    notes = models.TextField(blank=True, null=True)

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='fyp_posts_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "FYP Post Value"
        verbose_name_plural = "FYP Post Values"
        ordering = ['-post_date', '-viral_score', '-created_at']
        indexes = [
            models.Index(fields=['-viral_score']),  # Untuk leaderboard
        ]

    def __str__(self):
        return f"{self.post_title} - {self.platform}"

    def calculate_viral_score(self):
        """Auto calculate viral score berdasarkan rumus engagement"""
        if self.total_views == 0:
            self.viral_score = 0.0
        else:
            # Formula: (engagement_rate * 0.3) + (fyp_percentage * 0.3) + (views_score * 0.2) + (reach_score * 0.2)
            engagement_score = self.engagement_rate * 0.3
            fyp_score = self.fyp_percentage * 0.3

            # Views score (normalisasi berdasarkan milestone)
            views_score = 0.0
            if self.total_views >= 10000000:
                views_score = 20.0
            elif self.total_views >= 5000000:
                views_score = 18.0
            elif self.total_views >= 1000000:
                views_score = 15.0
            elif self.total_views >= 500000:
                views_score = 12.0
            elif self.total_views >= 100000:
                views_score = 10.0
            elif self.total_views >= 50000:
                views_score = 8.0
            else:
                views_score = (self.total_views / 50000) * 8.0

            # Reach score (normalisasi)
            reach_score = min(20.0, (self.reach / self.total_views * 100) * 0.2) if self.total_views > 0 else 0

            total_score = engagement_score + fyp_score + views_score + reach_score
            self.viral_score = min(100.0, max(0.0, total_score))

        # Update milestone
        if self.total_views >= 10000000:
            self.view_milestone = '10m'
        elif self.total_views >= 5000000:
            self.view_milestone = '5m'
        elif self.total_views >= 1000000:
            self.view_milestone = '1m'
        elif self.total_views >= 500000:
            self.view_milestone = '500k'
        elif self.total_views >= 100000:
            self.view_milestone = '100k'
        elif self.total_views >= 50000:
            self.view_milestone = '50k'

        self.save(update_fields=['viral_score', 'view_milestone'])
        return self.viral_score


class Campaign(models.Model):
    """Model untuk Management Campaign (Kampanye pemasaran social media)"""
    # Relasi ke Company
    company = models.ForeignKey('Company', on_delete=models.SET_NULL, null=True, blank=True, related_name='campaigns', help_text="Perusahaan/Cabang")

    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('planning', 'Planning'),
        ('active', 'Active'),
        ('paused', 'Paused'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    OBJECTIVE_CHOICES = [
        ('brand_awareness', 'Brand Awareness'),
        ('lead', 'Lead Generation'),
        ('engagement', 'Engagement'),
        ('promo', 'Promo/Sale'),
        ('season', 'Seasonal Campaign'),
        ('product_launch', 'Product Launch'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField()
    objective = models.CharField(max_length=50, choices=OBJECTIVE_CHOICES, default='brand_awareness', help_text="Objective (Brand Awareness / Lead / Engagement / Promo / Season)")

    start_date = models.DateField()
    end_date = models.DateField()
    budget = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    spent = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    # KPI Target & Achieved
    kpi_target = models.JSONField(default=dict, blank=True, help_text="Target KPIs (reach, engagement, conversion) in JSON format")
    kpi_achieved = models.JSONField(default=dict, blank=True, help_text="Achieved KPIs in JSON format")

    target_platforms = models.CharField(max_length=500, help_text="Comma-separated platforms")
    target_audience = models.TextField(blank=True, null=True)
    goals = models.TextField(help_text="Campaign goals and objectives")
    campaign_url = models.URLField(blank=True, null=True, help_text="URL tautan campaign")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')

    # Owner / PIC
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='campaigns_owned', help_text="Owner / PIC Campaign")

    notes = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='campaigns_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Campaign"
        verbose_name_plural = "Campaigns"
        ordering = ['-start_date', '-created_at']

    def __str__(self):
        return f"{self.name} ({self.status})"

    @property
    def budget_remaining(self):
        return self.budget - self.spent

    @property
    def progress_percentage(self):
        """Calculate progress KPI percentage"""
        if not self.kpi_target or not self.kpi_achieved:
            return 0.0

        total_target = sum(self.kpi_target.values()) if isinstance(self.kpi_target, dict) else 0
        total_achieved = sum(self.kpi_achieved.values()) if isinstance(self.kpi_achieved, dict) else 0

        if total_target == 0:
            return 0.0

        return min(100.0, (total_achieved / total_target) * 100)

    def get_campaign_summary(self):
        """Generate campaign summary auto report"""
        summary = {
            'name': self.name,
            'status': self.get_status_display(),
            'objective': self.get_objective_display(),
            'budget': float(self.budget),
            'spent': float(self.spent),
            'remaining': float(self.budget_remaining),
            'progress': self.progress_percentage,
            'kpi_target': self.kpi_target,
            'kpi_achieved': self.kpi_achieved,
            'stories_count': self.stories.count(),
            'feeds_count': self.feeds.count(),
            'collabs_count': self.collabs.count(),
        }
        return summary


class CollabBrand(models.Model):
    """Model untuk Management Brand Collaboration (Pengelolaan kerja sama brand / influencer marketing)"""
    STATUS_CHOICES = [
        ('negotiating', 'Negotiating'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('partial', 'Partial'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
    ]

    DELIVERABLES_CHOICES = [
        ('story', 'Story'),
        ('feed', 'Feed'),
        ('reels', 'Reels'),
        ('live_session', 'Live Session'),
        ('other', 'Other'),
    ]

    brand_name = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=100, help_text="PIC kontak")
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    company = models.CharField(max_length=200, blank=True, null=True)
    collaboration_type = models.CharField(max_length=100, help_text="e.g., Sponsored Post, Brand Ambassador, etc.")

    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True, help_text="Durasi kontrak")
    contract_value = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, help_text="Agreement value / kontrak")
    payment_status = models.CharField(max_length=50, choices=PAYMENT_STATUS_CHOICES, default='pending')

    # Deliverables
    deliverables = models.TextField(help_text="List of deliverables (story, feed, reels, live session)")
    deliverables_list = models.JSONField(default=list, blank=True, help_text="Deliverables dalam format JSON")

    # Document upload kontrak
    contract_document = models.FileField(upload_to='collab_contracts/', blank=True, null=True, help_text="Document upload kontrak")

    # Reminder fields
    payment_reminder_date = models.DateField(blank=True, null=True, help_text="Tanggal reminder pembayaran")
    renewal_reminder_date = models.DateField(blank=True, null=True, help_text="Tanggal reminder renewal collab")
    last_reminder_sent = models.DateTimeField(blank=True, null=True)

    # Relasi ke Campaign
    campaign = models.ForeignKey('Campaign', on_delete=models.SET_NULL, null=True, blank=True, related_name='collabs', help_text="Campaign turunannya")

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='negotiating')
    notes = models.TextField(blank=True, null=True)

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='collabs_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Collab Brand"
        verbose_name_plural = "Collab Brands"
        ordering = ['-start_date', '-created_at']

    def __str__(self):
        return f"{self.brand_name} - {self.collaboration_type}"

    def check_payment_reminder(self):
        """Check if payment reminder needed"""
        if self.payment_status in ['pending', 'partial'] and self.payment_reminder_date:
            if timezone.now().date() >= self.payment_reminder_date:
                return True
        return False

    def check_renewal_reminder(self):
        """Check if renewal reminder needed"""
        if self.status == 'active' and self.end_date and self.renewal_reminder_date:
            if timezone.now().date() >= self.renewal_reminder_date:
                return True
        return False


class DashboardSettings(models.Model):
    """Model untuk Dashboard Management - Setting layout widget dan permission"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dashboard_settings', null=True, blank=True)
    role = models.CharField(max_length=50, blank=True, null=True, help_text="Role yang bisa lihat dashboard")

    # Widget settings
    show_total_campaign = models.BooleanField(default=True)
    show_total_story = models.BooleanField(default=True)
    show_total_fyp = models.BooleanField(default=True)
    show_engagement_avg = models.BooleanField(default=True)
    show_revenue_kpi = models.BooleanField(default=True)
    show_user_activity = models.BooleanField(default=True)
    show_notifications = models.BooleanField(default=True)

    # Layout settings
    widget_layout = models.JSONField(default=dict, blank=True, help_text="Layout widget configuration")

    # Permission
    can_view_dashboard = models.BooleanField(default=True)
    allowed_users = models.ManyToManyField(User, blank=True, related_name='allowed_dashboards', help_text="Siapa yang bisa lihat dashboard")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Dashboard Settings"
        verbose_name_plural = "Dashboard Settings"

    def __str__(self):
        return f"Dashboard Settings - {self.role or 'Default'}"


class Report(models.Model):
    """Model untuk CRUD Report / Laporan"""
    REPORT_TYPE_CHOICES = [
        ('campaign_summary', 'Campaign Summary'),
        ('posting_insight', 'Posting Insight Report'),
        ('collaboration', 'Collaboration Report'),
        ('viral_fyp', 'Viral FYP Analysis'),
        ('user_activity', 'Log Aktivitas User'),
        ('comprehensive', 'Comprehensive Report'),
    ]

    PERIOD_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('yearly', 'Yearly'),
        ('custom', 'Custom'),
    ]

    title = models.CharField(max_length=200)
    report_type = models.CharField(max_length=50, choices=REPORT_TYPE_CHOICES)
    period = models.CharField(max_length=20, choices=PERIOD_CHOICES, default='monthly')

    # Filter
    campaign_filter = models.ForeignKey(Campaign, on_delete=models.SET_NULL, null=True, blank=True, related_name='reports')
    brand_filter = models.ForeignKey(CollabBrand, on_delete=models.SET_NULL, null=True, blank=True, related_name='reports')
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    performance_type = models.CharField(max_length=100, blank=True, null=True, help_text="Filter per performance type")

    # Report data
    report_data = models.JSONField(default=dict, blank=True, help_text="Report data dalam format JSON")
    charts_data = models.JSONField(default=dict, blank=True, help_text="Data untuk grafik insight per timeline")

    # Export
    pdf_file = models.FileField(upload_to='reports/pdf/', blank=True, null=True)
    excel_file = models.FileField(upload_to='reports/excel/', blank=True, null=True)

    # Auto generation
    auto_generate = models.BooleanField(default=False, help_text="Auto generation monthly report")
    last_generated = models.DateTimeField(blank=True, null=True)

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='reports_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Report"
        verbose_name_plural = "Reports"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.get_report_type_display()}"

    def generate_report_data(self):
        """Generate report data berdasarkan type dan filter"""
        from django.db.models import Count, Avg, Sum

        data = {
            'summary': {},
            'charts': {},
            'details': []
        }

        if self.report_type == 'campaign_summary':
            campaigns = Campaign.objects.all()
            if self.campaign_filter:
                campaigns = campaigns.filter(id=self.campaign_filter.id)
            if self.start_date and self.end_date:
                campaigns = campaigns.filter(start_date__gte=self.start_date, end_date__lte=self.end_date)

            data['summary'] = {
                'total_campaigns': campaigns.count(),
                'total_budget': float(campaigns.aggregate(Sum('budget'))['budget__sum'] or 0),
                'total_spent': float(campaigns.aggregate(Sum('spent'))['spent__sum'] or 0),
            }
            data['details'] = [camp.get_campaign_summary() for camp in campaigns]

        elif self.report_type == 'posting_insight':
            stories = Story.objects.all()
            feeds = DailyFeedReels.objects.all()
            if self.start_date and self.end_date:
                stories = stories.filter(story_date__gte=self.start_date, story_date__lte=self.end_date)
                feeds = feeds.filter(publish_date__date__gte=self.start_date, publish_date__date__lte=self.end_date)

            data['summary'] = {
                'total_stories': stories.count(),
                'total_feeds': feeds.count(),
                'avg_engagement': float((stories.aggregate(Avg('engagement_rate'))['engagement_rate__avg'] or 0) +
                                       (feeds.aggregate(Avg('engagement_rate'))['engagement_rate__avg'] or 0)) / 2,
            }

        elif self.report_type == 'viral_fyp':
            fyp_posts = FYPPostValue.objects.all().order_by('-viral_score')
            if self.start_date and self.end_date:
                fyp_posts = fyp_posts.filter(post_date__gte=self.start_date, post_date__lte=self.end_date)

            data['summary'] = {
                'total_posts': fyp_posts.count(),
                'avg_viral_score': float(fyp_posts.aggregate(Avg('viral_score'))['viral_score__avg'] or 0),
                'top_posts': [{'title': p.post_title, 'score': p.viral_score} for p in fyp_posts[:10]],
            }

        self.report_data = data
        self.save(update_fields=['report_data'])
        return data


class AuditLog(models.Model):
    """Model untuk CRUD Log Aktifitas / Audit Log"""
    ACTION_CHOICES = [
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('approve', 'Approve'),
        ('reject', 'Reject'),
        ('view', 'View'),
        ('export', 'Export'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='audit_logs')
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)

    # Target object
    target_type = models.CharField(max_length=100, blank=True, null=True, help_text="Model name (Campaign, Story, User, etc)")
    target_id = models.IntegerField(blank=True, null=True, help_text="ID dari target object")
    target_name = models.CharField(max_length=200, blank=True, null=True, help_text="Nama target (Campaign X, Story Y, User Z)")

    # Details
    description = models.TextField(blank=True, null=True)
    old_data = models.JSONField(default=dict, blank=True, help_text="Data sebelum perubahan")
    new_data = models.JSONField(default=dict, blank=True, help_text="Data setelah perubahan")

    # System info
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True, help_text="OS/Browser agent")

    # Timestamp
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Audit Log"
        verbose_name_plural = "Audit Logs"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['action', '-created_at']),
        ]

    def __str__(self):
        return f"{self.user} - {self.get_action_display()} - {self.target_name} - {self.created_at}"


class SystemSettings(models.Model):
    """Model untuk Pengaturan Sistem Umum"""
    SETTING_TYPE_CHOICES = [
        ('general', 'Pengaturan Umum'),
        ('notification', 'Notifikasi'),
        ('security', 'Keamanan'),
        ('email', 'Email'),
        ('integration', 'Integrasi'),
        ('backup', 'Backup'),
        ('other', 'Lainnya'),
    ]

    name = models.CharField(max_length=200, unique=True, help_text="Nama pengaturan (unique key)")
    label = models.CharField(max_length=200, help_text="Label untuk ditampilkan")
    setting_type = models.CharField(max_length=50, choices=SETTING_TYPE_CHOICES, default='general')
    value = models.TextField(blank=True, null=True, help_text="Nilai pengaturan")
    value_type = models.CharField(
        max_length=20,
        default='text',
        help_text="Tipe nilai: text, number, boolean, json, email, url"
    )
    description = models.TextField(blank=True, null=True, help_text="Deskripsi pengaturan")
    is_active = models.BooleanField(default=True)
    is_public = models.BooleanField(
        default=False,
        help_text="Apakah pengaturan ini bisa diakses oleh non-admin?"
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_settings'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "System Setting"
        verbose_name_plural = "System Settings"
        ordering = ['setting_type', 'name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['setting_type', 'is_active']),
        ]

    def __str__(self):
        return f"{self.label} ({self.name})"

    def get_value(self):
        """Get value dengan type conversion"""
        if self.value_type == 'boolean':
            return self.value.lower() in ('true', '1', 'yes', 'on')
        elif self.value_type == 'number':
            try:
                if '.' in str(self.value):
                    return float(self.value)
                return int(self.value)
            except (ValueError, TypeError):
                return 0
        elif self.value_type == 'json':
            try:
                return json.loads(self.value) if self.value else {}
            except (json.JSONDecodeError, TypeError):
                return {}
        return self.value or ''


class SocialMediaAccount(models.Model):
    """Model untuk mengelola akun sosial media"""
    # Relasi ke Company
    company = models.ForeignKey('Company', on_delete=models.SET_NULL, null=True, blank=True, related_name='social_media_accounts', help_text="Perusahaan/Cabang")

    # Opsi Input Data
    INPUT_METHOD_CHOICES = [
        ('manual', 'Manual Input'),
        ('api', 'API/Token Sync'),
    ]
    input_method = models.CharField(max_length=20, choices=INPUT_METHOD_CHOICES, default='manual', help_text="Metode input: Manual atau API Sync")
    auto_sync_enabled = models.BooleanField(default=False, help_text="Aktifkan auto sync dari API")
    sync_schedule = models.CharField(max_length=50, blank=True, null=True, help_text="Jadwal sync (e.g., daily, weekly, hourly)")

    PLATFORM_CHOICES = [
        ('instagram', 'Instagram'),
        ('facebook', 'Facebook'),
        ('tiktok', 'TikTok'),
        ('youtube', 'YouTube'),
        ('twitter', 'Twitter/X'),
        ('linkedin', 'LinkedIn'),
        ('pinterest', 'Pinterest'),
        ('snapchat', 'Snapchat'),
        ('other', 'Lainnya'),
    ]

    STATUS_CHOICES = [
        ('active', 'Aktif'),
        ('inactive', 'Tidak Aktif'),
        ('suspended', 'Ditangguhkan'),
        ('deleted', 'Dihapus'),
    ]

    # Informasi Akun
    platform = models.CharField(max_length=50, choices=PLATFORM_CHOICES, help_text="Platform sosial media")
    account_name = models.CharField(max_length=200, help_text="Nama akun / username")
    account_id = models.CharField(max_length=200, blank=True, null=True, help_text="ID akun (jika tersedia)")
    display_name = models.CharField(max_length=200, blank=True, null=True, help_text="Nama tampilan")
    profile_url = models.URLField(blank=True, null=True, help_text="URL profil akun")

    # Informasi Pemilik
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='social_media_accounts', help_text="Pemilik akun")
    profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name='social_media_accounts', help_text="Profil terkait")

    # Status & Pengaturan
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    is_verified = models.BooleanField(default=False, help_text="Apakah akun terverifikasi?")
    is_business_account = models.BooleanField(default=False, help_text="Apakah akun bisnis?")

    # Statistik Akun
    followers_count = models.IntegerField(default=0, help_text="Jumlah followers")
    following_count = models.IntegerField(default=0, help_text="Jumlah following")
    posts_count = models.IntegerField(default=0, help_text="Jumlah postingan")
    engagement_rate = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(100.0)], help_text="Engagement rate (%)")

    # Kredensial & Akses
    access_token = models.TextField(blank=True, null=True, help_text="Access token (disimpan terenkripsi)")
    refresh_token = models.TextField(blank=True, null=True, help_text="Refresh token (disimpan terenkripsi)")
    api_key = models.CharField(max_length=500, blank=True, null=True, help_text="API Key")
    api_secret = models.CharField(max_length=500, blank=True, null=True, help_text="API Secret")

    # Metadata
    notes = models.TextField(blank=True, null=True, help_text="Catatan tambahan")
    tags = models.JSONField(default=list, blank=True, help_text="Tag untuk kategorisasi")

    # Timestamps
    connected_at = models.DateTimeField(blank=True, null=True, help_text="Tanggal terhubung")
    last_synced_at = models.DateTimeField(blank=True, null=True, help_text="Terakhir sinkronisasi data")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='social_accounts_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Social Media Account"
        verbose_name_plural = "Social Media Accounts"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['platform', 'status']),
            models.Index(fields=['owner', '-created_at']),
            models.Index(fields=['account_name']),
        ]

    def __str__(self):
        return f"{self.get_platform_display()} - {self.account_name}"

    @property
    def is_active(self):
        return self.status == 'active'

    def get_full_account_info(self):
        """Get full account information"""
        return {
            'platform': self.get_platform_display(),
            'account_name': self.account_name,
            'display_name': self.display_name or self.account_name,
            'status': self.get_status_display(),
            'followers': self.followers_count,
            'engagement_rate': self.engagement_rate,
            'is_verified': self.is_verified,
            'is_business': self.is_business_account,
        }

    def sync_from_api(self):
        """Sync data dari platform API (Instagram, Facebook, TikTok, dll)"""
        if not self.access_token and not self.api_key:
            return {'success': False, 'message': 'Access token atau API key belum diisi'}

        try:
            if self.platform == 'instagram':
                # Instagram Graph API
                import requests
                if self.access_token:
                    url = f"https://graph.instagram.com/{self.account_id}?fields=username,account_type,followers_count,media_count&access_token={self.access_token}"
                    response = requests.get(url, timeout=10)
                    if response.status_code == 200:
                        data = response.json()
                        self.followers_count = data.get('followers_count', 0)
                        self.posts_count = data.get('media_count', 0)
                        self.is_business_account = data.get('account_type') == 'BUSINESS'
                        self.last_synced_at = timezone.now()
                        self.save(update_fields=['followers_count', 'posts_count', 'is_business_account', 'last_synced_at'])
                        return {'success': True, 'message': 'Data berhasil di-sync dari Instagram API'}
                    else:
                        return {'success': False, 'message': f'Error API: {response.status_code}'}

            elif self.platform == 'facebook':
                # Facebook Graph API
                import requests
                if self.access_token:
                    url = f"https://graph.facebook.com/v18.0/{self.account_id}?fields=name,fan_count,posts&access_token={self.access_token}"
                    response = requests.get(url, timeout=10)
                    if response.status_code == 200:
                        data = response.json()
                        self.followers_count = data.get('fan_count', 0)
                        self.last_synced_at = timezone.now()
                        self.save(update_fields=['followers_count', 'last_synced_at'])
                        return {'success': True, 'message': 'Data berhasil di-sync dari Facebook API'}
                    else:
                        return {'success': False, 'message': f'Error API: {response.status_code}'}

            elif self.platform == 'tiktok':
                # TikTok API (jika tersedia)
                # Implementasi TikTok API sync
                return {'success': False, 'message': 'TikTok API sync belum diimplementasi'}

            else:
                return {'success': False, 'message': f'Platform {self.platform} belum didukung untuk API sync'}

        except Exception as e:
            return {'success': False, 'message': f'Error saat sync: {str(e)}'}

    def sync_insights_from_api(self, start_date=None, end_date=None):
        """Sync insight data (views, engagement, dll) dari API"""
        if not self.access_token:
            return {'success': False, 'message': 'Access token belum diisi'}

        try:
            if self.platform == 'instagram':
                import requests
                from datetime import datetime, timedelta

                if not start_date:
                    start_date = (timezone.now() - timedelta(days=30)).date()
                if not end_date:
                    end_date = timezone.now().date()

                # Instagram Insights API
                url = f"https://graph.instagram.com/{self.account_id}/insights"
                params = {
                    'metric': 'impressions,reach,profile_views',
                    'period': 'day',
                    'since': start_date.strftime('%Y-%m-%d'),
                    'until': end_date.strftime('%Y-%m-%d'),
                    'access_token': self.access_token
                }
                response = requests.get(url, params=params, timeout=10)

                if response.status_code == 200:
                    data = response.json()
                    # Process dan simpan data insights
                    # Note: Implementasi lengkap tergantung struktur response API
                    self.last_synced_at = timezone.now()
                    self.save(update_fields=['last_synced_at'])
                    return {'success': True, 'message': 'Insight data berhasil di-sync', 'data': data}
                else:
                    return {'success': False, 'message': f'Error API: {response.status_code}'}

            else:
                return {'success': False, 'message': f'Platform {self.platform} belum didukung untuk insight sync'}

        except Exception as e:
            return {'success': False, 'message': f'Error saat sync insight: {str(e)}'}


def get_client_ip(request):
    """Get client IP address from request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

