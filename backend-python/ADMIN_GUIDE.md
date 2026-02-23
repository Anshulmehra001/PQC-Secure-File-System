# 🔐 PQC File System - Admin Guide

## Admin Tools Overview

You have two admin tools to manage your file system:

1. **admin.py** - Interactive CLI for manual management
2. **auto_cleanup.py** - Automatic background cleanup service

---

## 🛠️ Tool 1: Admin CLI (`admin.py`)

### What It Does:
- View system statistics
- List all files in database
- Find orphaned files (files on disk but not in database)
- Cleanup orphaned files
- Delete expired shared files
- Empty trash bin

### How to Use:

```bash
cd /mnt/d/PQC\ App/backend-python
source venv/bin/activate
python3 admin.py
```

### Menu Options:

#### 1. 📊 Show Statistics
- Total users
- Cloud files count and size
- Shared files (active vs expired)
- Disk usage breakdown

#### 2. 📁 List All Files
- Shows all cloud storage files with owner
- Shows all shared files with expiration status
- Useful for auditing

#### 3. 🔍 Find Orphaned Files
- Scans `storage/` and `uploads/` directories
- Finds files that exist on disk but not in database
- Shows wasted disk space

#### 4. 🧹 Cleanup Orphaned Files
- **PERMANENTLY DELETES** orphaned files
- Requires typing 'DELETE' to confirm
- Frees up disk space

#### 5. 🗑️ Cleanup Expired Shares
- Finds all expired shared files
- Deletes both file and database entry
- Requires 'yes' confirmation

#### 6. 🗑️ Empty Trash
- Shows all files in trash bin
- **PERMANENTLY DELETES** everything in trash
- Requires typing 'EMPTY' to confirm

---

## 🤖 Tool 2: Auto Cleanup Service (`auto_cleanup.py`)

### What It Does:
- Runs automatically in the background
- Cleans up expired shares daily
- Removes orphaned files
- Deletes trash files older than 30 days
- Logs all actions to `cleanup.log`

### How to Start:

```bash
cd /mnt/d/PQC\ App/backend-python
source venv/bin/activate

# Install schedule package
pip install schedule

# Run in background
nohup python3 auto_cleanup.py > cleanup_output.log 2>&1 &
```

### Schedule:
- Runs every day at **2:00 AM**
- Also runs once immediately on startup

### What Gets Cleaned:
1. **Expired Shares**: Files past expiration date
2. **Orphaned Files**: Files on disk without database entry
3. **Old Trash**: Files in trash older than 30 days

### Check Logs:

```bash
# View cleanup log
tail -f cleanup.log

# View service output
tail -f cleanup_output.log
```

### Stop Service:

```bash
# Find process ID
ps aux | grep auto_cleanup.py

# Kill process
kill <PID>
```

---

## 🗑️ Trash Bin System

### How It Works:
- When users delete files, they go to `trash/` folder
- Files stay in trash for 30 days
- After 30 days, auto cleanup permanently deletes them
- You can manually empty trash anytime with admin.py

### Trash File Format:
```
trash/
  1738339200_4020addd-c623-4a58-8226-78921ddcf105_filename.enc
  └─ timestamp_fileid_originalname.enc
```

### Restore from Trash:
Currently not implemented in UI, but you can manually:
1. Find file in `trash/` folder
2. Move it back to `storage/` or `uploads/`
3. Update database filepath

---

## 📋 Common Admin Tasks

### Clean Up Everything:
```bash
python3 admin.py
# Select: 4 (Cleanup Orphaned)
# Select: 5 (Cleanup Expired)
# Select: 6 (Empty Trash)
```

### Check Disk Usage:
```bash
python3 admin.py
# Select: 1 (Show Statistics)
```

### Find What's Taking Space:
```bash
python3 admin.py
# Select: 3 (Find Orphaned Files)
```

### Manual Database Cleanup:
```bash
cd /mnt/d/PQC\ App/backend-python
sqlite3 pqc_files.db

-- See all tables
.tables

-- Count files
SELECT COUNT(*) FROM cloud_files;
SELECT COUNT(*) FROM shared_files;

-- Find expired shares
SELECT * FROM shared_files WHERE expires_at < strftime('%s', 'now') * 1000;

-- Delete specific file
DELETE FROM cloud_files WHERE id = 'file-id-here';

-- Exit
.quit
```

---

## ⚠️ Important Notes

### Orphaned Files Happen When:
1. Server crashes during upload
2. Database gets corrupted
3. Manual file deletion without database update
4. Failed delete operations

### Prevent Data Loss:
1. Always use admin.py for cleanup (has confirmations)
2. Check statistics before cleanup
3. Review orphaned files list before deleting
4. Keep auto_cleanup.py running for maintenance

### Backup Before Cleanup:
```bash
# Backup database
cp pqc_files.db pqc_files.db.backup

# Backup files
tar -czf files_backup.tar.gz storage/ uploads/ trash/
```

---

## 🔧 Troubleshooting

### "Database is locked" error:
- Stop the Flask app first
- Make sure no other admin.py is running

### Files not deleting:
- Check file permissions
- Make sure you're running as correct user
- Check if files are in use

### Auto cleanup not running:
```bash
# Check if process is running
ps aux | grep auto_cleanup

# Check logs for errors
tail -50 cleanup.log
```

---

## 📊 Monitoring

### Daily Checks:
```bash
# Check cleanup log
tail -20 cleanup.log

# Check disk usage
du -sh storage/ uploads/ trash/

# Check database size
ls -lh pqc_files.db
```

### Weekly Tasks:
- Review statistics
- Check for orphaned files
- Verify trash is being cleaned

### Monthly Tasks:
- Backup database
- Review user accounts
- Check total disk usage

---

## 🚀 Production Deployment

### Setup Auto Cleanup as System Service:

Create `/etc/systemd/system/pqc-cleanup.service`:
```ini
[Unit]
Description=PQC File System Auto Cleanup
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/mnt/d/PQC App/backend-python
ExecStart=/mnt/d/PQC App/backend-python/venv/bin/python3 auto_cleanup.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable pqc-cleanup
sudo systemctl start pqc-cleanup
sudo systemctl status pqc-cleanup
```

---

## 📞 Need Help?

Check the logs:
- `cleanup.log` - Auto cleanup actions
- `cleanup_output.log` - Service output
- Flask logs - Application errors

Common issues are usually:
- Permission problems
- Database locks
- Disk space full
