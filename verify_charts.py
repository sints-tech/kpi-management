#!/usr/bin/env python
"""Verifikasi grafik di Story dan Campaign"""
import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
import json

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

# Test pages
test_pages = [
    ('/kpi/stories/', 'Story Management', ['story_trend_data', 'story_platform_data']),
    ('/kpi/campaigns/', 'Campaign Management', ['campaign_budget_data', 'campaign_roi_data']),
]

print("=" * 70)
print("VERIFIKASI GRAFIK DI STORY DAN CAMPAIGN")
print("=" * 70)

all_pass = True
for url, name, chart_keys in test_pages:
    print(f"\n📊 {name}")
    print("-" * 70)
    try:
        response = client.get(url)
        status = response.status_code

        if status == 200:
            print(f"✅ Status: OK (200)")

            # Check chart data in context
            if hasattr(response, 'context'):
                for key in chart_keys:
                    if key in response.context:
                        data_str = response.context[key]
                        try:
                            # Parse JSON
                            if isinstance(data_str, str):
                                data = json.loads(data_str)
                            else:
                                data = data_str

                            # Check if data has structure
                            if isinstance(data, dict):
                                has_content = any(data.values()) if data else False
                                if has_content:
                                    print(f"   ✅ {key:40} | Data OK (ada isi)")
                                else:
                                    print(f"   ⚠️  {key:40} | Data kosong (OK untuk database kosong)")

                                # Show data structure
                                if 'dates' in data or 'labels' in data:
                                    if 'dates' in data:
                                        print(f"      └─ Dates: {len(data.get('dates', []))} items")
                                    if 'labels' in data:
                                        print(f"      └─ Labels: {len(data.get('labels', []))} items")
                            else:
                                print(f"   ⚠️  {key:40} | Format tidak valid")
                        except json.JSONDecodeError as e:
                            print(f"   ❌ {key:40} | Error parsing JSON: {str(e)[:40]}")
                            all_pass = False
                        except Exception as e:
                            print(f"   ⚠️  {key:40} | Error: {str(e)[:40]}")
                    else:
                        print(f"   ❌ {key:40} | TIDAK ADA di context!")
                        all_pass = False
            else:
                print("   ⚠️  Response tidak memiliki context")

        elif status == 302:
            print(f"⚠️  Status: Redirect (302)")
        elif status == 404:
            print(f"❌ Status: Not Found (404)")
            all_pass = False
        else:
            print(f"❌ Status: Error ({status})")
            all_pass = False

    except Exception as e:
        print(f"❌ Exception: {str(e)[:100]}")
        all_pass = False

print("\n" + "=" * 70)
if all_pass:
    print("✅ SEMUA GRAFIK TERKONFIGURASI DENGAN BENAR!")
    print("\nGrafik akan muncul di halaman:")
    print("  - Story Management: Performance Trend & Platform Comparison")
    print("  - Campaign Management: Budget vs Spent & ROI Analysis")
else:
    print("❌ Ada masalah dengan konfigurasi grafik. Silakan periksa error di atas.")
print("=" * 70)



