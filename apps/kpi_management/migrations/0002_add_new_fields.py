# Generated manually to add new fields

from django.conf import settings
from django.db import migrations, models
import django.core.validators
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('kpi_management', '0001_initial'),
    ]

    operations = [
        # Add new fields to Profile
        migrations.AddField(
            model_name='profile',
            name='brand_name',
            field=models.CharField(blank=True, help_text='Nama brand / Influencer name', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to='logos/'),
        ),
        migrations.AddField(
            model_name='profile',
            name='platform_linked',
            field=models.JSONField(blank=True, default=dict, help_text='Platform linked (IG, FB, TikTok) dengan username'),
        ),
        migrations.AddField(
            model_name='profile',
            name='category',
            field=models.CharField(blank=True, choices=[('fashion', 'Fashion'), ('beauty', 'Beauty'), ('food', 'Food'), ('travel', 'Travel'), ('lifestyle', 'Lifestyle'), ('tech', 'Technology'), ('fitness', 'Fitness'), ('education', 'Education'), ('business', 'Business'), ('entertainment', 'Entertainment'), ('other', 'Other')], help_text='Category/niche', max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='audience_segment',
            field=models.TextField(blank=True, help_text='Audience segment description', null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='performance_rating',
            field=models.FloatField(default=0.0, help_text='Auto average insight', validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(10.0)]),
        ),
        migrations.AddField(
            model_name='profile',
            name='contact_info',
            field=models.JSONField(blank=True, default=dict, help_text='Contact & payment info'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='role',
            field=models.CharField(choices=[('admin', 'Admin'), ('editor', 'Editor'), ('analyst', 'Analyst'), ('client', 'Client'), ('viewer', 'Viewer'), ('user', 'User')], default='user', max_length=20),
        ),

        # Add new fields to Story
        migrations.AddField(
            model_name='story',
            name='content_file',
            field=models.FileField(blank=True, help_text='Gambar/video upload', null=True, upload_to='story_content/'),
        ),
        migrations.AddField(
            model_name='story',
            name='content_image',
            field=models.ImageField(blank=True, help_text='Gambar story', null=True, upload_to='story_images/'),
        ),
        migrations.AddField(
            model_name='story',
            name='swipe_up',
            field=models.IntegerField(default=0, help_text='Swipe Up count', validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AddField(
            model_name='story',
            name='reaction_rate',
            field=models.FloatField(default=0.0, help_text='Reaction rate percentage', validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(100.0)]),
        ),
        migrations.AddField(
            model_name='story',
            name='saves',
            field=models.IntegerField(default=0, help_text='Save count', validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AddField(
            model_name='story',
            name='shares',
            field=models.IntegerField(default=0, help_text='Share count', validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AddField(
            model_name='story',
            name='replays',
            field=models.IntegerField(default=0, help_text='Replay count', validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AddField(
            model_name='story',
            name='performance_rating',
            field=models.FloatField(default=0.0, help_text='Auto calculated performance rating', validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(10.0)]),
        ),
        migrations.AddField(
            model_name='story',
            name='campaign',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='stories', to='kpi_management.campaign'),
        ),
        migrations.AddField(
            model_name='story',
            name='collab_brand',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='stories', to='kpi_management.collabbrand'),
        ),
        migrations.AlterField(
            model_name='story',
            name='link_clicks',
            field=models.IntegerField(default=0, help_text='CTR link / Swipe Up', validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='story',
            name='platform',
            field=models.CharField(choices=[('instagram', 'Instagram'), ('facebook', 'Facebook'), ('tiktok', 'TikTok'), ('twitter', 'Twitter'), ('youtube', 'YouTube Short'), ('youtube_long', 'YouTube')], max_length=20),
        ),
        migrations.AlterField(
            model_name='story',
            name='status',
            field=models.CharField(choices=[('draft', 'Draft'), ('scheduled', 'Scheduled'), ('live', 'Live'), ('published', 'Published'), ('archived', 'Archived')], default='draft', max_length=20),
        ),
        migrations.AlterField(
            model_name='story',
            name='story_date',
            field=models.DateField(help_text='Tanggal Publish'),
        ),

        # Add new fields to DailyFeedReels
        migrations.AddField(
            model_name='dailyfeedreels',
            name='format_type',
            field=models.CharField(choices=[('image', 'Image'), ('video', 'Video')], default='image', help_text='Format (image/video)', max_length=10),
        ),
        migrations.AddField(
            model_name='dailyfeedreels',
            name='content_file',
            field=models.FileField(blank=True, help_text='Upload gambar/video', null=True, upload_to='feed_reels_content/'),
        ),
        migrations.AddField(
            model_name='dailyfeedreels',
            name='hashtags',
            field=models.CharField(blank=True, help_text='Comma-separated hashtags', max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='dailyfeedreels',
            name='saves',
            field=models.IntegerField(default=0, help_text='Saves count', validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AddField(
            model_name='dailyfeedreels',
            name='target_post_date',
            field=models.DateTimeField(default=django.utils.timezone.now, help_text='Target post date untuk scheduling'),
        ),
        migrations.AddField(
            model_name='dailyfeedreels',
            name='campaign',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='feeds', to='kpi_management.campaign'),
        ),
        migrations.AddField(
            model_name='dailyfeedreels',
            name='collab_brand',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='feeds', to='kpi_management.collabbrand'),
        ),
        migrations.AlterField(
            model_name='dailyfeedreels',
            name='publish_date',
            field=models.DateTimeField(blank=True, help_text='Tanggal actual publish', null=True),
        ),
        migrations.AlterField(
            model_name='dailyfeedreels',
            name='status',
            field=models.CharField(choices=[('draft', 'Draft'), ('scheduled', 'Scheduled'), ('published', 'Published'), ('under_review', 'Under Review'), ('archived', 'Archived')], default='draft', max_length=20),
        ),
        migrations.AlterField(
            model_name='dailyfeedreels',
            name='tags',
            field=models.CharField(blank=True, help_text='Comma-separated tags/hashtag', max_length=500, null=True),
        ),
        migrations.AlterModelOptions(
            name='dailyfeedreels',
            options={'ordering': ['-target_post_date', '-created_at'], 'verbose_name': 'Daily Feed/Reels', 'verbose_name_plural': 'Daily Feeds/Reels'},
        ),

        # Create FeedReelsHistory model
        migrations.CreateModel(
            name='FeedReelsHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('update_type', models.CharField(help_text='Type of update (insight, status, content, etc)', max_length=50)),
                ('old_value', models.TextField(blank=True, null=True)),
                ('new_value', models.TextField(blank=True, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('feed_reels', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='history_logs', to='kpi_management.dailyfeedreels')),
                ('updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Feed/Reels History',
                'verbose_name_plural': 'Feed/Reels Histories',
                'ordering': ['-created_at'],
            },
        ),

        # Add new fields to FYPPostValue
        migrations.AddField(
            model_name='fyppostvalue',
            name='reach',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AddField(
            model_name='fyppostvalue',
            name='engagement_rate',
            field=models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(100.0)]),
        ),
        migrations.AddField(
            model_name='fyppostvalue',
            name='view_milestone',
            field=models.CharField(blank=True, choices=[('50k', '50K'), ('100k', '100K'), ('500k', '500K'), ('1m', '1M'), ('5m', '5M'), ('10m', '10M+')], help_text='View milestone (50K, 100K, 1M, etc)', max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='fyppostvalue',
            name='hashtags_used',
            field=models.CharField(blank=True, help_text='Hashtag yang digunakan', max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='fyppostvalue',
            name='audio_trending',
            field=models.CharField(blank=True, help_text='Audio trending yang digunakan', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='fyppostvalue',
            name='niche',
            field=models.CharField(blank=True, help_text='Niche konten', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='fyppostvalue',
            name='timing',
            field=models.CharField(blank=True, help_text='Timing posting (best practice)', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='fyppostvalue',
            name='best_practice_note',
            field=models.TextField(blank=True, help_text='Best practice note dari konten ini', null=True),
        ),
        migrations.AlterField(
            model_name='fyppostvalue',
            name='post_date',
            field=models.DateField(help_text='Tanggal viral'),
        ),
        migrations.AlterField(
            model_name='fyppostvalue',
            name='post_title',
            field=models.CharField(help_text='Judul konten viral', max_length=200),
        ),
        migrations.AlterField(
            model_name='fyppostvalue',
            name='viral_score',
            field=models.FloatField(default=0.0, help_text='Auto calculated viral score', validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(100.0)]),
        ),

        # Add new fields to Campaign
        migrations.AddField(
            model_name='campaign',
            name='objective',
            field=models.CharField(choices=[('brand_awareness', 'Brand Awareness'), ('lead', 'Lead Generation'), ('engagement', 'Engagement'), ('promo', 'Promo/Sale'), ('season', 'Seasonal Campaign'), ('product_launch', 'Product Launch'), ('other', 'Other')], default='brand_awareness', help_text='Objective (Brand Awareness / Lead / Engagement / Promo / Season)', max_length=50),
        ),
        migrations.AddField(
            model_name='campaign',
            name='owner',
            field=models.ForeignKey(blank=True, help_text='Owner / PIC Campaign', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='campaigns_owned', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='status',
            field=models.CharField(choices=[('draft', 'Draft'), ('planning', 'Planning'), ('active', 'Active'), ('paused', 'Paused'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='draft', max_length=20),
        ),

        # Add new fields to CollabBrand
        migrations.AddField(
            model_name='collabbrand',
            name='contract_document',
            field=models.FileField(blank=True, help_text='Document upload kontrak', null=True, upload_to='collab_contracts/'),
        ),
        migrations.AddField(
            model_name='collabbrand',
            name='payment_reminder_date',
            field=models.DateField(blank=True, help_text='Tanggal reminder pembayaran', null=True),
        ),
        migrations.AddField(
            model_name='collabbrand',
            name='renewal_reminder_date',
            field=models.DateField(blank=True, help_text='Tanggal reminder renewal collab', null=True),
        ),
        migrations.AddField(
            model_name='collabbrand',
            name='last_reminder_sent',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='collabbrand',
            name='deliverables_list',
            field=models.JSONField(blank=True, default=list, help_text='Deliverables dalam format JSON'),
        ),
        migrations.AddField(
            model_name='collabbrand',
            name='campaign',
            field=models.ForeignKey(blank=True, help_text='Campaign turunannya', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='collabs', to='kpi_management.campaign'),
        ),
        migrations.AlterField(
            model_name='collabbrand',
            name='end_date',
            field=models.DateField(blank=True, help_text='Durasi kontrak', null=True),
        ),
        migrations.AlterField(
            model_name='collabbrand',
            name='payment_status',
            field=models.CharField(choices=[('pending', 'Pending'), ('partial', 'Partial'), ('paid', 'Paid'), ('overdue', 'Overdue')], default='pending', max_length=50),
        ),
        migrations.AlterField(
            model_name='collabbrand',
            name='status',
            field=models.CharField(choices=[('negotiating', 'Negotiating'), ('active', 'Active'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='negotiating', max_length=20),
        ),

        # Create DashboardSettings model
        migrations.CreateModel(
            name='DashboardSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(blank=True, help_text='Role yang bisa lihat dashboard', max_length=50, null=True)),
                ('show_total_campaign', models.BooleanField(default=True)),
                ('show_total_story', models.BooleanField(default=True)),
                ('show_total_fyp', models.BooleanField(default=True)),
                ('show_engagement_avg', models.BooleanField(default=True)),
                ('show_revenue_kpi', models.BooleanField(default=True)),
                ('show_user_activity', models.BooleanField(default=True)),
                ('show_notifications', models.BooleanField(default=True)),
                ('widget_layout', models.JSONField(blank=True, default=dict, help_text='Layout widget configuration')),
                ('can_view_dashboard', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dashboard_settings', to=settings.AUTH_USER_MODEL)),
                ('allowed_users', models.ManyToManyField(blank=True, help_text='Siapa yang bisa lihat dashboard', related_name='allowed_dashboards', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Dashboard Settings',
                'verbose_name_plural': 'Dashboard Settings',
            },
        ),

        # Create Report model
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('report_type', models.CharField(choices=[('campaign_summary', 'Campaign Summary'), ('posting_insight', 'Posting Insight Report'), ('collaboration', 'Collaboration Report'), ('viral_fyp', 'Viral FYP Analysis'), ('user_activity', 'Log Aktivitas User'), ('comprehensive', 'Comprehensive Report')], max_length=50)),
                ('period', models.CharField(choices=[('daily', 'Daily'), ('weekly', 'Weekly'), ('monthly', 'Monthly'), ('quarterly', 'Quarterly'), ('yearly', 'Yearly'), ('custom', 'Custom')], default='monthly', max_length=20)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('performance_type', models.CharField(blank=True, help_text='Filter per performance type', max_length=100, null=True)),
                ('report_data', models.JSONField(blank=True, default=dict, help_text='Report data dalam format JSON')),
                ('charts_data', models.JSONField(blank=True, default=dict, help_text='Data untuk grafik insight per timeline')),
                ('pdf_file', models.FileField(blank=True, null=True, upload_to='reports/pdf/')),
                ('excel_file', models.FileField(blank=True, null=True, upload_to='reports/excel/')),
                ('auto_generate', models.BooleanField(default=False, help_text='Auto generation monthly report')),
                ('last_generated', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('brand_filter', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reports', to='kpi_management.collabbrand')),
                ('campaign_filter', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reports', to='kpi_management.campaign')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reports_created', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Report',
                'verbose_name_plural': 'Reports',
                'ordering': ['-created_at'],
            },
        ),

        # Create AuditLog model
        migrations.CreateModel(
            name='AuditLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(choices=[('create', 'Create'), ('update', 'Update'), ('delete', 'Delete'), ('login', 'Login'), ('logout', 'Logout'), ('approve', 'Approve'), ('reject', 'Reject'), ('view', 'View'), ('export', 'Export'), ('other', 'Other')], max_length=20)),
                ('target_type', models.CharField(blank=True, help_text='Model name (Campaign, Story, User, etc)', max_length=100, null=True)),
                ('target_id', models.IntegerField(blank=True, help_text='ID dari target object', null=True)),
                ('target_name', models.CharField(blank=True, help_text='Nama target (Campaign X, Story Y, User Z)', max_length=200, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('old_data', models.JSONField(blank=True, default=dict, help_text='Data sebelum perubahan')),
                ('new_data', models.JSONField(blank=True, default=dict, help_text='Data setelah perubahan')),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True)),
                ('user_agent', models.TextField(blank=True, help_text='OS/Browser agent', null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='audit_logs', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Audit Log',
                'verbose_name_plural': 'Audit Logs',
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddIndex(
            model_name='auditlog',
            index=models.Index(fields=['-created_at'], name='kpi_manage_created_idx'),
        ),
        migrations.AddIndex(
            model_name='auditlog',
            index=models.Index(fields=['user', '-created_at'], name='kpi_manage_user_cr_idx'),
        ),
        migrations.AddIndex(
            model_name='auditlog',
            index=models.Index(fields=['action', '-created_at'], name='kpi_manage_action_idx'),
        ),
        migrations.AddIndex(
            model_name='fyppostvalue',
            index=models.Index(fields=['-viral_score'], name='kpi_manage_viral_s_idx'),
        ),
    ]


