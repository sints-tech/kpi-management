# 📚 PANDUAN PEMBELAJARAN LENGKAP: Sneat Dashboard Free Django

> **Versi Lengkap & Detail** - Panduan komprehensif untuk memahami Django, Python, dan Sneat Dashboard secara menyeluruh

## 📑 Daftar Isi
1. [Pengenalan](#1-pengenalan)
2. [Konsep Dasar Django & Python](#2-konsep-dasar-django--python)
3. [Memahami Struktur Proyek](#3-memahami-struktur-proyek)
4. [Penjelasan File & Folder Secara Detail](#4-penjelasan-file--folder-secara-detail)
5. [Command-line Tools Django](#5-command-line-tools-django)
6. [Template Tags & Context - Penjelasan Lengkap](#6-template-tags--context---penjelasan-lengkap)
7. [Membuat CRUD dengan Komponen Sneat](#7-membuat-crud-dengan-komponen-sneat)
8. [Tutorial Step-by-Step Lengkap](#8-tutorial-step-by-step-lengkap)
9. [Tips & Best Practices](#9-tips--best-practices)

---

## 1. Pengenalan

### 1.1 Apa itu Sneat Dashboard?

**Sneat Dashboard** adalah admin template berbasis **Bootstrap 5** yang menyediakan:

- ✅ **UI/UX Modern & Responsif**: Desain yang menarik dan mudah digunakan
- ✅ **Komponen Siap Pakai**: Cards, tables, forms, charts, dll
- ✅ **Dark/Light Theme Support**: Dukungan tema gelap dan terang
- ✅ **Layout Fleksibel**: Vertical dan horizontal menu
- ✅ **Fully Responsive**: Tampil sempurna di desktop, tablet, dan mobile

**Website Resmi**: https://themeselection.com/item/sneat-dashboard-free-django/

### 1.2 Apa itu Django?

**Django** adalah web framework Python yang:

- 🎯 **Mengikuti Pola MVT**: Model-View-Template untuk struktur yang rapi
- 🗄️ **ORM Built-in**: Object-Relational Mapping untuk database
- 🔐 **Authentication & Authorization**: Sistem keamanan built-in
- ⚡ **Admin Panel Otomatis**: Panel admin yang powerful
- 📦 **Batteries Included**: Banyak fitur siap pakai

**Dokumentasi**: https://docs.djangoproject.com/

### 1.3 Apa itu Python?

**Python** adalah bahasa pemrograman yang:

- 📝 **Sintaks Mudah Dibaca**: Kode yang clean dan readable
- 🎨 **Object-Oriented**: Mendukung OOP
- 📚 **Ekosistem Luas**: Library yang banyak dan powerful
- 🌐 **Multi-purpose**: Web, data science, AI, automation, dll

---

## 2. Konsep Dasar Django & Python

### 2.1 Arsitektur Django (MVT Pattern)

Django menggunakan pola **MVT (Model-View-Template)**:

```
┌─────────────────────────────────────────┐
│           BROWSER (User)                │
│      Mengirim HTTP Request              │
└──────────────────┬──────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│         URL ROUTING (urls.py)            │
│  Menentukan view mana yang dipanggil     │
└──────────────────┬──────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│         VIEW (views.py)                   │
│  ┌──────────────────────────────────┐   │
│  │  Business Logic                  │   │
│  │  - Ambil data dari Model         │   │
│  │  - Proses form                   │   │
│  │  - Validasi data                 │   │
│  │  - Return response                │   │
│  └──────────────────────────────────┘   │
└──────┬───────────────────┬────────────────┘
       │                   │
       ▼                   ▼
┌──────────────┐    ┌──────────────────┐
│    MODEL     │    │    TEMPLATE      │
│ (models.py)  │    │   (.html files)  │
│              │    │                  │
│ Database     │    │  HTML + Django   │
│ Structure    │    │  Template Tags   │
└──────┬───────┘    └──────────────────┘
       │
       ▼
┌─────────────────────────────────────────┐
│      DATABASE (SQLite/PostgreSQL)        │
│  Menyimpan data secara persisten         │
└─────────────────────────────────────────┘
```

**Penjelasan Detail:**

1. **Model (models.py)**: 
   - Mendefinisikan struktur database
   - Setiap class Model = 1 tabel di database
   - Field-field = kolom di tabel

2. **View (views.py)**:
   - Logic bisnis aplikasi
   - Memproses request dari user
   - Mengambil data dari Model
   - Mengirim data ke Template

3. **Template (.html)**:
   - File HTML yang ditampilkan ke user
   - Menggunakan Django Template Language (DTL)
   - Menerima data dari View

4. **URL (urls.py)**:
   - Routing: menghubungkan URL ke View
   - Pattern matching untuk menentukan view mana yang dipanggil

### 2.2 Konsep Python Dasar untuk Django

#### Variabel & Tipe Data

```python
# String (Text)
nama = "Django"
versi = "5.2"

# Integer (Bilangan Bulat)
umur = 5
jumlah = 100

# Float (Bilangan Desimal)
harga = 99.99
rating = 4.5

# Boolean (True/False)
is_active = True
is_published = False

# List (Array)
daftar_menu = ["Dashboard", "Users", "Settings"]
angka = [1, 2, 3, 4, 5]

# Dictionary (Object/Key-Value)
data_user = {
    "nama": "John Doe",
    "email": "john@example.com",
    "role": "admin"
}

# None (Kosong)
data = None
```

#### Class & Object (OOP)

```python
# Definisi Class
class Story:
    # Constructor (dipanggil saat membuat object)
    def __init__(self, title, platform):
        self.title = title
        self.platform = platform
        self.views = 0
    
    # Method (function dalam class)
    def increment_views(self):
        self.views += 1
    
    def get_info(self):
        return f"{self.title} - {self.platform} ({self.views} views)"

# Membuat Object (Instance)
story1 = Story("My First Story", "Instagram")
story1.increment_views()
print(story1.get_info())  # Output: My First Story - Instagram (1 views)

story2 = Story("Second Story", "Facebook")
print(story2.get_info())  # Output: Second Story - Facebook (0 views)
```

#### Function

```python
# Function sederhana
def tambah(a, b):
    return a + b

hasil = tambah(5, 3)  # hasil = 8

# Function dengan default parameter
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"

print(greet("John"))  # Output: Hello, John!
print(greet("John", "Hi"))  # Output: Hi, John!

# Function dengan multiple return
def bagi(a, b):
    if b == 0:
        return None, "Error: Pembagian dengan nol"
    return a / b, "Success"

hasil, pesan = bagi(10, 2)  # hasil = 5.0, pesan = "Success"
```

#### Import & Module

```python
# Import module standar
import os
from datetime import datetime

# Import dari Django
from django.db import models
from django.shortcuts import render

# Import dari aplikasi sendiri
from .models import Story
from .forms import StoryForm
```

---

## 3. Memahami Struktur Proyek

### 3.1 Struktur Folder Utama

```
sneat-bootstrap-html-django-admin-template-free/
│
├── 📁 config/                    # Konfigurasi utama Django
│   ├── settings.py               # ⭐ Pengaturan aplikasi (PENTING!)
│   ├── urls.py                   # ⭐ URL routing utama (PENTING!)
│   ├── wsgi.py                   # WSGI config (untuk deployment)
│   ├── asgi.py                   # ASGI config (untuk async)
│   ├── context_processors.py     # Context processors (menambahkan variabel ke semua template)
│   └── template.py               # Template variables (theme config)
│
├── 📁 apps/                      # Aplikasi Django (modul-modul)
│   ├── authentication/          # Login, Register, Logout
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── templates/
│   │
│   ├── dashboards/              # Halaman dashboard
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── templates/
│   │
│   ├── kpi_management/          # ⭐ CRUD KPI Management (CONTOH LENGKAP)
│   │   ├── models.py           # Database structure
│   │   ├── views.py            # Business logic
│   │   ├── forms.py            # Form handling
│   │   ├── urls.py             # URL routing
│   │   ├── admin.py            # Admin panel config
│   │   └── templates/          # HTML templates
│   │       └── kpi_management/
│   │           ├── story_list.html
│   │           ├── story_form.html
│   │           └── ...
│   │
│   ├── layouts/                # Layout pages
│   ├── pages/                  # Static pages
│   ├── cards/                  # Card components
│   ├── ui/                     # UI components
│   └── ...                     # App lainnya
│
├── 📁 templates/                # Template global
│   └── layout/                 # Base layout templates
│       ├── master.html         # ⭐ Template utama (base template)
│       ├── layout_vertical.html # Layout vertical menu
│       ├── layout_blank.html   # Layout tanpa menu
│       └── partials/           # Komponen partial (reusable)
│           ├── header/
│           ├── navbar/
│           ├── menu/
│           │   └── vertical/
│           │       └── vertical_menu.html
│           └── footer/
│
├── 📁 web_project/             # Helper functions untuk template
│   ├── __init__.py            # ⭐ TemplateLayout class (PENTING!)
│   ├── template_helpers/
│   │   └── theme.py          # TemplateHelper class
│   └── template_tags/
│       └── theme.py           # Custom template tags
│
├── 📁 src/                     # Frontend assets (source files)
│   ├── assets/                # CSS, JS, Images
│   │   ├── css/              # Stylesheet
│   │   ├── js/               # JavaScript
│   │   ├── img/              # Images
│   │   └── vendor/           # Third-party libraries
│   └── scss/                 # SCSS source files
│
├── 📁 static/                  # Static files (collected, untuk production)
├── 📁 media/                   # User uploaded files (images, documents)
│
├── 📄 manage.py                # ⭐ Django command-line tool (PENTING!)
├── 📄 requirements.txt        # Python dependencies
└── 📄 db.sqlite3              # Database SQLite (development)
```

### 3.2 Penjelasan Folder Penting

#### `config/` - Konfigurasi Utama
- **settings.py**: Semua pengaturan aplikasi Django
- **urls.py**: URL routing utama (menghubungkan URL ke view)
- **context_processors.py**: Menambahkan variabel ke semua template

#### `apps/` - Aplikasi Django
- Setiap folder = 1 aplikasi Django
- Setiap aplikasi memiliki struktur sendiri (models, views, urls, templates)
- **kpi_management/**: Contoh CRUD lengkap yang bisa dipelajari

#### `templates/` - Template HTML
- **layout/**: Base templates yang digunakan semua halaman
- **master.html**: Template utama yang di-extend oleh semua halaman
- **partials/**: Komponen yang bisa di-include di template lain

#### `web_project/` - Helper Functions
- **TemplateLayout**: Class untuk menginisialisasi layout
- **TemplateHelper**: Helper untuk mapping context variables

---

## 4. Penjelasan File & Folder Secara Detail

### 4.1 File Konfigurasi

#### `config/settings.py` - Pengaturan Utama

**Fungsi**: File konfigurasi utama Django yang mengatur semua aspek aplikasi.

**Bagian Penting:**

```python
# ============================================
# 1. DATABASE CONFIGURATION
# ============================================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Database engine
        'NAME': BASE_DIR / 'db.sqlite3',         # Lokasi database file
    }
}

# Penjelasan:
# - ENGINE: Jenis database (sqlite3 untuk development, postgresql untuk production)
# - NAME: Lokasi file database
# - Untuk production, bisa tambahkan USER, PASSWORD, HOST, PORT

# ============================================
# 2. INSTALLED APPS
# ============================================
INSTALLED_APPS = [
    'django.contrib.admin',        # Django admin panel
    'django.contrib.auth',        # Authentication system
    'django.contrib.contenttypes', # Content types framework
    'django.contrib.sessions',     # Session framework
    'django.contrib.messages',    # Messaging framework
    'django.contrib.staticfiles', # Static files handling
    
    # Aplikasi lokal (custom)
    'apps.dashboards',            # Dashboard app
    'apps.kpi_management',        # KPI Management app
    'apps.authentication',        # Authentication app
    # ... apps lainnya
]

# Penjelasan:
# - Semua aplikasi yang digunakan harus terdaftar di sini
# - Django akan mencari models, views, templates di aplikasi yang terdaftar
# - Urutan penting untuk beberapa kasus (misalnya admin harus sebelum custom apps)

# ============================================
# 3. MIDDLEWARE
# ============================================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Serve static files
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',   # CSRF protection
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Penjelasan:
# - Middleware adalah komponen yang memproses request sebelum sampai ke view
# - Urutan sangat penting!
# - CSRF middleware: Melindungi dari CSRF attack
# - Authentication middleware: Menambahkan user ke request

# ============================================
# 4. TEMPLATES CONFIGURATION
# ============================================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Lokasi template global
        'APP_DIRS': True,  # Cari template di setiap app/templates/
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',  # Menambahkan 'user' ke context
                'django.contrib.messages.context_processors.messages',
                'config.context_processors.my_setting',         # Custom context processor
                'config.context_processors.environment',
                'config.context_processors.kpi_context',       # Menambahkan 'is_admin' ke context
            ],
            'libraries': {
                'theme': 'web_project.template_tags.theme',  # Custom template tags
            },
            'builtins': [
                'django.templatetags.static',
                'web_project.template_tags.theme',
            ],
        },
    },
]

# Penjelasan:
# - DIRS: Lokasi template global (di luar apps)
# - APP_DIRS: Django akan mencari template di apps/*/templates/
# - context_processors: Menambahkan variabel ke semua template
#   - auth: Menambahkan 'user' ke context
#   - messages: Menambahkan 'messages' untuk flash messages
#   - kpi_context: Custom processor yang menambahkan 'is_admin'

# ============================================
# 5. STATIC FILES (CSS, JS, Images)
# ============================================
STATIC_URL = '/static/'  # URL untuk mengakses static files
STATIC_ROOT = BASE_DIR / 'staticfiles'  # Lokasi collected static files (production)

STATICFILES_DIRS = [
    BASE_DIR / 'src' / 'assets',  # Lokasi static files source
]

# Penjelasan:
# - STATIC_URL: URL prefix untuk static files (http://domain.com/static/css/style.css)
# - STATIC_ROOT: Folder untuk mengumpulkan semua static files (setelah collectstatic)
# - STATICFILES_DIRS: Lokasi source static files yang akan di-collect

# ============================================
# 6. MEDIA FILES (User Uploads)
# ============================================
MEDIA_URL = '/media/'  # URL untuk mengakses media files
MEDIA_ROOT = BASE_DIR / 'media'  # Lokasi file yang di-upload user

# Penjelasan:
# - MEDIA_URL: URL prefix untuk media files
# - MEDIA_ROOT: Folder untuk menyimpan file upload (images, documents, dll)
# - Perlu konfigurasi di urls.py untuk serve media files di development

# ============================================
# 7. AUTHENTICATION
# ============================================
LOGIN_URL = '/auth/login/'  # URL untuk redirect jika belum login
LOGIN_REDIRECT_URL = '/'    # URL untuk redirect setelah login sukses

# ============================================
# 8. THEME CONFIGURATION
# ============================================
THEME_LAYOUT_DIR = THEME_LAYOUT_DIR  # Dari config/template.py
THEME_VARIABLES = THEME_VARIABLES    # Dari config/template.py
```

#### `config/urls.py` - URL Routing Utama

**Fungsi**: Menghubungkan URL ke view (routing).

```python
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Django Admin Panel
    path('admin/', admin.site.urls),
    
    # Dashboard URLs (root URL)
    path('', include('apps.dashboards.urls')),
    
    # KPI Management URLs (prefix: /kpi/)
    path('kpi/', include('apps.kpi_management.urls')),
    
    # Authentication URLs (prefix: /auth/)
    path('auth/', include('apps.authentication.urls')),
    
    # ... routing lainnya
]

# Serve media files in development (hanya untuk DEBUG=True)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

**Penjelasan:**
- `path('admin/', ...)`: URL `/admin/` akan menampilkan Django admin panel
- `path('', include(...))`: URL root `/` akan include URLs dari `apps.dashboards.urls`
- `path('kpi/', include(...))`: URL `/kpi/...` akan include URLs dari `apps.kpi_management.urls`
- `include()`: Meng-include URL patterns dari aplikasi lain

**Contoh Flow:**
```
User mengakses: http://127.0.0.1:8000/kpi/stories/
    │
    ▼
config/urls.py: path('kpi/', include('apps.kpi_management.urls'))
    │
    ▼
apps/kpi_management/urls.py: path('stories/', views.StoryListView.as_view())
    │
    ▼
apps/kpi_management/views.py: StoryListView
    │
    ▼
Template: story_list.html
```

### 4.2 File Model (`models.py`)

**Fungsi**: Mendefinisikan struktur database (tabel dan kolom).

**Contoh Lengkap Model Story:**

```python
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Story(models.Model):
    """
    Model untuk mengelola Insight Story di sosial media
    
    Setiap field = kolom di database
    Setiap instance = baris di database
    """
    
    # ============================================
    # CHOICES (Pilihan untuk field tertentu)
    # ============================================
    PLATFORM_CHOICES = [
        ('instagram', 'Instagram'),
        ('facebook', 'Facebook'),
        ('tiktok', 'TikTok'),
        ('twitter', 'Twitter'),
        ('youtube', 'YouTube Short'),
    ]
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]
    
    # ============================================
    # FIELD DEFINITIONS
    # ============================================
    
    # CharField: Text pendek (dengan max_length)
    title = models.CharField(
        max_length=200,
        help_text="Judul story"
    )
    
    # CharField dengan choices: Dropdown dengan pilihan
    platform = models.CharField(
        max_length=20,
        choices=PLATFORM_CHOICES,
        help_text="Platform sosial media"
    )
    
    account_name = models.CharField(max_length=100)
    
    # IntegerField: Bilangan bulat
    views = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],  # Validasi: minimal 0
        help_text="Jumlah views"
    )
    
    # FloatField: Bilangan desimal
    engagement_rate = models.FloatField(
        default=0.0,
        validators=[
            MinValueValidator(0.0),
            MaxValueValidator(100.0)
        ],
        help_text="Engagement rate dalam persen"
    )
    
    # DateField: Tanggal saja
    story_date = models.DateField(
        help_text="Tanggal publish story"
    )
    
    # DateTimeField: Tanggal & waktu
    created_at = models.DateTimeField(
        auto_now_add=True  # Otomatis diisi saat pertama dibuat
    )
    updated_at = models.DateTimeField(
        auto_now=True  # Otomatis diupdate setiap kali diubah
    )
    
    # ForeignKey: Relasi ke model lain (One-to-Many)
    # Satu User bisa punya banyak Story
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,  # Jika User dihapus, set NULL
        null=True,  # Boleh NULL
        related_name='stories_created'  # Nama untuk akses dari User: user.stories_created.all()
    )
    
    # ForeignKey ke Campaign (opsional)
    campaign = models.ForeignKey(
        'Campaign',  # String karena Campaign didefinisikan setelah Story
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='stories'
    )
    
    # TextField: Text panjang
    notes = models.TextField(
        blank=True,  # Boleh kosong
        null=True,   # Boleh NULL
        help_text="Catatan tambahan"
    )
    
    # FileField: Upload file
    content_file = models.FileField(
        upload_to='story_content/',  # Folder untuk menyimpan file
        blank=True,
        null=True,
        help_text="Gambar/video upload"
    )
    
    # ImageField: Upload gambar (sama seperti FileField tapi khusus gambar)
    content_image = models.ImageField(
        upload_to='story_images/',
        blank=True,
        null=True
    )
    
    # ============================================
    # META CLASS (Metadata untuk model)
    # ============================================
    class Meta:
        verbose_name = "Story"  # Nama singular di admin
        verbose_name_plural = "Stories"  # Nama plural di admin
        ordering = ['-story_date', '-created_at']  # Urutkan berdasarkan tanggal (terbaru dulu)
        indexes = [
            models.Index(fields=['platform', 'status']),  # Index untuk performa query
        ]
    
    # ============================================
    # METHODS
    # ============================================
    
    def __str__(self):
        """
        Representasi string dari object
        Digunakan di admin panel dan shell
        """
        return f"{self.title} - {self.platform}"
    
    def get_absolute_url(self):
        """
        URL untuk detail page (opsional, untuk redirect setelah create)
        """
        from django.urls import reverse
        return reverse('kpi_management:story-detail', kwargs={'pk': self.pk})
    
    def calculate_performance_rating(self):
        """
        Method custom untuk menghitung performance rating
        """
        if self.views == 0:
            self.performance_rating = 0.0
        else:
            # Formula custom
            rating = (self.engagement_rate * 0.4) + (self.reach / self.views * 100 * 0.3)
            self.performance_rating = min(10.0, max(0.0, rating / 10))
        
        self.save(update_fields=['performance_rating'])
        return self.performance_rating
```

**Jenis Field Django Lengkap:**

| Field Type | Python Type | Database Type | Keterangan |
|------------|-------------|---------------|------------|
| `CharField` | str | VARCHAR | Text pendek (wajib max_length) |
| `TextField` | str | TEXT | Text panjang |
| `IntegerField` | int | INTEGER | Bilangan bulat |
| `BigIntegerField` | int | BIGINT | Bilangan bulat besar |
| `FloatField` | float | REAL | Bilangan desimal |
| `DecimalField` | Decimal | NUMERIC | Bilangan desimal presisi |
| `BooleanField` | bool | BOOLEAN | True/False |
| `DateField` | date | DATE | Tanggal saja |
| `DateTimeField` | datetime | DATETIME | Tanggal & waktu |
| `TimeField` | time | TIME | Waktu saja |
| `EmailField` | str | VARCHAR | Email (validasi otomatis) |
| `URLField` | str | VARCHAR | URL (validasi otomatis) |
| `ForeignKey` | Model | INTEGER | Relasi One-to-Many |
| `ManyToManyField` | Model | Many-to-Many table | Relasi Many-to-Many |
| `OneToOneField` | Model | INTEGER UNIQUE | Relasi One-to-One |
| `FileField` | File | VARCHAR | Upload file |
| `ImageField` | Image | VARCHAR | Upload gambar |
| `JSONField` | dict/list | JSON | Data JSON |

**Relasi Model:**

```python
# 1. ForeignKey (One-to-Many)
# Satu Campaign punya banyak Story
class Campaign(models.Model):
    name = models.CharField(max_length=200)

class Story(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    # Akses: campaign.story_set.all() atau campaign.stories.all() (jika pakai related_name)

# 2. ManyToManyField (Many-to-Many)
# Satu Story bisa punya banyak Tag, satu Tag bisa punya banyak Story
class Tag(models.Model):
    name = models.CharField(max_length=50)

class Story(models.Model):
    tags = models.ManyToManyField(Tag)
    # Akses: story.tags.all()

# 3. OneToOneField (One-to-One)
# Satu User punya satu Profile
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Akses: user.profile (bukan user.profile_set)
```

### 4.3 File View (`views.py`)

**Fungsi**: Logic bisnis yang memproses request dan mengembalikan response.

**Jenis View:**

#### 1. Function-Based View (FBV)

```python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Story
from .forms import StoryForm

def story_list(request):
    """
    Function-based view untuk menampilkan list story
    
    Parameter:
    - request: HttpRequest object yang berisi informasi request
    """
    # Ambil semua story dari database
    stories = Story.objects.all()
    
    # Filter berdasarkan query parameter (jika ada)
    search = request.GET.get('search', '')
    if search:
        stories = stories.filter(title__icontains=search)
    
    # Context: data yang dikirim ke template
    context = {
        'stories': stories,
        'search': search,
    }
    
    # Render template dengan context
    return render(request, 'story_list.html', context)

@login_required  # Decorator: hanya user yang sudah login yang bisa akses
def story_create(request):
    """
    Function-based view untuk membuat story baru
    """
    if request.method == 'POST':
        # User submit form
        form = StoryForm(request.POST, request.FILES)  # request.FILES untuk file upload
        
        if form.is_valid():
            # Simpan ke database
            story = form.save(commit=False)  # Belum save dulu
            story.created_by = request.user  # Set user yang membuat
            story.save()  # Sekarang save
            
            # Redirect ke halaman list
            return redirect('kpi_management:story-list')
    else:
        # User request halaman form (GET request)
        form = StoryForm()
    
    context = {'form': form}
    return render(request, 'story_form.html', context)
```

#### 2. Class-Based View (CBV) - Lebih Powerful

```python
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Story
from .forms import StoryForm
from web_project import TemplateLayout

# ============================================
# BASE VIEW CLASS
# ============================================
class BaseKPIView(LoginRequiredMixin):
    """
    Base view class untuk semua KPI views
    LoginRequiredMixin: Hanya user yang sudah login yang bisa akses
    """
    login_url = '/auth/login/'  # Redirect ke login jika belum login
    redirect_field_name = 'next'
    
    def get_context_data(self, **kwargs):
        """
        Menambahkan context untuk semua views yang inherit dari ini
        TemplateLayout.init: Menginisialisasi layout Sneat
        """
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context

# ============================================
# LIST VIEW (Menampilkan daftar)
# ============================================
class StoryListView(BaseKPIView, ListView):
    """
    Menampilkan list semua story
    """
    model = Story  # Model yang digunakan
    template_name = 'kpi_management/story_list.html'  # Template HTML
    context_object_name = 'stories'  # Nama variabel di template (default: object_list)
    paginate_by = 20  # Pagination: 20 items per page
    
    def get_queryset(self):
        """
        Custom query dengan filter dan search
        """
        queryset = Story.objects.select_related('campaign', 'created_by').all()
        
        # Search
        search = self.request.GET.get('search', '')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(account_name__icontains=search)
            )
        
        # Filter platform
        platform = self.request.GET.get('platform', '')
        if platform:
            queryset = queryset.filter(platform=platform)
        
        # Filter status
        status = self.request.GET.get('status', '')
        if status:
            queryset = queryset.filter(status=status)
        
        return queryset.order_by('-story_date', '-created_at')
    
    def get_context_data(self, **kwargs):
        """
        Menambahkan data tambahan ke context
        """
        context = super().get_context_data(**kwargs)
        
        # Data untuk filter dropdown
        context['platforms'] = Story.PLATFORM_CHOICES
        context['statuses'] = Story.STATUS_CHOICES
        
        # Analytics data
        context['total_stories'] = Story.objects.count()
        context['total_views'] = Story.objects.aggregate(
            total=Sum('views')
        )['total'] or 0
        
        return context

# ============================================
# CREATE VIEW (Membuat data baru)
# ============================================
class StoryCreateView(BaseKPIView, CreateView):
    """
    Membuat story baru
    """
    model = Story
    form_class = StoryForm
    template_name = 'kpi_management/story_form.html'
    success_url = reverse_lazy('kpi_management:story-list')  # Redirect setelah sukses
    
    def form_valid(self, form):
        """
        Dipanggil jika form valid
        Bisa custom logic sebelum save
        """
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Story berhasil dibuat!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        """
        Dipanggil jika form tidak valid
        """
        messages.error(self.request, 'Terdapat error pada form.')
        return super().form_invalid(form)

# ============================================
# UPDATE VIEW (Mengupdate data)
# ============================================
class StoryUpdateView(BaseKPIView, UpdateView):
    """
    Mengupdate story yang sudah ada
    """
    model = Story
    form_class = StoryForm
    template_name = 'kpi_management/story_form.html'
    success_url = reverse_lazy('kpi_management:story-list')
    
    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        messages.success(self.request, 'Story berhasil diupdate!')
        return super().form_valid(form)

# ============================================
# DELETE VIEW (Menghapus data)
# ============================================
class StoryDeleteView(BaseKPIView, DeleteView):
    """
    Menghapus story
    """
    model = Story
    template_name = 'kpi_management/story_confirm_delete.html'
    success_url = reverse_lazy('kpi_management:story-list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Story berhasil dihapus!')
        return super().delete(request, *args, **kwargs)

# ============================================
# DETAIL VIEW (Menampilkan detail)
# ============================================
class StoryDetailView(BaseKPIView, DetailView):
    """
    Menampilkan detail satu story
    """
    model = Story
    template_name = 'kpi_management/story_detail.html'
    context_object_name = 'story'  # Di template: {{ story.title }}
```

**Penjelasan Class-Based Views:**

| View Class | Fungsi | Method yang Bisa Di-override |
|------------|--------|------------------------------|
| `ListView` | Menampilkan list | `get_queryset()`, `get_context_data()` |
| `CreateView` | Membuat data baru | `form_valid()`, `form_invalid()` |
| `UpdateView` | Update data | `form_valid()`, `form_invalid()` |
| `DeleteView` | Hapus data | `delete()` |
| `DetailView` | Detail data | `get_context_data()` |

**Mixins untuk Permission:**

```python
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# LoginRequiredMixin: Hanya user yang sudah login
class MyView(LoginRequiredMixin, ListView):
    ...

# UserPassesTestMixin: Custom permission check
class AdminOnlyView(UserPassesTestMixin, ListView):
    def test_func(self):
        return self.request.user.is_staff
```

### 4.4 File Form (`forms.py`)

**Fungsi**: Mendefinisikan form untuk input data dengan validasi.

```python
from django import forms
from .models import Story

class StoryForm(forms.ModelForm):
    """
    Form untuk Story model
    ModelForm: Form yang terhubung langsung dengan Model
    """
    
    class Meta:
        model = Story
        fields = [
            'title', 'platform', 'account_name', 'story_date',
            'views', 'impressions', 'reach', 'engagement_rate',
            'campaign', 'status', 'notes'
        ]
        # Atau bisa pakai: exclude = ['created_by', 'created_at']
        
        widgets = {
            # Custom HTML attributes untuk styling Bootstrap
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Masukkan judul story'
            }),
            'platform': forms.Select(attrs={
                'class': 'form-select'
            }),
            'story_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'  # HTML5 date picker
            }),
            'views': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            }),
            'engagement_rate': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': 0,
                'max': 100
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Catatan tambahan...'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        """
        Custom initialization
        Dipanggil saat form dibuat
        """
        super().__init__(*args, **kwargs)
        
        # Custom queryset untuk ForeignKey
        self.fields['campaign'].queryset = Campaign.objects.filter(
            status='active'
        ).order_by('-start_date')
        self.fields['campaign'].required = False
        
        # Custom label
        self.fields['title'].label = 'Judul Story'
        
        # Custom help text
        self.fields['engagement_rate'].help_text = 'Masukkan dalam persen (0-100)'
    
    def clean_title(self):
        """
        Custom validation untuk field 'title'
        Nama method: clean_<field_name>()
        """
        title = self.cleaned_data.get('title')
        
        if len(title) < 5:
            raise forms.ValidationError('Judul minimal 5 karakter')
        
        return title
    
    def clean(self):
        """
        Custom validation untuk seluruh form
        """
        cleaned_data = super().clean()
        views = cleaned_data.get('views')
        engagement_rate = cleaned_data.get('engagement_rate')
        
        # Validasi: jika views > 0, engagement_rate harus > 0
        if views and views > 0 and (not engagement_rate or engagement_rate == 0):
            raise forms.ValidationError({
                'engagement_rate': 'Engagement rate harus diisi jika views > 0'
            })
        
        return cleaned_data
```

**Jenis Widget:**

| Widget | HTML Output | Keterangan |
|--------|-------------|------------|
| `TextInput` | `<input type="text">` | Text input |
| `Textarea` | `<textarea>` | Text area |
| `NumberInput` | `<input type="number">` | Number input |
| `EmailInput` | `<input type="email">` | Email input |
| `DateInput` | `<input type="date">` | Date picker |
| `DateTimeInput` | `<input type="datetime-local">` | DateTime picker |
| `Select` | `<select>` | Dropdown |
| `CheckboxInput` | `<input type="checkbox">` | Checkbox |
| `RadioSelect` | Radio buttons | Radio buttons |
| `FileInput` | `<input type="file">` | File upload |

### 4.5 File URLs (`urls.py`)

**Fungsi**: Routing URL untuk aplikasi.

```python
from django.urls import path
from . import views

# App name: untuk namespacing URL
# Di template: {% url 'kpi_management:story-list' %}
app_name = 'kpi_management'

urlpatterns = [
    # ============================================
    # LIST URL
    # ============================================
    path('stories/', views.StoryListView.as_view(), name='story-list'),
    # URL: /kpi/stories/
    # Name: kpi_management:story-list
    
    # ============================================
    # CREATE URL
    # ============================================
    path('stories/create/', views.StoryCreateView.as_view(), name='story-create'),
    # URL: /kpi/stories/create/
    
    # ============================================
    # DETAIL URL (dengan parameter pk)
    # ============================================
    path('stories/<int:pk>/', views.StoryDetailView.as_view(), name='story-detail'),
    # URL: /kpi/stories/1/
    # pk = 1 (primary key dari Story)
    
    # ============================================
    # UPDATE URL
    # ============================================
    path('stories/<int:pk>/edit/', views.StoryUpdateView.as_view(), name='story-update'),
    # URL: /kpi/stories/1/edit/
    
    # ============================================
    # DELETE URL
    # ============================================
    path('stories/<int:pk>/delete/', views.StoryDeleteView.as_view(), name='story-delete'),
    # URL: /kpi/stories/1/delete/
]

# Penjelasan Parameter URL:
# - <int:pk>: Parameter integer dengan nama 'pk'
#   Di view: self.kwargs['pk'] atau self.get_object()
# - <str:slug>: Parameter string dengan nama 'slug'
# - <slug:slug>: Parameter slug (huruf, angka, dash, underscore)
```

**URL Pattern Types:**

```python
# Integer parameter
path('story/<int:pk>/', views.detail, name='detail')
# /story/123/ → pk = 123

# String parameter
path('user/<str:username>/', views.profile, name='profile')
# /user/john/ → username = 'john'

# Slug parameter (alphanumeric + dash/underscore)
path('post/<slug:slug>/', views.post, name='post')
# /post/my-first-post/ → slug = 'my-first-post'

# Multiple parameters
path('category/<int:cat_id>/post/<int:post_id>/', views.post, name='post')
# /category/1/post/5/ → cat_id = 1, post_id = 5
```

### 4.6 Template HTML

**Fungsi**: File HTML yang ditampilkan ke user dengan Django Template Language (DTL).

**Struktur Template Dasar:**

```django
{# ============================================
   EXTEND BASE LAYOUT
   ============================================ #}
{% extends layout_path %}
{# layout_path: Variabel dari TemplateLayout.init() #}

{# ============================================
   LOAD TEMPLATE TAGS
   ============================================ #}
{% load static %}  {# Untuk file static (CSS, JS, Images) #}
{% load i18n %}   {# Untuk internationalization #}

{# ============================================
   PAGE TITLE
   ============================================ #}
{% block title %}Story List{% endblock %}

{# ============================================
   PAGE CSS (Optional)
   ============================================ #}
{% block page_css %}
<link rel="stylesheet" href="{% static 'css/custom.css' %}">
{% endblock %}

{# ============================================
   MAIN CONTENT
   ============================================ #}
{% block content %}
<div class="row">
    <div class="col-12">
        <div class="card">
            <div class="card-header">
                <h5 class="mb-0">Story Management</h5>
            </div>
            <div class="card-body">
                {# Content here #}
            </div>
        </div>
    </div>
</div>
{% endblock %}

{# ============================================
   PAGE JAVASCRIPT (Optional)
   ============================================ #}
{% block page_js %}
<script src="{% static 'js/custom.js' %}"></script>
{% endblock %}
```

**Django Template Tags Lengkap:**

```django
{# ============================================
   COMMENTS
   ============================================ #}
{# Ini adalah komentar, tidak akan ditampilkan di HTML #}

{# ============================================
   VARIABLES
   ============================================ #}
{{ variable }}                    {# Output variable #}
{{ story.title }}                 {# Attribute dari object #}
{{ user.get_full_name }}          {# Method dari object #}

{# ============================================
   FILTERS (Modifikasi output)
   ============================================ #}
{{ title|upper }}                 {# Uppercase #}
{{ title|lower }}                 {# Lowercase #}
{{ title|title }}                 {# Title Case #}
{{ content|truncatewords:30 }}    {# Potong menjadi 30 kata #}
{{ content|truncatechars:100 }}   {# Potong menjadi 100 karakter #}
{{ date|date:"d M Y" }}          {# Format tanggal #}
{{ date|time:"H:i" }}            {# Format waktu #}
{{ number|floatformat:2 }}       {# Format angka (2 desimal) #}
{{ text|default:"N/A" }}         {# Default value jika kosong #}
{{ text|default_if_none:"N/A" }} {# Default jika None #}
{{ list|length }}                {# Panjang list #}
{{ list|first }}                 {# Item pertama #}
{{ list|last }}                  {# Item terakhir #}
{{ url|urlize }}                 {# Convert URL menjadi link #}
{{ html|safe }}                  {# Render HTML (hati-hati!) #}
{{ text|linebreaks }}            {# Convert newline menjadi <br> #}
{{ text|striptags }}             {# Hapus HTML tags #}

{# ============================================
   CONDITIONAL (IF/ELSE)
   ============================================ #}
{% if user.is_authenticated %}
    <p>Welcome, {{ user.username }}!</p>
{% else %}
    <p>Please login.</p>
{% endif %}

{% if story.status == 'published' %}
    <span class="badge bg-success">Published</span>
{% elif story.status == 'draft' %}
    <span class="badge bg-warning">Draft</span>
{% else %}
    <span class="badge bg-secondary">Archived</span>
{% endif %}

{# Operators: ==, !=, <, >, <=, >=, in, not in, and, or, not #}
{% if user.is_staff and user.is_active %}
    <p>Admin user</p>
{% endif %}

{# ============================================
   LOOP (FOR)
   ============================================ #}
{% for story in stories %}
    <div>{{ story.title }}</div>
{% endfor %}

{# Dengan index #}
{% for story in stories %}
    <div>{{ forloop.counter }}. {{ story.title }}</div>
    {# forloop.counter: 1, 2, 3, ... #}
    {# forloop.counter0: 0, 1, 2, ... #}
    {# forloop.first: True jika item pertama #}
    {# forloop.last: True jika item terakhir #}
{% endfor %}

{# Empty clause #}
{% for story in stories %}
    <div>{{ story.title }}</div>
{% empty %}
    <p>No stories found.</p>
{% endfor %}

{# ============================================
   URL GENERATION
   ============================================ #}
{% url 'kpi_management:story-list' %}                    {# URL tanpa parameter #}
{% url 'kpi_management:story-detail' story.pk %}          {# URL dengan parameter #}
{% url 'kpi_management:story-detail' pk=story.pk %}     {# URL dengan named parameter #}

{# Di HTML #}
<a href="{% url 'kpi_management:story-list' %}">List</a>
<a href="{% url 'kpi_management:story-detail' story.pk %}">Detail</a>

{# ============================================
   STATIC FILES
   ============================================ #}
{% load static %}
<img src="{% static 'img/logo.png' %}" alt="Logo">
<link rel="stylesheet" href="{% static 'css/style.css' %}">
<script src="{% static 'js/app.js' %}"></script>

{# ============================================
   CSRF TOKEN (Wajib di form!)
   ============================================ #}
<form method="post">
    {% csrf_token %}  {# Wajib untuk POST request! #}
    {# Form fields #}
</form>

{# ============================================
   FORM RENDERING
   ============================================ #}
{# Render seluruh form #}
{{ form }}

{# Render field per field #}
{{ form.title }}
{{ form.platform }}

{# Render dengan label #}
{{ form.title.label }}
{{ form.title }}

{# Render dengan error #}
{% if form.title.errors %}
    <div class="text-danger">{{ form.title.errors }}</div>
{% endif %}

{# Render semua errors #}
{% if form.errors %}
    <div class="alert alert-danger">
        {{ form.errors }}
    </div>
{% endif %}

{# ============================================
   INCLUDE (Include template lain)
   ============================================ #}
{% include 'partials/header.html' %}
{% include 'partials/footer.html' %}

{# Dengan variabel #}
{% include 'partials/card.html' with title="My Title" content="My Content" %}

{# ============================================
   BLOCK & EXTENDS (Template Inheritance)
   ============================================ #}
{# Di base template (master.html) #}
{% block content %}
    {# Default content #}
{% endblock %}

{# Di child template #}
{% extends 'layout/master.html' %}
{% block content %}
    {# Override content #}
{% endblock %}

{# ============================================
   CUSTOM TEMPLATE TAGS
   ============================================ #}
{% load theme %}  {# Load custom template tags #}
{% get_theme_variables 'template_name' %}  {# Custom tag #}

{# ============================================
   MESSAGES (Flash messages)
   ============================================ #}
{% if messages %}
    {% for message in messages %}
        <div class="alert alert-{{ message.tags }}">
            {{ message }}
        </div>
    {% endfor %}
{% endif %}

{# ============================================
   PAGINATION
   ============================================ #}
{% if is_paginated %}
    <nav>
        {% if page_obj.has_previous %}
            <a href="?page={{ page_obj.previous_page_number }}">Previous</a>
        {% endif %}
        
        <span>Page {{ page_obj.number }} of {{ page_obj.paginator.num_pages }}</span>
        
        {% if page_obj.has_next %}
            <a href="?page={{ page_obj.next_page_number }}">Next</a>
        {% endif %}
    </nav>
{% endif %}
```

---

## 5. Command-line Tools Django

### 5.1 Command Dasar

#### `python manage.py runserver`
**Fungsi**: Menjalankan development server

```bash
python manage.py runserver
# Server berjalan di http://127.0.0.1:8000

python manage.py runserver 8080
# Server berjalan di port 8080

python manage.py runserver 0.0.0.0:8000
# Server accessible dari network lain
```

#### `python manage.py makemigrations`
**Fungsi**: Membuat file migration (perubahan struktur database)

```bash
python manage.py makemigrations
# Membuat migration untuk semua apps yang berubah

python manage.py makemigrations kpi_management
# Membuat migration hanya untuk app kpi_management

python manage.py makemigrations --name add_company_field
# Membuat migration dengan nama custom
```

**Apa yang terjadi:**
1. Django membandingkan models.py dengan database saat ini
2. Jika ada perubahan, membuat file migration di `apps/*/migrations/`
3. File migration berisi instruksi untuk mengubah database

#### `python manage.py migrate`
**Fungsi**: Menerapkan migration ke database

```bash
python manage.py migrate
# Terapkan semua migration yang belum diterapkan

python manage.py migrate kpi_management
# Terapkan migration hanya untuk app kpi_management

python manage.py migrate kpi_management 0001
# Terapkan migration spesifik (0001_initial.py)

python manage.py migrate --fake kpi_management 0001
# Fake migration (tandai sudah diterapkan tanpa benar-benar menjalankan)
```

#### `python manage.py createsuperuser`
**Fungsi**: Membuat admin user

```bash
python manage.py createsuperuser
# Akan diminta input:
# - Username
# - Email (opsional)
# - Password (2x untuk konfirmasi)
```

#### `python manage.py shell`
**Fungsi**: Membuka Django shell (interactive Python dengan Django context)

```bash
python manage.py shell

# Di shell:
>>> from apps.kpi_management.models import Story
>>> Story.objects.all()
>>> Story.objects.count()
>>> story = Story.objects.get(pk=1)
>>> story.title
>>> Story.objects.create(title="Test", platform="instagram", account_name="test")
```

#### `python manage.py collectstatic`
**Fungsi**: Mengumpulkan static files ke folder `staticfiles` (untuk production)

```bash
python manage.py collectstatic
# Mengumpulkan semua static files dari STATICFILES_DIRS ke STATIC_ROOT
```

#### `python manage.py showmigrations`
**Fungsi**: Menampilkan status migration

```bash
python manage.py showmigrations
# Menampilkan daftar migration dan statusnya ([X] = sudah diterapkan, [ ] = belum)
```

### 5.2 Workflow Development Lengkap

```bash
# ============================================
# 1. SETUP PROJECT (Pertama kali)
# ============================================
# Install dependencies
pip install -r requirements.txt

# Buat migration awal
python manage.py makemigrations

# Terapkan migration
python manage.py migrate

# Buat superuser
python manage.py createsuperuser

# ============================================
# 2. DEVELOPMENT WORKFLOW
# ============================================
# Setelah mengubah models.py:
python manage.py makemigrations
python manage.py migrate

# Jalankan server
python manage.py runserver

# ============================================
# 3. DEBUGGING
# ============================================
# Buka shell untuk test
python manage.py shell

# Check migration status
python manage.py showmigrations

# ============================================
# 4. PRODUCTION PREPARATION
# ============================================
# Collect static files
python manage.py collectstatic

# Check untuk error
python manage.py check
```

---

## 6. Template Tags & Context - Penjelasan Lengkap

### 6.1 Context - Apa itu Context?

**Context** adalah dictionary (key-value) yang berisi data yang dikirim dari View ke Template.

```python
# Di View (views.py)
def story_list(request):
    stories = Story.objects.all()
    context = {
        'stories': stories,        # Key: 'stories', Value: QuerySet
        'total': stories.count(), # Key: 'total', Value: integer
        'user': request.user,     # Key: 'user', Value: User object
    }
    return render(request, 'story_list.html', context)

# Di Template (story_list.html)
{% for story in stories %}  {# Mengakses context['stories'] #}
    {{ story.title }}
{% endfor %}

Total: {{ total }}  {# Mengakses context['total'] #}
User: {{ user.username }}  {# Mengakses context['user'] #}
```

### 6.2 Context Processors - Menambahkan Context Global

**Context Processors** adalah fungsi yang menambahkan variabel ke **semua template** secara otomatis.

**File: `config/context_processors.py`**

```python
from django.conf import settings

def my_setting(request):
    """Menambahkan settings ke semua template"""
    return {'MY_SETTING': settings}

def environment(request):
    """Menambahkan ENVIRONMENT ke semua template"""
    return {'ENVIRONMENT': settings.ENVIRONMENT}

def kpi_context(request):
    """
    Menambahkan is_admin dan theme ke semua template
    Dipanggil untuk setiap request
    """
    is_admin = False
    if request.user.is_authenticated:
        try:
            from apps.kpi_management.models import Profile
            profile = Profile.objects.select_related('user').filter(
                user=request.user
            ).first()
            if profile:
                is_admin = getattr(profile, 'role', 'user') == 'admin'
        except Exception:
            pass
    
    # Get theme dari session
    theme = request.session.get('theme', 'light')
    language = request.session.get('language', 'id')
    
    return {
        'is_admin': is_admin,  # Sekarang tersedia di semua template!
        'theme': theme,
        'language': language,
    }
```

**Register di `settings.py`:**

```python
TEMPLATES = [{
    'OPTIONS': {
        'context_processors': [
            'django.template.context_processors.auth',  # Menambahkan 'user'
            'django.template.context_processors.messages',  # Menambahkan 'messages'
            'config.context_processors.kpi_context',  # Custom processor
        ],
    },
}]
```

**Penggunaan di Template:**

```django
{# user tersedia di semua template (dari auth processor) #}
{% if user.is_authenticated %}
    Welcome, {{ user.username }}!
{% endif %}

{# is_admin tersedia di semua template (dari kpi_context processor) #}
{% if is_admin %}
    <a href="{% url 'admin:index' %}">Admin Panel</a>
{% endif %}

{# theme tersedia di semua template #}
<body data-theme="{{ theme }}">
```

### 6.3 TemplateLayout.init() - Inisialisasi Layout Sneat

**Fungsi**: Menginisialisasi layout Sneat dan menambahkan context variables untuk template.

**File: `web_project/__init__.py`**

```python
class TemplateLayout:
    @staticmethod
    def init(view_or_request, context):
        """
        Menginisialisasi layout Sneat
        
        Parameter:
        - view_or_request: View instance atau request object
        - context: Context dictionary dari view
        
        Return:
        - context: Context yang sudah di-update dengan layout variables
        """
        layout = "vertical"  # Default layout
        
        # Set layout_path untuk template
        context.update({
            "layout_path": TemplateHelper.set_layout(
                "layout_" + layout + ".html", context
            ),
        })
        
        # Map context variables (container_class, dll)
        TemplateHelper.map_context(context)
        
        return context
```

**Penggunaan di View:**

```python
from web_project import TemplateLayout

class StoryListView(ListView):
    def get_context_data(self, **kwargs):
        # Inisialisasi layout Sneat
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        
        # Context sekarang sudah berisi:
        # - layout_path: 'layout/layout_vertical.html'
        # - container_class: 'container-xxl' atau 'container-fluid'
        # - content_layout_class: 'layout-compact' atau 'layout-wide'
        # - is_menu: True
        # - is_navbar: True
        # - is_footer: True
        # - dll
        
        return context
```

**Variabel Context yang Ditambahkan:**

| Variable | Nilai | Keterangan |
|----------|-------|------------|
| `layout_path` | `'layout/layout_vertical.html'` | Path ke layout template |
| `container_class` | `'container-xxl'` atau `'container-fluid'` | CSS class untuk container |
| `content_layout_class` | `'layout-compact'` atau `'layout-wide'` | CSS class untuk layout |
| `is_menu` | `True` | Tampilkan menu sidebar |
| `is_navbar` | `True` | Tampilkan navbar |
| `is_footer` | `True` | Tampilkan footer |
| `layout` | `'vertical'` | Tipe layout |

### 6.4 Custom Template Tags

**Custom Template Tags** adalah fungsi Python yang bisa dipanggil di template.

**File: `web_project/template_tags/theme.py`**

```python
from django import template
from web_project.template_helpers.theme import TemplateHelper

register = template.Library()

@register.simple_tag
def get_theme_variables(scope):
    """
    Custom template tag untuk mendapatkan theme variables
    
    Penggunaan di template:
    {% get_theme_variables 'template_name' %}
    """
    return TemplateHelper.get_theme_variables(scope)
```

**Penggunaan di Template:**

```django
{% load theme %}  {# Load custom template tags #}

{# Get theme variable #}
{% get_theme_variables 'template_name' %}
{# Output: "Sneat" #}

{# Di master.html #}
<title>{% block title %}{% endblock %} | {% get_theme_variables 'template_name' %}</title>
```

**Membuat Custom Template Tag Sendiri:**

```python
# File: apps/kpi_management/templatetags/kpi_tags.py
from django import template

register = template.Library()

@register.simple_tag
def total_stories():
    """Menghitung total stories"""
    from .models import Story
    return Story.objects.count()

@register.filter
def multiply(value, arg):
    """Multiply filter"""
    return float(value) * float(arg)

@register.inclusion_tag('kpi_management/stats_card.html')
def stats_card(title, value, icon):
    """Inclusion tag untuk render stats card"""
    return {
        'title': title,
        'value': value,
        'icon': icon,
    }
```

**Penggunaan:**

```django
{% load kpi_tags %}

{# Simple tag #}
Total Stories: {% total_stories %}

{# Filter #}
{{ 10|multiply:5 }}  {# Output: 50 #}

{# Inclusion tag #}
{% stats_card "Total Stories" total_stories "bx-book" %}
```

### 6.5 Template Inheritance - Cara Kerjanya

**Template Inheritance** memungkinkan template child mewarisi dan meng-override bagian dari template parent.

**Struktur:**

```
master.html (Base Template)
    │
    ├── layout_vertical.html (Layout Template)
    │       │
    │       └── story_list.html (Page Template)
```

**1. Base Template (`templates/layout/master.html`)**

```django
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}{% endblock %} | Sneat</title>
    {% block page_css %}{% endblock %}
</head>
<body>
    {% block layout %}{% endblock %}
    {% block page_js %}{% endblock %}
</body>
</html>
```

**2. Layout Template (`templates/layout/layout_vertical.html`)**

```django
{% extends 'layout/master.html' %}

{% block layout %}
<div class="layout-wrapper">
    {% if is_menu %}
        {% include "layout/partials/menu/vertical/vertical_menu.html" %}
    {% endif %}
    
    <div class="layout-page">
        {% if is_navbar %}
            {% include "layout/partials/navbar/navbar.html" %}
        {% endif %}
        
        <div class="content-wrapper">
            <div class="{{ container_class }}">
                {% block content %}{% endblock %}
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

**3. Page Template (`templates/kpi_management/story_list.html`)**

```django
{% extends layout_path %}  {# layout_path dari TemplateLayout.init() #}

{% block title %}Story List{% endblock %}

{% block content %}
<div class="card">
    <h5>Story Management</h5>
    {# Content here #}
</div>
{% endblock %}
```

**Flow Rendering:**

```
1. User request: /kpi/stories/
   │
2. View: StoryListView
   │
3. TemplateLayout.init() → context['layout_path'] = 'layout/layout_vertical.html'
   │
4. Render story_list.html
   │
5. story_list.html extends layout_path (layout_vertical.html)
   │
6. layout_vertical.html extends master.html
   │
7. Final HTML output
```

---

## 7. Membuat CRUD dengan Komponen Sneat

### 7.1 Langkah-langkah Lengkap Membuat CRUD

Mari kita buat CRUD lengkap untuk **Product** dengan komponen Sneat.

#### Step 1: Buat Model (`apps/products/models.py`)

```python
from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    """Model untuk Product"""
    
    name = models.CharField(max_length=200, help_text="Nama produk")
    description = models.TextField(blank=True, help_text="Deskripsi produk")
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Harga produk"
    )
    stock = models.IntegerField(default=0, help_text="Stok tersedia")
    is_active = models.BooleanField(default=True, help_text="Status aktif")
    
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='products_created'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
```

#### Step 2: Buat Form (`apps/products/forms.py`)

```python
from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'stock', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Masukkan nama produk'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Masukkan deskripsi produk'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': 0
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
    
    def clean_price(self):
        """Validasi harga harus > 0"""
        price = self.cleaned_data.get('price')
        if price and price <= 0:
            raise forms.ValidationError('Harga harus lebih dari 0')
        return price
```

#### Step 3: Buat Views (`apps/products/views.py`)

```python
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Q
from web_project import TemplateLayout
from .models import Product
from .forms import ProductForm

class BaseProductView(LoginRequiredMixin):
    """Base view untuk semua product views"""
    login_url = '/auth/login/'
    
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context

class ProductListView(BaseProductView, ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Product.objects.all()
        search = self.request.GET.get('search', '')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(description__icontains=search)
            )
        return queryset.order_by('-created_at')

class ProductCreateView(BaseProductView, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_form.html'
    success_url = reverse_lazy('products:product-list')
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, 'Product berhasil dibuat!')
        return super().form_valid(form)

class ProductUpdateView(BaseProductView, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_form.html'
    success_url = reverse_lazy('products:product-list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Product berhasil diupdate!')
        return super().form_valid(form)

class ProductDeleteView(BaseProductView, DeleteView):
    model = Product
    template_name = 'products/product_confirm_delete.html'
    success_url = reverse_lazy('products:product-list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Product berhasil dihapus!')
        return super().delete(request, *args, **kwargs)

class ProductDetailView(BaseProductView, DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'
```

#### Step 4: Buat URLs (`apps/products/urls.py`)

```python
from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.ProductListView.as_view(), name='product-list'),
    path('create/', views.ProductCreateView.as_view(), name='product-create'),
    path('<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('<int:pk>/edit/', views.ProductUpdateView.as_view(), name='product-update'),
    path('<int:pk>/delete/', views.ProductDeleteView.as_view(), name='product-delete'),
]
```

#### Step 5: Buat Templates

**`templates/products/product_list.html`:**

```django
{% extends layout_path %}
{% load static %}

{% block title %}Product List{% endblock %}

{% block content %}
<div class="row">
    <div class="col-12">
        <div class="card">
            <div class="card-header d-flex justify-content-between align-items-center">
                <h5 class="mb-0">Product Management</h5>
                <a href="{% url 'products:product-create' %}" class="btn btn-primary">
                    <i class="bx bx-plus me-1"></i>
                    Tambah Product
                </a>
            </div>
            <div class="card-body">
                {# Search Form #}
                <form method="get" class="mb-4">
                    <div class="row">
                        <div class="col-md-10">
                            <input type="text" name="search" class="form-control" 
                                   placeholder="Cari produk..." value="{{ request.GET.search }}">
                        </div>
                        <div class="col-md-2">
                            <button type="submit" class="btn btn-primary w-100">Search</button>
                        </div>
                    </div>
                </form>
                
                {# Messages #}
                {% if messages %}
                    {% for message in messages %}
                        <div class="alert alert-{{ message.tags }} alert-dismissible fade show">
                            {{ message }}
                            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                        </div>
                    {% endfor %}
                {% endif %}
                
                {# Table #}
                <div class="table-responsive">
                    <table class="table table-hover">
                        <thead>
                            <tr>
                                <th>Name</th>
                                <th>Price</th>
                                <th>Stock</th>
                                <th>Status</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for product in products %}
                            <tr>
                                <td>{{ product.name }}</td>
                                <td>${{ product.price|floatformat:2 }}</td>
                                <td>{{ product.stock }}</td>
                                <td>
                                    {% if product.is_active %}
                                        <span class="badge bg-success">Active</span>
                                    {% else %}
                                        <span class="badge bg-secondary">Inactive</span>
                                    {% endif %}
                                </td>
                                <td>
                                    <a href="{% url 'products:product-detail' product.pk %}" 
                                       class="btn btn-sm btn-info">
                                        <i class="bx bx-show"></i>
                                    </a>
                                    <a href="{% url 'products:product-update' product.pk %}" 
                                       class="btn btn-sm btn-warning">
                                        <i class="bx bx-edit"></i>
                                    </a>
                                    <a href="{% url 'products:product-delete' product.pk %}" 
                                       class="btn btn-sm btn-danger">
                                        <i class="bx bx-trash"></i>
                                    </a>
                                </td>
                            </tr>
                            {% empty %}
                            <tr>
                                <td colspan="5" class="text-center">No products found.</td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
                
                {# Pagination #}
                {% if is_paginated %}
                    <nav aria-label="Page navigation">
                        <ul class="pagination justify-content-center">
                            {% if page_obj.has_previous %}
                                <li class="page-item">
                                    <a class="page-link" href="?page={{ page_obj.previous_page_number }}">Previous</a>
                                </li>
                            {% endif %}
                            
                            <li class="page-item active">
                                <span class="page-link">
                                    Page {{ page_obj.number }} of {{ page_obj.paginator.num_pages }}
                                </span>
                            </li>
                            
                            {% if page_obj.has_next %}
                                <li class="page-item">
                                    <a class="page-link" href="?page={{ page_obj.next_page_number }}">Next</a>
                                </li>
                            {% endif %}
                        </ul>
                    </nav>
                {% endif %}
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

**`templates/products/product_form.html`:**

```django
{% extends layout_path %}
{% load static %}

{% block title %}{% if object %}Edit{% else %}Create{% endif %} Product{% endblock %}

{% block content %}
<div class="row">
    <div class="col-12">
        <div class="card">
            <div class="card-header">
                <h5 class="mb-0">{% if object %}Edit{% else %}Create{% endif %} Product</h5>
            </div>
            <div class="card-body">
                <form method="post">
                    {% csrf_token %}
                    
                    <div class="row mb-3">
                        <div class="col-md-12">
                            <label class="form-label">{{ form.name.label }}</label>
                            {{ form.name }}
                            {% if form.name.errors %}
                                <div class="text-danger">{{ form.name.errors }}</div>
                            {% endif %}
                        </div>
                    </div>
                    
                    <div class="row mb-3">
                        <div class="col-md-12">
                            <label class="form-label">{{ form.description.label }}</label>
                            {{ form.description }}
                            {% if form.description.errors %}
                                <div class="text-danger">{{ form.description.errors }}</div>
                            {% endif %}
                        </div>
                    </div>
                    
                    <div class="row mb-3">
                        <div class="col-md-6">
                            <label class="form-label">{{ form.price.label }}</label>
                            {{ form.price }}
                            {% if form.price.errors %}
                                <div class="text-danger">{{ form.price.errors }}</div>
                            {% endif %}
                        </div>
                        <div class="col-md-6">
                            <label class="form-label">{{ form.stock.label }}</label>
                            {{ form.stock }}
                            {% if form.stock.errors %}
                                <div class="text-danger">{{ form.stock.errors }}</div>
                            {% endif %}
                        </div>
                    </div>
                    
                    <div class="row mb-3">
                        <div class="col-md-12">
                            <div class="form-check">
                                {{ form.is_active }}
                                <label class="form-check-label" for="{{ form.is_active.id_for_label }}">
                                    {{ form.is_active.label }}
                                </label>
                            </div>
                            {% if form.is_active.errors %}
                                <div class="text-danger">{{ form.is_active.errors }}</div>
                            {% endif %}
                        </div>
                    </div>
                    
                    {# Form errors #}
                    {% if form.non_field_errors %}
                        <div class="alert alert-danger">
                            {{ form.non_field_errors }}
                        </div>
                    {% endif %}
                    
                    <div class="d-flex gap-2">
                        <button type="submit" class="btn btn-primary">
                            <i class="bx bx-save me-1"></i>
                            Save
                        </button>
                        <a href="{% url 'products:product-list' %}" class="btn btn-secondary">
                            <i class="bx bx-x me-1"></i>
                            Cancel
                        </a>
                    </div>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

#### Step 6: Register App & URLs

**`config/settings.py`:**

```python
INSTALLED_APPS = [
    # ... existing apps
    'apps.products',  # Tambahkan ini
]
```

**`config/urls.py`:**

```python
urlpatterns = [
    # ... existing patterns
    path('products/', include('apps.products.urls')),  # Tambahkan ini
]
```

#### Step 7: Migrate Database

```bash
python manage.py makemigrations products
python manage.py migrate
```

#### Step 8: Test

```bash
python manage.py runserver
# Buka http://127.0.0.1:8000/products/
```

---

## 8. Tutorial Step-by-Step Lengkap

### Tutorial: Membuat CRUD Blog Post dengan Fitur Lengkap

Ikuti langkah-langkah ini untuk membuat CRUD blog post yang lengkap dengan:
- Authentication (hanya user yang login bisa create/edit)
- Author (setiap post punya author)
- Rich text editor (opsional)
- Image upload
- Categories
- Tags
- Search & Filter
- Pagination

**Langkah-langkah akan dijelaskan secara detail di bagian berikutnya...**

---

## 9. Tips & Best Practices

### 9.1 Struktur Kode yang Baik
- ✅ Pisahkan logic ke dalam functions/classes
- ✅ Gunakan naming convention yang konsisten
- ✅ Comment kode yang kompleks
- ✅ Gunakan Django best practices

### 9.2 Security
- ✅ Selalu gunakan `{% csrf_token %}` di form
- ✅ Validasi input di form
- ✅ Gunakan `LoginRequiredMixin` untuk protected views
- ✅ Sanitize user input
- ✅ Gunakan `@csrf_exempt` hanya jika benar-benar diperlukan

### 9.3 Performance
- ✅ Gunakan `select_related()` untuk ForeignKey
- ✅ Gunakan `prefetch_related()` untuk ManyToMany
- ✅ Implementasi pagination untuk list yang besar
- ✅ Cache query yang sering digunakan
- ✅ Gunakan database indexes

### 9.4 Testing
- ✅ Test setiap view
- ✅ Test form validation
- ✅ Test permission/authorization
- ✅ Test edge cases

---

**Selamat belajar dan coding! 🚀**

*Dokumen ini akan terus di-update dengan penjelasan yang lebih detail.*



