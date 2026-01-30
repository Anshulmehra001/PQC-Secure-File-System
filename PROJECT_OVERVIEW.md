# 🎯 Project Overview

Quick reference guide for the PQC Secure File System.

## 📁 Project Structure

```
PQC App/
├── README.md              # Project overview + how to use
├── SETUP.md              # Complete installation guide
├── DOCUMENTATION.md      # Full technical documentation
├── PROVE_PQC.md         # How to verify quantum encryption
├── PROJECT_OVERVIEW.md  # This file (quick reference)
├── setup.sh             # Automated setup script
├── .gitignore           # Git ignore rules
│
├── backend-python/
│   ├── app.py           # Flask server + PQC crypto
│   ├── requirements.txt # Python dependencies
│   ├── pqc_files.db    # SQLite database
│   ├── venv/           # Python virtual environment
│   ├── uploads/        # Shared files (encrypted)
│   └── storage/        # Cloud files (encrypted)
│
└── frontend/
    ├── src/
    │   ├── main.jsx           # App entry + routing
    │   ├── Login.jsx          # Login/register
    │   ├── FileSharing.jsx    # File sharing UI
    │   ├── CloudStorage.jsx   # Cloud storage UI
    │   ├── ShareDownload.jsx  # Download page
    │   └── styles.css         # Cyberpunk theme
    ├── index.html
    ├── package.json
    └── vite.config.js
```

## 📚 Documentation Guide

### For First-Time Setup
**Read:** [SETUP.md](SETUP.md)
- WSL2 installation
- Ubuntu setup
- liboqs compilation
- Python environment
- Frontend setup
- Running the app

### For Understanding the Project
**Read:** [DOCUMENTATION.md](DOCUMENTATION.md)
- Architecture overview
- Technology stack explained
- Cryptography details
- WSL2 & Ubuntu explained
- Backend implementation
- Frontend implementation
- Database schema
- API reference
- Security analysis
- Performance benchmarks

### For Verifying Quantum Encryption
**Read:** [PROVE_PQC.md](PROVE_PQC.md)
- Quick verification methods
- Code inspection
- Runtime tests
- Cryptographic proofs
- Performance benchmarks
- File integrity tests
- Signature verification
- Library verification

### For Quick Start
**Read:** [README.md](README.md)
- Project overview
- Quick start guide
- How to use the app
- Technology summary
- Links to other docs

## 🚀 Quick Commands

### Start the Application

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

**Open:** http://localhost:5173

### Stop the Application

Press `Ctrl+C` in both terminals

### Verify Installation

```bash
# Check liboqs
ls /usr/local/lib/liboqs.so

# Check Python
python3 -c "import oqs; print(oqs.oqs_version())"

# Check Node
node --version
npm --version
```

## 🔐 Key Features

### File Sharing
- Upload files with quantum-safe encryption
- Generate expiring share links (1-24 hours)
- Digital signatures for integrity
- No login required

### Cloud Storage
- User authentication (login/register)
- Personal encrypted storage
- Upload/download/delete files
- Complete user isolation

### Cryptography
- **Kyber512**: Post-quantum key exchange
- **ML-DSA-44**: Post-quantum signatures
- **AES-256-GCM**: Fast symmetric encryption
- **PBKDF2**: Secure password hashing

## 🎓 Learning Path

### Beginner
1. Read README.md (overview)
2. Follow SETUP.md (installation)
3. Try the app (upload/download files)
4. Read "How to Use" section in README

### Intermediate
1. Read DOCUMENTATION.md (technical details)
2. Inspect backend code (app.py)
3. Inspect frontend code (src/*.jsx)
4. Run verification tests from PROVE_PQC.md

### Advanced
1. Study cryptography section in DOCUMENTATION.md
2. Run all tests in PROVE_PQC.md
3. Modify code and experiment
4. Benchmark performance
5. Deploy to production (add HTTPS, etc.)

## 🔍 Common Questions

**Q: Is this really quantum-safe?**
A: Yes! Uses NIST-standardized PQC algorithms (Kyber, ML-DSA) via liboqs.

**Q: How do I prove it's not simulated?**
A: See PROVE_PQC.md for 20 verification methods.

**Q: Can I use this in production?**
A: It's a demonstration. For production, add HTTPS, rate limiting, etc. (see DOCUMENTATION.md Security section).

**Q: Why WSL2?**
A: liboqs requires Linux build tools. WSL2 provides full Linux environment on Windows.

**Q: What's the difference between File Sharing and Cloud Storage?**
A: File Sharing = temporary links, no login. Cloud Storage = permanent storage, requires login.

**Q: How long does setup take?**
A: 20-30 minutes (mostly compiling liboqs).

**Q: What if I get errors?**
A: Check SETUP.md Troubleshooting section.

## 📊 File Sizes

- **README.md**: ~5 KB (overview)
- **SETUP.md**: ~15 KB (installation guide)
- **DOCUMENTATION.md**: ~50 KB (complete technical docs)
- **PROVE_PQC.md**: ~20 KB (verification methods)
- **app.py**: ~15 KB (backend code)
- **Frontend src/**: ~10 KB total (React components)

## 🎯 Use Cases

- **Education**: Learn PQC concepts
- **Demonstration**: Show real quantum-safe crypto
- **Research**: Experiment with NIST algorithms
- **Prototyping**: Base for production apps
- **Portfolio**: Showcase advanced crypto skills

## 🛠️ Technologies Used

### Operating System
- Windows 10/11 (host)
- WSL2 (virtualization)
- Ubuntu 24.04 LTS (guest)

### Backend
- Python 3.12
- Flask 3.0.0
- liboqs 0.15.0 (C library)
- liboqs-python 0.14.1
- cryptography 41.0.7
- SQLite 3

### Frontend
- React 18.3.1
- React Router 6.28.0
- Vite 5.4.21
- Custom CSS (cyberpunk theme)

### Cryptography
- Kyber512 (PQC KEM)
- ML-DSA-44 (PQC signatures)
- AES-256-GCM (symmetric)
- PBKDF2-HMAC-SHA256 (password hashing)

## 📈 Performance

- **Kyber512**: ~0.1 ms per operation
- **ML-DSA-44**: ~1 ms signing, ~0.5 ms verification
- **AES-256-GCM**: ~100-500 MB/s
- **File upload**: ~10 ms for 1 MB file
- **File download**: ~8 ms for 1 MB file

## 🔒 Security

### Strengths
- ✅ Quantum-resistant encryption
- ✅ NIST-standardized algorithms
- ✅ Strong password hashing
- ✅ Session management
- ✅ User isolation

### Limitations
- ⚠️ No HTTPS (dev mode)
- ⚠️ No rate limiting
- ⚠️ Basic input validation
- ⚠️ No CSRF protection

See DOCUMENTATION.md Security Analysis for details.

## 🎨 UI Theme

**Cyberpunk Dark Theme:**
- Dark background (#0a0e27)
- Neon green accent (#00ff88)
- Glowing effects
- Animated elements
- Grid pattern background
- Space Grotesk font

## 📞 Support

- **Setup issues**: See SETUP.md Troubleshooting
- **Technical questions**: See DOCUMENTATION.md
- **Verification**: See PROVE_PQC.md
- **General info**: See README.md

## 🎉 Success Checklist

After setup, you should be able to:

- [ ] Access http://localhost:5173 in browser
- [ ] See cyberpunk dark theme UI
- [ ] Upload file in File Sharing mode
- [ ] Get share link
- [ ] Download file from share link
- [ ] Create account in Cloud Storage
- [ ] Login to Cloud Storage
- [ ] Upload file to cloud
- [ ] Download file from cloud
- [ ] Delete file from cloud
- [ ] Logout from Cloud Storage
- [ ] Verify encrypted files on disk (gibberish)
- [ ] Run verification tests from PROVE_PQC.md

## 🚀 Next Steps

1. **Complete setup** (if not done): Follow SETUP.md
2. **Try the app**: Upload and download files
3. **Verify PQC**: Run tests from PROVE_PQC.md
4. **Learn details**: Read DOCUMENTATION.md
5. **Experiment**: Modify code and test
6. **Share**: Show others real quantum-safe crypto!

---

**Everything you need is in these 4 documents:**
- README.md (overview + how to use)
- SETUP.md (installation)
- DOCUMENTATION.md (technical details)
- PROVE_PQC.md (verification)

**Happy quantum-safe computing!** 🔐
