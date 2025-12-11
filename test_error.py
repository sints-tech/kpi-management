#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from apps.kpi_management.models import Profile

# Create admin user if not exists
user, created = User.objects.get_or_create(
    username='admin',
    defaults={
        'email': 'admin@example.com',
        'is_staff': True,
        'is_superuser': True,
        'is_active': True
    }
)
if created:
    user.set_password('admin123')
    user.save()
    # Create profile
    Profile.objects.get_or_create(user=user, defaults={'role': 'admin'})
    print("Created admin user and profile")
else:
    # Ensure profile exists
    profile, _ = Profile.objects.get_or_create(user=user, defaults={'role': 'admin'})
    if profile.role != 'admin':
        profile.role = 'admin'
        profile.save()
    print("Admin user exists")

# Test client
c = Client()
c.force_login(user)

# Test URLs
test_urls = [
    ('Story', '/kpi/stories/'),
    ('Daily Feed/Reels', '/kpi/daily-feeds/'),
    ('Campaign', '/kpi/campaigns/'),
    ('Social Media Account', '/kpi/social-media-accounts/'),
    ('Dashboard', '/kpi/dashboard/'),
]

print("\n" + "="*70)
print("TESTING CRUD PAGES - CHECKING FOR ERRORS")
print("="*70 + "\n")

for name, url in test_urls:
    sys.stdout.write(f"Testing {name}... ")
    sys.stdout.flush()
    try:
        response = c.get(url)
        if response.status_code == 200:
            print(f"✓ OK")
        else:
            print(f"✗ ERROR - Status: {response.status_code}")
            content = response.content.decode('utf-8', errors='ignore')
            if content:
                # Look for traceback
                if 'Traceback' in content:
                    tb_start = content.find('Traceback')
                    tb_end = content.find('</div>', tb_start) if '</div>' in content[tb_start:] else tb_start + 5000
                    print("\n" + "="*70)
                    print(f"TRACEBACK for {name}:")
                    print("="*70)
                    print(content[tb_start:tb_end])
                    print("="*70 + "\n")
                elif 'Error' in content or 'Exception' in content:
                    # Find error message
                    error_lines = [line for line in content.split('\n') if 'Error' in line or 'Exception' in line]
                    if error_lines:
                        print(f"\nError found:")
                        for line in error_lines[:5]:
                            print(f"  {line[:200]}")
    except Exception as e:
        print(f"✗ EXCEPTION: {type(e).__name__}: {str(e)}")
        import traceback
        print("\n" + "="*70)
        print(f"EXCEPTION TRACEBACK for {name}:")
        print("="*70)
        traceback.print_exc()
        print("="*70 + "\n")

print("\n" + "="*70)
print("TEST COMPLETE")
print("="*70)
