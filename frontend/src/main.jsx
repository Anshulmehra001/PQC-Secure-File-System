import React, { useState, useEffect } from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter, Routes, Route, Link, useLocation } from 'react-router-dom';
import FileSharing from './FileSharing';
import CloudStorage from './CloudStorage';
import ShareDownload from './ShareDownload';
import Login from './Login';
import { API_URL } from './config';
import './styles.css';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [token, setToken] = useState(null);
  const [username, setUsername] = useState(null);
  const location = useLocation();

  useEffect(() => {
    const savedToken = localStorage.getItem('token');
    const savedUsername = localStorage.getItem('username');
    if (savedToken && savedUsername) {
      setToken(savedToken);
      setUsername(savedUsername);
      setIsAuthenticated(true);
    }
  }, []);

  const handleLogin = (newToken, newUsername) => {
    setToken(newToken);
    setUsername(newUsername);
    setIsAuthenticated(true);
  };

  const handleLogout = () => {
    if (token) {
      fetch(`${API_URL}/api/auth/logout`, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}` }
      }).catch(() => {});
    }
    localStorage.removeItem('token');
    localStorage.removeItem('username');
    setToken(null);
    setUsername(null);
    setIsAuthenticated(false);
  };

  const isStoragePage = location.pathname === '/storage';

  return (
    <div className="app">
      <nav className="navbar">
        <div className="nav-brand">🔐 PQC Secure File System</div>
        <div className="nav-links">
          <Link to="/">File Sharing</Link>
          <Link to="/storage">Cloud Storage</Link>
          {isAuthenticated && (
            <span className="user-info">
              👤 {username}
              <button onClick={handleLogout} className="logout-btn">Logout</button>
            </span>
          )}
        </div>
      </nav>
      <Routes>
        <Route path="/" element={<FileSharing />} />
        <Route path="/storage" element={
          isAuthenticated ? 
            <CloudStorage token={token} username={username} /> : 
            <Login onLogin={handleLogin} />
        } />
        <Route path="/share/:id" element={<ShareDownload />} />
      </Routes>
    </div>
  );
}

function AppWrapper() {
  return (
    <BrowserRouter>
      <App />
    </BrowserRouter>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(<AppWrapper />);
