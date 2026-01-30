# 🛠️ Complete Setup Guide

Step-by-step guide to install and run the PQC Secure File System on Windows with WSL2.

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [WSL2 Setup](#wsl2-setup)
3. [Install Dependencies](#install-dependencies)
4. [Install liboqs](#install-liboqs)
5. [Setup Python Environment](#setup-python-environment)
6. [Setup Frontend](#setup-frontend)
7. [Running the Application](#running-the-application)
8. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### System Requirements

- **Operating System**: Windows 10/11 (64-bit)
- **RAM**: 4 GB minimum (8 GB recommended)
- **Disk Space**: 5 GB free space
- **Internet**: Required for downloading dependencies

### Software Requirements

- Windows Subsystem for Linux 2 (WSL2)
- Ubuntu 24.04 LTS (or similar)
- Python 3.12+
- Node.js 18+
- Git

---

## WSL2 Setup

### Step 1: Enable WSL2

Open **PowerShell as Administrator** and run:

```powershell
wsl --install
```

This installs:
- WSL2
- Ubuntu (default distribution)
- Virtual Machine Platform

**Restart your computer** after installation.

### Step 2: Verify WSL Installation

```powershell
wsl --list --verbose
```

Expected output:
```
  NAME      STATE           VERSION
* Ubuntu    Running         2
```

### Step 3: Set Default WSL Version

```powershell
wsl --set-default-version 2
```

### Step 4: Install Ubuntu (if not installed)

```powershell
wsl --install -d Ubuntu
```

### Step 5: First Launch

Launch Ubuntu from Start Menu. You'll be asked to:

1. **Create username**: Enter your username (e.g., `anshul`)
2. **Create password**: Enter a password (you'll need this for sudo)
3. **Confirm password**: Re-enter password

### Step 6: Update Ubuntu

```bash
sudo apt update
sudo apt upgrade -y
```

### WSL2 Storage Location

By default, WSL2 stores data in:
```
C:\Users\[YourName]\AppData\Local\Packages\CanonicalGroupLimited.Ubuntu...\LocalState\ext4.vhdx
```

To use D: drive instead, you can move the VHDX file or mount D: drive in WSL.

### Accessing Windows Files from WSL

Windows drives are mounted at `/mnt/`:
- C: drive → `/mnt/c/`
- D: drive → `/mnt/d/`

Example:
```bash
cd "/mnt/d/PQC App"
```

---

## Install Dependencies

### Step 1: Install Build Tools

```bash
sudo apt update
sudo apt install -y build-essential cmake git wget
```

**What this installs:**
- `build-essential`: GCC compiler, make, etc.
- `cmake`: Build system for liboqs
- `git`: Version control
- `wget`: Download tool

### Step 2: Install Python Development Tools

```bash
sudo apt install -y python3 python3-pip python3-venv python3-dev
```

**What this installs:**
- `python3`: Python interpreter
- `python3-pip`: Package installer
- `python3-venv`: Virtual environment support
- `python3-dev`: Development headers

### Step 3: Install Node.js

```bash
# Install Node.js 20.x
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs
```

**Verify installation:**
```bash
node --version   # Should show v20.x.x
npm --version    # Should show 10.x.x
```

### Step 4: Install Additional Libraries

```bash
sudo apt install -y libssl-dev pkg-config
```

**What this installs:**
- `libssl-dev`: OpenSSL development files
- `pkg-config`: Helper tool for compiling

---

## Install liboqs

liboqs is the **Open Quantum Safe** library that provides real PQC algorithms.

### Step 1: Clone liboqs Repository

```bash
cd ~
git clone --branch 0.15.0 https://github.com/open-quantum-safe/liboqs.git
cd liboqs
```

**Why version 0.15.0?**
- Latest stable release
- Includes ML-DSA-44 (renamed from Dilithium2)
- Compatible with liboqs-python 0.14.1

### Step 2: Create Build Directory

```bash
mkdir build
cd build
```

### Step 3: Configure Build

```bash
cmake -DCMAKE_INSTALL_PREFIX=/usr/local \
      -DBUILD_SHARED_LIBS=ON \
      -DOQS_BUILD_ONLY_LIB=ON \
      ..
```

**Configuration options:**
- `CMAKE_INSTALL_PREFIX=/usr/local`: Install location
- `BUILD_SHARED_LIBS=ON`: Build shared libraries (.so files)
- `OQS_BUILD_ONLY_LIB=ON`: Build only library (skip tests)

### Step 4: Compile liboqs

```bash
make -j$(nproc)
```

**What this does:**
- Compiles all PQC algorithms
- Uses all CPU cores (`-j$(nproc)`)
- Takes 5-10 minutes

**Expected output:**
```
[100%] Built target oqs
```

### Step 5: Install liboqs

```bash
sudo make install
sudo ldconfig
```

**What this does:**
- Copies libraries to `/usr/local/lib/`
- Copies headers to `/usr/local/include/`
- Updates library cache

### Step 6: Verify Installation

```bash
ls -la /usr/local/lib/liboqs.*
```

**Expected output:**
```
-rw-r--r-- 1 root root 8234567 ... /usr/local/lib/liboqs.a
-rwxr-xr-x 1 root root 5678901 ... /usr/local/lib/liboqs.so
```

---

## Setup Python Environment

### Step 1: Navigate to Project

```bash
cd "/mnt/d/PQC App/backend-python"
```

### Step 2: Create Virtual Environment

```bash
python3 -m venv venv
```

**What this does:**
- Creates isolated Python environment
- Prevents conflicts with system Python
- Located in `backend-python/venv/`

### Step 3: Activate Virtual Environment

```bash
source venv/bin/activate
```

**You'll see:**
```
(venv) anshul@LAPTOP:~/backend-python$
```

The `(venv)` prefix indicates the virtual environment is active.

### Step 4: Upgrade pip

```bash
pip install --upgrade pip
```

### Step 5: Install Python Dependencies

```bash
pip install -r requirements.txt
```

**What this installs:**
- `flask==3.0.0`: Web framework
- `flask-cors==4.0.0`: Cross-origin resource sharing
- `liboqs-python==0.14.1`: Python bindings for liboqs
- `cryptography==41.0.7`: AES-GCM encryption

**Installation time:** 1-2 minutes

### Step 6: Verify Installation

```bash
python3 -c "import oqs; print('liboqs version:', oqs.oqs_version())"
```

**Expected output:**
```
liboqs version: 0.15.0
```

---

## Setup Frontend

### Step 1: Navigate to Frontend

```bash
cd "/mnt/d/PQC App/frontend"
```

### Step 2: Install Node Dependencies

```bash
npm install
```

**What this installs:**
- `react`: UI library
- `react-dom`: React DOM renderer
- `react-router-dom`: Routing
- `vite`: Build tool and dev server

**Installation time:** 2-3 minutes

### Step 3: Verify Installation

```bash
npm list --depth=0
```

**Expected output:**
```
pqc-frontend@1.0.0
├── react@18.3.1
├── react-dom@18.3.1
├── react-router-dom@6.28.0
└── vite@5.4.21
```

---

## Running the Application

### Method 1: Manual (Recommended for Development)

**Terminal 1 - Backend:**
```bash
cd "/mnt/d/PQC App/backend-python"
source venv/bin/activate
python3 app.py
```

**Expected output:**
```
🔐 PQC Secure File System (Python + Real Crypto)
Using: Kyber512 + ML-DSA-44
 * Running on http://127.0.0.1:3001
```

**Terminal 2 - Frontend:**
```bash
cd "/mnt/d/PQC App/frontend"
npm run dev
```

**Expected output:**
```
VITE v5.4.21  ready in 633 ms
➜  Local:   http://localhost:5173/
```

**Open browser:** http://localhost:5173

### Method 2: Using Setup Script

```bash
cd "/mnt/d/PQC App"
./setup.sh
```

This script:
1. Checks for dependencies
2. Installs missing packages
3. Sets up Python venv
4. Installs npm packages
5. Provides run commands

---

## Troubleshooting

### Issue: "wsl: command not found"

**Solution:**
1. Open PowerShell as Administrator
2. Run: `wsl --install`
3. Restart computer

### Issue: "liboqs not found"

**Solution:**
```bash
# Reinstall liboqs
cd ~/liboqs/build
sudo make install
sudo ldconfig

# Verify
ldconfig -p | grep liboqs
```

### Issue: "Python externally-managed-environment"

**Solution:**
Always use virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: "Port 3001 already in use"

**Solution:**
```bash
# Kill process using port 3001
lsof -ti:3001 | xargs kill -9

# Or use different port in app.py:
# app.run(host='0.0.0.0', port=3002)
```

### Issue: "Port 5173 already in use"

**Solution:**
```bash
# Kill process using port 5173
lsof -ti:5173 | xargs kill -9

# Vite will auto-select next available port
```

### Issue: "Module 'oqs' not found"

**Solution:**
```bash
# Make sure venv is activated
source venv/bin/activate

# Reinstall liboqs-python
pip install --force-reinstall liboqs-python==0.14.1
```

### Issue: "cmake: command not found"

**Solution:**
```bash
sudo apt update
sudo apt install -y cmake build-essential
```

### Issue: "npm: command not found"

**Solution:**
```bash
# Install Node.js
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs
```

### Issue: Slow WSL2 Performance

**Solution:**
1. Store project files in WSL filesystem (not /mnt/c or /mnt/d)
2. Or use Windows native tools (not recommended for this project)

### Issue: "Permission denied" errors

**Solution:**
```bash
# Make scripts executable
chmod +x setup.sh

# Or run with bash
bash setup.sh
```

### Issue: Database locked

**Solution:**
```bash
# Stop all running instances
pkill -f "python3 app.py"

# Remove lock file
rm backend-python/pqc_files.db-journal
```

---

## Verification Checklist

After setup, verify everything works:

- [ ] WSL2 installed and running
- [ ] Ubuntu accessible from Windows Terminal
- [ ] Python 3.12+ installed (`python3 --version`)
- [ ] Node.js 18+ installed (`node --version`)
- [ ] liboqs 0.15.0 installed (`ls /usr/local/lib/liboqs.so`)
- [ ] Python venv created and activated
- [ ] Python packages installed (`pip list`)
- [ ] Node packages installed (`npm list`)
- [ ] Backend starts without errors
- [ ] Frontend starts without errors
- [ ] Browser opens http://localhost:5173
- [ ] Can upload and download files

---

## Next Steps

1. **Read DOCUMENTATION.md** - Understand the technical details
2. **Read PROVE_PQC.md** - Learn how to verify quantum encryption
3. **Try the app** - Upload files and test features
4. **Explore the code** - Check `backend-python/app.py` and `frontend/src/`

---

## Quick Reference

### Start Backend
```bash
cd "/mnt/d/PQC App/backend-python"
source venv/bin/activate
python3 app.py
```

### Start Frontend
```bash
cd "/mnt/d/PQC App/frontend"
npm run dev
```

### Stop Servers
Press `Ctrl+C` in each terminal

### Deactivate Python venv
```bash
deactivate
```

### Update Dependencies
```bash
# Python
pip install --upgrade -r requirements.txt

# Node
npm update
```

---

**Setup complete! Your quantum-safe file system is ready to use.** 🚀
