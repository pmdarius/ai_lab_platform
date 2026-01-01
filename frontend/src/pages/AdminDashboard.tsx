import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import '../styles/AdminDashboard.css';

export const AdminDashboard: React.FC = () => {
  const { user, token } = useAuth();
  const [stats, setStats] = useState<any>(null);
  const [users, setUsers] = useState<any[]>([]);
  const [bookings, setBookings] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

  useEffect(() => {
    const fetchAdminData = async () => {
      if (!token || user?.user_type !== 'admin') {
        setLoading(false);
        return;
      }

      try {
        // Fetch users
        const usersRes = await fetch(`${API_URL}/api/users/`, {
          headers: { 'Authorization': `Bearer ${token}` },
        });
        const usersData = await usersRes.json();
        setUsers(Array.isArray(usersData) ? usersData : []);

        // Fetch bookings
        const bookingsRes = await fetch(`${API_URL}/api/bookings/`, {
          headers: { 'Authorization': `Bearer ${token}` },
        });
        const bookingsData = await bookingsRes.json();
        setBookings(Array.isArray(bookingsData) ? bookingsData : []);

        // Calculate stats
        setStats({
          total_users: usersData.length || 0,
          total_bookings: bookingsData.length || 0,
          active_bookings: bookingsData.filter((b: any) => b.is_active).length || 0,
          total_revenue: bookingsData.reduce((sum: number, b: any) => sum + (b.cost || 0), 0) || 0,
        });
      } finally {
        setLoading(false);
      }
    };

    fetchAdminData();
  }, [token, user]);

  if (user?.user_type !== 'admin') {
    return <div className="admin-error">Access Denied: Admin only</div>;
  }

  return (
    <div className="admin-dashboard">
      <header className="admin-header">
        <h1>Admin Dashboard</h1>
        <p>KSRCE AI Lab Management System</p>
      </header>

      {loading ? (
        <p>Loading...</p>
      ) : (
        <>
          {/* Stats Cards */}
          <div className="stats-grid">
            <div className="stat-card">
              <h3>Total Users</h3>
              <p className="stat-number">{stats?.total_users || 0}</p>
            </div>
            <div className="stat-card">
              <h3>Total Bookings</h3>
              <p className="stat-number">{stats?.total_bookings || 0}</p>
            </div>
            <div className="stat-card">
              <h3>Active Sessions</h3>
              <p className="stat-number">{stats?.active_bookings || 0}</p>
            </div>
            <div className="stat-card">
              <h3>Total Revenue</h3>
              <p className="stat-number">₹{stats?.total_revenue || 0}</p>
            </div>
          </div>

          {/* Users Table */}
          <div className="admin-section">
            <h2>Recent Users</h2>
            <table className="admin-table">
              <thead>
                <tr>
                  <th>Email</th>
                  <th>Name</th>
                  <th>Type</th>
                  <th>College</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {users.slice(0, 10).map((user: any) => (
                  <tr key={user.id}>
                    <td>{user.email}</td>
                    <td>{user.first_name} {user.last_name}</td>
                    <td><span className="badge">{user.user_type}</span></td>
                    <td>{user.college_name || '-'}</td>
                    <td>
                      <button className="action-btn">View</button>
                      <button className="action-btn delete">Delete</button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Bookings Table */}
          <div className="admin-section">
            <h2>Recent Bookings</h2>
            <table className="admin-table">
              <thead>
                <tr>
                  <th>User</th>
                  <th>GPU Slot</th>
                  <th>Start Time</th>
                  <th>End Time</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {bookings.slice(0, 10).map((booking: any) => (
                  <tr key={booking.id}>
                    <td>{booking.user_email || 'N/A'}</td>
                    <td>{booking.gpu_slot}</td>
                    <td>{new Date(booking.start_time).toLocaleString()}</td>
                    <td>{new Date(booking.end_time).toLocaleString()}</td>
                    <td>
                      <span className={`status ${booking.is_active ? 'active' : 'inactive'}`}>
                        {booking.is_active ? 'Active' : 'Completed'}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </>
      )}
    </div>
  );
};
