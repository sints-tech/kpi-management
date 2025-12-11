#!/usr/bin/env python
"""Script to create SocialMediaAccount table"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web_project.settings')
django.setup()

from django.db import connection
from apps.kpi_management.models import SocialMediaAccount

print("=" * 60)
print("Creating SocialMediaAccount Table")
print("=" * 60)

# Check if table exists
cursor = connection.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='kpi_management_socialmediaaccount'")
result = cursor.fetchone()

if result:
    print(f"✓ Table already exists: {result[0]}")
    try:
        count = SocialMediaAccount.objects.count()
        print(f"✓ Model works! Current count: {count}")
    except Exception as e:
        print(f"✗ Error accessing model: {e}")
        sys.exit(1)
else:
    print("✗ Table does not exist. Creating...")
    try:
        # Use Django's schema editor
        with connection.schema_editor() as schema_editor:
            schema_editor.create_model(SocialMediaAccount)
        print("✓ Table created successfully!")

        # Verify
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='kpi_management_socialmediaaccount'")
        result = cursor.fetchone()
        if result:
            print(f"✓ Verified: Table '{result[0]}' exists")
            try:
                count = SocialMediaAccount.objects.count()
                print(f"✓ Model works! Current count: {count}")
            except Exception as e:
                print(f"✗ Error accessing model: {e}")
                sys.exit(1)
        else:
            print("✗ Error: Table was not created")
            sys.exit(1)
    except Exception as e:
        print(f"✗ Error creating table: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

print("=" * 60)

