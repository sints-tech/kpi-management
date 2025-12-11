#!/usr/bin/env python
"""Script untuk membuat tabel Company secara langsung"""
import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection

def create_company_table():
    cursor = connection.cursor()

    # Cek apakah tabel sudah ada
    cursor.execute("""
        SELECT name FROM sqlite_master
        WHERE type='table' AND name='kpi_management_company'
    """)

    if cursor.fetchone():
        print("Tabel kpi_management_company sudah ada")
        return

    # Buat tabel Company
    cursor.execute("""
        CREATE TABLE kpi_management_company (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(200) NOT NULL,
            company_type VARCHAR(20) NOT NULL,
            code VARCHAR(50) UNIQUE NOT NULL,
            address TEXT,
            phone VARCHAR(20),
            email VARCHAR(254),
            is_active BOOLEAN NOT NULL DEFAULT 1,
            notes TEXT,
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            parent_company_id INTEGER REFERENCES kpi_management_company(id)
        )
    """)
    print("✓ Tabel kpi_management_company berhasil dibuat")

    # Tambahkan kolom company_id ke tabel lain
    tables_to_update = [
        'kpi_management_campaign',
        'kpi_management_story',
        'kpi_management_dailyfeedreels',
        'kpi_management_socialmediaaccount'
    ]

    for table in tables_to_update:
        try:
            cursor.execute(f"SELECT * FROM {table} LIMIT 1")
            # Cek apakah kolom company_id sudah ada
            cursor.execute(f"PRAGMA table_info({table})")
            columns = [row[1] for row in cursor.fetchall()]

            if 'company_id' not in columns:
                cursor.execute(f"ALTER TABLE {table} ADD COLUMN company_id INTEGER")
                print(f"✓ Kolom company_id ditambahkan ke {table}")
            else:
                print(f"- Kolom company_id sudah ada di {table}")
        except Exception as e:
            print(f"⚠ {table}: {e}")

    # Commit changes
    connection.commit()
    print("\n✓ Semua perubahan telah disimpan ke database")

if __name__ == "__main__":
    try:
        create_company_table()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)



