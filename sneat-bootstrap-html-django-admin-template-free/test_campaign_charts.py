#!/usr/bin/env python
"""Test grafik Campaign"""
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

# Test Campaign page
print("=" * 70)
print("TEST GRAFIK CAMPAIGN")
print("=" * 70)

try:
    response = client.get('/kpi/campaigns/')
    status = response.status_code

    if status == 200:
        print("✅ Status: OK (200)\n")

        # Check chart data in context
        if hasattr(response, 'context'):
            chart_keys = ['campaign_budget_data', 'campaign_roi_data']

            for key in chart_keys:
                if key in response.context:
                    data_str = response.context[key]
                    try:
                        # Parse JSON
                        if isinstance(data_str, str):
                            data = json.loads(data_str)
                        else:
                            data = data_str

                        # Check data structure
                        if isinstance(data, dict):
                            print(f"✅ {key}")
                            print(f"   └─ Labels: {len(data.get('labels', []))} items")

                            if 'budget' in data:
                                print(f"   └─ Budget: {len(data.get('budget', []))} items")
                                print(f"   └─ Spent: {len(data.get('spent', []))} items")
                                print(f"   └─ Remaining: {len(data.get('remaining', []))} items")
                            elif 'roi' in data:
                                print(f"   └─ ROI: {len(data.get('roi', []))} items")

                            # Show sample data
                            if data.get('labels'):
                                print(f"   └─ Sample labels: {data['labels'][:3]}")
                        else:
                            print(f"⚠️  {key}: Format tidak valid")
                    except json.JSONDecodeError as e:
                        print(f"❌ {key}: Error parsing JSON - {str(e)[:50]}")
                    except Exception as e:
                        print(f"⚠️  {key}: Error - {str(e)[:50]}")
                else:
                    print(f"❌ {key}: TIDAK ADA di context!")
        else:
            print("⚠️  Response tidak memiliki context")
    else:
        print(f"❌ Status: {status}")

except Exception as e:
    print(f"❌ Exception: {str(e)[:100]}")

print("\n" + "=" * 70)
print("✅ Verifikasi selesai!")
print("=" * 70)



