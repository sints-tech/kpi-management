#!/usr/bin/env python
"""Script untuk test Report dan AuditLog views"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.test import Client

print("=" * 70)
print("TEST REPORT DAN AUDIT LOG VIEWS")
print("=" * 70)

c = Client()
result = c.login(username='admin', password='admin123')
print(f"\nLogin: {'✅ Berhasil' if result else '❌ Gagal'}")

if not result:
    print("❌ Tidak bisa login!")
    sys.exit(1)

# Test Reports
print("\n1. Testing /kpi/reports/...")
try:
    r1 = c.get('/kpi/reports/')
    print(f"   Status: {r1.status_code}")
    if r1.status_code == 200:
        print("   ✅ Reports berhasil!")
        if 'layout_path' in r1.context if hasattr(r1, 'context') else False:
            print("   ✅ layout_path ada di context")
        else:
            print("   ⚠️  layout_path tidak ada di context")
    elif r1.status_code == 302:
        print(f"   ⚠️  Redirect ke: {r1.url}")
    else:
        print(f"   ❌ Error: Status {r1.status_code}")
        if hasattr(r1, 'content'):
            content = r1.content.decode('utf-8', errors='ignore')
            if 'TemplateSyntaxError' in content:
                print("   ❌ TemplateSyntaxError ditemukan!")
except Exception as e:
    print(f"   ❌ Exception: {str(e)}")

# Test AuditLogs
print("\n2. Testing /kpi/audit-logs/...")
try:
    r2 = c.get('/kpi/audit-logs/')
    print(f"   Status: {r2.status_code}")
    if r2.status_code == 200:
        print("   ✅ AuditLogs berhasil!")
        if 'layout_path' in r2.context if hasattr(r2, 'context') else False:
            print("   ✅ layout_path ada di context")
        else:
            print("   ⚠️  layout_path tidak ada di context")
    elif r2.status_code == 302:
        print(f"   ⚠️  Redirect ke: {r2.url}")
    else:
        print(f"   ❌ Error: Status {r2.status_code}")
        if hasattr(r2, 'content'):
            content = r2.content.decode('utf-8', errors='ignore')
            if 'TemplateSyntaxError' in content:
                print("   ❌ TemplateSyntaxError ditemukan!")
except Exception as e:
    print(f"   ❌ Exception: {str(e)}")

print("\n" + "=" * 70)


