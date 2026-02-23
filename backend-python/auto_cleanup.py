#!/usr/bin/env python3
"""
PQC File System - Automatic Cleanup Service
Runs periodically to clean up expired files and orphaned data
"""

import sqlite3
import os
import time
from pathlib import Path
import schedule
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('cleanup.log'),
        logging.StreamHandler()
    ]
)

DB_PATH = Path(__file__).parent / 'pqc_files.db'
STORAGE_DIR = Path(__file__).parent / 'storage'
UPLOADS_DIR = Path(__file__).parent / 'uploads'
TRASH_DIR = Path(__file__).parent / 'trash'

# Ensure trash directory exists
TRASH_DIR.mkdir(exist_ok=True)

def cleanup_expired_shares():
    """Delete expired shared files automatically"""
    logging.info("🧹 Starting cleanup of expired shares...")
    
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        current_time = int(time.time() * 1000)
        
        # Find expired files
        c.execute("""
            SELECT id, filename, filepath
            FROM shared_files
            WHERE expires_at < ?
        """, (current_time,))
        
        expired_files = c.fetchall()
        
        if not expired_files:
            logging.info("✅ No expired files found")
            conn.close()
            return
        
        deleted_count = 0
        for file_id, filename, filepath in expired_files:
            try:
                # Delete file from disk
                file_path = Path(filepath)
                if file_path.exists():
                    file_path.unlink()
                    logging.info(f"  ✓ Deleted file: {filename}")
                
                # Delete from database
                c.execute("DELETE FROM shared_files WHERE id = ?", (file_id,))
                deleted_count += 1
            except Exception as e:
                logging.error(f"  ✗ Failed to delete {filename}: {e}")
        
        conn.commit()
        conn.close()
        
        logging.info(f"✅ Cleanup complete: Deleted {deleted_count} expired files")
    
    except Exception as e:
        logging.error(f"❌ Cleanup failed: {e}")

def cleanup_old_trash():
    """Delete files from trash older than 30 days"""
    logging.info("🗑️  Starting cleanup of old trash files...")
    
    try:
        if not TRASH_DIR.exists():
            logging.info("✅ Trash directory doesn't exist")
            return
        
        current_time = time.time()
        thirty_days_ago = current_time - (30 * 24 * 60 * 60)
        
        deleted_count = 0
        total_size = 0
        
        for file in TRASH_DIR.glob('*'):
            try:
                # Extract timestamp from filename (format: timestamp_fileid_filename.enc)
                parts = file.name.split('_', 1)
                if len(parts) < 2:
                    continue
                
                file_timestamp = int(parts[0])
                
                if file_timestamp < thirty_days_ago:
                    file_size = file.stat().st_size
                    file.unlink()
                    deleted_count += 1
                    total_size += file_size
                    logging.info(f"  ✓ Deleted old trash: {file.name}")
            
            except Exception as e:
                logging.error(f"  ✗ Failed to delete {file.name}: {e}")
        
        if deleted_count > 0:
            logging.info(f"✅ Deleted {deleted_count} old files from trash ({total_size / (1024 * 1024):.2f}MB freed)")
        else:
            logging.info("✅ No old trash files to delete")
    
    except Exception as e:
        logging.error(f"❌ Trash cleanup failed: {e}")

def cleanup_orphaned_files():
    """Delete files on disk that aren't in database"""
    logging.info("🔍 Starting cleanup of orphaned files...")
    
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        # Get all file IDs from database
        c.execute("SELECT id FROM cloud_files")
        cloud_ids = {row[0] for row in c.fetchall()}
        
        c.execute("SELECT id FROM shared_files")
        shared_ids = {row[0] for row in c.fetchall()}
        
        conn.close()
        
        deleted_count = 0
        total_size = 0
        
        # Check storage directory
        if STORAGE_DIR.exists():
            for file in STORAGE_DIR.glob('*.enc'):
                file_id = file.stem
                if file_id not in cloud_ids:
                    try:
                        file_size = file.stat().st_size
                        file.unlink()
                        deleted_count += 1
                        total_size += file_size
                        logging.info(f"  ✓ Deleted orphaned storage file: {file.name}")
                    except Exception as e:
                        logging.error(f"  ✗ Failed to delete {file.name}: {e}")
        
        # Check uploads directory
        if UPLOADS_DIR.exists():
            for file in UPLOADS_DIR.glob('*.enc'):
                file_id = file.stem
                if file_id not in shared_ids:
                    try:
                        file_size = file.stat().st_size
                        file.unlink()
                        deleted_count += 1
                        total_size += file_size
                        logging.info(f"  ✓ Deleted orphaned upload file: {file.name}")
                    except Exception as e:
                        logging.error(f"  ✗ Failed to delete {file.name}: {e}")
        
        if deleted_count > 0:
            logging.info(f"✅ Deleted {deleted_count} orphaned files ({total_size / (1024 * 1024):.2f}MB freed)")
        else:
            logging.info("✅ No orphaned files found")
    
    except Exception as e:
        logging.error(f"❌ Orphaned files cleanup failed: {e}")

def run_all_cleanups():
    """Run all cleanup tasks"""
    logging.info("="*60)
    logging.info("🚀 Starting automatic cleanup service")
    logging.info("="*60)
    
    cleanup_expired_shares()
    cleanup_orphaned_files()
    cleanup_old_trash()
    
    logging.info("="*60)
    logging.info("✅ All cleanup tasks completed")
    logging.info("="*60)

if __name__ == '__main__':
    logging.info("🔐 PQC File System - Auto Cleanup Service Started")
    logging.info("📅 Schedule: Every day at 2:00 AM")
    logging.info("Press Ctrl+C to stop")
    
    # Schedule cleanup tasks
    schedule.every().day.at("02:00").do(run_all_cleanups)
    
    # Run once immediately on startup
    run_all_cleanups()
    
    # Keep running
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute
