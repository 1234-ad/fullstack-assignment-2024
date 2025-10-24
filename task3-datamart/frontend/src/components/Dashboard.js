import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../utils/api';

const Dashboard = () => {
  const [datasets, setDatasets] = useState([]);
  const [userStats, setUserStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      const [datasetsResponse, statsResponse] = await Promise.all([
        api.get('/datasets'),
        api.get('/user/stats')
      ]);
      
      setDatasets(datasetsResponse.data);
      setUserStats(statsResponse.data);
    } catch (err) {
      setError('Failed to load dashboard data');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="loading">Loading dashboard...</div>;
  }

  return (
    <div>
      <h1>DataMart Dashboard</h1>
      
      {error && (
        <div className="alert alert-error">
          {error}
        </div>
      )}

      {/* User Stats */}
      {userStats && (
        <div className="card mb-3">
          <h3>Your Statistics</h3>
          <div className="grid grid-2">
            <div>
              <strong>Total Purchases:</strong> {userStats.total_purchases}
            </div>
            <div>
              <strong>Total Spent:</strong> ${userStats.total_spent.toFixed(2)}
            </div>
            <div>
              <strong>Rows Purchased:</strong> {userStats.total_rows_purchased}
            </div>
          </div>
        </div>
      )}

      {/* Available Datasets */}
      <div className="card">
        <h3>Available Datasets</h3>
        <p>Explore our curated datasets and purchase the data you need.</p>
        
        {datasets.length === 0 ? (
          <p>No datasets available at the moment.</p>
        ) : (
          <div className="grid grid-2">
            {datasets.map(dataset => (
              <div key={dataset.id} className="card">
                <h4>{dataset.name}</h4>
                <p>{dataset.description}</p>
                <div className="mb-3">
                  <strong>Category:</strong> {dataset.category}<br/>
                  <strong>Total Rows:</strong> {dataset.total_rows.toLocaleString()}<br/>
                  <strong>Price per Row:</strong> ${dataset.price_per_row}
                </div>
                <Link 
                  to={`/explore/${dataset.id}`} 
                  className="btn btn-primary"
                >
                  Explore Dataset
                </Link>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;