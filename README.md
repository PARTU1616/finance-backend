# Finance Data Processing and Access Control Backend

**Author**: Prathamesh Galugade  
**Email**: pratu1616@gmail.com

**Live Backend API**: https://finance-backend-1j75.onrender.com

A role-based financial dashboard system with Flask backend, PostgreSQL database, and Quasar + Vue 3 frontend. The system provides RESTful APIs for managing financial transactions, user accounts, and analytical summaries with three-tier access control.

## Live Demo

- **Frontend Application**: https://finance-backend-hvvf.vercel.app
- **Backend API**: https://finance-backend-1j75.onrender.com
- **API Base URL**: https://finance-backend-1j75.onrender.com/api
- **Test Credentials**: 
  - Email: `admin@finance.com`
  - Password: `admin123`

### Using the Application

1. **Visit the frontend**: https://finance-backend-hvvf.vercel.app
2. **Login** with the credentials above
3. **Explore**:
   - Dashboard: View financial summary, category breakdown, and recent transactions
   - Transactions: View, create, update, and delete transactions (Admin only)
   - Users: Manage user accounts (Admin only)

### Testing the API Directly

You can also test the API using cURL, Postman, or any HTTP client:

```bash
# Login
curl -X POST https://finance-backend-1j75.onrender.com/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@finance.com","password":"admin123"}'

# Get dashboard summary (after login with session cookie)
curl https://finance-backend-1j75.onrender.com/api/dashboard/summary/ \
  -H "Cookie: session=YOUR_SESSION_COOKIE"
```

## Features

- **Role-Based Access Control**: Three user roles (Viewer, Analyst, Admin) with different permissions
- **Financial Transaction Management**: CRUD operations with filtering, pagination, and search
- **Dashboard Analytics**: Summary statistics, category breakdowns, and trend analysis
- **User Management**: Create, update, and deactivate user accounts
- **Session-Based Authentication**: Redis-backed sessions with bcrypt password hashing
- **Rate Limiting**: 200 requests/day, 50 requests/hour per IP
- **Audit Trail**: Automatic tracking of created_by, updated_by, created_at, updated_at
- **Database Migrations**: Alembic for easy schema changes

## Technology Stack

**Backend:**
- Flask 3.1.1
- PostgreSQL with SQLAlchemy ORM
- Redis for session storage
- bcrypt for password hashing
- Flask-Limiter for rate limiting
- Alembic for database migrations

**Frontend:**
- Quasar 2.19.2 + Vue 3 + Vite
- Pinia for state management
- Axios for API calls

## Quick Start

### Prerequisites

- Python 3.10+
- PostgreSQL 12+
- Redis 6+
- Node.js 18+ (for frontend)

### Backend Setup

1. **Create Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

3. **Set Up PostgreSQL Database**
```bash
createdb finance_db
```

4. **Configure Environment Variables**

Create `.env` file:
```bash
SECRET_KEY=your-secret-key-here
FLASK_ENV=development
DATABASE_URL=postgresql://localhost:5432/finance_db
REDIS_URL=redis://localhost:6379/0
CORS_ORIGINS=http://localhost:9000
```

5. **Initialize Database**
```bash
python init_db.py
```

This creates:
- All database tables
- Default admin user (email: `admin@finance.com`, password: `admin123`)

6. **Run Backend**
```bash
python app.py
```

Backend runs at `http://localhost:5000`

### Frontend Setup

1. **Install Dependencies**
```bash
cd quasar-project
npm install
```

2. **Run Frontend**
```bash
npm run dev
```

Frontend runs at `http://localhost:9000`

### Default Login

- **Email**: admin@finance.com
- **Password**: admin123

⚠️ Change this password immediately in production!

## Project Structure

```
finance-backend/
├── api/                    # API route blueprints
│   ├── auth.py            # Authentication endpoints
│   ├── users.py           # User management
│   ├── transactions.py    # Transaction CRUD
│   └── dashboard.py       # Analytics endpoints
├── models/                # SQLAlchemy models
│   ├── user.py           # User model
│   └── financial_record.py # Transaction model
├── utils/                 # Utilities
│   └── authorization.py  # Auth decorator
├── migrations/            # Alembic migrations
├── quasar-project/       # Frontend application
├── app.py                # Flask app
├── config.py             # Configuration
├── init_db.py            # DB initialization
└── requirements.txt      # Python dependencies
```

## API Documentation

### Base URL
```
http://localhost:5000/api
```

### Response Format

**Success:**
```json
{
  "ok": true,
  "data": {...},
  "msg": "Success"
}
```

**Error:**
```json
{
  "ok": false,
  "error": "Error description",
  "msg": "User-friendly message"
}
```

### Authentication Endpoints

#### POST /auth/login/
```json
{
  "email": "admin@finance.com",
  "password": "admin123"
}
```

#### POST /auth/logout/
Destroy session

#### GET /auth/session/
Get current session info

### User Management (Admin Only)

#### GET /users/list/
Query params: `page`, `limit`, `search` (email)

#### POST /users/create/
```json
{
  "email": "user@example.com",
  "password": "password123",
  "role": "Viewer"
}
```

Valid roles: `Viewer`, `Analyst`, `Admin`

#### POST /users/update/<user_id>/
Update user details

#### POST /users/deactivate/<user_id>/
Deactivate user account

### Transaction Endpoints

#### GET /transactions/list/
Query params: `page`, `limit`, `category`, `type`, `start_date`, `end_date`

#### POST /transactions/create/ (Admin Only)
```json
{
  "amount": 1500.50,
  "type": "income",
  "category": "Salary",
  "date": "2024-01-15",
  "notes": "Monthly salary"
}
```

Valid types: `income`, `expense`

#### POST /transactions/update/<transaction_id>/ (Admin Only)
Update transaction

#### POST /transactions/delete/<transaction_id>/ (Admin Only)
Delete transaction

### Dashboard Endpoints (Analyst & Admin Only)

#### GET /dashboard/summary/
Query params: `start_date`, `end_date`

Returns: total income, total expenses, net balance, recent transactions

#### GET /dashboard/category-breakdown/
Query params: `start_date`, `end_date`

Returns: totals grouped by category

#### GET /dashboard/trends/
Query params: `period` (monthly/weekly), `periods` (number of periods)

Returns: time-series trend data

## User Roles and Permissions

| Role | Permissions |
|------|------------|
| **Viewer** | View transactions only |
| **Analyst** | View transactions + Dashboard analytics |
| **Admin** | Full access (CRUD transactions, manage users) |

## Database Migrations

### Create Migration
```bash
alembic revision --autogenerate -m "Description"
```

### Apply Migrations
```bash
alembic upgrade head
```

### Rollback
```bash
alembic downgrade -1
```

## Testing

### Test API
```bash
python test_api.py
```

### Manual Testing with cURL
```bash
# Login
curl -X POST http://localhost:5000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@finance.com","password":"admin123"}' \
  -c cookies.txt

# Create transaction
curl -X POST http://localhost:5000/api/transactions/create/ \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"amount":1500.50,"type":"income","category":"Salary","date":"2024-01-15"}'

# Get dashboard
curl http://localhost:5000/api/dashboard/summary/ -b cookies.txt
```

## Production Deployment

### Backend

1. **Set Production Environment**
```bash
SECRET_KEY=<strong-random-key>
FLASK_ENV=production
DATABASE_URL=postgresql://user:password@host:5432/finance_db
REDIS_URL=redis://host:6379/0
```

2. **Use Gunicorn**
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

3. **Set Up PostgreSQL**
```sql
CREATE DATABASE finance_db;
CREATE USER finance_user WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE finance_db TO finance_user;
```

### Frontend

```bash
cd quasar-project
npm run build
# Deploy dist/spa to static hosting or CDN
```

## Security Features

- ✅ Session-based authentication with Redis
- ✅ bcrypt password hashing
- ✅ Role-based access control
- ✅ Rate limiting (200/day, 50/hour per IP)
- ✅ Input validation on all endpoints
- ✅ SQL injection protection (SQLAlchemy ORM)
- ✅ CORS configuration
- ✅ Generic error messages (no information leakage)
- ✅ Audit trail (created_by, updated_by, timestamps)

## Design Decisions

### Why Session-Based Auth?
- Simpler than JWT for this use case
- Redis provides fast session storage
- Easy to invalidate sessions
- Works well with browser-based frontends

### Why Direct Database Queries?
- No unnecessary abstractions
- Clear and maintainable code
- Easy to understand and debug

### Why Standardized Response Format?
- Consistent client-side handling
- Easy to parse and display errors
- Clear success/failure indication

## Troubleshooting

### Database Connection Error
- Ensure PostgreSQL is running
- Check DATABASE_URL in .env
- Verify database exists

### Redis Connection Error
- Ensure Redis is running
- Check REDIS_URL in .env

### Import Errors
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt`

### Frontend Not Loading
- Check backend is running on port 5000
- Check frontend proxy configuration in quasar.config.js
- Verify CORS_ORIGINS in backend .env

## License

This project is for assessment purposes.

## Contact

**Prathamesh Galugade**  
Email: pratu1616@gmail.com
