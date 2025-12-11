# 🚀 QUICK REFERENCE GUIDE - Sneat Django

> **Cheat Sheet Lengkap** - Referensi cepat untuk syntax, command, dan pattern yang sering digunakan

## 📑 Daftar Isi
1. [Command Cheat Sheet](#1-command-cheat-sheet)
2. [File Structure](#2-file-structure)
3. [Django Template Tags](#3-django-template-tags)
4. [Template Filters](#4-template-filters)
5. [Model Field Types](#5-model-field-types)
6. [Class-Based Views](#6-class-based-views)
7. [URL Patterns](#7-url-patterns)
8. [Form Handling](#8-form-handling)
9. [Query Examples](#9-query-examples)
10. [Sneat Bootstrap Components](#10-sneat-bootstrap-components)
11. [Common Patterns](#11-common-patterns)
12. [Debugging Tips](#12-debugging-tips)

---

## 1. Command Cheat Sheet

### Setup Project
```bash
# Install dependencies
pip install -r requirements.txt

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Migrate database
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### Development
```bash
# Run development server
python manage.py runserver
python manage.py runserver 8080        # Custom port
python manage.py runserver 0.0.0.0:8000  # Accessible from network

# Django shell (interactive Python)
python manage.py shell

# Check for errors
python manage.py check
```

### Database
```bash
# Create migrations
python manage.py makemigrations
python manage.py makemigrations kpi_management  # Specific app
python manage.py makemigrations --name add_field  # Named migration

# Apply migrations
python manage.py migrate
python manage.py migrate kpi_management         # Specific app
python manage.py migrate kpi_management 0001    # Specific migration

# Show migration status
python manage.py showmigrations

# Fake migration (mark as applied without running)
python manage.py migrate --fake kpi_management 0001
```

### Static Files
```bash
# Collect static files (for production)
python manage.py collectstatic

# Find static files
python manage.py findstatic css/style.css
```

### Other Useful Commands
```bash
# Create new app
python manage.py startapp myapp

# Create app in apps folder
python manage.py startapp myapp apps/myapp

# Dump data
python manage.py dumpdata kpi_management.Story > stories.json

# Load data
python manage.py loaddata stories.json

# Reset database (WARNING: deletes all data!)
python manage.py flush
python manage.py migrate
```

---

## 2. File Structure

### Project Structure
```
sneat-bootstrap-html-django-admin-template-free/
├── config/                    # Konfigurasi utama
│   ├── settings.py           # ⭐ Pengaturan aplikasi
│   ├── urls.py               # ⭐ URL routing utama
│   ├── context_processors.py # Context processors
│   └── template.py           # Theme variables
│
├── apps/                      # Aplikasi Django
│   └── [app_name]/
│       ├── models.py         # ⭐ Database structure
│       ├── views.py          # ⭐ Business logic
│       ├── forms.py          # ⭐ Form handling
│       ├── urls.py           # ⭐ URL routing app
│       ├── admin.py          # Admin panel config
│       ├── apps.py           # App config
│       └── templates/        # HTML templates
│           └── [app_name]/
│
├── templates/                 # Template global
│   └── layout/               # Base templates
│       ├── master.html       # ⭐ Base template
│       ├── layout_vertical.html
│       └── partials/         # Reusable components
│
├── web_project/              # Helper functions
│   ├── __init__.py          # ⭐ TemplateLayout
│   └── template_helpers/
│       └── theme.py         # TemplateHelper
│
├── src/assets/              # Frontend assets
│   ├── css/                 # Stylesheets
│   ├── js/                  # JavaScript
│   └── img/                 # Images
│
├── manage.py                # ⭐ Django CLI tool
└── requirements.txt         # Python dependencies
```

### App Structure (CRUD)
```
apps/myapp/
├── models.py          # Define database structure
├── views.py           # Handle requests & business logic
├── forms.py           # Define forms
├── urls.py            # Define URL patterns
├── admin.py           # Admin panel configuration
└── templates/
    └── myapp/
        ├── [model]_list.html      # List view
        ├── [model]_form.html      # Create/Update form
        ├── [model]_detail.html    # Detail view
        └── [model]_confirm_delete.html  # Delete confirmation
```

---

## 3. Django Template Tags

### Basic Tags
```django
{# Comments - tidak ditampilkan di HTML #}
{% comment %}Multi-line comment{% endcomment %}

{# Extend template #}
{% extends layout_path %}
{% extends 'layout/master.html' %}

{# Load template tags library #}
{% load static %}
{% load i18n %}
{% load theme %}

{# Define block #}
{% block title %}Page Title{% endblock %}
{% block content %}...{% endblock %}

{# Include template #}
{% include 'partials/header.html' %}
{% include 'partials/card.html' with title="Title" %}
```

### Variables & Output
```django
{# Output variable #}
{{ variable }}
{{ object.field }}
{{ object.method }}
{{ object.method|filter }}

{# Default value #}
{{ variable|default:"N/A" }}
{{ variable|default_if_none:"N/A" }}
```

### Conditional
```django
{# If/Else #}
{% if condition %}
    Content
{% endif %}

{% if condition %}
    True content
{% else %}
    False content
{% endif %}

{% if condition1 %}
    Content 1
{% elif condition2 %}
    Content 2
{% else %}
    Default content
{% endif %}

{# Operators #}
{% if value == 10 %}
{% if value != 10 %}
{% if value > 10 %}
{% if value < 10 %}
{% if value >= 10 %}
{% if value <= 10 %}
{% if 'admin' in user.groups.all %}
{% if value and other_value %}
{% if value or other_value %}
{% if not value %}
```

### Loop
```django
{# For loop #}
{% for item in items %}
    {{ item }}
{% endfor %}

{# With counter #}
{% for item in items %}
    {{ forloop.counter }}. {{ item }}      {# 1, 2, 3, ... #}
    {{ forloop.counter0 }}. {{ item }}     {# 0, 1, 2, ... #}
{% endfor %}

{# First/Last #}
{% for item in items %}
    {% if forloop.first %}First{% endif %}
    {% if forloop.last %}Last{% endif %}
{% endfor %}

{# Empty clause #}
{% for item in items %}
    {{ item }}
{% empty %}
    No items found.
{% endfor %}

{# Reversed #}
{% for item in items reversed %}
    {{ item }}
{% endfor %}
```

### URL Generation
```django
{# URL without parameters #}
{% url 'app_name:view-name' %}

{# URL with positional parameters #}
{% url 'app_name:view-name' pk %}
{% url 'app_name:view-name' pk1 pk2 %}

{# URL with named parameters #}
{% url 'app_name:view-name' pk=object.pk %}
{% url 'app_name:view-name' pk=object.pk slug=object.slug %}

{# In HTML #}
<a href="{% url 'kpi_management:story-list' %}">List</a>
<a href="{% url 'kpi_management:story-detail' story.pk %}">Detail</a>
```

### CSRF & Forms
```django
{# CSRF token (WAJIB di form POST!) #}
<form method="post">
    {% csrf_token %}
    {# Form fields #}
</form>

{# Form rendering #}
{{ form }}                    {# Render seluruh form #}
{{ form.field }}              {# Render satu field #}
{{ form.field.label }}        {# Label field #}
{{ form.field.errors }}       {# Errors field #}
{{ form.non_field_errors }}   {# Non-field errors #}
```

### With Tag
```django
{# Define local variable #}
{% with total=items.count %}
    Total: {{ total }}
{% endwith %}

{# Multiple variables #}
{% with title=story.title author=story.author %}
    <h1>{{ title }}</h1>
    <p>By {{ author }}</p>
{% endwith %}
```

---

## 4. Template Filters

### String Filters
```django
{{ text|upper }}              {# UPPERCASE #}
{{ text|lower }}              {# lowercase #}
{{ text|title }}              {# Title Case #}
{{ text|capfirst }}           {# Capitalize First #}
{{ text|truncatewords:10 }}   {# Truncate to 10 words #}
{{ text|truncatechars:50 }}   {# Truncate to 50 chars #}
{{ text|length }}             {# String length #}
{{ text|default:"N/A" }}      {# Default if empty #}
{{ text|slugify }}            {# Convert to slug #}
```

### Number Filters
```django
{{ number|floatformat:2 }}    {# Format: 99.99 #}
{{ number|floatformat }}       {# Format: 99.9 #}
{{ number|add:1 }}             {# Add 1 #}
{{ number|add:"-5" }}         {# Subtract 5 #}
{{ number|mul:2 }}            {# Multiply by 2 #}
```

### Date/Time Filters
```django
{{ date|date:"d M Y" }}        {# 25 Dec 2023 #}
{{ date|date:"Y-m-d" }}       {# 2023-12-25 #}
{{ date|date:"d/m/Y" }}       {# 25/12/2023 #}
{{ date|time:"H:i" }}         {# 14:30 #}
{{ date|timesince }}          {# 2 hours ago #}
{{ date|timeuntil }}          {# in 3 days #}
```

### List Filters
```django
{{ list|length }}             {# List length #}
{{ list|first }}              {# First item #}
{{ list|last }}               {# Last item #}
{{ list|join:", " }}          {# Join with separator #}
{{ list|slice:":5" }}         {# Slice list #}
{{ list|random }}             {# Random item #}
```

### HTML Filters
```django
{{ html|safe }}               {# Render HTML (careful!) #}
{{ text|linebreaks }}         {# Convert \n to <br> #}
{{ text|striptags }}          {# Remove HTML tags #}
{{ url|urlize }}              {# Convert URL to link #}
{{ text|escape }}             {# Escape HTML #}
```

### Other Filters
```django
{{ value|yesno:"Yes,No,Maybe" }}  {# Yes/No/Maybe #}
{{ value|pluralize }}              {# Pluralize #}
{{ value|make_list }}              {# Convert to list #}
{{ dict|dictsort:"key" }}          {# Sort dictionary #}
```

---

## 5. Model Field Types

### Text Fields
```python
CharField(max_length=200)     # Text pendek (wajib max_length)
TextField()                   # Text panjang
SlugField()                   # URL-friendly text
EmailField()                  # Email (validasi otomatis)
URLField()                    # URL (validasi otomatis)
```

### Number Fields
```python
IntegerField()                # Bilangan bulat
BigIntegerField()             # Bilangan bulat besar
PositiveIntegerField()        # Bilangan bulat positif
SmallIntegerField()           # Bilangan bulat kecil
FloatField()                  # Bilangan desimal
DecimalField(max_digits=10, decimal_places=2)  # Decimal presisi
```

### Date/Time Fields
```python
DateField()                  # Tanggal saja
DateTimeField()              # Tanggal & waktu
TimeField()                  # Waktu saja
DurationField()              # Durasi waktu
```

### Boolean & Choice Fields
```python
BooleanField()               # True/False
NullBooleanField()           # True/False/None
CharField(choices=CHOICES)   # Dropdown dengan pilihan
```

### Relationship Fields
```python
ForeignKey(Model, on_delete=models.CASCADE)      # One-to-Many
OneToOneField(Model, on_delete=models.CASCADE)    # One-to-One
ManyToManyField(Model)                           # Many-to-Many
```

### File Fields
```python
FileField(upload_to='folder/')    # Upload file
ImageField(upload_to='folder/')   # Upload gambar
```

### Other Fields
```python
JSONField()                  # JSON data
UUIDField()                  # UUID
IPAddressField()            # IP address
GenericIPAddressField()     # IPv4/IPv6
```

### Field Options
```python
# Common options
null=True                    # Boleh NULL di database
blank=True                   # Boleh kosong di form
default=0                    # Default value
unique=True                  # Harus unique
db_index=True                # Create database index
verbose_name="Title"         # Human-readable name
help_text="Help text"        # Help text di form
choices=CHOICES              # Dropdown choices
validators=[validator]       # Custom validators
```

---

## 6. Class-Based Views

### Basic Views
```python
from django.views.generic import ListView, DetailView
from django.views.generic import CreateView, UpdateView, DeleteView
from django.views.generic import TemplateView, RedirectView

# List view
class StoryListView(ListView):
    model = Story
    template_name = 'story_list.html'
    context_object_name = 'stories'
    paginate_by = 20
    
    def get_queryset(self):
        return Story.objects.filter(is_active=True)

# Detail view
class StoryDetailView(DetailView):
    model = Story
    template_name = 'story_detail.html'

# Create view
class StoryCreateView(CreateView):
    model = Story
    form_class = StoryForm
    template_name = 'story_form.html'
    success_url = reverse_lazy('story-list')
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

# Update view
class StoryUpdateView(UpdateView):
    model = Story
    form_class = StoryForm
    template_name = 'story_form.html'
    success_url = reverse_lazy('story-list')

# Delete view
class StoryDeleteView(DeleteView):
    model = Story
    template_name = 'story_confirm_delete.html'
    success_url = reverse_lazy('story-list')
```

### Mixins
```python
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.mixins import PermissionRequiredMixin

# Login required
class MyView(LoginRequiredMixin, ListView):
    login_url = '/auth/login/'
    redirect_field_name = 'next'

# Permission check
class AdminView(UserPassesTestMixin, ListView):
    def test_func(self):
        return self.request.user.is_staff

# Permission required
class StaffView(PermissionRequiredMixin, ListView):
    permission_required = 'app.view_model'
```

### TemplateLayout Integration
```python
from web_project import TemplateLayout

class BaseView(LoginRequiredMixin):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context

class StoryListView(BaseView, ListView):
    model = Story
    template_name = 'story_list.html'
```

---

## 7. URL Patterns

### Basic Patterns
```python
from django.urls import path, include

# Simple path
path('', views.index, name='index')

# With parameter
path('story/<int:pk>/', views.detail, name='detail')
path('user/<str:username>/', views.profile, name='profile')
path('post/<slug:slug>/', views.post, name='post')

# Multiple parameters
path('category/<int:cat_id>/post/<int:post_id>/', views.post, name='post')

# Include URLs from app
path('kpi/', include('apps.kpi_management.urls'))
```

### Parameter Types
```python
<int:pk>        # Integer
<str:name>      # String
<slug:slug>     # Slug (alphanumeric + dash/underscore)
<uuid:uuid>     # UUID
<path:path>     # Path (includes slashes)
```

### URL Namespacing
```python
# In app urls.py
app_name = 'kpi_management'

urlpatterns = [
    path('stories/', views.list, name='story-list'),
]

# In template
{% url 'kpi_management:story-list' %}
```

---

## 8. Form Handling

### ModelForm
```python
from django import forms
from .models import Story

class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ['title', 'platform', 'views']
        # atau: exclude = ['created_by', 'created_at']
        
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'platform': forms.Select(attrs={'class': 'form-select'}),
        }
    
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 5:
            raise forms.ValidationError('Title minimal 5 karakter')
        return title
```

### Form in View
```python
# Function-based view
def create_view(request):
    if request.method == 'POST':
        form = StoryForm(request.POST, request.FILES)
        if form.is_valid():
            story = form.save(commit=False)
            story.created_by = request.user
            story.save()
            return redirect('story-list')
    else:
        form = StoryForm()
    return render(request, 'form.html', {'form': form})

# Class-based view
class StoryCreateView(CreateView):
    model = Story
    form_class = StoryForm
    template_name = 'story_form.html'
    success_url = reverse_lazy('story-list')
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
```

### Form Widgets
```python
forms.TextInput()           # <input type="text">
forms.Textarea()            # <textarea>
forms.NumberInput()         # <input type="number">
forms.EmailInput()          # <input type="email">
forms.DateInput()           # <input type="date">
forms.DateTimeInput()       # <input type="datetime-local">
forms.Select()              # <select>
forms.CheckboxInput()       # <input type="checkbox">
forms.RadioSelect()         # Radio buttons
forms.FileInput()           # <input type="file">
```

---

## 9. Query Examples

### Basic Queries
```python
# Get all
Story.objects.all()

# Get one
Story.objects.get(pk=1)
Story.objects.get(title="My Story")

# Filter
Story.objects.filter(platform='instagram')
Story.objects.filter(views__gt=1000)  # Greater than
Story.objects.filter(views__gte=1000) # Greater than or equal
Story.objects.filter(views__lt=100)   # Less than
Story.objects.filter(views__lte=100) # Less than or equal

# Exclude
Story.objects.exclude(status='draft')

# Order by
Story.objects.order_by('-created_at')  # Descending
Story.objects.order_by('title')        # Ascending
Story.objects.order_by('platform', '-created_at')  # Multiple

# Limit
Story.objects.all()[:10]  # First 10
Story.objects.all()[10:20]  # Skip 10, take 10
```

### Lookups
```python
# Exact match
Story.objects.filter(title__exact='My Story')
Story.objects.filter(title='My Story')  # Same as above

# Case-insensitive contains
Story.objects.filter(title__icontains='story')

# Case-sensitive contains
Story.objects.filter(title__contains='Story')

# Starts with
Story.objects.filter(title__istartswith='my')

# Ends with
Story.objects.filter(title__iendswith='story')

# In list
Story.objects.filter(platform__in=['instagram', 'facebook'])

# Date lookups
Story.objects.filter(story_date__year=2023)
Story.objects.filter(story_date__month=12)
Story.objects.filter(story_date__day=25)
Story.objects.filter(story_date__gte=date(2023, 1, 1))
Story.objects.filter(story_date__range=(start_date, end_date))

# Null check
Story.objects.filter(campaign__isnull=True)
Story.objects.filter(campaign__isnull=False)
```

### Complex Queries
```python
from django.db.models import Q

# OR condition
Story.objects.filter(
    Q(title__icontains='story') | Q(platform='instagram')
)

# AND condition
Story.objects.filter(
    Q(title__icontains='story') & Q(platform='instagram')
)

# NOT condition
Story.objects.filter(~Q(status='draft'))
```

### Aggregations
```python
from django.db.models import Count, Sum, Avg, Max, Min

# Count
Story.objects.count()
Story.objects.filter(platform='instagram').count()

# Sum
Story.objects.aggregate(Sum('views'))
Story.objects.aggregate(total_views=Sum('views'))

# Average
Story.objects.aggregate(Avg('engagement_rate'))

# Max/Min
Story.objects.aggregate(Max('views'))
Story.objects.aggregate(Min('views'))

# Group by
Story.objects.values('platform').annotate(count=Count('id'))
```

### Related Queries
```python
# ForeignKey - Forward
story.campaign.name  # Access related object

# ForeignKey - Reverse
campaign.stories.all()  # All stories in campaign (if related_name='stories')

# ManyToMany
story.tags.all()  # All tags
story.tags.add(tag)  # Add tag
story.tags.remove(tag)  # Remove tag
story.tags.clear()  # Remove all tags

# Select related (optimize ForeignKey queries)
Story.objects.select_related('campaign', 'created_by').all()

# Prefetch related (optimize ManyToMany queries)
Story.objects.prefetch_related('tags').all()
```

### Create/Update/Delete
```python
# Create
Story.objects.create(title="New Story", platform="instagram")

# Create with save
story = Story(title="New Story", platform="instagram")
story.save()

# Update
story = Story.objects.get(pk=1)
story.title = "Updated Title"
story.save()

# Bulk update
Story.objects.filter(platform='instagram').update(status='published')

# Delete
story = Story.objects.get(pk=1)
story.delete()

# Bulk delete
Story.objects.filter(status='archived').delete()
```

---

## 10. Sneat Bootstrap Components

### Cards
```html
<div class="card">
    <div class="card-header">
        <h5 class="mb-0">Card Title</h5>
    </div>
    <div class="card-body">
        Card content
    </div>
    <div class="card-footer">
        Footer content
    </div>
</div>
```

### Buttons
```html
<button class="btn btn-primary">Primary</button>
<button class="btn btn-secondary">Secondary</button>
<button class="btn btn-success">Success</button>
<button class="btn btn-danger">Danger</button>
<button class="btn btn-warning">Warning</button>
<button class="btn btn-info">Info</button>
<button class="btn btn-light">Light</button>
<button class="btn btn-dark">Dark</button>

<!-- Button sizes -->
<button class="btn btn-primary btn-sm">Small</button>
<button class="btn btn-primary">Normal</button>
<button class="btn btn-primary btn-lg">Large</button>

<!-- Button with icon -->
<button class="btn btn-primary">
    <i class="bx bx-plus me-1"></i>
    Add
</button>
```

### Forms
```html
<!-- Text input -->
<input type="text" class="form-control" name="field_name">

<!-- Select -->
<select class="form-select" name="field_name">
    <option value="">Select</option>
    <option value="1">Option 1</option>
</select>

<!-- Textarea -->
<textarea class="form-control" rows="4" name="field_name"></textarea>

<!-- Checkbox -->
<div class="form-check">
    <input class="form-check-input" type="checkbox" id="check1">
    <label class="form-check-label" for="check1">Checkbox label</label>
</div>

<!-- Radio -->
<div class="form-check">
    <input class="form-check-input" type="radio" name="radio" id="radio1">
    <label class="form-check-label" for="radio1">Radio label</label>
</div>
```

### Tables
```html
<div class="table-responsive">
    <table class="table table-hover">
        <thead>
            <tr>
                <th>Column 1</th>
                <th>Column 2</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Data 1</td>
                <td>Data 2</td>
            </tr>
        </tbody>
    </table>
</div>

<!-- Table variants -->
<table class="table table-striped">  <!-- Striped -->
<table class="table table-bordered">  <!-- Bordered -->
<table class="table table-sm">        <!-- Small -->
```

### Alerts
```html
<div class="alert alert-success" role="alert">
    Success message
</div>
<div class="alert alert-danger" role="alert">
    Error message
</div>
<div class="alert alert-warning" role="alert">
    Warning message
</div>
<div class="alert alert-info" role="alert">
    Info message
</div>

<!-- Dismissible -->
<div class="alert alert-success alert-dismissible fade show">
    Message
    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
</div>
```

### Badges
```html
<span class="badge bg-primary">Primary</span>
<span class="badge bg-success">Success</span>
<span class="badge bg-danger">Danger</span>
<span class="badge bg-warning">Warning</span>
<span class="badge bg-info">Info</span>
```

### Modals
```html
<!-- Button trigger -->
<button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#myModal">
    Open Modal
</button>

<!-- Modal -->
<div class="modal fade" id="myModal">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title">Modal Title</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">
                Modal content
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                <button type="button" class="btn btn-primary">Save</button>
            </div>
        </div>
    </div>
</div>
```

---

## 11. Common Patterns

### CRUD Pattern
```python
# 1. Model (models.py)
class Story(models.Model):
    title = models.CharField(max_length=200)
    # ...

# 2. Form (forms.py)
class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ['title', ...]

# 3. View (views.py)
class StoryListView(ListView):
    model = Story
    template_name = 'story_list.html'

class StoryCreateView(CreateView):
    model = Story
    form_class = StoryForm
    template_name = 'story_form.html'
    success_url = reverse_lazy('story-list')

# 4. URL (urls.py)
path('stories/', views.StoryListView.as_view(), name='story-list')
path('stories/create/', views.StoryCreateView.as_view(), name='story-create')

# 5. Template (story_list.html)
{% extends layout_path %}
{% block content %}
    {% for story in stories %}
        {{ story.title }}
    {% endfor %}
{% endblock %}
```

### Authentication Pattern
```python
# Function-based view
from django.contrib.auth.decorators import login_required

@login_required
def my_view(request):
    return render(request, 'template.html')

# Class-based view
from django.contrib.auth.mixins import LoginRequiredMixin

class MyView(LoginRequiredMixin, ListView):
    login_url = '/auth/login/'
    redirect_field_name = 'next'
```

### Permission Pattern
```python
from django.contrib.auth.mixins import UserPassesTestMixin

class AdminView(UserPassesTestMixin, ListView):
    def test_func(self):
        return self.request.user.is_staff
```

### TemplateLayout Pattern
```python
from web_project import TemplateLayout

class BaseView(LoginRequiredMixin):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context

class MyView(BaseView, ListView):
    model = MyModel
    template_name = 'my_template.html'
```

---

## 12. Debugging Tips

### Django Shell
```python
python manage.py shell

>>> from apps.kpi_management.models import Story
>>> Story.objects.all()
>>> Story.objects.count()
>>> story = Story.objects.get(pk=1)
>>> story.title
>>> Story.objects.create(title="Test", platform="instagram")
```

### Print Debugging
```python
# In views.py
def my_view(request):
    print("Request method:", request.method)
    print("User:", request.user)
    print("GET params:", request.GET)
    # ...

# In template
{{ request.GET }}  {# Print GET parameters #}
{{ request.user }}  {# Print user #}
```

### Check Migrations
```bash
python manage.py showmigrations
python manage.py migrate --plan
```

### Check URLs
```python
python manage.py shell
>>> from django.urls import reverse
>>> reverse('kpi_management:story-list')
```

### Django Debug Toolbar (Recommended)
```bash
pip install django-debug-toolbar

# Add to INSTALLED_APPS
INSTALLED_APPS = [
    'debug_toolbar',
    # ...
]

# Add to urls.py
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
```

---

**Selamat coding! 🚀**

*Gunakan cheat sheet ini sebagai referensi cepat saat development.*



