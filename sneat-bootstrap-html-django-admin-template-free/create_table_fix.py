#!/usr/bin/env python
"""Script to create SocialMediaAccount table using schema editor"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web_project.settings')
django.setup()

from django.db import connection
from django.db import models
from apps.kpi_management.models import SocialMediaAccount

# Check if table exists
cursor = connection.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='kpi_management_socialmediaaccount'")
result = cursor.fetchone()

if result:
    print("✓ Table already exists")
else:
    print("Creating table...")
    # Use Django's schema editor
    from django.db import connection
    with connection.schema_editor() as schema_editor:
        schema_editor.create_model(SocialMediaAccount)
    print("✓ Table created successfully!")

# Verify
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='kpi_management_socialmediaaccount'")
result = cursor.fetchone()
if result:
    print(f"✓ Verified: Table '{result[0]}' exists")
else:
    print("✗ Error: Table was not created")

