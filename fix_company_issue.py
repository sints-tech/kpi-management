#!/usr/bin/env python
"""Script untuk memperbaiki masalah Company table"""
import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection, migrations, models
from django.conf import settings
import sqlite3

print(f"Database path: {settings.DATABASES['default']['NAME']}")

# Connect directly to SQLite
db_path = settings.DATABASES['default']['NAME']
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Check existing tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
tables = cursor.fetchall()
print("\nExisting tables:")
for table in tables:
    print(f"  - {table[0]}")

# Check if kpi_management_company exists
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='kpi_management_company'")
company_exists = cursor.fetchone()

if not company_exists:
    print("\n Creating kpi_management_company table...")
    cursor.execute("""
        CREATE TABLE kpi_management_company (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(200) NOT NULL,
            company_type VARCHAR(20) NOT NULL DEFAULT 'pusat',
            code VARCHAR(50) UNIQUE NOT NULL,
            address TEXT,
            phone VARCHAR(20),
            email VARCHAR(254),
            is_active BOOLEAN NOT NULL DEFAULT 1,
            notes TEXT,
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            parent_company_id INTEGER
        )
    """)
    print("✓ Table created successfully")
else:
    print("\n✓ kpi_management_company table already exists")

# Add company_id to related tables
tables_to_update = [
    'kpi_management_campaign',
    'kpi_management_story',
    'kpi_management_dailyfeedreels',
    'kpi_management_socialmediaaccount'
]

print("\nUpdating related tables...")
for table_name in tables_to_update:
    # Check if table exists
    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
    if cursor.fetchone():
        # Check if company_id column exists
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = [col[1] for col in cursor.fetchall()]

        if 'company_id' not in columns:
            try:
                cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN company_id INTEGER")
                print(f"  ✓ Added company_id to {table_name}")
            except Exception as e:
                print(f"  ⚠ Error adding company_id to {table_name}: {e}")
        else:
            print(f"  - company_id already exists in {table_name}")
    else:
        print(f"  ⚠ Table {table_name} not found")

# Commit changes
conn.commit()
conn.close()

print("\n✓ Database update completed successfully!")
print("\nPlease restart the server to apply changes.")



