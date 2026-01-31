import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { API_URL } from './config';

export default function ShareDownload() {
  const { id } = useParams();
  const [fileInfo, setFileInfo] = useState(null);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchFileInfo();
  }, [id]);

  const fetchFileInfo = async () => {
    try {
      const response = await fetch(`${API_URL}/api/share/${id}`);
      if (!response.ok) {
        const data = await response.json();
        setError(data.error);
        return;
      }
      const data = await response.json();
      setFileInfo(data);
    } catch (error) {
      setError('Failed to load file');
    }
  };

  const handleDownload = async () => {
    try {
      const response = await fetch(`${API_URL}/api/share/${id}/download`);
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = fileInfo.filename;
      a.click();
    } catch (error) {
      alert('Download failed: ' + error.message);
    }
  };

  if (error) {
    return (
      <div className="container">
        <div className="card error-card">
          <h2>❌ {error}</h2>
          <p>This link may have expired or doesn't exist.</p>
        </div>
      </div>
    );
  }

  if (!fileInfo) {
    return (
      <div className="container">
        <div className="card">
          <p>Loading...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="container">
      <div className="card">
        <h2>📥 Download Shared File</h2>
        <div className="download-info">
          <div className="file-preview">
            <span className="file-icon-large">📄</span>
            <h3>{fileInfo.filename}</h3>
          </div>
          <div className="security-info">
            <p>✓ Encrypted with REAL CRYSTALS-Kyber512 (NIST PQC)</p>
            <p>✓ Signed with CRYSTALS-Dilithium2</p>
            <p>✓ Protected by AES-256-GCM</p>
            <p>⏰ Link expires: {new Date(fileInfo.expiresAt).toLocaleString()}</p>
          </div>
          <button onClick={handleDownload} className="btn-primary btn-large">
            Download File
          </button>
        </div>
      </div>
    </div>
  );
}
