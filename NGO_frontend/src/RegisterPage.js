import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const API_URL = 'http://127.0.0.1:5000';

function RegisterPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [role, setRole] = useState('Donor'); // Default role
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const navigate = useNavigate();

  const handleRegister = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    try {
      const response = await fetch(`${API_URL}/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password, role }),
      });

      const data = await response.json();

      if (response.ok) {
        setSuccess(data.message || 'Registration successful! Please login.');
        // Optionally clear form or redirect after success
        setEmail('');
        setPassword('');
        setRole('Donor');
        // navigate('/login'); // Can auto-redirect to login
      } else {
        setError(data.message || 'Registration failed. Please try again.');
      }
    } catch (err) {
      console.error('Network error during registration:', err);
      setError('Network error. Please try again.');
    }
  };

  return (
    <div className="auth-container">
      <form onSubmit={handleRegister} className="auth-form">
        <h2>Register</h2>
        {error && <p className="error-message">{error}</p>}
        {success && <p className="success-message">{success}</p>}
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
        <select value={role} onChange={(e) => setRole(e.target.value)}>
          <option value="Donor">Register as Donor</option>
          <option value="Volunteer">Register as Volunteer</option>
          {/* Admin role typically not self-registered in real apps */}
          {/* <option value="Owner">Admin</option> */}
        </select>
        <button type="submit">Register</button>
        <p className="auth-switch">
          Already have an account? <span onClick={() => navigate('/login')}>Login here.</span>
        </p>
      </form>
    </div>
  );
}

export default RegisterPage;