import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const API_URL = 'http://127.0.0.1:5000';

function LoginPage({ onLoginSuccess }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setError(''); // Clear previous errors

    try {
      const response = await fetch(`${API_URL}/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      const data = await response.json();

      if (response.ok) {
        // Login successful
        console.log('Login successful:', data);
        // Pass user role and ID back to App.js
        onLoginSuccess(data.user_id, data.role);
        // Redirect based on role (App.js will handle this via onLoginSuccess)
      } else {
        // Login failed
        setError(data.message || 'Login failed. Please check your credentials.');
      }
    } catch (err) {
      console.error('Network error during login:', err);
      setError('Network error. Please try again.');
    }
  };

  return (
    <div className="auth-container">
      <form onSubmit={handleLogin} className="auth-form">
        <h2>Login</h2>
        {error && <p className="error-message">{error}</p>}
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <button type="submit">Login</button>
        <p className="auth-switch">
          Don't have an account? <span onClick={() => navigate('/register')}>Register here.</span>
        </p>
      </form>
    </div>
  );
}

export default LoginPage;