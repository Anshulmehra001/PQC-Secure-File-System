from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import oqs
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import hashes
import os
import json
import time
import uuid
import sqlite3
import hashlib
import secrets
from pathlib import Path

app = Flask(__name__)
CORS(app)

UPLOAD_DIR = Path('uploads')
STORAGE_DIR = Path('storage')
UPLOAD_DIR.mkdir(exist_ok=True)
STORAGE_DIR.mkdir(exist_ok=True)

DB_PATH = 'pqc_files.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at INTEGER NOT NULL
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS shared_files (
            id TEXT PRIMARY KEY,
            filename TEXT NOT NULL,
            filepath TEXT NOT NULL,
            kem_ciphertext TEXT NOT NULL,
            encrypted_key TEXT NOT NULL,
            signature TEXT NOT NULL,
            sig_public_key TEXT NOT NULL,
            expires_at INTEGER NOT NULL,
            created_at INTEGER NOT NULL
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS cloud_files (
            id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            filename TEXT NOT NULL,
            filepath TEXT NOT NULL,
            kem_ciphertext TEXT NOT NULL,
            encrypted_key TEXT NOT NULL,
            size INTEGER NOT NULL,
            created_at INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            token TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            created_at INTEGER NOT NULL,
            expires_at INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    conn.commit()
    conn.close()

init_db()

class PQCCrypto:
    KEM_ALGORITHM = 'Kyber512'
    SIG_ALGORITHM = 'ML-DSA-44'
    
    @staticmethod
    def encrypt_file(file_data):
        with oqs.KeyEncapsulation(PQCCrypto.KEM_ALGORITHM) as kem:
            public_key = kem.generate_keypair()
            ciphertext, shared_secret = kem.encap_secret(public_key)
            
            aes_key = shared_secret[:32]
            aesgcm = AESGCM(aes_key)
            nonce = os.urandom(12)
            encrypted_data = aesgcm.encrypt(nonce, file_data, None)
            
            final_encrypted = nonce + encrypted_data
            
            return {
                'encrypted_data': final_encrypted.hex(),
                'kem_ciphertext': ciphertext.hex(),
                'kem_public_key': public_key.hex()
            }
    
    @staticmethod
    def decrypt_file(encrypted_data_hex, kem_ciphertext_hex, kem_public_key_hex):
        with oqs.KeyEncapsulation(PQCCrypto.KEM_ALGORITHM) as kem:
            raise NotImplementedError("Use decrypt_file_simple")
    
    @staticmethod
    def encrypt_file_simple(file_data):
        with oqs.KeyEncapsulation(PQCCrypto.KEM_ALGORITHM) as kem:
            public_key = kem.generate_keypair()
            ciphertext, shared_secret = kem.encap_secret(public_key)
            
            aes_key = shared_secret[:32]
            aesgcm = AESGCM(aes_key)
            nonce = os.urandom(12)
            encrypted_data = aesgcm.encrypt(nonce, file_data, None)
            
            final_encrypted = nonce + encrypted_data
            
            return {
                'encrypted_data': final_encrypted.hex(),
                'kem_ciphertext': ciphertext.hex(),
                'shared_secret': shared_secret.hex()
            }
    
    @staticmethod
    def decrypt_file_simple(encrypted_data_hex, shared_secret_hex):
        encrypted_data = bytes.fromhex(encrypted_data_hex)
        shared_secret = bytes.fromhex(shared_secret_hex)
        
        nonce = encrypted_data[:12]
        ciphertext = encrypted_data[12:]
        
        aes_key = shared_secret[:32]
        aesgcm = AESGCM(aes_key)
        decrypted_data = aesgcm.decrypt(nonce, ciphertext, None)
        
        return decrypted_data
    
    @staticmethod
    def sign_data(data):
        with oqs.Signature(PQCCrypto.SIG_ALGORITHM) as signer:
            public_key = signer.generate_keypair()
            signature = signer.sign(data)
            
            return {
                'signature': signature.hex(),
                'public_key': public_key.hex()
            }
    
    @staticmethod
    def verify_signature(data, signature_hex, public_key_hex):
        with oqs.Signature(PQCCrypto.SIG_ALGORITHM) as verifier:
            signature = bytes.fromhex(signature_hex)
            public_key = bytes.fromhex(public_key_hex)
            
            return verifier.verify(data, signature, public_key)

class Auth:
    @staticmethod
    def hash_password(password):
        salt = secrets.token_hex(16)
        pwd_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
        return f"{salt}${pwd_hash.hex()}"
    
    @staticmethod
    def verify_password(password, password_hash):
        salt, pwd_hash = password_hash.split('$')
        new_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
        return new_hash.hex() == pwd_hash
    
    @staticmethod
    def create_session(user_id):
        token = secrets.token_urlsafe(32)
        expires_at = int(time.time() * 1000) + (24 * 60 * 60 * 1000)
        
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('INSERT INTO sessions (token, user_id, created_at, expires_at) VALUES (?, ?, ?, ?)',
                  (token, user_id, int(time.time() * 1000), expires_at))
        conn.commit()
        conn.close()
        
        return token
    
    @staticmethod
    def verify_session(token):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('SELECT user_id, expires_at FROM sessions WHERE token = ?', (token,))
        result = c.fetchone()
        conn.close()
        
        if not result:
            return None
        
        user_id, expires_at = result
        if time.time() * 1000 > expires_at:
            return None
        
        return user_id

@app.route('/api/auth/register', methods=['POST'])
def register():
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'error': 'Username and password required'}), 400
        
        if len(password) < 6:
            return jsonify({'error': 'Password must be at least 6 characters'}), 400
        
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('SELECT id FROM users WHERE username = ?', (username,))
        if c.fetchone():
            conn.close()
            return jsonify({'error': 'Username already exists'}), 400
        
        user_id = str(uuid.uuid4())
        password_hash = Auth.hash_password(password)
        
        c.execute('INSERT INTO users (id, username, password_hash, created_at) VALUES (?, ?, ?, ?)',
                  (user_id, username, password_hash, int(time.time() * 1000)))
        conn.commit()
        conn.close()
        
        token = Auth.create_session(user_id)
        
        return jsonify({
            'token': token,
            'username': username
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'error': 'Username and password required'}), 400
        
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('SELECT id, password_hash FROM users WHERE username = ?', (username,))
        result = c.fetchone()
        conn.close()
        
        if not result:
            return jsonify({'error': 'Invalid credentials'}), 401
        
        user_id, password_hash = result
        
        if not Auth.verify_password(password, password_hash):
            return jsonify({'error': 'Invalid credentials'}), 401
        
        token = Auth.create_session(user_id)
        
        return jsonify({
            'token': token,
            'username': username
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/logout', methods=['POST'])
def logout():
    try:
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        
        if token:
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute('DELETE FROM sessions WHERE token = ?', (token,))
            conn.commit()
            conn.close()
        
        return jsonify({'success': True})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/verify', methods=['GET'])
def verify_auth():
    try:
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        user_id = Auth.verify_session(token)
        
        if not user_id:
            return jsonify({'error': 'Invalid session'}), 401
        
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('SELECT username FROM users WHERE id = ?', (user_id,))
        result = c.fetchone()
        conn.close()
        
        if not result:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'username': result[0],
            'userId': user_id
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# File Sharing Routes
@app.route('/api/share/upload', methods=['POST'])
def share_upload():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        expiry_hours = int(request.form.get('expiryHours', 24))
        file_data = file.read()
        
        encryption_result = PQCCrypto.encrypt_file_simple(file_data)
        signature_result = PQCCrypto.sign_data(bytes.fromhex(encryption_result['encrypted_data']))
        
        share_id = str(uuid.uuid4())
        encrypted_path = UPLOAD_DIR / f"{share_id}.enc"
        
        with open(encrypted_path, 'w') as f:
            f.write(encryption_result['encrypted_data'])
        
        expires_at = int(time.time() * 1000) + (expiry_hours * 60 * 60 * 1000)
        
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''
            INSERT INTO shared_files 
            (id, filename, filepath, kem_ciphertext, encrypted_key, signature, sig_public_key, expires_at, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            share_id,
            file.filename,
            str(encrypted_path),
            encryption_result['kem_ciphertext'],
            encryption_result['shared_secret'],
            signature_result['signature'],
            signature_result['public_key'],
            expires_at,
            int(time.time() * 1000)
        ))
        conn.commit()
        conn.close()
        
        return jsonify({
            'shareId': share_id,
            'shareLink': f'http://localhost:5173/share/{share_id}',
            'expiresAt': expires_at,
            'algorithm': f'Kyber512 + AES-256-GCM + ML-DSA-44'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/share/<share_id>', methods=['GET'])
def get_share_info(share_id):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('SELECT filename, expires_at FROM shared_files WHERE id = ?', (share_id,))
        result = c.fetchone()
        conn.close()
        
        if not result:
            return jsonify({'error': 'File not found'}), 404
        
        filename, expires_at = result
        
        if time.time() * 1000 > expires_at:
            return jsonify({'error': 'Link expired'}), 410
        
        return jsonify({
            'filename': filename,
            'expiresAt': expires_at
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/share/<share_id>/download', methods=['GET'])
def download_shared_file(share_id):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('SELECT * FROM shared_files WHERE id = ?', (share_id,))
        result = c.fetchone()
        conn.close()
        
        if not result:
            return jsonify({'error': 'File not found'}), 404
        
        _, filename, filepath, kem_ct, shared_secret, signature, sig_pk, expires_at, _ = result
        
        if time.time() * 1000 > expires_at:
            return jsonify({'error': 'Link expired'}), 410
        
        with open(filepath, 'r') as f:
            encrypted_data = f.read()
        
        if not PQCCrypto.verify_signature(bytes.fromhex(encrypted_data), signature, sig_pk):
            return jsonify({'error': 'Signature verification failed'}), 400
        
        decrypted_data = PQCCrypto.decrypt_file_simple(encrypted_data, shared_secret)
        
        temp_path = UPLOAD_DIR / f"temp_{share_id}"
        with open(temp_path, 'wb') as f:
            f.write(decrypted_data)
        
        response = send_file(temp_path, as_attachment=True, download_name=filename)
        
        @response.call_on_close
        def cleanup():
            if temp_path.exists():
                temp_path.unlink()
        
        return response
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Cloud Storage Routes
@app.route('/api/storage/upload', methods=['POST'])
def storage_upload():
    try:
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        user_id = Auth.verify_session(token)
        
        if not user_id:
            return jsonify({'error': 'Unauthorized'}), 401
        
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        file_data = file.read()
        file_size = len(file_data)
        
        encryption_result = PQCCrypto.encrypt_file_simple(file_data)
        
        file_id = str(uuid.uuid4())
        storage_path = STORAGE_DIR / f"{file_id}.enc"
        
        with open(storage_path, 'w') as f:
            f.write(encryption_result['encrypted_data'])
        
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''
            INSERT INTO cloud_files 
            (id, user_id, filename, filepath, kem_ciphertext, encrypted_key, size, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            file_id,
            user_id,
            file.filename,
            str(storage_path),
            encryption_result['kem_ciphertext'],
            encryption_result['shared_secret'],
            file_size,
            int(time.time() * 1000)
        ))
        conn.commit()
        conn.close()
        
        return jsonify({
            'fileId': file_id,
            'filename': file.filename,
            'size': file_size
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/storage/files', methods=['GET'])
def list_storage_files():
    try:
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        user_id = Auth.verify_session(token)
        
        if not user_id:
            return jsonify({'error': 'Unauthorized'}), 401
        
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''
            SELECT id, filename, size, created_at 
            FROM cloud_files 
            WHERE user_id = ?
            ORDER BY created_at DESC
        ''', (user_id,))
        results = c.fetchall()
        conn.close()
        
        files = [
            {
                'id': row[0],
                'filename': row[1],
                'size': row[2],
                'created_at': row[3]
            }
            for row in results
        ]
        
        return jsonify(files)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/storage/files/<file_id>/download', methods=['GET'])
def download_storage_file(file_id):
    try:
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        user_id = Auth.verify_session(token)
        
        if not user_id:
            return jsonify({'error': 'Unauthorized'}), 401
        
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('SELECT * FROM cloud_files WHERE id = ? AND user_id = ?', (file_id, user_id))
        result = c.fetchone()
        conn.close()
        
        if not result:
            return jsonify({'error': 'File not found'}), 404
        
        _, _, filename, filepath, kem_ct, shared_secret, _, _ = result
        
        with open(filepath, 'r') as f:
            encrypted_data = f.read()
        
        decrypted_data = PQCCrypto.decrypt_file_simple(encrypted_data, shared_secret)
        
        temp_path = STORAGE_DIR / f"temp_{file_id}"
        with open(temp_path, 'wb') as f:
            f.write(decrypted_data)
        
        response = send_file(temp_path, as_attachment=True, download_name=filename)
        
        @response.call_on_close
        def cleanup():
            if temp_path.exists():
                temp_path.unlink()
        
        return response
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/storage/files/<file_id>', methods=['DELETE'])
def delete_storage_file(file_id):
    try:
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        user_id = Auth.verify_session(token)
        
        if not user_id:
            return jsonify({'error': 'Unauthorized'}), 401
        
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('SELECT filepath FROM cloud_files WHERE id = ? AND user_id = ?', (file_id, user_id))
        result = c.fetchone()
        
        if not result:
            conn.close()
            return jsonify({'error': 'File not found'}), 404
        
        filepath = result[0]
        
        if os.path.exists(filepath):
            os.remove(filepath)
        
        c.execute('DELETE FROM cloud_files WHERE id = ?', (file_id,))
        conn.commit()
        conn.close()
        
        return jsonify({'success': True})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🔐 PQC Secure File System (Python + Real Crypto)")
    print(f"Using: {PQCCrypto.KEM_ALGORITHM} + {PQCCrypto.SIG_ALGORITHM}")
    app.run(host='0.0.0.0', port=3001, debug=True)
