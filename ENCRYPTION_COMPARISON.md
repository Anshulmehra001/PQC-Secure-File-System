# 🔐 Encryption Architecture Comparison

## Current vs Zero-Knowledge Implementation

This document explains the difference between the current server-side encryption and a potential zero-knowledge implementation.

---

## 📊 Side-by-Side Comparison

| Feature | Current (Server-Side) | Zero-Knowledge (Future) |
|---------|----------------------|-------------------------|
| **Encryption Location** | Server (Python) | Browser (JavaScript) |
| **Who Has Keys** | Server stores in database | Only user (in memory) |
| **Server Can Decrypt** | ✅ Yes | ❌ No |
| **Password Recovery** | ✅ Possible | ❌ Impossible |
| **Performance** | ⚡ Fast (native liboqs) | 🐌 Slower (JS crypto) |
| **Privacy Level** | Google Drive level | ProtonDrive level |
| **Quantum Resistant** | ✅ Yes | ✅ Yes |
| **Implementation Complexity** | ✅ Simple | ⚠️ Complex |
| **User Experience** | ✅ Easy | ⚠️ Must remember password |

---

## 🔄 Current Implementation: Server-Side Encryption

### Architecture Flow

```
┌─────────┐                    ┌─────────────┐                    ┌──────────┐
│ Browser │                    │   Server    │                    │ Database │
└────┬────┘                    └──────┬──────┘                    └────┬─────┘
     │                                │                                 │
     │  1. Upload raw file            │                                 │
     ├───────────────────────────────>│                                 │
     │                                │                                 │
     │                                │  2. Generate Kyber512 keypair   │
     │                                │     (public_key, private_key)   │
     │                                │                                 │
     │                                │  3. Encrypt file with AES-256   │
     │                                │     (key from Kyber KEM)        │
     │                                │                                 │
     │                                │  4. Store encrypted file        │
     │                                ├────────────────────────────────>│
     │                                │     + encryption keys           │
     │                                │     + metadata                  │
     │                                │                                 │
     │  5. Return success             │                                 │
     │<───────────────────────────────┤                                 │
     │                                │                                 │
```

### What Gets Stored

**Database (SQLite):**
```sql
cloud_files table:
- id: "4020addd-c623-4a58-8226-78921ddcf105"
- user_id: 1
- filename: "document.pdf"
- filepath: "/storage/4020addd-c623-4a58-8226-78921ddcf105.enc"
- kem_ciphertext: "a3f2b8c9..." (Kyber ciphertext - 768 bytes)
- encrypted_key: "d4e5f6a7..." (Shared secret - 32 bytes)  ⚠️ SERVER HAS THIS
- size: 1048576
- created_at: 1738339200000
```

**Disk (storage/ folder):**
```
4020addd-c623-4a58-8226-78921ddcf105.enc
↓
[12-byte nonce][AES-256-GCM encrypted file data]
```

### Security Analysis

**✅ Protected Against:**
- Disk theft (files are encrypted)
- File system access without database
- Network sniffing (if using HTTPS)
- Quantum computer attacks (Kyber512)

**❌ NOT Protected Against:**
- Server administrator access (you can decrypt)
- Database breach (keys are in database)
- Government subpoena (must provide decrypted files)
- Insider threat (employees with DB access)
- Compromised server (attacker gets keys)

### Code Example (Current)

**Backend (app.py):**
```python
def storage_upload():
    file_data = request.files['file'].read()
    
    # Server encrypts the file
    encryption_result = PQCCrypto.encrypt_file_simple(file_data)
    
    # Store encrypted file on disk
    with open(storage_path, 'w') as f:
        f.write(encryption_result['encrypted_data'])
    
    # Store keys in database ⚠️ THIS IS THE PROBLEM
    c.execute('''INSERT INTO cloud_files 
                 (id, filename, kem_ciphertext, encrypted_key, ...)
                 VALUES (?, ?, ?, ?, ...)''',
              (file_id, filename, 
               encryption_result['kem_ciphertext'],
               encryption_result['shared_secret'],  # ⚠️ Server has decryption key
               ...))
```

**Frontend (CloudStorage.jsx):**
```javascript
const handleUpload = async (file) => {
  const formData = new FormData();
  formData.append('file', file);  // Raw file sent to server
  
  const response = await fetch(`${API_URL}/api/storage/upload`, {
    method: 'POST',
    body: formData
  });
};
```

---

## 🔒 Zero-Knowledge Implementation (Future)

### Architecture Flow

```
┌─────────┐                    ┌─────────────┐                    ┌──────────┐
│ Browser │                    │   Server    │                    │ Database │
└────┬────┘                    └──────┬──────┘                    └────┬─────┘
     │                                │                                 │
     │  1. User enters password       │                                 │
     │     Derive key: PBKDF2(pwd)    │                                 │
     │                                │                                 │
     │  2. Generate Kyber keypair     │                                 │
     │     in browser (JS)            │                                 │
     │                                │                                 │
     │  3. Encrypt file in browser    │                                 │
     │     with AES-256 + Kyber       │                                 │
     │                                │                                 │
     │  4. Upload encrypted blob      │                                 │
     ├───────────────────────────────>│                                 │
     │     (server can't decrypt)     │                                 │
     │                                │                                 │
     │                                │  5. Store blob + metadata only  │
     │                                ├────────────────────────────────>│
     │                                │     (NO KEYS STORED)            │
     │                                │                                 │
     │  6. Return success             │                                 │
     │<───────────────────────────────┤                                 │
     │                                │                                 │
```

### What Gets Stored

**Database (SQLite):**
```sql
cloud_files table:
- id: "4020addd-c623-4a58-8226-78921ddcf105"
- user_id: 1
- filename: "document.pdf"
- filepath: "/storage/4020addd-c623-4a58-8226-78921ddcf105.enc"
- kem_ciphertext: NULL  ❌ NOT STORED
- encrypted_key: NULL   ❌ NOT STORED
- size: 1048576
- created_at: 1738339200000
- salt: "random_salt_for_key_derivation"  ✅ NEW FIELD
```

**Disk (storage/ folder):**
```
4020addd-c623-4a58-8226-78921ddcf105.enc
↓
[12-byte nonce][Kyber ciphertext][AES-256-GCM encrypted file data]
(All encrypted in browser, server just stores the blob)
```

### Security Analysis

**✅ Protected Against:**
- Everything from current implementation, PLUS:
- Server administrator access (can't decrypt)
- Database breach (no keys to steal)
- Government subpoena (server can't provide plaintext)
- Insider threat (employees can't decrypt)
- Compromised server (attacker gets nothing useful)

**❌ NOT Protected Against:**
- User forgetting password (files lost forever)
- Keylogger on user's device
- Browser compromise
- Phishing attacks

### Code Example (Zero-Knowledge)

**Frontend (CloudStorage.jsx):**
```javascript
import { Kyber512 } from 'pqc-kyber';  // NEW: Browser PQC library

const handleUpload = async (file, userPassword) => {
  // 1. Derive encryption key from password
  const salt = crypto.getRandomValues(new Uint8Array(16));
  const keyMaterial = await crypto.subtle.importKey(
    'raw',
    new TextEncoder().encode(userPassword),
    'PBKDF2',
    false,
    ['deriveBits']
  );
  const derivedKey = await crypto.subtle.deriveBits(
    { name: 'PBKDF2', salt, iterations: 100000, hash: 'SHA-256' },
    keyMaterial,
    256
  );
  
  // 2. Generate Kyber keypair in browser
  const kyber = new Kyber512();
  const { publicKey, secretKey } = await kyber.generateKeyPair();
  const { ciphertext, sharedSecret } = await kyber.encapsulate(publicKey);
  
  // 3. Encrypt file in browser
  const aesKey = sharedSecret.slice(0, 32);
  const nonce = crypto.getRandomValues(new Uint8Array(12));
  const fileData = await file.arrayBuffer();
  
  const encryptedData = await crypto.subtle.encrypt(
    { name: 'AES-GCM', iv: nonce },
    await crypto.subtle.importKey('raw', aesKey, 'AES-GCM', false, ['encrypt']),
    fileData
  );
  
  // 4. Combine everything into blob
  const blob = new Blob([nonce, ciphertext, encryptedData]);
  
  // 5. Upload encrypted blob (server can't decrypt)
  const formData = new FormData();
  formData.append('file', blob, file.name);
  formData.append('salt', btoa(String.fromCharCode(...salt)));
  
  const response = await fetch(`${API_URL}/api/storage/upload`, {
    method: 'POST',
    body: formData
  });
};
```

**Backend (app.py):**
```python
def storage_upload():
    file_data = request.files['file'].read()  # Already encrypted blob
    salt = request.form.get('salt')
    
    # Server just stores the blob, can't decrypt it
    file_id = str(uuid.uuid4())
    storage_path = STORAGE_DIR / f"{file_id}.enc"
    
    with open(storage_path, 'wb') as f:
        f.write(file_data)  # Store encrypted blob as-is
    
    # Store metadata only (NO KEYS)
    c.execute('''INSERT INTO cloud_files 
                 (id, filename, filepath, salt, size, ...)
                 VALUES (?, ?, ?, ?, ?, ...)''',
              (file_id, filename, str(storage_path), salt, len(file_data), ...))
    
    # Server never sees or stores decryption keys ✅
```

---

## 🛠️ Implementation Changes Required

### 1. Frontend Changes (Medium Difficulty)

**Files to modify:**
- `frontend/package.json` - Add dependencies
- `frontend/src/CloudStorage.jsx` - Client-side encryption
- `frontend/src/Login.jsx` - Key derivation from password
- `frontend/src/ShareDownload.jsx` - Client-side decryption

**New dependencies:**
```json
{
  "dependencies": {
    "@noble/post-quantum": "^0.2.0",  // Pure JS PQC library
    // OR
    "pqc-kyber": "^1.0.0"  // Alternative
  }
}
```

**Estimated time:** 4-5 hours

### 2. Backend Changes (Easy Difficulty)

**Files to modify:**
- `backend-python/app.py` - Remove encryption logic, store blobs only

**Changes:**
```python
# REMOVE: PQCCrypto.encrypt_file_simple()
# REMOVE: PQCCrypto.decrypt_file_simple()
# KEEP: User authentication
# KEEP: File storage/retrieval
# ADD: Salt storage for key derivation
```

**Estimated time:** 1-2 hours

### 3. Database Changes (Easy Difficulty)

**Migration required:**
```sql
-- Remove encryption key columns
ALTER TABLE cloud_files DROP COLUMN kem_ciphertext;
ALTER TABLE cloud_files DROP COLUMN encrypted_key;

-- Add salt for key derivation
ALTER TABLE cloud_files ADD COLUMN salt TEXT;
```

**Estimated time:** 30 minutes

### 4. Testing Changes (Medium Difficulty)

**New test cases:**
- Password-based key derivation
- Browser encryption/decryption
- File integrity after round-trip
- Performance benchmarks (JS vs Python)
- Password change workflow

**Estimated time:** 2-3 hours

---

## 📈 Performance Comparison

| Operation | Current (Python liboqs) | Zero-Knowledge (JS) | Difference |
|-----------|------------------------|---------------------|------------|
| **Kyber512 KeyGen** | ~0.05ms | ~5ms | 100x slower |
| **Kyber512 Encaps** | ~0.06ms | ~6ms | 100x slower |
| **AES-256 Encrypt (10MB)** | ~50ms | ~80ms | 1.6x slower |
| **Total Upload (10MB)** | ~100ms | ~200ms | 2x slower |
| **Total Download (10MB)** | ~100ms | ~200ms | 2x slower |

**Verdict:** Zero-knowledge is noticeably slower but still acceptable for most use cases.

---

## 🎯 Recommendation

### Keep Current Implementation If:
- ✅ You want fast performance
- ✅ You need password recovery
- ✅ You trust the server operator
- ✅ You want simpler code
- ✅ You're okay with Google Drive-level security

### Implement Zero-Knowledge If:
- ✅ Maximum privacy is critical
- ✅ You don't trust the server
- ✅ You can accept no password recovery
- ✅ You're willing to sacrifice some performance
- ✅ You want ProtonDrive-level security

---

## 🚀 Migration Path

If you decide to implement zero-knowledge later:

1. **Phase 1:** Implement alongside current system (dual mode)
2. **Phase 2:** Let users opt-in to zero-knowledge
3. **Phase 3:** Migrate existing files (requires user passwords)
4. **Phase 4:** Make zero-knowledge default

**Estimated total time:** 10-15 hours for full migration

---

**Current Status:** Server-side encryption (Google Drive model)  
**Future Option:** Zero-knowledge encryption (ProtonDrive model)  
**Decision:** Up to you based on your security vs usability priorities
