import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from apps.kpi_management.models import Profile

# Buat superuser jika belum ada
username = 'admin'
email = 'admin@example.com'
password = 'admin123'

if not User.objects.filter(username=username).exists():
    user = User.objects.create_superuser(username=username, email=email, password=password)
    print(f'Superuser {username} berhasil dibuat!')
    
    # Buat profile dengan role admin
    Profile.objects.create(user=user, role='admin')
    print(f'Profile admin untuk {username} berhasil dibuat!')
else:
    print(f'User {username} sudah ada!')
    user = User.objects.get(username=username)
    # Pastikan profile ada
    if not hasattr(user, 'profile'):
        Profile.objects.create(user=user, role='admin')
        print(f'Profile admin untuk {username} berhasil dibuat!')
    else:
        # Update role menjadi admin
        user.profile.role = 'admin'
        user.profile.save()
        print(f'Role {username} sudah diupdate menjadi admin!')

print('\nLogin credentials:')
print(f'Username: {username}')
print(f'Password: {password}')

