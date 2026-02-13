# 🔐 PQC Secure File System

A quantum-safe file sharing and cloud storage application using **real Post-Quantum Cryptography** (not simulated).

## 🎯 What Is This?

A web application that demonstrates **real quantum-resistant encryption** for file sharing and cloud storage:

- **File Sharing**: WeTransfer-style secure file sharing with expiring links
- **Cloud Storage**: Personal encrypted cloud storage with user authentication

## 🔒 Security Features

- **REAL Post-Quantum Cryptography**: Uses NIST-standardized algorithms via liboqs
- **Kyber512**: Quantum-resistant key encapsulation (KEM)
- **ML-DSA-44**: Quantum-resistant digital signatures (formerly Dilithium2)
- **AES-256-GCM**: Fast symmetric encryption for file data
- **User Authentication**: Secure login with PBKDF2 password hashing
- **Session Management**: Token-based authentication with 24-hour expiration

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
3. Choose expiration time (1-24 hours)
4. Click **"Upload & Encrypt"**
5. Copy the share link and send it to anyone
6. Recipients can download the file until it expires

**What happens:**
- File encrypted with Kyber512 + AES-256-GCM
- Digital signature created with ML-DSA-44
- Unique share link generated
- Link expires automatically

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
- **CSS3** - Custom cyberpunk theme (neon green #00ff88)

### Backend
- **Python 3.12** - Latest Python with performance improvements
- **Flask** - Lightweight web framework with CORS support
- **liboqs 0.15.0** - Real post-quantum cryptography library
- **SQLite** - Embedded database for user data and metadata
- **CORS** - Cross-origin resource sharing for API access

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
│   ├── requirements.txt    # Python dependencies
│   ├── pqc_files.db       # SQLite database
│   ├── uploads/           # Shared files (encrypted)
│   ├── storage/           # Cloud files (encrypted)
│   └── venv/              # Python virtual environment
├── frontend/
│   ├── src/
│   │   ├── main.jsx       # App entry + routing
│   │   ├── Login.jsx      # Login/register component
│   │   ├── FileSharing.jsx    # File sharing UI
│   │   ├── CloudStorage.jsx   # Cloud storage UI
│   │   ├── ShareDownload.jsx  # Download page
│   │   └── styles.css     # Cyberpunk theme
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
4. **Expiring Links**: Time-limited file sharing (1-24 hours)
5. **User Isolation**: Complete separation between user accounts
6. **WSL2 Integration**: Seamless Windows + Linux development workflow

### Security Level:
- **Encryption at Rest**: ✅ (Files encrypted on disk)
- **Encryption in Transit**: ✅ (HTTPS recommended for production)
- **Quantum Resistance**: ✅ (Kyber512 + ML-DSA-44)
- **Zero-Knowledge**: ❌ (Server can decrypt - same as Google Drive)
- **Access Control**: ✅ (User authentication + session management)

**Bottom Line**: This project offers **Google Drive-level security with quantum protection** - something major cloud providers don't have yet.

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
