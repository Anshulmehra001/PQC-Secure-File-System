import React, { useState } from 'react';
import { API_URL } from './config';
import Loader from './Loader';

export default function FileSharing() {
  const [file, setFile] = useState(null);
  const [expiryHours, setExpiryHours] = useState(24);
  const [shareMode, setShareMode] = useState('download'); // 'download' or 'view_only'
  const [shareLink, setShareLink] = useState('');
  const [loading, setLoading] = useState(false);
  const [encryptionSteps, setEncryptionSteps] = useState([]);

  const handleUpload = async () => {
    if (!file) return;

    setLoading(true);
    setEncryptionSteps([]);
    setShareLink('');

    // Show encryption steps
    const steps = [
      { step: 1, text: '🔑 Generating Kyber512 keypair...', delay: 500 },
      { step: 2, text: '🔐 Encrypting file with AES-256-GCM...', delay: 1000 },
      { step: 3, text: '✍️ Signing with Dilithium2...', delay: 1500 },
      { step: 4, text: '💾 Storing encrypted file...', delay: 2000 },
      { step: 5, text: '✅ Generating share link...', delay: 2500 }
    ];

    steps.forEach(({ step, text, delay }) => {
      setTimeout(() => {
        setEncryptionSteps(prev => [...prev, text]);
      }, delay);
    });

    const formData = new FormData();
    formData.append('file', file);
    formData.append('expiryHours', expiryHours);
    formData.append('shareMode', shareMode);

    try {
      console.log('Uploading file to backend...');
      const response = await fetch(`${API_URL}/api/share/upload`, {
        method: 'POST',
        body: formData
      });
      
      console.log('Response status:', response.status);
      const data = await response.json();
      console.log('Response data:', data);
      
      if (!response.ok || data.error) {
        throw new Error(data.error || `Server error: ${response.status}`);
      }
      
      setTimeout(() => {
        console.log('Setting share link:', data.shareLink);
        setShareLink(data.shareLink);
        setLoading(false);
      }, 3000);
    } catch (error) {
      console.error('Upload error:', error);
      alert('Upload failed: ' + error.message);
      setLoading(false);
      setEncryptionSteps([]);
    }
  };

  return (
    <div className="container">
      {loading && (
        <Loader 
          steps={[
            '🔑 Generating Kyber512 keypair...',
            '🔐 Encrypting with AES-256-GCM...',
            '✍️ Signing with ML-DSA-44...',
            '💾 Storing encrypted file...',
            '✅ Generating share link...'
          ]} 
        />
      )}
      
      <div className="hero">
        <h1>🔐 PQC-Based Secure File Sharing</h1>
        <p className="subtitle">Share files that even quantum computers can't hack</p>
        <div className="hero-badges">
          <span className="hero-badge">NIST-Approved</span>
          <span className="hero-badge">Quantum-Safe</span>
          <span className="hero-badge">Real PQC</span>
        </div>
      </div>

      <div className="card">
        <h2>📤 Upload & Share</h2>
        <div className="upload-section">
          <div className="file-input-wrapper">
            <input
              type="file"
              onChange={(e) => setFile(e.target.files[0])}
              className="file-input"
              id="file-upload"
            />
            <label htmlFor="file-upload" className="file-input-label">
              {file ? `📄 ${file.name}` : '📁 Choose a file to encrypt'}
            </label>
          </div>
          
          <div className="expiry-section">
            <label>🔒 Share Type:</label>
            <select value={shareMode} onChange={(e) => setShareMode(e.target.value)} className="share-mode-select">
              <option value="download">📥 Allow Download</option>
              <option value="view_only">👁️ View Only (No Download)</option>
            </select>
          </div>
          
          <div className="expiry-section">
            <label>⏰ Link expires in:</label>
            <select value={expiryHours} onChange={(e) => setExpiryHours(e.target.value)}>
              <option value="1">1 hour</option>
              <option value="6">6 hours</option>
              <option value="24">24 hours (recommended)</option>
              <option value="72">3 days</option>
              <option value="168">1 week</option>
            </select>
          </div>

          <button onClick={handleUpload} disabled={!file || loading} className="btn-primary btn-large">
            {loading ? '🔐 Encrypting with PQC...' : '🚀 Upload & Generate Quantum-Safe Link'}
          </button>
        </div>

        {shareLink && (
          <div className="share-result">
            <h3>✅ File Encrypted & Shared Successfully!</h3>
            <p className="success-message">Your file is now protected with quantum-safe encryption</p>
            <div className="share-link">
              <input type="text" value={shareLink} readOnly />
              <button onClick={() => {
                navigator.clipboard.writeText(shareLink);
                alert('Link copied! Share it securely.');
              }}>📋 Copy Link</button>
            </div>
            <div className="security-badges">
              <span className="badge badge-kyber">✓ CRYSTALS-Kyber512</span>
              <span className="badge badge-dilithium">✓ CRYSTALS-Dilithium2</span>
              <span className="badge badge-aes">✓ AES-256-GCM</span>
              <span className="badge badge-expiry">⏰ Expires in {expiryHours}h</span>
            </div>
            <div className="info-box">
              <p><strong>🔬 What just happened?</strong></p>
              <p>Your file was encrypted using REAL Post-Quantum Cryptography algorithms approved by NIST. Even future quantum computers cannot decrypt it!</p>
            </div>
          </div>
        )}
      </div>

      <div className="features">
        <div className="feature">
          <div className="feature-icon">🔒</div>
          <h3>REAL Quantum-Safe Encryption</h3>
          <p>CRYSTALS-Kyber512 via liboqs</p>
          <span className="feature-badge">NIST-Approved</span>
        </div>
        <div className="feature">
          <div className="feature-icon">⏰</div>
          <h3>Expiring Links</h3>
          <p>Links automatically expire after set time</p>
          <span className="feature-badge">Secure Sharing</span>
        </div>
        <div className="feature">
          <div className="feature-icon">✍️</div>
          <h3>REAL PQC Signatures</h3>
          <p>CRYSTALS-Dilithium2 ensures authenticity</p>
          <span className="feature-badge">No Simulation</span>
        </div>
      </div>

      <div className="info-section">
        <h2>🎓 How It Works</h2>
        <div className="how-it-works">
          <div className="work-step">
            <div className="step-number">1</div>
            <h4>Upload File</h4>
            <p>Choose any file you want to share securely</p>
          </div>
          <div className="work-step">
            <div className="step-number">2</div>
            <h4>PQC Encryption</h4>
            <p>File encrypted with Kyber512 + AES-256-GCM</p>
          </div>
          <div className="work-step">
            <div className="step-number">3</div>
            <h4>Digital Signature</h4>
            <p>Signed with Dilithium2 for authenticity</p>
          </div>
          <div className="work-step">
            <div className="step-number">4</div>
            <h4>Share Link</h4>
            <p>Get quantum-safe shareable link</p>
          </div>
        </div>
      </div>
    </div>
  );
}
