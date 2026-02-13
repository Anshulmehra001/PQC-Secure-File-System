import React, { useState, useEffect } from 'react';
import { API_URL } from './config';

export default function CloudStorage({ token, username }) {
  const [files, setFiles] = useState([]);
  const [uploading, setUploading] = useState(false);

  useEffect(() => {
    fetchFiles();
  }, []);

  const fetchFiles = async () => {
    try {
      const response = await fetch(`${API_URL}/api/storage/files`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (!response.ok) throw new Error('Failed to fetch files');
      const data = await response.json();
      setFiles(data);
    } catch (error) {
      console.error('Failed to fetch files:', error);
    }
  };

  const handleUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setUploading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch(`${API_URL}/api/storage/upload`, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}` },
        body: formData
      });
      if (!response.ok) throw new Error('Upload failed');
      fetchFiles();
    } catch (error) {
      alert('Upload failed: ' + error.message);
    } finally {
      setUploading(false);
    }
  };

  const handleDownload = async (fileId, filename) => {
    try {
      const response = await fetch(`${API_URL}/api/storage/files/${fileId}/download`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (!response.ok) throw new Error('Download failed');
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = filename;
      a.click();
    } catch (error) {
      alert('Download failed: ' + error.message);
    }
  };

  const handleDelete = async (fileId) => {
    if (!confirm('Delete this file?')) return;

    try {
      const response = await fetch(`${API_URL}/api/storage/files/${fileId}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (!response.ok) throw new Error('Delete failed');
      fetchFiles();
    } catch (error) {
      alert('Delete failed: ' + error.message);
    }
  };

  return (
    <div className="container">
      <div className="hero">
        <h1>☁️ PQC Secure Cloud Storage</h1>
        <p className="subtitle">Welcome back, {username}! Your quantum-safe storage</p>
        <div className="hero-badges">
          <span className="hero-badge">Quantum-Resistant</span>
          <span className="hero-badge">Kyber512 + ML-DSA-44</span>
          <span className="hero-badge">AES-256-GCM</span>
        </div>
      </div>

      <div className="card">
        <div className="upload-header">
          <h2>My Files</h2>
          <label className="btn-primary upload-btn">
            {uploading ? 'Uploading...' : '+ Upload File'}
            <input type="file" onChange={handleUpload} disabled={uploading} style={{ display: 'none' }} />
          </label>
        </div>

        <div className="files-list">
          {files.length === 0 ? (
            <div className="empty-state">
              <p>No files yet. Upload your first file!</p>
            </div>
          ) : (
            files.map(file => (
              <div key={file.id} className="file-item">
                <div className="file-info">
                  <span className="file-icon">📄</span>
                  <div>
                    <div className="file-name">{file.filename}</div>
                    <div className="file-meta">
                      {(file.size / 1024).toFixed(2)} KB • {new Date(file.created_at).toLocaleDateString()}
                    </div>
                  </div>
                </div>
                <div className="file-actions">
                  <button onClick={() => handleDownload(file.id, file.filename)} className="btn-secondary">
                    Download
                  </button>
                  <button onClick={() => handleDelete(file.id)} className="btn-danger">
                    Delete
                  </button>
                </div>
              </div>
            ))
          )}
        </div>
      </div>

      <div className="features">
        <div className="feature">
          <div className="feature-icon">🔐</div>
          <h3>REAL PQC Encryption</h3>
          <p>CRYSTALS-Kyber512 + AES-256-GCM via liboqs</p>
          <span className="feature-badge">Not Simulated</span>
        </div>
        <div className="feature">
          <div className="feature-icon">🔑</div>
          <h3>NIST-Approved Algorithms</h3>
          <p>Using actual quantum-safe cryptography standards</p>
          <span className="feature-badge">2022 Standard</span>
        </div>
        <div className="feature">
          <div className="feature-icon">🛡️</div>
          <h3>128-bit Quantum Security</h3>
          <p>Protected against both classical and quantum attacks</p>
          <span className="feature-badge">Future-Proof</span>
        </div>
      </div>

      <div className="info-section">
        <h2>💡 Why Quantum-Safe Storage?</h2>
        <div className="info-grid">
          <div className="info-card">
            <h4>⚠️ The Threat</h4>
            <p>Quantum computers will break RSA and ECDSA encryption. "Harvest now, decrypt later" attacks are already happening.</p>
          </div>
          <div className="info-card">
            <h4>✅ The Solution</h4>
            <p>Post-Quantum Cryptography uses math problems that even quantum computers can't solve efficiently.</p>
          </div>
          <div className="info-card">
            <h4>🔬 Our Implementation</h4>
            <p>We use REAL NIST-approved algorithms (Kyber512, Dilithium2) via liboqs - not simulation!</p>
          </div>
        </div>
      </div>
    </div>
  );
}
