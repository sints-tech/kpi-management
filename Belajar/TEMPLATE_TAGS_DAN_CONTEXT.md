# 📝 TEMPLATE TAGS & CONTEXT - Penjelasan Lengkap

> Panduan detail tentang Django Template Tags, Context, dan bagaimana mereka bekerja di Sneat Django

## Daftar Isi
1. [Apa itu Context?](#1-apa-itu-context)
2. [Context Processors](#2-context-processors)
3. [Template Tags Dasar](#3-template-tags-dasar)
4. [Template Filters](#4-template-filters)
5. [Custom Template Tags](#5-custom-template-tags)
6. [TemplateLayout & Context Variables](#6-templatelayout--context-variables)
7. [Contoh Praktis](#7-contoh-praktis)

---

## 1. Apa itu Context?

**Context** adalah dictionary Python yang berisi data yang dikirim dari **View** ke **Template**.

### 1.1 Cara Kerja Context

```python
# Di View (views.py)
def story_list(request):
    stories = Story.objects.all()
    
    # Context adalah dictionary
    context = {
        'stories': stories,           # Key: 'stories', Value: QuerySet
        'total': stories.count(),     # Key: 'total', Value: integer
        'user': request.user,         # Key: 'user', Value: User object
        'page_title': 'Story List',   # Key: 'page_title', Value: string
    }
    
    # Kirim context ke template
    return render(request, 'story_list.html', context)
```

```django
{# Di Template (story_list.html) #}
<h1>{{ page_title }}</h1>  {# Mengakses context['page_title'] #}

{% for story in stories %}  {# Mengakses context['stories'] #}
    <div>{{ story.title }}</div>
{% endfor %}

<p>Total: {{ total }}</p>  {# Mengakses context['total'] #}
<p>User: {{ user.username }}</p>  {# Mengakses context['user'] #}
```

### 1.2 Context di Class-Based Views

```python
from django.views.generic import ListView
from web_project import TemplateLayout

class StoryListView(ListView):
    model = Story
    template_name = 'story_list.html'
    context_object_name = 'stories'  # Nama variabel di template
    
    def get_context_data(self, **kwargs):
        """
        Method untuk menambahkan context tambahan
        """
        # Ambil context default dari parent class
        context = super().get_context_data(**kwargs)
        
        # Inisialisasi layout Sneat (menambahkan layout_path, dll)
        context = TemplateLayout.init(self, context)
        
        # Tambahkan context custom
        context['total'] = Story.objects.count()
        context['page_title'] = 'Story Management'
        
        return context
```

**Context yang Tersedia di Template:**

```django
{# Dari ListView #}
{{ stories }}              {# QuerySet semua story #}
{{ object_list }}          {# Sama seperti stories (default name) #}
{{ is_paginated }}         {# True jika ada pagination #}
{{ page_obj }}             {# Page object untuk pagination #}

{# Dari TemplateLayout.init() #}
{{ layout_path }}          {# Path ke layout template #}
{{ container_class }}       {# CSS class untuk container #}
{{ is_menu }}              {# True jika menu ditampilkan #}
{{ is_navbar }}            {# True jika navbar ditampilkan #}

{# Dari Context Processors #}
{{ user }}                 {# User object (dari auth processor) #}
{{ messages }}             {# Messages list (dari messages processor) #}
{{ is_admin }}             {# True jika admin (dari kpi_context processor) #}
{{ theme }}                {# Theme (light/dark) #}
```

---

## 2. Context Processors

**Context Processors** adalah fungsi yang menambahkan variabel ke **semua template** secara otomatis.

### 2.1 Context Processors Built-in Django

Django sudah menyediakan beberapa context processors:

#### 1. `django.template.context_processors.auth`
Menambahkan `user` ke semua template:

```django
{# user tersedia di semua template #}
{% if user.is_authenticated %}
    Welcome, {{ user.username }}!
    <a href="{% url 'logout' %}">Logout</a>
{% else %}
    <a href="{% url 'login' %}">Login</a>
{% endif %}
```

**Variabel yang ditambahkan:**
- `user`: User object (AnonymousUser jika belum login)
- `perms`: Permission object

#### 2. `django.template.context_processors.messages`
Menambahkan `messages` ke semua template:

```django
{# messages tersedia di semua template #}
{% if messages %}
    {% for message in messages %}
        <div class="alert alert-{{ message.tags }}">
            {{ message }}
        </div>
    {% endfor %}
{% endif %}
```

**Message Tags:**
- `debug`, `info`, `success`, `warning`, `error`

### 2.2 Custom Context Processor

**File: `config/context_processors.py`**

```python
from django.conf import settings

def kpi_context(request):
    """
    Custom context processor untuk KPI Management
    Menambahkan is_admin, theme, dan language ke semua template
    """
    is_admin = False
    
    # Check jika user sudah login
    if request.user.is_authenticated:
        try:
            from apps.kpi_management.models import Profile
            profile = Profile.objects.select_related('user').filter(
                user=request.user
            ).first()
            
            if profile:
                # Check role
                is_admin = getattr(profile, 'role', 'user') == 'admin'
        except Exception:
            # Jika error, tetap False
            pass
    
    # Get theme dari session (default: 'light')
    theme = request.session.get('theme', 'light')
    
    # Get language dari session (default: 'id')
    language = request.session.get('language', 'id')
    
    return {
        'is_admin': is_admin,    # Tersedia di semua template!
        'theme': theme,           # Tersedia di semua template!
        'language': language,    # Tersedia di semua template!
    }
```

**Register di `config/settings.py`:**

```python
TEMPLATES = [{
    'OPTIONS': {
        'context_processors': [
            'django.template.context_processors.debug',
            'django.template.context_processors.request',
            'django.template.context_processors.auth',      # Built-in
            'django.template.context_processors.messages',   # Built-in
            'config.context_processors.kpi_context',        # Custom
        ],
    },
}]
```

**Penggunaan di Template:**

```django
{# is_admin tersedia di semua template #}
{% if is_admin %}
    <a href="{% url 'admin:index' %}" class="btn btn-primary">
        Admin Panel
    </a>
{% endif %}

{# theme tersedia di semua template #}
<body data-theme="{{ theme }}">
    {# ... #}
</body>

{# language tersedia di semua template #}
<html lang="{{ language }}">
```

### 2.3 Cara Membuat Context Processor Sendiri

```python
# File: config/context_processors.py

def site_settings(request):
    """Menambahkan site settings ke semua template"""
    from apps.settings.models import SiteSetting
    
    try:
        settings_obj = SiteSetting.objects.first()
        return {
            'site_name': settings_obj.name if settings_obj else 'My Site',
            'site_logo': settings_obj.logo.url if settings_obj and settings_obj.logo else None,
        }
    except Exception:
        return {
            'site_name': 'My Site',
            'site_logo': None,
        }

def cart_count(request):
    """Menambahkan cart count ke semua template"""
    if request.user.is_authenticated:
        from apps.ecommerce.models import Cart
        count = Cart.objects.filter(user=request.user).count()
        return {'cart_count': count}
    return {'cart_count': 0}
```

---

## 3. Template Tags Dasar

**Template Tags** adalah perintah khusus di Django Template Language untuk melakukan operasi tertentu.

### 3.1 Template Tags Penting

#### `{% extends %}` - Template Inheritance

```django
{# Extend template parent #}
{% extends 'layout/master.html' %}
{% extends layout_path %}  {# Menggunakan variabel #}
```

#### `{% block %}` - Define Block

```django
{# Di parent template #}
{% block content %}
    {# Default content #}
{% endblock %}

{# Di child template #}
{% block content %}
    {# Override content #}
    <h1>My Content</h1>
{% endblock %}
```

#### `{% load %}` - Load Template Tags Library

```django
{% load static %}      {# Load static files tags #}
{% load i18n %}        {# Load internationalization tags #}
{% load theme %}       {# Load custom theme tags #}
```

#### `{% url %}` - Generate URL

```django
{# URL tanpa parameter #}
{% url 'kpi_management:story-list' %}
{# Output: /kpi/stories/ #}

{# URL dengan parameter #}
{% url 'kpi_management:story-detail' story.pk %}
{# Output: /kpi/stories/1/ #}

{# URL dengan named parameter #}
{% url 'kpi_management:story-detail' pk=story.pk %}
{# Output: /kpi/stories/1/ #}

{# Di HTML #}
<a href="{% url 'kpi_management:story-list' %}">List</a>
```

#### `{% csrf_token %}` - CSRF Protection

```django
{# Wajib di setiap form POST! #}
<form method="post">
    {% csrf_token %}
    {# Form fields #}
</form>
```

#### `{% if %}` - Conditional

```django
{% if user.is_authenticated %}
    <p>Welcome, {{ user.username }}!</p>
{% else %}
    <p>Please login.</p>
{% endif %}

{# Operators #}
{% if story.views > 1000 %}
    <span class="badge bg-success">Viral!</span>
{% endif %}

{% if story.status == 'published' and story.is_active %}
    <span>Published & Active</span>
{% endif %}

{% if 'admin' in user.groups.all %}
    <span>Admin User</span>
{% endif %}
```

#### `{% for %}` - Loop

```django
{# Basic loop #}
{% for story in stories %}
    <div>{{ story.title }}</div>
{% endfor %}

{# Loop dengan index #}
{% for story in stories %}
    <div>
        {{ forloop.counter }}. {{ story.title }}
        {# forloop.counter: 1, 2, 3, ... #}
        {# forloop.counter0: 0, 1, 2, ... #}
    </div>
{% endfor %}

{# Loop dengan first/last #}
{% for story in stories %}
    {% if forloop.first %}
        <div class="first-item">{{ story.title }}</div>
    {% elif forloop.last %}
        <div class="last-item">{{ story.title }}</div>
    {% else %}
        <div>{{ story.title }}</div>
    {% endif %}
{% endfor %}

{# Empty clause #}
{% for story in stories %}
    <div>{{ story.title }}</div>
{% empty %}
    <p>No stories found.</p>
{% endfor %}
```

#### `{% include %}` - Include Template

```django
{# Include template lain #}
{% include 'partials/header.html' %}

{# Include dengan variabel #}
{% include 'partials/card.html' with title="My Title" content="My Content" %}

{# Include dengan variabel dari context #}
{% include 'partials/card.html' with title=story.title content=story.description %}
```

#### `{% with %}` - Define Variable

```django
{# Define variabel lokal #}
{% with total=stories.count %}
    <p>Total: {{ total }}</p>
{% endwith %}

{# Multiple variables #}
{% with title=story.title author=story.created_by.username %}
    <h1>{{ title }}</h1>
    <p>By {{ author }}</p>
{% endwith %}
```

#### `{% comment %}` - Comment

```django
{% comment %}
    Ini adalah komentar multi-line
    Tidak akan ditampilkan di HTML
{% endcomment %}
```

---

## 4. Template Filters

**Filters** adalah fungsi yang memodifikasi output variabel.

### 4.1 Filters Penting

#### String Filters

```django
{{ title|upper }}              {# Uppercase: "HELLO" #}
{{ title|lower }}              {# Lowercase: "hello" #}
{{ title|title }}              {# Title Case: "Hello World" #}
{{ title|capfirst }}           {# Capitalize First: "Hello" #}
{{ title|truncatewords:10 }}   {# Potong menjadi 10 kata #}
{{ title|truncatechars:50 }}   {# Potong menjadi 50 karakter #}
{{ title|length }}             {# Panjang string #}
{{ title|default:"N/A" }}      {# Default jika kosong #}
{{ title|default_if_none:"N/A" }}  {# Default jika None #}
```

#### Number Filters

```django
{{ price|floatformat:2 }}      {# Format angka: 99.99 #}
{{ price|floatformat }}        {# Format dengan 1 desimal #}
{{ count|add:1 }}              {# Tambah 1 #}
{{ count|add:"-5" }}           {# Kurang 5 #}
```

#### Date/Time Filters

```django
{{ date|date:"d M Y" }}        {# Format: 25 Dec 2023 #}
{{ date|date:"Y-m-d" }}        {# Format: 2023-12-25 #}
{{ date|time:"H:i" }}          {# Format waktu: 14:30 #}
{{ date|timesince }}           {# Relative: "2 hours ago" #}
{{ date|timeuntil }}           {# Relative: "in 3 days" #}
```

#### List Filters

```django
{{ list|length }}              {# Panjang list #}
{{ list|first }}               {# Item pertama #}
{{ list|last }}                {# Item terakhir #}
{{ list|join:", " }}           {# Join dengan separator #}
{{ list|slice:":5" }}          {# Slice list #}
```

#### HTML Filters

```django
{{ html|safe }}                {# Render HTML (hati-hati!) #}
{{ text|linebreaks }}          {# Convert newline menjadi <br> #}
{{ text|linebreaksbr }}       {# Convert newline menjadi <br> #}
{{ text|striptags }}           {# Hapus HTML tags #}
{{ url|urlize }}               {# Convert URL menjadi link #}
```

#### Other Filters

```django
{{ value|yesno:"Yes,No,Maybe" }}  {# Yes/No/Maybe #}
{{ value|pluralize }}              {# Pluralize #}
{{ value|make_list }}              {# Convert ke list #}
{{ value|dictsort:"key" }}         {# Sort dictionary #}
```

### 4.2 Chaining Filters

```django
{# Bisa chain multiple filters #}
{{ title|upper|truncatewords:5 }}  {# Uppercase lalu truncate #}
{{ date|date:"Y-m-d"|upper }}     {# Format date lalu uppercase #}
```

---

## 5. Custom Template Tags

**Custom Template Tags** adalah fungsi Python yang bisa dipanggil di template.

### 5.1 Membuat Custom Template Tag

**File: `apps/kpi_management/templatetags/kpi_tags.py`**

```python
from django import template

register = template.Library()

# ============================================
# SIMPLE TAG
# ============================================
@register.simple_tag
def total_stories():
    """Menghitung total stories"""
    from .models import Story
    return Story.objects.count()

@register.simple_tag
def greeting(name):
    """Greeting tag"""
    return f"Hello, {name}!"

# ============================================
# FILTER
# ============================================
@register.filter
def multiply(value, arg):
    """Multiply filter"""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def percentage(value, total):
    """Calculate percentage"""
    try:
        if total == 0:
            return 0
        return round((float(value) / float(total)) * 100, 2)
    except (ValueError, TypeError):
        return 0

# ============================================
# INCLUSION TAG (Render template)
# ============================================
@register.inclusion_tag('kpi_management/stats_card.html')
def stats_card(title, value, icon, color='primary'):
    """Render stats card"""
    return {
        'title': title,
        'value': value,
        'icon': icon,
        'color': color,
    }

@register.inclusion_tag('kpi_management/breadcrumb.html')
def breadcrumb(items):
    """Render breadcrumb"""
    return {'items': items}
```

**Template untuk Inclusion Tag (`templates/kpi_management/stats_card.html`):**

```django
<div class="card">
    <div class="card-body">
        <div class="d-flex align-items-center">
            <div class="avatar avatar-md bg-{{ color }} me-3">
                <i class="bx {{ icon }}"></i>
            </div>
            <div>
                <h6 class="mb-0">{{ title }}</h6>
                <h4 class="mb-0">{{ value }}</h4>
            </div>
        </div>
    </div>
</div>
```

**Penggunaan di Template:**

```django
{% load kpi_tags %}

{# Simple tag #}
Total Stories: {% total_stories %}
Greeting: {% greeting "John" %}

{# Filter #}
{{ 10|multiply:5 }}  {# Output: 50 #}
{{ 25|percentage:100 }}  {# Output: 25.0 #}

{# Inclusion tag #}
{% stats_card "Total Stories" total_stories "bx-book" "primary" %}
{% stats_card "Total Views" total_views "bx-show" "success" %}
```

### 5.2 Custom Template Tag yang Sudah Ada

**File: `web_project/template_tags/theme.py`**

```python
from django import template
from web_project.template_helpers.theme import TemplateHelper

register = template.Library()

@register.simple_tag
def get_theme_variables(scope):
    """
    Get theme variables dari settings
    
    Penggunaan:
    {% get_theme_variables 'template_name' %}
    """
    return TemplateHelper.get_theme_variables(scope)
```

**Penggunaan:**

```django
{% load theme %}

{# Di master.html #}
<title>{% block title %}{% endblock %} | {% get_theme_variables 'template_name' %}</title>
{# Output: My Page | Sneat #}
```

---

## 6. TemplateLayout & Context Variables

### 6.1 TemplateLayout.init()

**Fungsi**: Menginisialisasi layout Sneat dan menambahkan context variables.

**File: `web_project/__init__.py`**

```python
class TemplateLayout:
    @staticmethod
    def init(view_or_request, context):
        """
        Menginisialisasi layout Sneat
        
        Menambahkan variabel ke context:
        - layout_path: Path ke layout template
        - container_class: CSS class untuk container
        - content_layout_class: CSS class untuk layout
        - is_menu, is_navbar, is_footer: Boolean flags
        """
        layout = "vertical"  # Default layout
        
        # Set layout_path
        context.update({
            "layout_path": TemplateHelper.set_layout(
                "layout_" + layout + ".html", context
            ),
        })
        
        # Map context variables
        TemplateHelper.map_context(context)
        
        return context
```

**Penggunaan di View:**

```python
from web_project import TemplateLayout

class StoryListView(ListView):
    def get_context_data(self, **kwargs):
        # Inisialisasi layout
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        
        # Context sekarang sudah berisi:
        # - layout_path: 'layout/layout_vertical.html'
        # - container_class: 'container-xxl'
        # - content_layout_class: 'layout-compact'
        # - is_menu: True
        # - is_navbar: True
        # - is_footer: True
        
        return context
```

### 6.2 Context Variables yang Ditambahkan

| Variable | Nilai Default | Keterangan |
|----------|---------------|------------|
| `layout_path` | `'layout/layout_vertical.html'` | Path ke layout template |
| `container_class` | `'container-xxl'` | CSS class untuk container (compact) |
| `container_class` | `'container-fluid'` | CSS class untuk container (wide) |
| `content_layout_class` | `'layout-compact'` | CSS class untuk layout compact |
| `content_layout_class` | `'layout-wide'` | CSS class untuk layout wide |
| `is_menu` | `True` | Tampilkan menu sidebar |
| `is_navbar` | `True` | Tampilkan navbar |
| `is_footer` | `True` | Tampilkan footer |
| `layout` | `'vertical'` | Tipe layout |

### 6.3 Custom Context di View

```python
class StoryListView(ListView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        
        # Custom context
        context['page_title'] = 'Story Management'
        context['breadcrumbs'] = [
            {'name': 'Home', 'url': '/'},
            {'name': 'KPI Management', 'url': '/kpi/'},
            {'name': 'Stories', 'url': None},
        ]
        context['stats'] = {
            'total': Story.objects.count(),
            'published': Story.objects.filter(status='published').count(),
            'draft': Story.objects.filter(status='draft').count(),
        }
        
        return context
```

**Penggunaan di Template:**

```django
{# Custom context #}
<h1>{{ page_title }}</h1>

{# Breadcrumbs #}
<nav aria-label="breadcrumb">
    <ol class="breadcrumb">
        {% for breadcrumb in breadcrumbs %}
            {% if breadcrumb.url %}
                <li class="breadcrumb-item">
                    <a href="{{ breadcrumb.url }}">{{ breadcrumb.name }}</a>
                </li>
            {% else %}
                <li class="breadcrumb-item active">{{ breadcrumb.name }}</li>
            {% endif %}
        {% endfor %}
    </ol>
</nav>

{# Stats #}
<div class="row">
    <div class="col-md-4">
        <div class="card">
            <div class="card-body">
                <h6>Total</h6>
                <h3>{{ stats.total }}</h3>
            </div>
        </div>
    </div>
    <div class="col-md-4">
        <div class="card">
            <div class="card-body">
                <h6>Published</h6>
                <h3>{{ stats.published }}</h3>
            </div>
        </div>
    </div>
    <div class="col-md-4">
        <div class="card">
            <div class="card-body">
                <h6>Draft</h6>
                <h3>{{ stats.draft }}</h3>
            </div>
        </div>
    </div>
</div>
```

---

## 7. Contoh Praktis

### 7.1 Template dengan Context Lengkap

```django
{% extends layout_path %}
{% load static %}
{% load kpi_tags %}

{% block title %}Story Management{% endblock %}

{% block content %}
<div class="row">
    <div class="col-12">
        {# Page Header #}
        <div class="d-flex justify-content-between align-items-center mb-4">
            <h4 class="mb-0">{{ page_title|default:"Story Management" }}</h4>
            <a href="{% url 'kpi_management:story-create' %}" class="btn btn-primary">
                <i class="bx bx-plus me-1"></i>
                Tambah Story
            </a>
        </div>
        
        {# Stats Cards dengan Custom Tag #}
        <div class="row mb-4">
            <div class="col-md-3">
                {% stats_card "Total Stories" stats.total "bx-book" "primary" %}
            </div>
            <div class="col-md-3">
                {% stats_card "Published" stats.published "bx-check-circle" "success" %}
            </div>
            <div class="col-md-3">
                {% stats_card "Draft" stats.draft "bx-edit" "warning" %}
            </div>
            <div class="col-md-3">
                {% stats_card "Total Views" stats.total_views "bx-show" "info" %}
            </div>
        </div>
        
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
        <div class="card">
            <div class="card-body">
                <div class="table-responsive">
                    <table class="table table-hover">
                        <thead>
                            <tr>
                                <th>Title</th>
                                <th>Platform</th>
                                <th>Views</th>
                                <th>Engagement</th>
                                <th>Status</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for story in stories %}
                            <tr>
                                <td>{{ story.title|truncatewords:5 }}</td>
                                <td>
                                    <span class="badge bg-info">{{ story.get_platform_display }}</span>
                                </td>
                                <td>{{ story.views|floatformat:0 }}</td>
                                <td>
                                    {{ story.engagement_rate|floatformat:2 }}%
                                    {# Progress bar dengan filter #}
                                    <div class="progress" style="height: 5px;">
                                        <div class="progress-bar" 
                                             style="width: {{ story.engagement_rate|percentage:100 }}%">
                                        </div>
                                    </div>
                                </td>
                                <td>
                                    {% if story.status == 'published' %}
                                        <span class="badge bg-success">Published</span>
                                    {% elif story.status == 'draft' %}
                                        <span class="badge bg-warning">Draft</span>
                                    {% else %}
                                        <span class="badge bg-secondary">Archived</span>
                                    {% endif %}
                                </td>
                                <td>
                                    <div class="btn-group">
                                        <a href="{% url 'kpi_management:story-detail' story.pk %}" 
                                           class="btn btn-sm btn-info">
                                            <i class="bx bx-show"></i>
                                        </a>
                                        {% if is_admin or story.created_by == user %}
                                        <a href="{% url 'kpi_management:story-update' story.pk %}" 
                                           class="btn btn-sm btn-warning">
                                            <i class="bx bx-edit"></i>
                                        </a>
                                        <a href="{% url 'kpi_management:story-delete' story.pk %}" 
                                           class="btn btn-sm btn-danger">
                                            <i class="bx bx-trash"></i>
                                        </a>
                                        {% endif %}
                                    </div>
                                </td>
                            </tr>
                            {% empty %}
                            <tr>
                                <td colspan="6" class="text-center">
                                    <p class="text-muted">No stories found.</p>
                                </td>
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

---

**Selamat belajar! 🚀**

*Dokumen ini menjelaskan secara detail tentang Template Tags dan Context di Django.*



