import React, { useState } from 'react';
import { API_URL } from './config';

export default function Login({ onLogin }) {
  const [isLogin, setIsLogin] = useState(true);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    const endpoint = isLogin ? '/api/auth/login' : '/api/auth/register';

    try {
      const response = await fetch(`${API_URL}${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Authentication failed');
      }

      localStorage.setItem('token', data.token);
      localStorage.setItem('username', data.username);
      onLogin(data.token, data.username);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-page">
      <div className="glow-box">
        <div className="login-form-container">
          <div className="login-form-box">
            <h2 className="login-title">
              <span className="login-icon">⚡</span>
              {isLogin ? 'Login' : 'Sign Up'}
              <span className="login-icon-heart">🔐</span>
            </h2>
            
            <form onSubmit={handleSubmit}>
              <input
                type="text"
                placeholder="Username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
                className="glow-input"
              />
              <input
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                minLength="6"
                className="glow-input"
              />

              {error && <div className="error-message">{error}</div>}

              <button type="submit" disabled={loading} className="glow-submit">
                {loading ? 'Please wait...' : (isLogin ? 'Sign In' : 'Create Account')}
              </button>
            </form>

            <div className="login-links">
              <a href="#" onClick={(e) => e.preventDefault()}>Forgot Password?</a>
              <a href="#" onClick={(e) => { e.preventDefault(); setIsLogin(!isLogin); }} className="signup-link">
                {isLogin ? 'Sign Up' : 'Login'}
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
