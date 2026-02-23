#!/usr/bin/env python3
"""
PQC File System - Admin CLI Tool
Manage files, cleanup, and database maintenance
"""

import sqlite3
import os
import time
from pathlib import Path
import shutil

DB_PATH = Path(__file__).parent / 'pqc_files.db'
STORAGE_DIR = Path(__file__).parent / 'storage'
UPLOADS_DIR = Path(__file__).parent / 'uploads'
TRASH_DIR = Path(__file__).parent / 'trash'

# Ensure trash directory exists
TRASH_DIR.mkdir(exist_ok=True)

def get_db():
    return sqlite3.connect(DB_PATH)

def print_header(text):
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)

def list_all_files():
    """List all files in database"""
    print_header("📁 ALL FILES IN DATABASE")
    
    conn = get_db()
    c = conn.cursor()
    
    # Cloud files
    c.execute("""
        SELECT cf.id, cf.filename, cf.size, cf.created_at, u.username
        FROM cloud_files cf
        JOIN users u ON cf.user_id = u.id
        ORDER BY cf.created_at DESC
    """)
    cloud_files = c.fetchall()
    
    # Shared files
    c.execute("""
        SELECT id, filename, expires_at, created_at
        FROM shared_files
        ORDER BY created_at DESC
    """)
    shared_files = c.fetchall()
    
    print(f"\n☁️  CLOUD STORAGE FILES: {len(cloud_files)}")
    print("-" * 60)
    for file_id, filename, size, created_at, username in cloud_files:
        size_mb = size / (1024 * 1024)
        created = time.strftime('%Y-%m-%d %H:%M', time.localtime(created_at/1000))
        print(f"  {file_id[:8]}... | {filename[:30]:30} | {size_mb:.2f}MB | {username} | {created}")
    
    print(f"\n🔗 SHARED FILES: {len(shared_files)}")
    print("-" * 60)
    for file_id, filename, expires_at, created_at in shared_files:
        expires = time.strftime('%Y-%m-%d %H:%M', time.localtime(expires_at/1000))
        created = time.strftime('%Y-%m-%d %H:%M', time.localtime(created_at/1000))
        expired = "❌ EXPIRED" if expires_at < time.time() * 1000 else "✅ ACTIVE"
        print(f"  {file_id[:8]}... | {filename[:30]:30} | {expired} | Exp: {expires}")
    
    conn.close()

def find_orphaned_files():
    """Find files on disk that aren't in database"""
    print_header("🔍 FINDING ORPHANED FILES")
    
    conn = get_db()
    c = conn.cursor()
    
    # Get all file IDs from database
    c.execute("SELECT id FROM cloud_files")
    cloud_ids = {row[0] for row in c.fetchall()}
    
    c.execute("SELECT id FROM shared_files")
    shared_ids = {row[0] for row in c.fetchall()}
    
    conn.close()
    
    # Check storage directory
    orphaned_storage = []
    if STORAGE_DIR.exists():
        for file in STORAGE_DIR.glob('*.enc'):
            file_id = file.stem
            if file_id not in cloud_ids:
                orphaned_storage.append(file)
    
    # Check uploads directory
    orphaned_uploads = []
    if UPLOADS_DIR.exists():
        for file in UPLOADS_DIR.glob('*.enc'):
            file_id = file.stem
            if file_id not in shared_ids:
                orphaned_uploads.append(file)
    
    print(f"\n📦 Orphaned files in storage/: {len(orphaned_storage)}")
    for file in orphaned_storage:
        size_mb = file.stat().st_size / (1024 * 1024)
        print(f"  {file.name} ({size_mb:.2f}MB)")
    
    print(f"\n📤 Orphaned files in uploads/: {len(orphaned_uploads)}")
    for file in orphaned_uploads:
        size_mb = file.stat().st_size / (1024 * 1024)
        print(f"  {file.name} ({size_mb:.2f}MB)")
    
    total_size = sum(f.stat().st_size for f in orphaned_storage + orphaned_uploads)
    print(f"\n💾 Total wasted space: {total_size / (1024 * 1024):.2f}MB")
    
    return orphaned_storage, orphaned_uploads

def cleanup_orphaned_files():
    """Delete orphaned files from disk"""
    orphaned_storage, orphaned_uploads = find_orphaned_files()
    
    if not orphaned_storage and not orphaned_uploads:
        print("\n✅ No orphaned files found!")
        return
    
    print("\n⚠️  WARNING: This will permanently delete orphaned files!")
    confirm = input("Type 'DELETE' to confirm: ")
    
    if confirm != 'DELETE':
        print("❌ Cancelled")
        return
    
    deleted_count = 0
    for file in orphaned_storage + orphaned_uploads:
        try:
            file.unlink()
            deleted_count += 1
            print(f"  ✓ Deleted: {file.name}")
        except Exception as e:
            print(f"  ✗ Failed to delete {file.name}: {e}")
    
    print(f"\n✅ Deleted {deleted_count} orphaned files")

def cleanup_expired_shares():
    """Delete expired shared files"""
    print_header("🧹 CLEANING UP EXPIRED SHARES")
    
    conn = get_db()
    c = conn.cursor()
    
    current_time = int(time.time() * 1000)
    
    # Find expired files
    c.execute("""
        SELECT id, filename, filepath, expires_at
        FROM shared_files
        WHERE expires_at < ?
    """, (current_time,))
    
    expired_files = c.fetchall()
    
    if not expired_files:
        print("\n✅ No expired files found!")
        conn.close()
        return
    
    print(f"\n📋 Found {len(expired_files)} expired files:")
    for file_id, filename, filepath, expires_at in expired_files:
        expired_date = time.strftime('%Y-%m-%d %H:%M', time.localtime(expires_at/1000))
        print(f"  {file_id[:8]}... | {filename[:40]:40} | Expired: {expired_date}")
    
    confirm = input(f"\n⚠️  Delete {len(expired_files)} expired files? (yes/no): ")
    
    if confirm.lower() != 'yes':
        print("❌ Cancelled")
        conn.close()
        return
    
    deleted_count = 0
    for file_id, filename, filepath, expires_at in expired_files:
        try:
            # Delete file from disk
            file_path = Path(filepath)
            if file_path.exists():
                file_path.unlink()
            
            # Delete from database
            c.execute("DELETE FROM shared_files WHERE id = ?", (file_id,))
            deleted_count += 1
            print(f"  ✓ Deleted: {filename}")
        except Exception as e:
            print(f"  ✗ Failed to delete {filename}: {e}")
    
    conn.commit()
    conn.close()
    
    print(f"\n✅ Deleted {deleted_count} expired files")

def move_to_trash(file_id, file_type='cloud'):
    """Move file to trash instead of permanent delete"""
    conn = get_db()
    c = conn.cursor()
    
    if file_type == 'cloud':
        c.execute("SELECT filename, filepath FROM cloud_files WHERE id = ?", (file_id,))
    else:
        c.execute("SELECT filename, filepath FROM shared_files WHERE id = ?", (file_id,))
    
    result = c.fetchone()
    if not result:
        print(f"❌ File {file_id} not found in database")
        conn.close()
        return False
    
    filename, filepath = result
    file_path = Path(filepath)
    
    if not file_path.exists():
        print(f"❌ File not found on disk: {filepath}")
        conn.close()
        return False
    
    # Move to trash with timestamp
    timestamp = int(time.time())
    trash_filename = f"{timestamp}_{file_id}_{file_path.name}"
    trash_path = TRASH_DIR / trash_filename
    
    try:
        shutil.move(str(file_path), str(trash_path))
        
        # Update database to mark as deleted
        if file_type == 'cloud':
            c.execute("UPDATE cloud_files SET filepath = ? WHERE id = ?", 
                     (str(trash_path), file_id))
        else:
            c.execute("UPDATE shared_files SET filepath = ? WHERE id = ?", 
                     (str(trash_path), file_id))
        
        conn.commit()
        print(f"✅ Moved to trash: {filename}")
        return True
    except Exception as e:
        print(f"❌ Failed to move to trash: {e}")
        return False
    finally:
        conn.close()

def empty_trash():
    """Permanently delete all files in trash"""
    print_header("🗑️  EMPTY TRASH")
    
    if not TRASH_DIR.exists():
        print("✅ Trash is already empty!")
        return
    
    trash_files = list(TRASH_DIR.glob('*'))
    
    if not trash_files:
        print("✅ Trash is empty!")
        return
    
    total_size = sum(f.stat().st_size for f in trash_files)
    print(f"\n📋 Trash contains {len(trash_files)} files ({total_size / (1024 * 1024):.2f}MB)")
    
    for file in trash_files[:10]:  # Show first 10
        size_mb = file.stat().st_size / (1024 * 1024)
        print(f"  {file.name} ({size_mb:.2f}MB)")
    
    if len(trash_files) > 10:
        print(f"  ... and {len(trash_files) - 10} more files")
    
    confirm = input("\n⚠️  PERMANENTLY DELETE ALL? Type 'EMPTY' to confirm: ")
    
    if confirm != 'EMPTY':
        print("❌ Cancelled")
        return
    
    deleted_count = 0
    for file in trash_files:
        try:
            file.unlink()
            deleted_count += 1
        except Exception as e:
            print(f"  ✗ Failed to delete {file.name}: {e}")
    
    print(f"\n✅ Permanently deleted {deleted_count} files")

def show_stats():
    """Show database and storage statistics"""
    print_header("📊 SYSTEM STATISTICS")
    
    conn = get_db()
    c = conn.cursor()
    
    # User stats
    c.execute("SELECT COUNT(*) FROM users")
    user_count = c.fetchone()[0]
    
    # Cloud files stats
    c.execute("SELECT COUNT(*), SUM(size) FROM cloud_files")
    cloud_count, cloud_size = c.fetchone()
    cloud_size = cloud_size or 0
    
    # Shared files stats
    c.execute("SELECT COUNT(*) FROM shared_files")
    shared_count = c.fetchone()[0]
    
    # Expired shares
    current_time = int(time.time() * 1000)
    c.execute("SELECT COUNT(*) FROM shared_files WHERE expires_at < ?", (current_time,))
    expired_count = c.fetchone()[0]
    
    conn.close()
    
    # Disk usage
    storage_size = sum(f.stat().st_size for f in STORAGE_DIR.glob('*.enc')) if STORAGE_DIR.exists() else 0
    uploads_size = sum(f.stat().st_size for f in UPLOADS_DIR.glob('*.enc')) if UPLOADS_DIR.exists() else 0
    trash_size = sum(f.stat().st_size for f in TRASH_DIR.glob('*')) if TRASH_DIR.exists() else 0
    
    print(f"\n👥 Users: {user_count}")
    print(f"☁️  Cloud Files: {cloud_count} ({cloud_size / (1024 * 1024):.2f}MB)")
    print(f"🔗 Shared Files: {shared_count} (Active: {shared_count - expired_count}, Expired: {expired_count})")
    print(f"\n💾 Disk Usage:")
    print(f"  storage/: {storage_size / (1024 * 1024):.2f}MB")
    print(f"  uploads/: {uploads_size / (1024 * 1024):.2f}MB")
    print(f"  trash/:   {trash_size / (1024 * 1024):.2f}MB")
    print(f"  TOTAL:    {(storage_size + uploads_size + trash_size) / (1024 * 1024):.2f}MB")

def main_menu():
    """Main admin menu"""
    while True:
        print_header("🔐 PQC FILE SYSTEM - ADMIN PANEL")
        print("\n1. 📊 Show Statistics")
        print("2. 📁 List All Files")
        print("3. 🔍 Find Orphaned Files")
        print("4. 🧹 Cleanup Orphaned Files")
        print("5. 🗑️  Cleanup Expired Shares")
        print("6. 🗑️  Empty Trash")
        print("7. ❌ Exit")
        
        choice = input("\nSelect option (1-7): ").strip()
        
        if choice == '1':
            show_stats()
        elif choice == '2':
            list_all_files()
        elif choice == '3':
            find_orphaned_files()
        elif choice == '4':
            cleanup_orphaned_files()
        elif choice == '5':
            cleanup_expired_shares()
        elif choice == '6':
            empty_trash()
        elif choice == '7':
            print("\n👋 Goodbye!")
            break
        else:
            print("❌ Invalid option")
        
        input("\nPress Enter to continue...")

if __name__ == '__main__':
    main_menu()
