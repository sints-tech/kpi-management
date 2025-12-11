#!/usr/bin/env python
"""Script to create SocialMediaAccount table"""
import os
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
    print("Table already exists")
else:
    print("Creating table...")
    # Use Django's schema editor to create the table
    from django.db import models
    from django.core.management.sql import sql_create_model
    from django.core.management.color import no_style

    style = no_style()
    sql_statements = connection.ops.sql_create_model(SocialMediaAccount, style)

    for sql in sql_statements:
        cursor.execute(sql)

    connection.commit()
    print("Table created successfully!")

