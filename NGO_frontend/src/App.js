import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, useNavigate } from 'react-router-dom';
import './App.css';
import LoginPage from './LoginPage';
import RegisterPage from './RegisterPage';
import AdminDashboard from './AdminDashboard';
import ClientProfilePage from './ClientProfilePage';
import UserManagementPage from './UserManagementPage';

// --- Home Page Component (moved to its own component for routing) ---
const API_URL = 'http://127.0.0.1:5000';

function HomePage({ userRole, onLogout }) {
  const [stats, setStats] = useState(null);
  const [campaigns, setCampaigns] = useState([]);
  const navigate = useNavigate(); // Hook for navigation

  useEffect(() => {
    fetch(`${API_URL}/api/public-stats`)
      .then(response => response.json())
      .then(data => setStats(data))
      .catch(error => console.error('Error fetching stats:', error));

    fetch(`${API_URL}/campaigns`)
      .then(response => response.json())
      .then(data => {
        setCampaigns(data.slice(0, 3)); // Show first 3 campaigns
      })
      .catch(error => console.error('Error fetching campaigns:', error));
  }, []);

  const handleLoginClick = () => {
    navigate('/login');
  };

  const handleLogoutClick = () => {
    onLogout(); // Call the logout function passed from App component
    navigate('/'); // Redirect to home after logout
  };

  const handleDashboardClick = () => {
    if (userRole === 'Owner' || userRole === 'Worker') {
      navigate('/admin/dashboard');
    } else if (userRole === 'Donor' || userRole === 'Volunteer') {
      navigate('/dashboard/profile');
    }
  };

  return (
    <div className="App">
      {/* --- Navigation Bar --- */}
      <nav className="navbar">
        <div className="navbar-logo">NGO-Connect</div>
        <div className="navbar-links">
          <a href="/">Home</a>
          <a href="/about">About Us</a>
          <a href="/campaigns">Campaigns</a>
          <a href="/get-involved">Get Involved</a>
          
          {userRole ? ( // Show Logout/Dashboard if logged in
            <>
              <span className="navbar-text">Welcome, {userRole}!</span>
              <span onClick={handleDashboardClick} className="navbar-login clickable">Dashboard</span>
              <span onClick={handleLogoutClick} className="navbar-login clickable">Logout</span>
            </>
          ) : ( // Show Login if not logged in
            <span onClick={handleLoginClick} className="navbar-login clickable">Login</span>
          )}
        </div>
      </nav>

      {/* --- Hero Section --- */}
      <header className="hero">
        <div className="hero-content">
          <h1>Empowering Change, Together.</h1>
          <p>We connect donors and volunteers with causes that matter.</p>
          <a href="/get-involved" className="hero-button">Get Involved Now</a>
        </div>
      </header>

      {/* --- Public Statistics Section --- */}
      <section className="stats-section">
        <h2>Our Impact at a Glance</h2>
        <div className="stats-container">
          {stats ? (
            <>
              <div className="stat-card">
                <h3>₹{stats.total_raised.toLocaleString('en-IN')}</h3>
                <p>Total Donations Raised</p>
              </div>
              <div className="stat-card">
                <h3>{stats.total_volunteers}</h3>
                <p>Registered Volunteers</p>
              </div>
              <div className="stat-card">
                <h3>{stats.active_campaigns}</h3>
                <p>Active Campaigns</p>
              </div>
            </>
          ) : (
            <p>Loading stats...</p>
          )}
        </div>
      </section>

      {/* --- "Our Campaigns" Section --- */}
      <section className="campaigns-section">
        <h2>Our Active Campaigns</h2>
        <div className="campaigns-container">
          {campaigns.length > 0 ? (
            campaigns.map(campaign => (
              <div className="campaign-card" key={campaign.campaign_id}>
                <h3>{campaign.campaign_name}</h3>
                <p>Status: {campaign.status}</p>
                <p>Goal: ₹{campaign.goal_amount.toLocaleString('en-IN')}</p>
                {/* You would add a progress bar here */}
                <a href={`/campaigns/${campaign.campaign_id}`} className="hero-button">
                  Learn More & Donate
                </a>
              </div>
            ))
          ) : (
            <p>Loading campaigns...</p>
          )}
        </div>
      </section>

    </div>
  );
}

// --- Main App Component (Handles Routing and Global State) ---
function App() {
  const [userId, setUserId] = useState(null);
  const [userRole, setUserRole] = useState(null);
  const navigate = useNavigate(); // This hook works inside Router context

  // Check for stored user info on initial load (for persistence)
  useEffect(() => {
    const storedUserId = localStorage.getItem('userId');
    const storedUserRole = localStorage.getItem('userRole');
    if (storedUserId && storedUserRole) {
      setUserId(storedUserId);
      setUserRole(storedUserRole);
    }
  }, []);

  const handleLoginSuccess = (id, role) => {
    setUserId(id);
    setUserRole(role);
    localStorage.setItem('userId', id); // Store in local storage
    localStorage.setItem('userRole', role); // Store in local storage
    
    // Redirect based on role
    if (role === 'Owner' || role === 'Worker') {
      navigate('/admin/dashboard');
    } else { // Donor or Volunteer
      navigate('/dashboard/profile');
    }
  };

  const handleLogout = () => {
    setUserId(null);
    setUserRole(null);
    localStorage.removeItem('userId');
    localStorage.removeItem('userRole');
    navigate('/'); // Go to home page
  };

  return (
    <Routes>
  <Route path="/" element={<HomePage userRole={userRole} onLogout={handleLogout} />} />
  <Route path="/login" element={<LoginPage onLoginSuccess={handleLoginSuccess} />} />
  <Route path="/register" element={<RegisterPage />} />

  {/* --- THIS IS THE NEW ADMIN ROUTE --- */}

<Route path="/admin/dashboard/*" element={<AdminDashboard onLogout={handleLogout} />} >

  {/* This is a nested "child" route. It will render inside the <Outlet /> */}
  <Route index element={<div><h2>Dashboard Statistics</h2><p>Here you will see charts and graphs.</p></div>} />

  <Route path="stats" element={<div><h2>Dashboard Statistics</h2><p>Here you will see charts and graphs.</p></div>} />

  {/* --- THIS IS THE UPDATED LINE --- */}
  <Route path="users" element={<UserManagementPage />} />

</Route>

  {/* --- THIS IS THE UPDATED LINE --- */}
  <Route 
    path="/dashboard/profile" 
    element={<ClientProfilePage userId={userId} userRole={userRole} onLogout={handleLogout} />} 
  />

  {/* Add more routes here as you build out other pages */}
</Routes>
  );
}

// Export a wrapper component for Router
function AppWrapper() {
  return (
    <Router>
      <App />
    </Router>
  );
}

export default AppWrapper;