import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { API_URL } from './config';

export default function FileViewer() {
  const { id } = useParams();
  const [fileInfo, setFileInfo] = useState(null);
  const [error, setError] = useState('');
  const [viewUrl, setViewUrl] = useState('');
  const [pdfInfo, setPdfInfo] = useState(null);
  const [loadingPdf, setLoadingPdf] = useState(false);

  useEffect(() => {
    fetchFileInfo();
    
    const handleContextMenu = (e) => {
      e.preventDefault();
      return false;
    };
    
    const handleKeyDown = (e) => {
      if ((e.ctrlKey || e.metaKey) && (e.key === 's' || e.key === 'p')) {
        e.preventDefault();
        return false;
      }
      if (e.key === 'F12' || 
          ((e.ctrlKey || e.metaKey) && e.shiftKey && (e.key === 'I' || e.key === 'C' || e.key === 'J'))) {
        e.preventDefault();
        return false;
      }
    };
    
    document.addEventListener('contextmenu', handleContextMenu);
    document.addEventListener('keydown', handleKeyDown);
    
    return () => {
      document.removeEventListener('contextmenu', handleContextMenu);
      document.removeEventListener('keydown', handleKeyDown);
    };
  }, [id]);

  useEffect(() => {
    return () => {
      if (viewUrl) {
        URL.revokeObjectURL(viewUrl);
      }
    };
  }, [viewUrl]);

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
      
      const fileExtension = data.filename.split('.').pop().toLowerCase();
      
      if (fileExtension === 'pdf') {
        await fetchPdfInfo();
      } else {
        const fileResponse = await fetch(`${API_URL}/api/share/${id}/view`);
        if (!fileResponse.ok) {
          setError('Failed to load file content');
          return;
        }
        
        const blob = await fileResponse.blob();
        const objectUrl = URL.createObjectURL(blob);
        setViewUrl(objectUrl);
      }
    } catch (error) {
      setError('Failed to load file');
    }
  };

  const fetchPdfInfo = async () => {
    setLoadingPdf(true);
    try {
      const response = await fetch(`${API_URL}/api/share/${id}/pdf-info`);
      if (!response.ok) {
        setError('Failed to load PDF info');
        return;
      }
      const data = await response.json();
      setPdfInfo(data);
    } catch (error) {
      setError('Failed to load PDF');
    } finally {
      setLoadingPdf(false);
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

  const fileExtension = fileInfo.filename.split('.').pop().toLowerCase();
  const isImage = ['jpg', 'jpeg', 'png', 'gif', 'webp', 'svg'].includes(fileExtension);
  const isPDF = fileExtension === 'pdf';
  const isVideo = ['mp4', 'webm', 'ogg'].includes(fileExtension);
  const isAudio = ['mp3', 'wav', 'ogg'].includes(fileExtension);

  return (
    <div className="viewer-container" onContextMenu={(e) => e.preventDefault()}>
      <div className="viewer-header">
        <div className="viewer-info">
          <h2>👁️ {fileInfo.filename}</h2>
          <p className="viewer-warning">🔒 View-Only Mode - Download Disabled</p>
          <p className="viewer-expiry">⏰ Expires: {new Date(fileInfo.expiresAt).toLocaleString()}</p>
        </div>
      </div>
      
      <div className="viewer-content">
        {isImage && (
          <div className="image-viewer">
            <img 
              src={viewUrl} 
              alt={fileInfo.filename}
              onContextMenu={(e) => e.preventDefault()}
              draggable={false}
              style={{ userSelect: 'none', pointerEvents: 'none' }}
            />
            <div className="watermark">VIEW ONLY - {new Date().toLocaleDateString()}</div>
          </div>
        )}
        
        {isPDF && (
          <div className="pdf-viewer-secure">
            {loadingPdf && <p className="loading-text">🔄 Loading secure PDF viewer...</p>}
            {pdfInfo && (
              <div className="pdf-pages-secure">
                <p className="pdf-page-count">📄 {pdfInfo.pageCount} pages</p>
                {Array.from({ length: pdfInfo.pageCount }, (_, i) => i + 1).map((pageNum) => (
                  <div key={pageNum} className="pdf-page-container">
                    <div className="pdf-page-number">Page {pageNum} of {pdfInfo.pageCount}</div>
                    <div className="pdf-page-wrapper-secure">
                      <img 
                        src={`${API_URL}/api/share/${id}/pdf-page/${pageNum}`}
                        alt={`Page ${pageNum}`}
                        onContextMenu={(e) => e.preventDefault()}
                        draggable={false}
                        loading="lazy"
                        style={{ userSelect: 'none', pointerEvents: 'none', width: '100%', display: 'block' }}
                      />
                      <div className="page-watermark-secure">VIEW ONLY - Page {pageNum}</div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
        
        {isVideo && (
          <div className="video-viewer">
            <video 
              controls 
              controlsList="nodownload nofullscreen noremoteplayback"
              disablePictureInPicture
              onContextMenu={(e) => e.preventDefault()}
              style={{ width: '100%', maxHeight: '80vh' }}
            >
              <source src={viewUrl} />
            </video>
            <div className="watermark">VIEW ONLY - {new Date().toLocaleDateString()}</div>
          </div>
        )}
        
        {isAudio && (
          <div className="audio-viewer">
            <audio 
              controls 
              controlsList="nodownload"
              onContextMenu={(e) => e.preventDefault()}
              style={{ width: '100%' }}
            >
              <source src={viewUrl} />
            </audio>
            <p className="viewer-note">🎵 Audio file - View only mode</p>
          </div>
        )}
        
        {!isImage && !isPDF && !isVideo && !isAudio && (
          <div className="unsupported-viewer">
            <h3>📄 Preview Not Available</h3>
            <p>This file type cannot be previewed in the browser.</p>
            <p>File: {fileInfo.filename}</p>
          </div>
        )}
      </div>
      
      <div className="viewer-footer">
        <p>⚠️ This file is protected. Download, right-click, save, print, and DevTools are disabled.</p>
        <p>🔐 Encrypted with Kyber512 + AES-256-GCM + ML-DSA-44</p>
        <p className="disclaimer">⚠️ Note: Screenshots and screen recording cannot be prevented.</p>
      </div>
    </div>
  );
}
