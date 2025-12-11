# Generated migration to add Company model and company fields

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kpi_management', '0003_add_socialmediaaccount'),
    ]

    operations = [
        # Create Company model
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Nama perusahaan', max_length=200)),
                ('company_type', models.CharField(choices=[('pusat', 'Pusat'), ('cabang', 'Cabang')], default='pusat', help_text='Tipe: Pusat atau Cabang', max_length=20)),
                ('code', models.CharField(help_text='Kode perusahaan (unique)', max_length=50, unique=True)),
                ('address', models.TextField(blank=True, help_text='Alamat perusahaan', null=True)),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('is_active', models.BooleanField(default=True, help_text='Status aktif')),
                ('notes', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('parent_company', models.ForeignKey(blank=True, help_text='Perusahaan induk (untuk cabang)', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='branches', to='kpi_management.company')),
            ],
            options={
                'verbose_name': 'Company',
                'verbose_name_plural': 'Companies',
                'ordering': ['company_type', 'name'],
            },
        ),
        migrations.AddIndex(
            model_name='company',
            index=models.Index(fields=['company_type', 'is_active'], name='kpi_manage_company_idx'),
        ),
        migrations.AddIndex(
            model_name='company',
            index=models.Index(fields=['code'], name='kpi_manage_code_idx'),
        ),

        # Add company field to Story
        migrations.AddField(
            model_name='story',
            name='company',
            field=models.ForeignKey(blank=True, help_text='Perusahaan/Cabang', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='stories', to='kpi_management.company'),
        ),

        # Add company field to DailyFeedReels
        migrations.AddField(
            model_name='dailyfeedreels',
            name='company',
            field=models.ForeignKey(blank=True, help_text='Perusahaan/Cabang', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='feeds_reels', to='kpi_management.company'),
        ),

        # Add company field to Campaign
        migrations.AddField(
            model_name='campaign',
            name='company',
            field=models.ForeignKey(blank=True, help_text='Perusahaan/Cabang', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='campaigns', to='kpi_management.company'),
        ),

        # Add company field to SocialMediaAccount
        migrations.AddField(
            model_name='socialmediaaccount',
            name='company',
            field=models.ForeignKey(blank=True, help_text='Perusahaan/Cabang', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='social_media_accounts', to='kpi_management.company'),
        ),
    ]



