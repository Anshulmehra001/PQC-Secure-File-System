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

### Backend
- **Python 3.12** + Flask
- **liboqs 0.15.0** - Real PQC implementation
- **SQLite** - Database for metadata
- **PBKDF2** - Password hashing

### Frontend
- **React 18** + Vite
- **React Router** - Navigation
- **Custom CSS** - Cyberpunk dark theme

### Cryptography
- **Kyber512** - Post-quantum KEM (NIST Level 1)
- **ML-DSA-44** - Post-quantum signatures (NIST Level 2)
- **AES-256-GCM** - Symmetric encryption
- **PBKDF2-HMAC-SHA256** - Password hashing (100k iterations)

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
