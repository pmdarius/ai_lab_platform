import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import '../styles/Wallet.css';

declare global {
  interface Window {
    Razorpay: any;
  }
}

export const WalletRecharge: React.FC = () => {
  const [amount, setAmount] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const { token } = useAuth();

  const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

  const handleRecharge = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    setLoading(true);

    try {
      // Create order
      const orderResponse = await fetch(`${API_URL}/api/payments/create_order/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({ amount }),
      });

      const orderData = await orderResponse.json();

      if (!orderData.order_id) {
        setError('Failed to create payment order');
        setLoading(false);
        return;
      }

      // Load Razorpay script
      const script = document.createElement('script');
      script.src = 'https://checkout.razorpay.com/v1/checkout.js';
      script.onload = () => {
        const options = {
          key: orderData.key_id,
          amount: parseInt(amount) * 100,
          currency: 'INR',
          name: 'KSRCE AI Lab',
          description: 'Wallet Recharge',
          order_id: orderData.order_id,
          handler: async (response: any) => {
            // Verify payment
            const verifyResponse = await fetch(`${API_URL}/api/payments/verify_payment/`, {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`,
              },
              body: JSON.stringify({
                razorpay_order_id: response.razorpay_order_id,
                razorpay_payment_id: response.razorpay_payment_id,
                razorpay_signature: response.razorpay_signature,
                amount,
              }),
            });

            const verifyData = await verifyResponse.json();
            if (verifyResponse.ok) {
              setSuccess(`Wallet recharged successfully! New balance: ₹${verifyData.new_balance}`);
              setAmount('');
            } else {
              setError(verifyData.error || 'Payment verification failed');
            }
            setLoading(false);
          },
          prefill: {
            name: 'Student Name',
            email: 'student@ksrce.com',
          },
          theme: {
            color: '#00d9ff',
          },
        };

        const rzp = new window.Razorpay(options);
        rzp.open();
      };
      document.body.appendChild(script);
    } catch (err: any) {
      setError(err.message || 'An error occurred');
      setLoading(false);
    }
  };

  return (
    <div className="wallet-container">
      <div className="wallet-card">
        <h1>Recharge Wallet</h1>
        <p className="subtitle">Add funds to your account to book GPU slots</p>

        {error && <div className="error-message">{error}</div>}
        {success && <div className="success-message">{success}</div>}

        <form onSubmit={handleRecharge}>
          <div className="form-group">
            <label>Amount (₹)</label>
            <input
              type="number"
              value={amount}
              onChange={(e) => setAmount(e.target.value)}
              placeholder="Enter amount"
              min="100"
              step="100"
              required
            />
          </div>

          <div className="preset-amounts">
            <button type="button" onClick={() => setAmount('500')} className="preset-btn">₹500</button>
            <button type="button" onClick={() => setAmount('1000')} className="preset-btn">₹1000</button>
            <button type="button" onClick={() => setAmount('2000')} className="preset-btn">₹2000</button>
            <button type="button" onClick={() => setAmount('5000')} className="preset-btn">₹5000</button>
          </div>

          <button type="submit" disabled={loading || !amount} className="btn-primary">
            {loading ? 'Processing...' : 'Proceed to Payment'}
          </button>
        </form>

        <div className="info-box">
          <h3>Pricing Information</h3>
          <p>GPU Slot: ₹100/hour</p>
          <p>Mentor Session: ₹500/hour</p>
          <p>Minimum recharge: ₹100</p>
        </div>
      </div>
    </div>
  );
};
