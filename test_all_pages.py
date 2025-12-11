#!/usr/bin/env python
"""Test all CRUD pages"""
import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User

# Create test client
client = Client()

# Login as admin
try:
    user = User.objects.get(username='admin')
    client.force_login(user)
    print("✓ Logged in as admin")
except User.DoesNotExist:
    print("❌ Admin user not found!")
    sys.exit(1)

# Test pages
test_urls = [
    ('/kpi/stories/', 'Story Page'),
    ('/kpi/daily-feeds/', 'Daily Feed/Reels'),
    ('/kpi/campaigns/', 'Campaign'),
    ('/kpi/social-media-accounts/', 'Social Media Accounts'),
    ('/kpi/dashboard/', 'Dashboard Management KPI'),
    ('/kpi/fyp-posts/', 'FYP Posts'),
    ('/kpi/collab-brands/', 'Collab Brands'),
    ('/kpi/users/', 'User Management'),
    ('/kpi/settings/', 'Settings'),
]

print("\nTesting all CRUD pages:")
print("=" * 60)

all_pass = True
for url, name in test_urls:
    try:
        response = client.get(url)
        status = response.status_code

        if status == 200:
            print(f"✅ {name:30} | {url:30} | OK (200)")
        elif status == 302:
            print(f"⚠️  {name:30} | {url:30} | Redirect (302)")
        elif status == 404:
            print(f"❌ {name:30} | {url:30} | Not Found (404)")
            all_pass = False
        else:
            print(f"❌ {name:30} | {url:30} | Error ({status})")
            all_pass = False

    except Exception as e:
        print(f"❌ {name:30} | {url:30} | Exception: {str(e)[:50]}")
        all_pass = False

print("=" * 60)
if all_pass:
    print("✅ All pages are accessible!")
else:
    print("❌ Some pages have errors. Please check the issues above.")



