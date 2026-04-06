# 🔐 PQC Secure File System

A quantum-safe file sharing and cloud storage application using **real Post-Quantum Cryptography** (not simulated).

## 🎯 What Is This?

A web application that demonstrates **real quantum-resistant encryption** for file sharing and cloud storage:

- **File Sharing**: WeTransfer-style secure file sharing with expiring links
- **Cloud Storage**: Personal encrypted cloud storage with user authentication

## 🆕 New Features

### View-Only File Sharing
Share files that recipients can view in browser but cannot download:
- **PDF Protection**: PDFs rendered page-by-page as PNG images
- **No Download Button**: Download functionality completely disabled
- **Watermarks**: Each page/image has "VIEW ONLY" watermark
- **Right-Click Disabled**: Context menu and keyboard shortcuts blocked
- **Supported Files**: PDFs, images, videos, audio

### Admin Tools
Manage your file system with powerful CLI tools:
- **admin.py**: Interactive menu for manual management
  - View statistics (users, files, disk usage)
  - List all files with metadata
  - Find and cleanup orphaned files
  - Delete expired shares
  - Empty trash bin
- **auto_cleanup.py**: Automatic background service
  - Runs daily at 2:00 AM
  - Cleans expired shares automatically
  - Removes orphaned files
  - Deletes trash files older than 30 days
  - Logs all actions to cleanup.log

### Enhanced UI
- **3D Animated Loader**: Rotating cubes with encryption step indicators
- **Glowing Login Form**: Animated border with hover effects
- **Cyberpunk Theme**: Dark mode with neon green accents

## 🔐 Security Features

- **REAL Post-Quantum Cryptography**: Uses NIST-standardized algorithms via liboqs
- **Kyber512**: Quantum-resistant key encapsulation (KEM)
- **ML-DSA-44**: Quantum-resistant digital signatures (formerly Dilithium2)
- **AES-256-GCM**: Fast symmetric encryption for file data
- **User Authentication**: Secure login with PBKDF2 password hashing
- **Session Management**: Token-based authentication with 24-hour expiration
- **View-Only Mode**: Share files for viewing without download capability
- **PDF Protection**: Server-side PDF-to-image conversion prevents downloads
- **Admin Tools**: CLI for file management and cleanup
- **Auto Cleanup**: Scheduled cleanup of expired files and orphaned data
- **Trash Bin**: 30-day retention before permanent deletion

## 🚀 Quick Start

### Prerequisites

- Windows with WSL2 (Ubuntu)
- Python 3.12+
- Node.js 18+
- liboqs 0.15.0

### Installation

```bash
# In WSL Ubuntu terminal
cd "/mnt/d/PQC App"
./setup.sh
```

This will:
1. Install system dependencies
2. Compile liboqs from source
3. Set up Python virtual environment
4. Install frontend dependencies

### Running the App

**Terminal 1 - Backend:**
```bash
cd "/mnt/d/PQC App/backend-python"
source venv/bin/activate
python3 app.py
```

**Terminal 2 - Frontend:**
```bash
cd "/mnt/d/PQC App/frontend"
npm run dev
```

**Open browser:** http://localhost:5173

## 📖 How to Use

### File Sharing (No Login Required)

1. Click **"File Sharing"** tab
2. Select a file to upload
3. Choose **share mode**:
   - **Allow Download**: Recipients can download the file
   - **View Only**: Recipients can only view in browser (no download)
4. Choose expiration time (1-24 hours)
5. Click **"Upload & Encrypt"**
6. Copy the share link and send it to anyone
7. Recipients can access the file until it expires

**What happens:**
- File encrypted with Kyber512 + AES-256-GCM
- Digital signature created with ML-DSA-44
- Unique share link generated
- Link expires automatically
- View-only mode prevents downloads (PDFs rendered as images)

### Cloud Storage (Login Required)

1. Click **"Cloud Storage"** tab
2. **Create account** or **Login**:
   - Click "Sign Up" for new account
   - Enter username and password (min 6 characters)
   - Or click "Login" if you have an account
3. **Upload files**: Click "+ Upload File"
4. **Download files**: Click "Download" button (auto-decrypts)
5. **Delete files**: Click "Delete" button
6. **Logout**: Click "Logout" in navbar when done

**What happens:**
- Each file encrypted with unique Kyber512 keys
- Files linked to your account (complete user isolation)
- Encrypted at rest on disk
- Automatic decryption on download

## 🔬 Technology Stack

### Frontend
- **React 18** - Modern UI framework with hooks
- **Vite** - Lightning-fast build tool and dev server
- **React Router** - Client-side routing and navigation
- **JavaScript (JSX)** - Component-based architecture
- **CSS3** - Custom cyberpunk theme with glowing animations
- **3D Loader** - Animated cube loader with encryption steps

### Backend
- **Python 3.12** - Latest Python with performance improvements
- **Flask** - Lightweight web framework with CORS support
- **liboqs 0.15.0** - Real post-quantum cryptography library
- **PyMuPDF (fitz)** - PDF to image conversion for secure viewing
- **Pillow** - Image processing for watermarks
- **SQLite** - Embedded database for user data and metadata
- **schedule** - Automated cleanup task scheduling

### Cryptography
- **Kyber512** - Post-quantum key encapsulation (NIST PQC standard)
- **ML-DSA-44** (Dilithium2) - Post-quantum digital signatures
- **AES-256-GCM** - Symmetric encryption with authentication
- **PBKDF2-HMAC-SHA256** - Password hashing (100k iterations)

### Infrastructure
- **WSL2 Ubuntu** - Windows Subsystem for Linux development environment
- **Git/GitHub** - Version control and collaboration

## 📊 Project Structure

```
PQC App/
├── backend-python/
│   ├── app.py              # Flask server + PQC crypto
│   ├── admin.py            # Admin CLI tool
│   ├── auto_cleanup.py     # Automatic cleanup service
│   ├── ADMIN_GUIDE.md      # Admin documentation
│   ├── requirements.txt    # Python dependencies
│   ├── pqc_files.db       # SQLite database
│   ├── uploads/           # Shared files (encrypted)
│   ├── storage/           # Cloud files (encrypted)
│   ├── trash/             # Deleted files (30-day retention)
│   └── venv/              # Python virtual environment
├── frontend/
│   ├── src/
│   │   ├── main.jsx           # App entry + routing
│   │   ├── Login.jsx          # Login/register component
│   │   ├── FileSharing.jsx    # File sharing UI
│   │   ├── CloudStorage.jsx   # Cloud storage UI
│   │   ├── ShareDownload.jsx  # Download page
│   │   ├── FileViewer.jsx     # View-only file viewer
│   │   ├── Loader.jsx         # 3D animated loader
│   │   ├── config.js          # API configuration
│   │   └── styles.css         # Cyberpunk theme
│   ├── package.json       # Node dependencies
│   └── vite.config.js     # Vite config
├── README.md              # This file
├── SETUP.md              # Complete setup guide
├── DOCUMENTATION.md      # Technical documentation
└── PROVE_PQC.md         # How to prove quantum encryption
```

## 🎓 Documentation

- **[SETUP.md](SETUP.md)** - Complete installation and setup guide
- **[DOCUMENTATION.md](DOCUMENTATION.md)** - Detailed technical documentation
- **[PROVE_PQC.md](PROVE_PQC.md)** - All methods to prove quantum encryption works
- **[ADMIN_GUIDE.md](backend-python/ADMIN_GUIDE.md)** - Admin tools and file management

## 🧪 Proving It Works

Want to verify this uses **real quantum encryption**? See **[PROVE_PQC.md](PROVE_PQC.md)** for:

- Code inspection methods
- Runtime verification tests
- Cryptographic proofs
- Performance benchmarks
- File integrity tests
- Signature verification tests

## 🔐 Security Notes

### What's Quantum-Safe
- ✅ Key exchange (Kyber512)
- ✅ Digital signatures (ML-DSA-44)
- ✅ File encryption (hybrid: PQC + AES)

### What's Classical
- ⚠️ Password hashing (PBKDF2 - quantum-resistant but not PQC)
- ⚠️ Session tokens (random bytes - quantum-resistant)
- ⚠️ Symmetric encryption (AES-256 - quantum-resistant with 256-bit keys)

### Production Considerations
- Add HTTPS/TLS for network security
- Use production WSGI server (not Flask dev server)
- Implement rate limiting
- Add file size limits
- Set up proper backup system
- Use environment variables for secrets

## 🎯 Use Cases

- **Demonstration**: Show real PQC in action
- **Education**: Learn how quantum-safe crypto works
- **Research**: Experiment with NIST PQC algorithms
- **Prototype**: Base for quantum-safe applications
- **Testing**: Benchmark PQC performance

## ⭐ What Makes This Special?

### Compared to Google Drive / Dropbox / OneDrive:
- ✅ **Quantum-Resistant**: Protected against future quantum computer attacks
- ✅ **NIST Standardized**: Uses official post-quantum algorithms (Kyber, Dilithium)
- ✅ **Open Source Crypto**: Transparent implementation with liboqs
- ✅ **Educational**: Full source code to learn from
- ❌ **Not Zero-Knowledge**: Server can decrypt files (same as Google Drive)

### Compared to ProtonDrive / Tresorit (Zero-Knowledge):
- ✅ **Quantum-Resistant**: They use classical crypto, we use PQC
- ✅ **Faster Development**: Server-side encryption is simpler
- ✅ **Password Recovery**: Possible to reset passwords
- ❌ **Not Zero-Knowledge**: Server has encryption keys (trade-off for convenience)

### Compared to Academic PQC Demos:
- ✅ **Real Implementation**: Uses actual liboqs library, not simulation
- ✅ **Full Application**: Complete file sharing + cloud storage system
- ✅ **Modern UI**: React-based interface, not command-line only
- ✅ **Production-Ready Crypto**: NIST-standardized algorithms

### Unique Features:
1. **Hybrid Encryption**: Combines PQC (Kyber) with AES for optimal performance
2. **Digital Signatures**: Every file signed with quantum-safe ML-DSA-44
3. **Dual Mode**: Both anonymous file sharing AND authenticated cloud storage
4. **View-Only Sharing**: Share files for viewing without download capability
5. **Enhanced PDF Protection**: PDFs rendered page-by-page as images
6. **Expiring Links**: Time-limited file sharing (1-24 hours)
7. **User Isolation**: Complete separation between user accounts
8. **Admin Tools**: CLI for file management, cleanup, and statistics
9. **Auto Cleanup**: Scheduled maintenance with trash bin system
10. **WSL2 Integration**: Seamless Windows + Linux development workflow

### Security Level:
- **Encryption at Rest**: ✅ (Files encrypted on disk)
- **Encryption in Transit**: ✅ (HTTPS recommended for production)
- **Quantum Resistance**: ✅ (Kyber512 + ML-DSA-44)
- **Zero-Knowledge**: ❌ (Server can decrypt - same as Google Drive)
- **Access Control**: ✅ (User authentication + session management)

**Bottom Line**: This project offers **Google Drive-level security with quantum protection** - something major cloud providers don't have yet.

## 🗺️ Roadmap

### Current Implementation: Server-Side Encryption
**How it works now:**
```
User → Upload file → Server encrypts with Kyber512 → Server stores encrypted file + keys in database
                                                      ↓
                                                Server can decrypt anytime
```

**What you get:**
- ✅ Quantum-resistant encryption (Kyber512 + ML-DSA-44)
- ✅ Fast encryption/decryption (native Python liboqs)
- ✅ Password recovery possible
- ✅ Easy to use
- ❌ Server can read your files (like Google Drive)

### Future: Zero-Knowledge Encryption (Planned)
**How it would work:**
```
User enters password → Browser derives encryption key → Encrypt file in browser → Upload encrypted blob
                       ↓                                                          ↓
                   Key never sent to server                              Server stores blob only (can't decrypt)
```

**What you would get:**
- ✅ True zero-knowledge (server CANNOT read files)
- ✅ Maximum privacy (like ProtonDrive)
- ✅ Still quantum-resistant
- ❌ Forget password = lose all files forever (no recovery)
- ❌ Slower (JavaScript crypto vs native Python)


**Changes Required:**

| Component | Current | Zero-Knowledge | Difficulty |
|-----------|---------|----------------|------------|
| **Frontend** | Upload raw file | Encrypt in browser with `pqc-kyber` npm package | Medium |
| **Key Derivation** | None | PBKDF2 from password in browser | Easy |
| **Backend** | Encrypt + store keys | Just store encrypted blobs | Easy |
| **Database** | Stores encryption keys | Only stores metadata | Easy |
| **Download** | Server decrypts | Browser decrypts with password | Medium |
| **File Sharing** | Server generates keys | Share encrypted key with link | Hard |
| **Password Reset** | Possible | **IMPOSSIBLE** (by design) | N/A |


**Files to Modify:**
1. `frontend/package.json` - Add `pqc-kyber` or `@noble/post-quantum`
2. `frontend/src/CloudStorage.jsx` - Add client-side encryption logic
3. `frontend/src/Login.jsx` - Derive encryption key from password
4. `backend-python/app.py` - Remove server-side encryption, store blobs only
5. `backend-python/pqc_files.db` - Remove `encrypted_key` column

**Trade-off Decision:**
- **Keep current** = Convenience + password recovery (like Google Drive)
- **Implement zero-knowledge** = Maximum privacy + no password recovery (like ProtonDrive)

**Status:** 🔄 Not yet implemented (current version prioritizes usability)

### Implemented Features
- [x] View-only file sharing mode
- [x] Enhanced PDF protection (page-by-page rendering)
- [x] Admin CLI tool for file management
- [x] Automatic cleanup service
- [x] Trash bin system (30-day retention)
- [x] 3D animated loader with encryption steps
- [x] Glowing login form with animations

### Future Features
- [ ] HTTPS/TLS support for production
- [ ] File size limits and quotas
- [ ] Multi-file upload
- [ ] Folder support
- [ ] File versioning
- [ ] 2FA authentication
- [ ] Web-based admin dashboard
- [ ] Docker deployment
- [ ] Mobile app (React Native)

## 📝 License

This is a demonstration project. Use at your own risk.

## 🙏 Credits

- **liboqs**: Open Quantum Safe project
- **NIST**: Post-Quantum Cryptography standardization
- **Kyber/Dilithium**: CRYSTALS team

## 🤝 Contributing

This is a personal project, but feel free to fork and modify.

## 📧 Support

For issues or questions, check the documentation files:
- Setup issues → SETUP.md
- Technical details → DOCUMENTATION.md
- Verification → PROVE_PQC.md

---

**Built with real quantum-safe cryptography. Not simulated. Not fake. Real PQC.** 🔐
