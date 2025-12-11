# 🚀 QUICK REFERENCE GUIDE - Sneat Django

## Command Cheat Sheet

```bash
# Setup Project
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser

# Development
python manage.py runserver
python manage.py shell

# Database
python manage.py makemigrations
python manage.py migrate
python manage.py migrate --fake-initial

# Static Files
python manage.py collectstatic
```

## File Structure Quick Reference

```
config/
  ├── settings.py      → Pengaturan aplikasi
  ├── urls.py          → URL routing utama
  └── wsgi.py          → Deployment config

apps/
  └── [app_name]/
      ├── models.py    → Database structure
      ├── views.py     → Business logic
      ├── forms.py     → Form handling
      ├── urls.py      → URL routing app
      └── templates/   → HTML templates

templates/
  └── layout/
      └── master.html  → Base template
```

## Django Template Tags

```django
{# Comments #}
{% extends 'base.html' %}
{% block content %}...{% endblock %}
{% for item in items %}...{% endfor %}
{% if condition %}...{% endif %}
{{ variable }}
{% url 'route-name' %}
{% csrf_token %}
{% load static %}
{% static 'path/to/file.css' %}
```

## Model Field Types

```python
CharField(max_length=200)        # Text pendek
TextField()                       # Text panjang
IntegerField()                    # Bilangan bulat
FloatField()                      # Bilangan desimal
DecimalField(max_digits=10, decimal_places=2)  # Decimal
BooleanField()                    # True/False
DateField()                       # Tanggal
DateTimeField()                   # Tanggal & waktu
ForeignKey(Model)                 # Relasi one-to-many
ManyToManyField(Model)            # Relasi many-to-many
FileField(upload_to='folder/')    # File upload
ImageField(upload_to='folder/')   # Image upload
```

## Class-Based Views

```python
ListView      # Menampilkan list
CreateView    # Membuat data baru
UpdateView    # Update data
DeleteView    # Hapus data
DetailView    # Detail data
```

## Sneat Bootstrap Classes

```html
<!-- Cards -->
<div class="card">
  <div class="card-header">...</div>
  <div class="card-body">...</div>
</div>

<!-- Buttons -->
<button class="btn btn-primary">Primary</button>
<button class="btn btn-secondary">Secondary</button>
<button class="btn btn-success">Success</button>
<button class="btn btn-danger">Danger</button>
<button class="btn btn-warning">Warning</button>

<!-- Forms -->
<input class="form-control">
<select class="form-select">
<textarea class="form-control">

<!-- Tables -->
<table class="table table-hover">
  <thead>...</thead>
  <tbody>...</tbody>
</table>

<!-- Alerts -->
<div class="alert alert-success">...</div>
<div class="alert alert-danger">...</div>
```

## URL Patterns

```python
# Simple
path('', views.index, name='index')

# With parameter
path('post/<int:pk>/', views.detail, name='detail')

# Class-based view
path('list/', views.ListView.as_view(), name='list')
```

## Form Handling

```python
# In views.py
def create_view(request):
    if request.method == 'POST':
        form = MyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = MyForm()
    return render(request, 'form.html', {'form': form})
```

## Query Examples

```python
# Get all
Model.objects.all()

# Filter
Model.objects.filter(field='value')
Model.objects.filter(field__icontains='search')

# Get one
Model.objects.get(pk=1)

# Create
Model.objects.create(field='value')

# Update
obj.field = 'new_value'
obj.save()

# Delete
obj.delete()
```

## Common Patterns

### CRUD Pattern
1. Model → Define structure
2. Form → Define input
3. View → Handle logic
4. URL → Route request
5. Template → Display UI

### Authentication Pattern
```python
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

@login_required
def my_view(request):
    ...

class MyView(LoginRequiredMixin, ListView):
    ...
```

## Debugging Tips

```python
# Print in shell
python manage.py shell
>>> from apps.kpi_management.models import Story
>>> Story.objects.all()

# Check migrations
python manage.py showmigrations

# Reset database (WARNING: deletes all data)
python manage.py flush
python manage.py migrate
```

## Sneat Components Location

```
src/assets/
  ├── css/        → Stylesheets
  ├── js/         → JavaScript
  └── img/        → Images

templates/layout/
  ├── master.html → Base template
  └── partials/   → Reusable components
```

## Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| ModuleNotFoundError | Check INSTALLED_APPS in settings.py |
| TemplateDoesNotExist | Check TEMPLATES['DIRS'] in settings.py |
| CSRF verification failed | Add {% csrf_token %} in form |
| FieldError | Run makemigrations & migrate |
| 404 Not Found | Check urls.py routing |

