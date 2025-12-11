# 📚 PANDUAN PEMBELAJARAN LENGKAP: Sneat Dashboard Free Django

## Daftar Isi
1. [Pengenalan](#pengenalan)
2. [Konsep Dasar Django & Python](#konsep-dasar-django--python)
3. [Memahami Struktur Proyek](#memahami-struktur-proyek)
4. [Penjelasan File & Folder](#penjelasan-file--folder)
5. [Command-line Tools Django](#command-line-tools-django)
6. [Membuat CRUD dengan Komponen Sneat](#membuat-crud-dengan-komponen-sneat)
7. [Tutorial Step-by-Step](#tutorial-step-by-step)

---

## 1. Pengenalan

### Apa itu Sneat Dashboard?
**Sneat Dashboard** adalah admin template berbasis Bootstrap 5 yang menyediakan:
- UI/UX modern dan responsif
- Komponen siap pakai (cards, tables, forms, charts)
- Dark/Light theme support
- Layout yang dapat dikustomisasi

### Apa itu Django?
**Django** adalah web framework Python yang:
- Mengikuti pola **MVT (Model-View-Template)**
- Menyediakan ORM (Object-Relational Mapping) untuk database
- Memiliki sistem authentication & authorization built-in
- Menyediakan admin panel otomatis

### Apa itu Python?
**Python** adalah bahasa pemrograman yang:
- Sintaks mudah dibaca
- Mendukung pemrograman berorientasi objek
- Memiliki ekosistem library yang luas
- Digunakan untuk web development, data science, AI, dll

---

## 2. Konsep Dasar Django & Python

### 2.1 Arsitektur Django (MVT Pattern)

```
┌─────────────┐
│   Browser   │
└──────┬──────┘
       │ HTTP Request
       ▼
┌─────────────────┐
│   URL Routing    │ (urls.py)
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│     View        │ (views.py) - Logic bisnis
└──────┬──────────┘
       │
       ├──────────┐
       │          │
       ▼          ▼
┌──────────┐  ┌──────────┐
│  Model   │  │ Template │ (HTML)
│ (Database)│  │  (UI)    │
└──────────┘  └──────────┘
```

**Penjelasan:**
- **Model**: Struktur data di database (tabel)
- **View**: Logic/function yang memproses request
- **Template**: File HTML yang ditampilkan ke user
- **URL**: Routing yang menghubungkan URL ke View

### 2.2 Konsep Python Dasar

#### Variabel & Tipe Data
```python
# String
nama = "Django"
# Integer
umur = 5
# List (Array)
daftar = [1, 2, 3]
# Dictionary (Object)
data = {"nama": "Django", "versi": 5.2}
```

#### Class & Object
```python
class Story:
    def __init__(self, title):
        self.title = title
    
    def get_title(self):
        return self.title

# Membuat object
story = Story("My Story")
print(story.get_title())  # Output: My Story
```

#### Function
```python
def tambah(a, b):
    return a + b

hasil = tambah(5, 3)  # hasil = 8
```

---

## 3. Memahami Struktur Proyek

### Struktur Folder Utama

```
sneat-bootstrap-html-django-admin-template-free/
│
├── config/                    # Konfigurasi utama Django
│   ├── settings.py            # Pengaturan aplikasi
│   ├── urls.py                # URL routing utama
│   ├── wsgi.py                # WSGI config (deployment)
│   └── asgi.py                # ASGI config (async)
│
├── apps/                      # Aplikasi Django (modul)
│   ├── authentication/        # Login, Register, Logout
│   ├── dashboards/           # Halaman dashboard
│   ├── kpi_management/       # CRUD KPI Management
│   │   ├── models.py         # Struktur database
│   │   ├── views.py          # Logic bisnis
│   │   ├── forms.py          # Form handling
│   │   ├── urls.py           # URL routing app
│   │   └── templates/        # Template HTML
│   ├── layouts/              # Layout pages
│   ├── pages/                # Static pages
│   └── ...                   # App lainnya
│
├── templates/                 # Template global
│   └── layout/               # Base layout templates
│       ├── master.html       # Template utama
│       └── partials/         # Komponen partial
│
├── src/                      # Frontend assets
│   ├── assets/              # CSS, JS, Images
│   │   ├── css/             # Stylesheet
│   │   ├── js/              # JavaScript
│   │   └── img/             # Images
│   └── scss/                # SCSS source files
│
├── static/                   # Static files (collected)
├── media/                    # User uploaded files
├── manage.py                 # Django command-line tool
├── requirements.txt          # Python dependencies
└── db.sqlite3               # Database SQLite
```

---

## 4. Penjelasan File & Folder

### 4.1 File Konfigurasi

#### `config/settings.py`
**Fungsi**: Pengaturan utama aplikasi Django

**Bagian Penting:**
```python
# Database Configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Installed Apps (daftar aplikasi yang digunakan)
INSTALLED_APPS = [
    'django.contrib.admin',
    'apps.dashboards',
    'apps.kpi_management',
    # ... apps lainnya
]

# Static Files (CSS, JS, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'src' / 'assets']

# Media Files (User uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

**Penjelasan:**
- `DATABASES`: Konfigurasi database (SQLite untuk development)
- `INSTALLED_APPS`: Daftar aplikasi yang terdaftar di Django
- `STATIC_URL`: URL untuk mengakses file statis
- `MEDIA_URL`: URL untuk mengakses file yang di-upload user

#### `config/urls.py`
**Fungsi**: Routing URL utama (menghubungkan URL ke view)

```python
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),  # Django Admin Panel
    path('', include('apps.dashboards.urls')),  # Dashboard URLs
    path('kpi/', include('apps.kpi_management.urls')),  # KPI Management URLs
    # ... routing lainnya
]
```

**Penjelasan:**
- `path()`: Mendefinisikan route URL
- `include()`: Meng-include URL dari aplikasi lain

### 4.2 File Model (`models.py`)

**Fungsi**: Mendefinisikan struktur database (tabel)

**Contoh Model Story:**
```python
from django.db import models
from django.contrib.auth.models import User

class Story(models.Model):
    # Field database
    title = models.CharField(max_length=200)  # Text field (max 200 karakter)
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    views = models.IntegerField(default=0)  # Integer field
    engagement_rate = models.FloatField(default=0.0)  # Decimal field
    story_date = models.DateField()  # Date field
    created_at = models.DateTimeField(auto_now_add=True)  # Auto timestamp
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL)  # Relasi ke User
    
    class Meta:
        ordering = ['-story_date']  # Urutkan berdasarkan tanggal
    
    def __str__(self):
        return self.title  # Representasi string
```

**Jenis Field Django:**
- `CharField`: Text pendek (dengan max_length)
- `TextField`: Text panjang
- `IntegerField`: Bilangan bulat
- `FloatField`: Bilangan desimal
- `DateField`: Tanggal
- `DateTimeField`: Tanggal & waktu
- `ForeignKey`: Relasi ke model lain (One-to-Many)
- `ManyToManyField`: Relasi many-to-many
- `OneToOneField`: Relasi one-to-one

### 4.3 File View (`views.py`)

**Fungsi**: Logic bisnis yang memproses request

**Jenis View:**

#### 1. Function-Based View
```python
from django.shortcuts import render
from .models import Story

def story_list(request):
    stories = Story.objects.all()  # Ambil semua data
    return render(request, 'story_list.html', {'stories': stories})
```

#### 2. Class-Based View (Lebih Powerful)
```python
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Story
from .forms import StoryForm

class StoryListView(ListView):
    model = Story  # Model yang digunakan
    template_name = 'story_list.html'  # Template HTML
    context_object_name = 'stories'  # Nama variabel di template
    paginate_by = 20  # Pagination (20 items per page)
    
    def get_queryset(self):
        # Custom query dengan filter
        queryset = Story.objects.all()
        search = self.request.GET.get('search', '')
        if search:
            queryset = queryset.filter(title__icontains=search)
        return queryset

class StoryCreateView(CreateView):
    model = Story
    form_class = StoryForm
    template_name = 'story_form.html'
    success_url = reverse_lazy('story-list')  # Redirect setelah sukses
```

**Penjelasan:**
- `ListView`: Menampilkan daftar data
- `CreateView`: Membuat data baru
- `UpdateView`: Mengupdate data
- `DeleteView`: Menghapus data
- `DetailView`: Menampilkan detail data

### 4.4 File Form (`forms.py`)

**Fungsi**: Mendefinisikan form untuk input data

```python
from django import forms
from .models import Story

class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ['title', 'platform', 'views', 'engagement_rate']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'platform': forms.Select(attrs={'class': 'form-select'}),
            'views': forms.NumberInput(attrs={'class': 'form-control'}),
        }
```

**Penjelasan:**
- `ModelForm`: Form yang terhubung dengan Model
- `fields`: Field yang ditampilkan di form
- `widgets`: Custom HTML attributes (untuk styling Bootstrap)

### 4.5 File URLs (`urls.py`)

**Fungsi**: Routing URL untuk aplikasi

```python
from django.urls import path
from . import views

app_name = 'kpi_management'

urlpatterns = [
    path('stories/', views.StoryListView.as_view(), name='story-list'),
    path('stories/create/', views.StoryCreateView.as_view(), name='story-create'),
    path('stories/<int:pk>/', views.StoryDetailView.as_view(), name='story-detail'),
    path('stories/<int:pk>/edit/', views.StoryUpdateView.as_view(), name='story-update'),
    path('stories/<int:pk>/delete/', views.StoryDeleteView.as_view(), name='story-delete'),
]
```

**Penjelasan:**
- `path('stories/', ...)`: URL pattern
- `<int:pk>`: Parameter URL (primary key)
- `name='story-list'`: Nama route (untuk referensi di template)

### 4.6 Template HTML

**Fungsi**: File HTML yang ditampilkan ke user

**Struktur Template:**
```django
{% extends layout_path %}  {# Extend base layout #}

{% load static %}  {# Load static files #}

{% block title %}Story List{% endblock %}

{% block content %}
<div class="card">
    <div class="card-header">
        <h5>Story Management</h5>
    </div>
    <div class="card-body">
        {% for story in stories %}
        <div>{{ story.title }}</div>
        {% endfor %}
    </div>
</div>
{% endblock %}
```

**Django Template Tags:**
- `{% extends %}`: Extend template lain
- `{% block %}`: Define block yang bisa di-override
- `{% for %}`: Loop
- `{% if %}`: Conditional
- `{{ variable }}`: Output variable
- `{% url 'name' %}`: Generate URL dari route name

---

## 5. Command-line Tools Django

### 5.1 Command Dasar

#### `python manage.py runserver`
**Fungsi**: Menjalankan development server
```bash
python manage.py runserver
# Server berjalan di http://127.0.0.1:8000
```

#### `python manage.py makemigrations`
**Fungsi**: Membuat file migration (perubahan struktur database)
```bash
python manage.py makemigrations
# Membuat file migration di apps/*/migrations/
```

#### `python manage.py migrate`
**Fungsi**: Menerapkan migration ke database
```bash
python manage.py migrate
# Menerapkan perubahan ke database
```

#### `python manage.py createsuperuser`
**Fungsi**: Membuat admin user
```bash
python manage.py createsuperuser
# Akan diminta input username, email, password
```

#### `python manage.py shell`
**Fungsi**: Membuka Django shell (interactive Python)
```bash
python manage.py shell
>>> from apps.kpi_management.models import Story
>>> Story.objects.all()
```

#### `python manage.py collectstatic`
**Fungsi**: Mengumpulkan static files ke folder `staticfiles`
```bash
python manage.py collectstatic
# Untuk production deployment
```

### 5.2 Workflow Development

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Buat migration setelah mengubah models.py
python manage.py makemigrations

# 3. Terapkan migration
python manage.py migrate

# 4. Buat superuser (jika belum ada)
python manage.py createsuperuser

# 5. Jalankan server
python manage.py runserver
```

---

## 6. Membuat CRUD dengan Komponen Sneat

### 6.1 Langkah-langkah Membuat CRUD

#### Step 1: Buat Model (`models.py`)
```python
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
```

#### Step 2: Buat Form (`forms.py`)
```python
from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
```

#### Step 3: Buat Views (`views.py`)
```python
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Product
from .forms import ProductForm
from web_project import TemplateLayout

class BaseView:
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context

class ProductListView(BaseView, ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    paginate_by = 20

class ProductCreateView(BaseView, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_form.html'
    success_url = reverse_lazy('product-list')

class ProductUpdateView(BaseView, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/product_form.html'
    success_url = reverse_lazy('product-list')

class ProductDeleteView(BaseView, DeleteView):
    model = Product
    template_name = 'products/product_confirm_delete.html'
    success_url = reverse_lazy('product-list')
```

#### Step 4: Buat URLs (`urls.py`)
```python
from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.ProductListView.as_view(), name='product-list'),
    path('create/', views.ProductCreateView.as_view(), name='product-create'),
    path('<int:pk>/edit/', views.ProductUpdateView.as_view(), name='product-update'),
    path('<int:pk>/delete/', views.ProductDeleteView.as_view(), name='product-delete'),
]
```

#### Step 5: Buat Template List (`product_list.html`)
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
                <div class="table-responsive">
                    <table class="table table-hover">
                        <thead>
                            <tr>
                                <th>Name</th>
                                <th>Price</th>
                                <th>Description</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for product in products %}
                            <tr>
                                <td>{{ product.name }}</td>
                                <td>${{ product.price }}</td>
                                <td>{{ product.description|truncatewords:10 }}</td>
                                <td>
                                    <a href="{% url 'products:product-update' product.pk %}" class="btn btn-sm btn-warning">
                                        Edit
                                    </a>
                                    <a href="{% url 'products:product-delete' product.pk %}" class="btn btn-sm btn-danger">
                                        Delete
                                    </a>
                                </td>
                            </tr>
                            {% empty %}
                            <tr>
                                <td colspan="4" class="text-center">No products found.</td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

#### Step 6: Buat Template Form (`product_form.html`)
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
                    <div class="row">
                        <div class="col-md-12 mb-3">
                            <label class="form-label">Name</label>
                            {{ form.name }}
                            {% if form.name.errors %}
                                <div class="text-danger">{{ form.name.errors }}</div>
                            {% endif %}
                        </div>
                        <div class="col-md-6 mb-3">
                            <label class="form-label">Price</label>
                            {{ form.price }}
                            {% if form.price.errors %}
                                <div class="text-danger">{{ form.price.errors }}</div>
                            {% endif %}
                        </div>
                        <div class="col-md-12 mb-3">
                            <label class="form-label">Description</label>
                            {{ form.description }}
                            {% if form.description.errors %}
                                <div class="text-danger">{{ form.description.errors }}</div>
                            {% endif %}
                        </div>
                    </div>
                    <div class="d-flex gap-2">
                        <button type="submit" class="btn btn-primary">Save</button>
                        <a href="{% url 'products:product-list' %}" class="btn btn-secondary">Cancel</a>
                    </div>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

#### Step 7: Register di `config/urls.py`
```python
urlpatterns = [
    # ... existing patterns
    path('products/', include('apps.products.urls')),
]
```

#### Step 8: Register di `config/settings.py`
```python
INSTALLED_APPS = [
    # ... existing apps
    'apps.products',
]
```

#### Step 9: Buat Migration & Migrate
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6.2 Komponen Sneat yang Sering Digunakan

#### Card Component
```django
<div class="card">
    <div class="card-header">
        <h5 class="mb-0">Title</h5>
    </div>
    <div class="card-body">
        Content here
    </div>
</div>
```

#### Table Component
```django
<div class="table-responsive">
    <table class="table table-hover">
        <thead>
            <tr>
                <th>Column 1</th>
                <th>Column 2</th>
            </tr>
        </thead>
        <tbody>
            <!-- Table rows -->
        </tbody>
    </table>
</div>
```

#### Form Components
```django
<!-- Text Input -->
<input type="text" class="form-control" name="field_name">

<!-- Select -->
<select class="form-select" name="field_name">
    <option value="">Select</option>
</select>

<!-- Textarea -->
<textarea class="form-control" rows="4" name="field_name"></textarea>

<!-- Button -->
<button type="submit" class="btn btn-primary">Submit</button>
```

#### Alert Component
```django
<div class="alert alert-success" role="alert">
    Success message
</div>
```

---

## 7. Tutorial Step-by-Step

### Tutorial: Membuat CRUD Blog Post

#### Step 1: Buat App Baru
```bash
cd sneat-bootstrap-html-django-admin-template-free
python manage.py startapp blog
```

#### Step 2: Buat Model (`apps/blog/models.py`)
```python
from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
```

#### Step 3: Buat Form (`apps/blog/forms.py`)
```python
from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
        }
```

#### Step 4: Buat Views (`apps/blog/views.py`)
```python
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post
from .forms import PostForm
from web_project import TemplateLayout

class BaseBlogView:
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context

class PostListView(BaseBlogView, ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10

class PostCreateView(LoginRequiredMixin, BaseBlogView, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('blog:post-list')
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, BaseBlogView, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('blog:post-list')

class PostDeleteView(LoginRequiredMixin, BaseBlogView, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog:post-list')
```

#### Step 5: Buat URLs (`apps/blog/urls.py`)
```python
from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='post-list'),
    path('create/', views.PostCreateView.as_view(), name='post-create'),
    path('<int:pk>/edit/', views.PostUpdateView.as_view(), name='post-update'),
    path('<int:pk>/delete/', views.PostDeleteView.as_view(), name='post-delete'),
]
```

#### Step 6: Buat Templates

**`templates/blog/post_list.html`:**
```django
{% extends layout_path %}
{% load static %}

{% block title %}Blog Posts{% endblock %}

{% block content %}
<div class="row">
    <div class="col-12">
        <div class="card">
            <div class="card-header d-flex justify-content-between align-items-center">
                <h5 class="mb-0">Blog Posts</h5>
                {% if user.is_authenticated %}
                <a href="{% url 'blog:post-create' %}" class="btn btn-primary">
                    <i class="bx bx-plus me-1"></i>
                    New Post
                </a>
                {% endif %}
            </div>
            <div class="card-body">
                {% for post in posts %}
                <div class="card mb-3">
                    <div class="card-body">
                        <h5 class="card-title">{{ post.title }}</h5>
                        <p class="card-text">{{ post.content|truncatewords:30 }}</p>
                        <small class="text-muted">By {{ post.author.username }} on {{ post.created_at|date:"M d, Y" }}</small>
                        {% if user == post.author %}
                        <div class="mt-2">
                            <a href="{% url 'blog:post-update' post.pk %}" class="btn btn-sm btn-warning">Edit</a>
                            <a href="{% url 'blog:post-delete' post.pk %}" class="btn btn-sm btn-danger">Delete</a>
                        </div>
                        {% endif %}
                    </div>
                </div>
                {% empty %}
                <p>No posts yet.</p>
                {% endfor %}
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

**`templates/blog/post_form.html`:**
```django
{% extends layout_path %}
{% load static %}

{% block title %}{% if object %}Edit{% else %}Create{% endif %} Post{% endblock %}

{% block content %}
<div class="row">
    <div class="col-12">
        <div class="card">
            <div class="card-header">
                <h5 class="mb-0">{% if object %}Edit{% else %}Create{% endif %} Post</h5>
            </div>
            <div class="card-body">
                <form method="post">
                    {% csrf_token %}
                    <div class="mb-3">
                        <label class="form-label">Title</label>
                        {{ form.title }}
                        {% if form.title.errors %}
                            <div class="text-danger">{{ form.title.errors }}</div>
                        {% endif %}
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Content</label>
                        {{ form.content }}
                        {% if form.content.errors %}
                            <div class="text-danger">{{ form.content.errors }}</div>
                        {% endif %}
                    </div>
                    <div class="d-flex gap-2">
                        <button type="submit" class="btn btn-primary">Save</button>
                        <a href="{% url 'blog:post-list' %}" class="btn btn-secondary">Cancel</a>
                    </div>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

#### Step 7: Register App & URLs

**`config/settings.py`:**
```python
INSTALLED_APPS = [
    # ... existing apps
    'apps.blog',
]
```

**`config/urls.py`:**
```python
urlpatterns = [
    # ... existing patterns
    path('blog/', include('apps.blog.urls')),
]
```

#### Step 8: Migrate Database
```bash
python manage.py makemigrations
python manage.py migrate
```

#### Step 9: Test
```bash
python manage.py runserver
# Buka http://127.0.0.1:8000/blog/
```

---

## 8. Tips & Best Practices

### 8.1 Struktur Kode yang Baik
- Pisahkan logic ke dalam functions/classes
- Gunakan naming convention yang konsisten
- Comment kode yang kompleks
- Gunakan Django best practices

### 8.2 Security
- Selalu gunakan `{% csrf_token %}` di form
- Validasi input di form
- Gunakan `LoginRequiredMixin` untuk protected views
- Sanitize user input

### 8.3 Performance
- Gunakan `select_related()` untuk ForeignKey
- Gunakan `prefetch_related()` untuk ManyToMany
- Implementasi pagination untuk list yang besar
- Cache query yang sering digunakan

### 8.4 Testing
- Test setiap view
- Test form validation
- Test permission/authorization

---

## 9. Sumber Belajar Tambahan

### Dokumentasi Resmi
- Django: https://docs.djangoproject.com/
- Bootstrap 5: https://getbootstrap.com/docs/5.0/
- Sneat Documentation: https://demos.themeselection.com/sneat-bootstrap-html-admin-template/documentation/

### Video Tutorial
- Django for Beginners (YouTube)
- Django Tutorial (Django Official)

### Buku
- "Django for Beginners" by William S. Vincent
- "Two Scoops of Django" by Daniel & Audrey Feldroy

---

## 10. Troubleshooting

### Error: "No module named 'apps'"
**Solusi**: Pastikan struktur folder benar dan `INSTALLED_APPS` sudah terdaftar

### Error: "TemplateDoesNotExist"
**Solusi**: Pastikan template ada di folder `templates/` dan `TEMPLATES` setting benar

### Error: "FieldError: Cannot resolve keyword"
**Solusi**: Pastikan field ada di model dan migration sudah dijalankan

### Error: "CSRF verification failed"
**Solusi**: Tambahkan `{% csrf_token %}` di form

---

## Kesimpulan

Dengan memahami konsep-konsep di atas, Anda sudah siap untuk:
1. ✅ Memahami struktur proyek Django
2. ✅ Membuat Model, View, Form, Template
3. ✅ Membuat CRUD lengkap dengan komponen Sneat
4. ✅ Menggunakan command-line tools Django
5. ✅ Mengembangkan aplikasi admin dashboard

**Selamat belajar dan coding! 🚀**

