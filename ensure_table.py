#!/usr/bin/env python
"""Script to ensure SocialMediaAccount table exists"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web_project.settings')
django.setup()

from django.db import connection
from apps.kpi_management.models import SocialMediaAccount

# Check if table exists
cursor = connection.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='kpi_management_socialmediaaccount'")
result = cursor.fetchone()

if result:
    print("✓ Table already exists: kpi_management_socialmediaaccount")
    sys.exit(0)
else:
    print("Creating table...")
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
            sys.exit(0)
        else:
            print("✗ Error: Table was not created")
            sys.exit(1)
    except Exception as e:
        print(f"✗ Error creating table: {e}")
        sys.exit(1)

