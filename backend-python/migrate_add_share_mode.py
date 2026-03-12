#!/usr/bin/env python3
"""
Database Migration: Add share_mode column to shared_files table
"""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / 'pqc_files.db'

def migrate():
    print("🔄 Starting database migration...")
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Check if column already exists
    c.execute("PRAGMA table_info(shared_files)")
    columns = [row[1] for row in c.fetchall()]
    
    if 'share_mode' in columns:
        print("✅ Column 'share_mode' already exists. No migration needed.")
        conn.close()
        return
    
    # Add share_mode column with default value 'download'
    try:
        c.execute("ALTER TABLE shared_files ADD COLUMN share_mode TEXT DEFAULT 'download'")
        conn.commit()
        print("✅ Successfully added 'share_mode' column to shared_files table")
        print("   Default value: 'download' (existing files remain downloadable)")
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    migrate()
