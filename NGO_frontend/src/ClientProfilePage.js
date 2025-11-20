// src/ClientProfilePage.js

import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

const API_URL = 'http://127.0.0.1:5000';

function ClientProfilePage({ userId, userRole, onLogout }) {
  const [profileData, setProfileData] = useState(null);
  const [error, setError] = useState('');

  // This useEffect runs when the component loads or when userId/userRole changes
  useEffect(() => {
    if (!userId || !userRole) {
      setError('Error: No user information found. Please log in again.');
      return;
    }

    // Determine which API endpoint to call based on the user's role
    const endpoint = userRole === 'Donor' ? `donors/${userId}` : `volunteers/${userId}`;

    // Fetch the user's specific profile data
    fetch(`${API_URL}/${endpoint}`)
      .then(response => {
        if (!response.ok) {
          throw new Error('Failed to fetch profile data.');
        }
        return response.json();
      })
      .then(data => {
        setProfileData(data);
      })
      .catch(err => {
        console.error('Error fetching profile:', err);
        setError(err.message);
      });
  }, [userId, userRole]); // Dependency array

  // --- Display loading, error, or profile data ---
  let content;
  if (error) {
    content = <p className="error-message">{error}</p>;
  } else if (!profileData) {
    content = <p>Loading profile...</p>;
  } else {
    // We have the data, display it
    content = (
      <div className="profile-details">
        {userRole === 'Donor' && (
          <>
            <p><strong>Name:</strong> {profileData.donor_name}</p>
            <p><strong>Email:</strong> {profileData.email}</p>
            <p><strong>Phone:</strong> {profileData.phone_number}</p>
            <p><strong>Address:</strong> {profileData.address}</p>
            <p><strong>Type:</strong> {profileData.donor_type}</p>
          </>
        )}
        {userRole === 'Volunteer' && (
          <>
            <p><strong>Name:</strong> {profileData.volunteer_name}</p>
            <p><strong>Email:</strong> {profileData.email}</p>
            <p><strong>Phone:</strong> {profileData.phone_number}</p>
            <p><strong>Skills:</strong> {profileData.skills}</p>
            <p><strong>Join Date:</strong> {profileData.join_date}</p>
          </>
        )}
      </div>
    );
  }

  return (
    <div className="dashboard-container">
      <nav className="navbar">
        <div className="navbar-logo">NGO-Connect (Dashboard)</div>
        <div className="navbar-links">
          <Link to="/" className="navbar-login clickable" onClick={onLogout}>Logout</Link>
        </div>
      </nav>
      
      <div className="dashboard-content">
        <h1>Welcome, {userRole}!</h1>
        <h3>Your Profile Details</h3>
        {content}
      </div>
    </div>
  );
}

export default ClientProfilePage;