import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const Navbar = () => {
  const { user, logout } = useAuth();

  return (
    <nav className="navbar">
      <div className="container">
        <div className="d-flex justify-content-between align-items-center">
          <Link to="/dashboard" className="navbar-brand">
            DataMart
          </Link>
          <ul className="navbar-nav">
            <li className="nav-item">
              <Link to="/dashboard" className="nav-link">
                Dashboard
              </Link>
            </li>
            <li className="nav-item">
              <Link to="/profile" className="nav-link">
                Profile
              </Link>
            </li>
            <li className="nav-item">
              <span className="nav-link">
                Welcome, {user?.full_name || user?.email}
              </span>
            </li>
            <li className="nav-item">
              <button 
                onClick={logout} 
                className="btn btn-secondary"
                style={{ marginLeft: '10px' }}
              >
                Logout
              </button>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;