// src/AdminDashboard.js

import React from 'react';
import { Link, Outlet } from 'react-router-dom'; // Using Outlet to render nested routes
import './AdminDashboard.css'; // We will create this CSS file

function AdminDashboard({ onLogout }) {
  return (
    <div className="admin-container">
      
      {/* --- Sidebar Navigation --- */}
      <nav className="admin-sidebar">
        <div className="admin-sidebar-header">
          <h3>Admin Panel</h3>
        </div>
        <ul>
          <li><Link to="/admin/dashboard/stats">Dashboard Stats</Link></li>
          <li><Link to="/admin/dashboard/users">User Management</Link></li>
          <li><Link to="/admin/dashboard/donors">Donor Management</Link></li>
          <li><Link to="/admin/dashboard/volunteers">Volunteer Management</Link></li>
          <li><Link to="/admin/dashboard/campaigns">Campaigns</Link></li>
          <li><Link to="/admin/dashboard/events">Events & Tasks</Link></li>
          <li><Link to="/admin/dashboard/finances">Finances (Donations & Expenses)</Link></li>
          <li><Link to="/admin/dashboard/distributions">Beneficiaries & Distributions</Link></li>
        </ul>
        <div className="admin-sidebar-footer">
          <Link to="/" onClick={onLogout} className="admin-logout">Logout</Link>
        </div>
      </nav>

      {/* --- Main Content Area --- */}
      <main className="admin-main-content">
        {/* Child routes will be rendered here */}
        <Outlet /> 
      </main>
    </div>
  );
}

export default AdminDashboard;