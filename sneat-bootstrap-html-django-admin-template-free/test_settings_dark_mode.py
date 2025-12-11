#!/usr/bin/env python
"""Test dark mode pada halaman CRUD Pengaturan"""
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
    print("✓ Logged in as admin\n")
except User.DoesNotExist:
    print("❌ Admin user not found!")
    sys.exit(1)

# Test semua halaman CRUD Pengaturan
print("=" * 70)
print("TEST DARK MODE - CRUD PENGATURAN")
print("=" * 70)

pages = [
    ('/kpi/settings/', 'Settings List'),
    ('/kpi/settings/theme/', 'Settings Theme'),
    ('/kpi/settings/language/', 'Settings Language'),
    ('/kpi/settings/create/', 'Settings Create'),
]

all_pass = True

for url, name in pages:
    try:
        response = client.get(url)
        status = response.status_code

        if status == 200:
            print(f"✅ {name:30} | Status: OK (200)")

            # Check if page_css block exists (CSS untuk dark mode)
            content = response.content.decode('utf-8')
            if 'page_css' in content and 'Dark Mode Improvements' in content:
                print(f"   └─ ✓ CSS Dark Mode ditemukan")
            else:
                print(f"   └─ ⚠️  CSS Dark Mode tidak ditemukan")
                all_pass = False

        elif status == 302:
            print(f"⚠️  {name:30} | Status: Redirect (302)")
        else:
            print(f"❌ {name:30} | Status: Error ({status})")
            all_pass = False

    except Exception as e:
        print(f"❌ {name:30} | Exception: {str(e)[:50]}")
        all_pass = False

print("\n" + "=" * 70)
if all_pass:
    print("✅ Semua halaman CRUD Pengaturan memiliki CSS Dark Mode!")
else:
    print("⚠️  Beberapa halaman mungkin belum memiliki CSS Dark Mode.")
print("=" * 70)



