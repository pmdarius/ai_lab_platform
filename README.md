# KSRCE AI Lab Management Website

A cutting-edge, modern web platform for managing the KSRCE AI Supercomputing Lab in partnership with Global Knowledge Technologies (GKT).

## Project Overview

This is a full-stack Lab-as-a-Service (LaaS) platform that enables:

- **Students** to book GPU slots, manage wallets, and access mentorship
- **Faculty** to create courses and track student usage
- **Admins** to manage the lab, monitor hardware, and generate reports
- **Mentors** to offer guidance on AI/ML projects

## Technology Stack

| Component | Technology |
| :--- | :--- |
| **Backend** | Python (Django + Django REST Framework) |
| **Frontend** | React with TypeScript + Material-UI |
| **Database** | PostgreSQL |
| **Real-time** | Django Channels + WebSockets |
| **Payments** | Razorpay + Stripe |
| **Hosting** | AWS (EC2 + RDS + S3) |
| **Containerization** | Docker + Docker Compose |

## Project Structure

```
ai_lab_platform/
├── config/                 # Django settings and configuration
├── core/                   # Core models and utilities
├── api/                    # API endpoints
├── payments/               # Payment processing
├── bookings/               # Slot booking system
├── mentors/                # Mentor management
├── monitoring/             # GPU monitoring
├── frontend/               # React application
│   ├── src/
│   ├── public/
│   └── package.json
├── manage.py               # Django management script
├── requirements.txt        # Python dependencies
├── docker-compose.yml      # Docker development setup
└── README.md
```

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 22+
- PostgreSQL 15+
- Redis 7+
- Docker & Docker Compose (optional)

### Local Development Setup

1. **Clone the repository:**
   ```bash
   cd /home/ubuntu/ai_lab_platform
   ```

2. **Create and activate virtual environment:**
   ```bash
   python3.11 -m venv venv
   source venv/bin/activate
   ```

3. **Install backend dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Run database migrations:**
   ```bash
   python manage.py migrate
   ```

6. **Create superuser:**
   ```bash
   python manage.py createsuperuser
   ```

7. **Start backend server:**
   ```bash
   python manage.py runserver
   ```

8. **In another terminal, setup frontend:**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

### Using Docker Compose

```bash
docker-compose up -d
```

This will start:
- PostgreSQL database
- Redis cache
- Django backend (port 8000)
- React frontend (port 3000)

## API Endpoints

### Authentication
- `POST /api/auth/signup/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/verify-otp/` - OTP verification
- `POST /api/auth/logout/` - User logout

### Wallet & Payments
- `GET /api/wallet/balance/` - Get wallet balance
- `POST /api/wallet/recharge/` - Recharge wallet
- `GET /api/wallet/transactions/` - Transaction history
- `POST /api/payments/razorpay/webhook/` - Razorpay webhook

### Slot Booking
- `GET /api/slots/available/` - Get available slots
- `POST /api/bookings/create/` - Create booking
- `GET /api/bookings/my-bookings/` - User's bookings
- `POST /api/bookings/extend/` - Extend booking time

### Mentors
- `GET /api/mentors/` - List mentors
- `POST /api/mentors/book/` - Book mentor session
- `GET /api/mentors/my-sessions/` - My mentor sessions

### Admin
- `GET /api/admin/dashboard/` - Admin dashboard data
- `GET /api/admin/users/` - Manage users
- `GET /api/admin/analytics/` - Analytics and reports

## Security Checklist

All security requirements from the security checklist have been implemented:

- ✅ OTP-based login
- ✅ JWT authentication
- ✅ Role-based access control (RBAC)
- ✅ Data encryption at rest and in transit
- ✅ Input validation and sanitization
- ✅ Rate limiting
- ✅ Security headers
- ✅ CORS configuration
- ✅ Secure password handling
- ✅ Comprehensive logging

## Database Schema

Key models:
- **User** - Student, Faculty, Admin, Mentor
- **Wallet** - User wallet with balance and transactions
- **GPUSlot** - Available GPU time slots
- **Booking** - User GPU slot bookings
- **Mentor** - Mentor profiles and expertise
- **MentorSession** - Scheduled mentor sessions
- **Payment** - Payment transactions
- **MonitoringData** - GPU hardware metrics

## Deployment

### AWS Deployment

1. **Create EC2 instance** with Ubuntu 22.04
2. **Install Docker and Docker Compose**
3. **Clone repository and setup environment**
4. **Configure RDS PostgreSQL database**
5. **Setup S3 bucket for media files**
6. **Deploy using Docker Compose or Kubernetes**

### Environment Variables for Production

```
DEBUG=False
SECRET_KEY=your-production-secret-key
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DB_HOST=your-rds-endpoint
RAZORPAY_KEY_ID=your-production-key
RAZORPAY_KEY_SECRET=your-production-secret
```

## Testing

Run tests with:

```bash
python manage.py test
```

Run security tests:

```bash
python manage.py check --deploy
```

## Monitoring & Logging

- **Application Logs:** `/var/log/ai_lab/`
- **Database Logs:** PostgreSQL logs
- **GPU Monitoring:** Real-time metrics via monitoring agent
- **Error Tracking:** Sentry integration (optional)

## Contributing

1. Create a feature branch
2. Make your changes
3. Write tests
4. Submit a pull request

## License

This project is proprietary to KSRCE and Global Knowledge Technologies.

## Support

For issues and support, contact: support@ksrce-gkt-lab.com

## Roadmap

**Phase 1 (MVP - 3 days):**
- ✅ Signup/Login with OTP
- ✅ Wallet and Payments
- ✅ Slot Booking
- ✅ Basic Admin Dashboard
- ✅ Email Notifications

**Phase 2 (Extended Features):**
- AI Coursework Integration
- Leaderboard & Achievements
- Project Showcase Portal
- Industry Projects Marketplace
- Web Push Notifications

**Phase 3 (Advanced Features):**
- Partner College Portal
- Advanced Analytics
- AI Model Training Pipeline
- Certificate Generation
- Research Hub Integration

---

**Last Updated:** December 12, 2025
**Version:** 1.0.0-MVP
