#!/usr/bin/env python
"""Script untuk memperbaiki database - membuat semua tabel dan kolom yang hilang"""
import sqlite3
import os
import json

# Path to database
db_path = 'db.sqlite3'

if not os.path.exists(db_path):
    print(f"Database {db_path} not found!")
    exit(1)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("=" * 60)
print("MEMPERBAIKI DATABASE - MEMBUAT TABEL DAN KOLOM YANG HILANG")
print("=" * 60)

# 1. Check and create DashboardSettings table
print("\n1. Checking DashboardSettings table...")
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='kpi_management_dashboardsettings'")
if not cursor.fetchone():
    print("   Creating kpi_management_dashboardsettings table...")
    cursor.execute("""
        CREATE TABLE "kpi_management_dashboardsettings" (
            "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
            "role" varchar(50) NULL,
            "show_total_campaign" bool NOT NULL DEFAULT 1,
            "show_total_story" bool NOT NULL DEFAULT 1,
            "show_total_fyp" bool NOT NULL DEFAULT 1,
            "show_engagement_avg" bool NOT NULL DEFAULT 1,
            "show_revenue_kpi" bool NOT NULL DEFAULT 1,
            "show_user_activity" bool NOT NULL DEFAULT 1,
            "show_notifications" bool NOT NULL DEFAULT 1,
            "widget_layout" text NOT NULL DEFAULT '{}',
            "can_view_dashboard" bool NOT NULL DEFAULT 1,
            "created_at" datetime NOT NULL,
            "updated_at" datetime NOT NULL,
            "user_id" integer NULL REFERENCES "auth_user" ("id") ON DELETE CASCADE
        )
    """)
    cursor.execute("""
        CREATE TABLE "kpi_management_dashboardsettings_allowed_users" (
            "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
            "dashboardsettings_id" bigint NOT NULL REFERENCES "kpi_management_dashboardsettings" ("id") ON DELETE CASCADE,
            "user_id" integer NOT NULL REFERENCES "auth_user" ("id") ON DELETE CASCADE,
            UNIQUE("dashboardsettings_id", "user_id")
        )
    """)
    print("   ✓ DashboardSettings table created")
else:
    print("   ✓ DashboardSettings table already exists")

# 2. Check and create Report table
print("\n2. Checking Report table...")
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='kpi_management_report'")
if not cursor.fetchone():
    print("   Creating kpi_management_report table...")
    cursor.execute("""
        CREATE TABLE "kpi_management_report" (
            "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
            "title" varchar(200) NOT NULL,
            "report_type" varchar(50) NOT NULL,
            "period" varchar(20) NOT NULL DEFAULT 'monthly',
            "start_date" date NULL,
            "end_date" date NULL,
            "performance_type" varchar(100) NULL,
            "report_data" text NOT NULL DEFAULT '{}',
            "charts_data" text NOT NULL DEFAULT '{}',
            "pdf_file" varchar(100) NULL,
            "excel_file" varchar(100) NULL,
            "auto_generate" bool NOT NULL DEFAULT 0,
            "last_generated" datetime NULL,
            "created_at" datetime NOT NULL,
            "updated_at" datetime NOT NULL,
            "brand_filter_id" integer NULL REFERENCES "kpi_management_collabbrand" ("id") ON DELETE SET NULL,
            "campaign_filter_id" integer NULL REFERENCES "kpi_management_campaign" ("id") ON DELETE SET NULL,
            "created_by_id" integer NULL REFERENCES "auth_user" ("id") ON DELETE SET NULL
        )
    """)
    print("   ✓ Report table created")
else:
    print("   ✓ Report table already exists")

# 3. Check and create AuditLog table
print("\n3. Checking AuditLog table...")
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='kpi_management_auditlog'")
if not cursor.fetchone():
    print("   Creating kpi_management_auditlog table...")
    cursor.execute("""
        CREATE TABLE "kpi_management_auditlog" (
            "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
            "action" varchar(20) NOT NULL,
            "target_type" varchar(100) NULL,
            "target_id" integer NULL,
            "target_name" varchar(200) NULL,
            "description" text NULL,
            "old_data" text NOT NULL DEFAULT '{}',
            "new_data" text NOT NULL DEFAULT '{}',
            "ip_address" varchar(39) NULL,
            "user_agent" text NULL,
            "created_at" datetime NOT NULL,
            "user_id" integer NULL REFERENCES "auth_user" ("id") ON DELETE SET NULL
        )
    """)
    # Create indexes
    cursor.execute("CREATE INDEX IF NOT EXISTS kpi_manage_created_idx ON kpi_management_auditlog(created_at DESC)")
    cursor.execute("CREATE INDEX IF NOT EXISTS kpi_manage_user_cr_idx ON kpi_management_auditlog(user_id, created_at DESC)")
    cursor.execute("CREATE INDEX IF NOT EXISTS kpi_manage_action_idx ON kpi_management_auditlog(action, created_at DESC)")
    print("   ✓ AuditLog table created with indexes")
else:
    print("   ✓ AuditLog table already exists")

# 4. Check and create FeedReelsHistory table
print("\n4. Checking FeedReelsHistory table...")
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='kpi_management_feedreelshistory'")
if not cursor.fetchone():
    print("   Creating kpi_management_feedreelshistory table...")
    cursor.execute("""
        CREATE TABLE "kpi_management_feedreelshistory" (
            "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
            "update_type" varchar(50) NOT NULL,
            "old_value" text NULL,
            "new_value" text NULL,
            "notes" text NULL,
            "created_at" datetime NOT NULL,
            "feed_reels_id" bigint NOT NULL REFERENCES "kpi_management_dailyfeedreels" ("id") ON DELETE CASCADE,
            "updated_by_id" integer NULL REFERENCES "auth_user" ("id") ON DELETE SET NULL
        )
    """)
    print("   ✓ FeedReelsHistory table created")
else:
    print("   ✓ FeedReelsHistory table already exists")

# 5. Check and add missing columns to Profile
print("\n5. Checking Profile table columns...")
cursor.execute("PRAGMA table_info(kpi_management_profile)")
existing_cols = [row[1] for row in cursor.fetchall()]
print(f"   Existing columns: {existing_cols}")

missing_cols = {
    'brand_name': 'TEXT',
    'logo': 'TEXT',
    'platform_linked': 'TEXT',
    'category': 'TEXT',
    'audience_segment': 'TEXT',
    'performance_rating': 'REAL DEFAULT 0.0',
    'contact_info': 'TEXT'
}

for col_name, col_type in missing_cols.items():
    if col_name not in existing_cols:
        try:
            print(f"   Adding {col_name} column...")
            cursor.execute(f"ALTER TABLE kpi_management_profile ADD COLUMN {col_name} {col_type}")
            print(f"   ✓ {col_name} added")
        except Exception as e:
            print(f"   ✗ Error adding {col_name}: {e}")

# 6. Check and add missing columns to DailyFeedReels
print("\n6. Checking DailyFeedReels table columns...")
cursor.execute("PRAGMA table_info(kpi_management_dailyfeedreels)")
existing_cols = [row[1] for row in cursor.fetchall()]

if 'format_type' not in existing_cols:
    try:
        print("   Adding format_type column...")
        cursor.execute("ALTER TABLE kpi_management_dailyfeedreels ADD COLUMN format_type TEXT DEFAULT 'image'")
        print("   ✓ format_type added")
    except Exception as e:
        print(f"   ✗ Error adding format_type: {e}")

if 'target_post_date' not in existing_cols:
    try:
        print("   Adding target_post_date column...")
        cursor.execute("ALTER TABLE kpi_management_dailyfeedreels ADD COLUMN target_post_date datetime NULL")
        print("   ✓ target_post_date added")
    except Exception as e:
        print(f"   ✗ Error adding target_post_date: {e}")

# 7. Check and add missing columns to FYPPostValue
print("\n7. Checking FYPPostValue table columns...")
cursor.execute("PRAGMA table_info(kpi_management_fyppostvalue)")
existing_cols = [row[1] for row in cursor.fetchall()]

missing_fyp_cols = {
    'view_milestone': 'TEXT',
    'hashtags_used': 'TEXT',
    'audio_trending': 'TEXT',
    'niche': 'TEXT',
    'timing': 'TEXT',
    'best_practice_note': 'TEXT',
    'fyp_views': 'INTEGER DEFAULT 0',
    'fyp_percentage': 'REAL DEFAULT 0.0',
    'engagement_value': 'DECIMAL(10,2) DEFAULT 0.00',
    'estimated_reach': 'INTEGER DEFAULT 0',
    'viral_score': 'REAL DEFAULT 0.0',
}

for col_name, col_type in missing_fyp_cols.items():
    if col_name not in existing_cols:
        try:
            print(f"   Adding {col_name} column...")
            cursor.execute(f"ALTER TABLE kpi_management_fyppostvalue ADD COLUMN {col_name} {col_type}")
            print(f"   ✓ {col_name} added")
        except Exception as e:
            print(f"   ✗ Error adding {col_name}: {e}")

# 5. Check and create SystemSettings table
print("\n5. Checking SystemSettings table...")
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='kpi_management_systemsettings'")
if not cursor.fetchone():
    print("   Creating kpi_management_systemsettings table...")
    cursor.execute("""
        CREATE TABLE "kpi_management_systemsettings" (
            "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
            "name" varchar(200) NOT NULL UNIQUE,
            "label" varchar(200) NOT NULL,
            "setting_type" varchar(50) NOT NULL DEFAULT 'general',
            "value" text NULL,
            "value_type" varchar(20) NOT NULL DEFAULT 'text',
            "description" text NULL,
            "is_active" bool NOT NULL DEFAULT 1,
            "is_public" bool NOT NULL DEFAULT 0,
            "created_at" datetime NOT NULL,
            "updated_at" datetime NOT NULL,
            "created_by_id" integer NULL REFERENCES "auth_user" ("id") ON DELETE SET NULL
        )
    """)
    cursor.execute("CREATE INDEX IF NOT EXISTS kpi_manage_system_name_idx ON kpi_management_systemsettings(name)")
    cursor.execute("CREATE INDEX IF NOT EXISTS kpi_manage_system_type_active_idx ON kpi_management_systemsettings(setting_type, is_active)")
    print("   ✓ kpi_management_systemsettings table created")
else:
    print("   ✓ kpi_management_systemsettings table already exists")

# Commit all changes
conn.commit()
print("\n" + "=" * 60)
print("✅ SEMUA PERBAIKAN DATABASE SELESAI!")
print("=" * 60)

# Final verification
print("\nVerifikasi akhir:")
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'kpi_management_%'")
all_tables = sorted([row[0] for row in cursor.fetchall()])
print(f"Total tabel kpi_management: {len(all_tables)}")
for table in all_tables:
    print(f"  ✓ {table}")

conn.close()


