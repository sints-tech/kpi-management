# Generated migration for SocialMediaAccount model

from django.conf import settings
from django.db import migrations, models
import django.core.validators
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kpi_management', '0002_add_new_fields'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SocialMediaAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('platform', models.CharField(choices=[('instagram', 'Instagram'), ('facebook', 'Facebook'), ('tiktok', 'TikTok'), ('youtube', 'YouTube'), ('twitter', 'Twitter/X'), ('linkedin', 'LinkedIn'), ('pinterest', 'Pinterest'), ('snapchat', 'Snapchat'), ('other', 'Lainnya')], help_text='Platform sosial media', max_length=50)),
                ('account_name', models.CharField(help_text='Nama akun / username', max_length=200)),
                ('account_id', models.CharField(blank=True, help_text='ID akun (jika tersedia)', max_length=200, null=True)),
                ('display_name', models.CharField(blank=True, help_text='Nama tampilan', max_length=200, null=True)),
                ('profile_url', models.URLField(blank=True, help_text='URL profil akun', null=True)),
                ('status', models.CharField(choices=[('active', 'Aktif'), ('inactive', 'Tidak Aktif'), ('suspended', 'Ditangguhkan'), ('deleted', 'Dihapus')], default='active', max_length=20)),
                ('is_verified', models.BooleanField(default=False, help_text='Apakah akun terverifikasi?')),
                ('is_business_account', models.BooleanField(default=False, help_text='Apakah akun bisnis?')),
                ('followers_count', models.IntegerField(default=0, help_text='Jumlah followers')),
                ('following_count', models.IntegerField(default=0, help_text='Jumlah following')),
                ('posts_count', models.IntegerField(default=0, help_text='Jumlah postingan')),
                ('engagement_rate', models.FloatField(default=0.0, help_text='Engagement rate (%)', validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(100.0)])),
                ('access_token', models.TextField(blank=True, help_text='Access token (disimpan terenkripsi)', null=True)),
                ('refresh_token', models.TextField(blank=True, help_text='Refresh token (disimpan terenkripsi)', null=True)),
                ('api_key', models.CharField(blank=True, help_text='API Key', max_length=500, null=True)),
                ('api_secret', models.CharField(blank=True, help_text='API Secret', max_length=500, null=True)),
                ('notes', models.TextField(blank=True, help_text='Catatan tambahan', null=True)),
                ('tags', models.JSONField(blank=True, default=list, help_text='Tag untuk kategorisasi')),
                ('connected_at', models.DateTimeField(blank=True, help_text='Tanggal terhubung', null=True)),
                ('last_synced_at', models.DateTimeField(blank=True, help_text='Terakhir sinkronisasi data', null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='social_accounts_created', to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(blank=True, help_text='Pemilik akun', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='social_media_accounts', to=settings.AUTH_USER_MODEL)),
                ('profile', models.ForeignKey(blank=True, help_text='Profil terkait', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='social_media_accounts', to='kpi_management.profile')),
            ],
            options={
                'verbose_name': 'Social Media Account',
                'verbose_name_plural': 'Social Media Accounts',
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddIndex(
            model_name='socialmediaaccount',
            index=models.Index(fields=['platform', 'status'], name='kpi_manage_platform_idx'),
        ),
        migrations.AddIndex(
            model_name='socialmediaaccount',
            index=models.Index(fields=['owner', '-created_at'], name='kpi_manage_owner_cr_idx'),
        ),
        migrations.AddIndex(
            model_name='socialmediaaccount',
            index=models.Index(fields=['account_name'], name='kpi_manage_account_idx'),
        ),
    ]

