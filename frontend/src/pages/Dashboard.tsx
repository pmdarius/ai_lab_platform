import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import '../styles/Dashboard.css';

export const Dashboard: React.FC = () => {
  const { user, token } = useAuth();
  const [wallet, setWallet] = useState<any>(null);
  const [bookings, setBookings] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

  useEffect(() => {
    const fetchData = async () => {
      if (!token) return;

      try {
        // Fetch wallet balance
        const walletRes = await fetch(`${API_URL}/api/wallet/balance/`, {
          headers: { 'Authorization': `Bearer ${token}` },
        });
        const walletData = await walletRes.json();
        setWallet(walletData);

        // Fetch bookings
        const bookingsRes = await fetch(`${API_URL}/api/bookings/my_bookings/`, {
          headers: { 'Authorization': `Bearer ${token}` },
        });
        const bookingsData = await bookingsRes.json();
        setBookings(bookingsData);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [token]);

  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <h1>Welcome, {user?.first_name}!</h1>
        <p>KSRCE AI Lab Management System</p>
      </header>

      <div className="dashboard-grid">
        {/* Wallet Card */}
        <div className="card wallet-card">
          <h2>Wallet Balance</h2>
          {loading ? (
            <p>Loading...</p>
          ) : (
            <>
              <div className="balance-display">
                <span className="currency">₹</span>
                <span className="amount">{wallet?.balance || 0}</span>
              </div>
              <button className="btn-primary">Recharge Wallet</button>
              <p className="free-minutes">Free Minutes: {wallet?.free_minutes || 0}</p>
            </>
          )}
        </div>

        {/* Quick Stats */}
        <div className="card stats-card">
          <h2>Quick Stats</h2>
          <div className="stat-item">
            <span className="stat-label">Total Bookings</span>
            <span className="stat-value">{bookings.length}</span>
          </div>
          <div className="stat-item">
            <span className="stat-label">Active Sessions</span>
            <span className="stat-value">{bookings.filter(b => b.is_active).length}</span>
          </div>
        </div>

        {/* Recent Bookings */}
        <div className="card bookings-card">
          <h2>Recent Bookings</h2>
          {loading ? (
            <p>Loading...</p>
          ) : bookings.length > 0 ? (
            <ul className="bookings-list">
              {bookings.slice(0, 3).map((booking) => (
                <li key={booking.id} className={booking.is_active ? 'active' : ''}>
                  <span className="booking-slot">{booking.gpu_slot}</span>
                  <span className="booking-time">{new Date(booking.start_time).toLocaleDateString()}</span>
                </li>
              ))}
            </ul>
          ) : (
            <p>No bookings yet</p>
          )}
          <button className="btn-secondary">View All Bookings</button>
        </div>
      </div>

      {/* Action Buttons */}
      <div className="action-buttons">
        <button className="btn-large">Book GPU Slot</button>
        <button className="btn-large">Find Mentors</button>
        <button className="btn-large">View Courses</button>
      </div>
    </div>
  );
};
