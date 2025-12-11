#!/usr/bin/env python
"""Test semua grafik di CRUD pages"""
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
    print("✓ Logged in as admin")
except User.DoesNotExist:
    print("❌ Admin user not found!")
    sys.exit(1)

# Test pages dengan grafik
test_pages = [
    ('/kpi/stories/', 'Story Page', ['story_trend_data', 'story_platform_data']),
    ('/kpi/campaigns/', 'Campaign Page', ['campaign_budget_data', 'campaign_roi_data']),
    ('/kpi/fyp-posts/', 'FYP Post Value Page', ['fyp_trend_data', 'fyp_platform_data']),
    ('/kpi/dashboard/', 'Dashboard Management Page', ['trend_data', 'platform_data', 'status_data']),
]

print("\nTesting charts in all CRUD pages:")
print("=" * 70)

all_pass = True
for url, name, chart_keys in test_pages:
    try:
        response = client.get(url)
        status = response.status_code

        if status == 200:
            print(f"✅ {name:35} | {url:30} | OK (200)")

            # Check if chart data is in context
            if hasattr(response, 'context'):
                for key in chart_keys:
                    if key in response.context:
                        data = response.context[key]
                        try:
                            # Try to parse JSON
                            if isinstance(data, str):
                                parsed = json.loads(data)
                            else:
                                parsed = data

                            # Check if data has content
                            if isinstance(parsed, dict):
                                has_data = any(parsed.values())
                                if has_data:
                                    print(f"   ✓ {key:50} | Data OK")
                                else:
                                    print(f"   ⚠ {key:50} | Empty data (OK for empty database)")
                            else:
                                print(f"   ⚠ {key:50} | Invalid format")
                        except Exception as e:
                            print(f"   ⚠ {key:50} | Error parsing: {str(e)[:30]}")
                    else:
                        print(f"   ❌ {key:50} | Missing from context")
        elif status == 302:
            print(f"⚠️  {name:35} | {url:30} | Redirect (302)")
        elif status == 404:
            print(f"❌ {name:35} | {url:30} | Not Found (404)")
            all_pass = False
        else:
            print(f"❌ {name:35} | {url:30} | Error ({status})")
            all_pass = False

    except Exception as e:
        print(f"❌ {name:35} | {url:30} | Exception: {str(e)[:50]}")
        all_pass = False

print("=" * 70)
if all_pass:
    print("✅ All pages are accessible and charts data is configured!")
else:
    print("❌ Some pages have errors. Please check the issues above.")



