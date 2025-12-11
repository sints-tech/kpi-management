#!/usr/bin/env python
"""Script untuk membuat ulang tabel dan kolom yang diperlukan"""
import os
import sys
import sqlite3

# Get database path
db_path = 'db.sqlite3'

if not os.path.exists(db_path):
    print(f"Error: Database {db_path} not found!")
    sys.exit(1)

print(f"Fixing database: {db_path}")

# Connect to database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 1. Create Company table
print("\n1. Creating Company table...")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS kpi_management_company (
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
print("   ✓ Company table created/verified")

# 2. Add company_id to related tables
tables_to_update = [
    'kpi_management_campaign',
    'kpi_management_story',
    'kpi_management_dailyfeedreels',
    'kpi_management_socialmediaaccount'
]

print("\n2. Adding company_id columns...")
for table_name in tables_to_update:
    # Check if table exists
    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
    if cursor.fetchone():
        # Check current columns
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = [col[1] for col in cursor.fetchall()]

        if 'company_id' not in columns:
            try:
                cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN company_id INTEGER")
                print(f"   ✓ Added company_id to {table_name}")
            except sqlite3.OperationalError as e:
                if "duplicate column" in str(e):
                    print(f"   - company_id already exists in {table_name}")
                else:
                    print(f"   ⚠ Error with {table_name}: {e}")
        else:
            print(f"   - company_id already exists in {table_name}")
    else:
        print(f"   ⚠ Table {table_name} not found")

# 3. Verify all changes
print("\n3. Verifying changes...")
cursor.execute("PRAGMA table_info(kpi_management_company)")
company_columns = cursor.fetchall()
if company_columns:
    print("   ✓ Company table verified with columns:")
    for col in company_columns:
        print(f"      - {col[1]} ({col[2]})")

print("\n4. Checking company_id in related tables...")
for table_name in tables_to_update:
    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
    if cursor.fetchone():
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = [col[1] for col in cursor.fetchall()]
        if 'company_id' in columns:
            print(f"   ✓ {table_name} has company_id column")
        else:
            print(f"   ✗ {table_name} missing company_id column")

# Commit all changes
conn.commit()
conn.close()

print("\n✅ Database fix completed successfully!")
print("Please restart the Django server now.")



