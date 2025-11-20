// src/UserManagementPage.js

import React, { useState, useEffect } from 'react';
import './AdminDashboard.css'; // We'll re-use the same CSS

const API_URL = 'http://127.0.0.1:5000';

function UserManagementPage() {
  const [users, setUsers] = useState([]);
  const [error, setError] = useState('');

  // --- Function to fetch all users ---
  const fetchUsers = () => {
    // NOTE: You need to create this /api/users endpoint in Flask!
    fetch(`${API_URL}/api/users`)
      .then(response => {
        if (!response.ok) {
          throw new Error('Failed to fetch users.');
        }
        return response.json();
      })
      .then(data => setUsers(data))
      .catch(err => {
        console.error('Error fetching users:', err);
        setError(err.message);
      });
  };

  // --- Run fetchUsers() once when the app loads ---
  useEffect(() => {
    fetchUsers();
  }, []);

  if (error) {
    return <div className="error-message">Error: {error} (Did you create the /api/users endpoint in Flask?)</div>;
  }

  if (!users) {
    return <p>Loading users...</p>;
  }

  return (
    <div className="admin-page-content">
      <h2>User Management</h2>
      <p>Here you can view all registered users and manage their roles.</p>

      <table className="admin-table">
        <thead>
          <tr>
            <th>User ID</th>
            <th>Email</th>
            <th>Role</th>
            <th>Created At</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {users.map(user => (
            <tr key={user.user_id}>
              <td>{user.user_id}</td>
              <td>{user.email}</td>
              <td>{user.role}</td>
              <td>{user.created_at}</td>
              <td>
                <button className="admin-btn-edit">Edit Role</button>
                <button className="admin-btn-delete">Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default UserManagementPage;