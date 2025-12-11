#!/usr/bin/env python
"""Script to fix SocialMediaAccount table - ensure it exists"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web_project.settings')
django.setup()

from django.db import connection
from django.core.management import call_command
from apps.kpi_management.models import SocialMediaAccount

print("=" * 60)
print("Fixing SocialMediaAccount Table")
print("=" * 60)

# Step 1: Check if table exists
cursor = connection.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='kpi_management_socialmediaaccount'")
result = cursor.fetchone()

if result:
    print(f"✓ Table already exists: {result[0]}")
    print("Testing model access...")
    try:
        count = SocialMediaAccount.objects.count()
        print(f"✓ Model works! Current count: {count}")
        sys.exit(0)
    except Exception as e:
        print(f"✗ Error accessing model: {e}")
        sys.exit(1)
else:
    print("✗ Table does not exist. Creating...")

    # Step 2: Try running migrations
    try:
        print("Running migrations...")
        call_command('migrate', 'kpi_management', '0003', verbosity=2)
        print("✓ Migration completed")
    except Exception as e:
        print(f"Migration error: {e}")

    # Step 3: Check again
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='kpi_management_socialmediaaccount'")
    result = cursor.fetchone()

    if result:
        print(f"✓ Table created via migration: {result[0]}")
    else:
        # Step 4: Create table directly using schema editor
        print("Creating table directly using schema editor...")
        try:
            with connection.schema_editor() as schema_editor:
                schema_editor.create_model(SocialMediaAccount)
            print("✓ Table created using schema editor")
        except Exception as e:
            print(f"✗ Error creating table: {e}")
            sys.exit(1)

    # Step 5: Final verification
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='kpi_management_socialmediaaccount'")
    result = cursor.fetchone()
    if result:
        print(f"✓ Final verification: Table '{result[0]}' exists")
        try:
            count = SocialMediaAccount.objects.count()
            print(f"✓ Model works! Current count: {count}")
            sys.exit(0)
        except Exception as e:
            print(f"✗ Error accessing model: {e}")
            sys.exit(1)
    else:
        print("✗ Error: Table was not created")
        sys.exit(1)

print("=" * 60)

