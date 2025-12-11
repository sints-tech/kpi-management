# KPI Management System - Dokumentasi

## Overview
Sistem KPI Management untuk tim kreatif yang dibangun menggunakan Django dengan template Sneat Bootstrap. Sistem ini memungkinkan pengelolaan, pemantauan, dan analisis performance/insight pada setiap akun sosial media.

## Fitur Utama

### 1. CRUD Story
- Mengelola Insight Story di sosial media
- Platform: Instagram, Facebook, TikTok, Twitter, YouTube
- Tracking: Views, Impressions, Reach, Engagement Rate, Link Clicks
- Status: Draft, Published, Archived

### 2. CRUD Daily Feed/Reels
- Management konten harian (Feed/Reels)
- Tracking: Likes, Comments, Shares, Views, Engagement Rate
- Support untuk multiple platform
- Status: Draft, Scheduled, Published, Archived

### 3. CRUD FYP Post Value
- Management nilai FYP Post
- Tracking: FYP Views, Total Views, FYP Percentage, Viral Score
- Engagement Value dan Estimated Reach

### 4. CRUD Campaign
- Management campaign marketing
- Budget tracking (Budget, Spent, Remaining)
- Target platforms dan audience
- KPI tracking (target dan achieved)

### 5. CRUD Collab Brand
- Management kolaborasi brand
- Contact management
- Contract value dan payment status
- Deliverables tracking

### 6. CRUD User Management
- Management user (Admin only)
- Role assignment (Admin/User)
- User activation/deactivation

### 7. CRUD Profile
- Profile management
- Avatar upload
- Bio, phone, address
- Role management

## Role System

### Admin (Super User)
- Akses penuh ke semua fitur
- Dapat mengelola user
- Dapat mengubah role user
- Akses ke semua data

### User
- Akses terbatas
- Dapat melihat dan mengelola data sendiri
- Tidak dapat mengakses User Management
- Dapat mengedit profile sendiri

## Instalasi

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Buat migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

3. Buat superuser (Admin):
```bash
python manage.py createsuperuser
```

4. Jalankan server:
```bash
python manage.py runserver
```

## Setup Admin User

Setelah membuat superuser, login ke admin panel dan:
1. Buka User Management di menu KPI Management
2. Edit user yang baru dibuat
3. Buat Profile untuk user tersebut dengan role 'admin'

Atau melalui Django shell:
```python
from django.contrib.auth.models import User
from apps.kpi_management.models import Profile

user = User.objects.get(username='admin')
Profile.objects.create(user=user, role='admin')
```

## Struktur URL

- `/kpi/stories/` - Story Management
- `/kpi/daily-feeds/` - Daily Feed/Reels Management
- `/kpi/fyp-posts/` - FYP Post Value Management
- `/kpi/campaigns/` - Campaign Management
- `/kpi/collab-brands/` - Collab Brand Management
- `/kpi/users/` - User Management (Admin only)
- `/kpi/profile/` - Profile Management

## Models

### Story
- title, platform, account_name
- views, impressions, reach, engagement_rate, link_clicks
- story_date, status, notes

### DailyFeedReels
- title, content_type, platform, account_name
- caption, content_url, thumbnail
- likes, comments, shares, views, engagement_rate
- publish_date, status, tags

### FYPPostValue
- post_title, platform, account_name, post_url
- fyp_views, total_views, fyp_percentage
- engagement_value, estimated_reach, viral_score
- post_date, notes

### Campaign
- name, description
- start_date, end_date
- budget, spent
- target_platforms, target_audience, goals
- status, kpi_target, kpi_achieved, notes

### CollabBrand
- brand_name, contact_person, email, phone, company
- collaboration_type
- start_date, end_date
- contract_value, payment_status
- deliverables, status, notes

### Profile
- user (OneToOne dengan User)
- role (admin/user)
- phone, address, bio, avatar

## Template Structure

Semua template menggunakan Sneat Bootstrap template dengan layout vertical:
- `story_list.html`, `story_form.html`, `story_detail.html`, `story_confirm_delete.html`
- `dailyfeedreels_list.html`, `dailyfeedreels_form.html`, `dailyfeedreels_detail.html`, `dailyfeedreels_confirm_delete.html`
- `fyppostvalue_list.html`, `fyppostvalue_form.html`, `fyppostvalue_detail.html`, `fyppostvalue_confirm_delete.html`
- `campaign_list.html`, `campaign_form.html`, `campaign_detail.html`, `campaign_confirm_delete.html`
- `collabbrand_list.html`, `collabbrand_form.html`, `collabbrand_detail.html`, `collabbrand_confirm_delete.html`
- `user_list.html`, `user_form.html`, `user_confirm_delete.html`
- `profile_form.html`, `profile_edit.html`

## Media Files

Media files (avatars, thumbnails) disimpan di:
- `MEDIA_ROOT = BASE_DIR / "media"`
- `MEDIA_URL = "/media/"`

Pastikan folder `media` dibuat di root project.

## Menu Navigation

Menu KPI Management telah ditambahkan ke vertical menu dengan submenu:
- Story
- Daily Feed/Reels
- FYP Post Value
- Campaign
- Collab Brand
- User Management (hanya untuk Admin)
- Profile

## Permission System

- Semua view memerlukan login (`LoginRequiredMixin`)
- User Management hanya untuk Admin (dicek di view)
- Context processor `kpi_context` menyediakan `is_admin` ke semua template

## Catatan Penting

1. Pastikan untuk membuat Profile untuk setiap user yang dibuat
2. Role 'admin' memberikan akses penuh ke sistem
3. Media files perlu dikonfigurasi dengan benar untuk upload avatar dan thumbnail
4. Semua form menggunakan Bootstrap classes dari Sneat template
5. Pagination tersedia untuk semua list view (20 items per page)

## Support

Untuk pertanyaan atau masalah, silakan hubungi tim development.

