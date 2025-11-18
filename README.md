# NotifyX 📬

![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?logo=postgresql)
![Redis](https://img.shields.io/badge/Redis-7-DC382D?logo=redis)
![Celery](https://img.shields.io/badge/Celery-5.4-37814A?logo=celery)
![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?logo=docker)
![License](https://img.shields.io/badge/License-MIT-green)

A multi-channel notification service built with FastAPI, Celery, and PostgreSQL. Send notifications via email, SMS, push, and in-app channels with user preference management and real-time updates.

## 🎯 What It Does

NotifyX lets you send notifications across multiple channels while respecting user preferences. It handles async processing, retries failed deliveries, and provides real-time status updates via WebSockets.

**Live Demo**: [notifyx.fly.dev](https://notifyx.fly.dev) 

## ✨ Features

- **Multi-Channel Support**: Email, SMS, Push, In-App notifications
- **User Preferences**: Users can enable/disable specific channels
- **Async Processing**: Background task processing with Celery
- **Real-Time Updates**: WebSocket support for in-app notifications
- **Retry Logic**: Automatic retry with exponential backoff for failed deliveries
- **REST API**: Complete CRUD operations with JWT authentication
- **Monitoring**: Prometheus metrics + Grafana dashboards
- **Rate Limiting**: Built-in API rate limiting to prevent abuse

## 🏗️ Tech Stack

- **Backend**: FastAPI (Python 3.13)
- **Database**: PostgreSQL
- **Task Queue**: Celery + Redis
- **Monitoring**: Prometheus + Pushgateway + Grafana
- **Deployment**: Docker + Fly.io
- **Authentication**: JWT (OAuth2)

## 📋 Prerequisites

- Python 3.13+
- Docker & Docker Compose
- PostgreSQL (or use Docker)
- Redis (or use Docker)
- SMTP credentials (Gmail, SendGrid, etc.)
- Twilio account (for SMS, optional)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/notifyx.git
cd notifyx
```

### 2. Environment Setup

Create a `.env` file in the root directory:

```env
# Database
DATABASE_URL=postgresql://postgres:password@localhost:5432/notifyx
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_DB=notifyx

# Redis
REDIS_URL=redis://localhost:6379/0

# JWT Secret
SECRET_KEY=your-super-secret-key-change-this
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Email (Gmail example)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_EMAIL=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# SMS (Twilio - optional)
TWILIO_ACCOUNT_SID=your-account-sid
TWILIO_AUTH_TOKEN=your-auth-token
TWILIO_PHONE_NUMBER=+1234567890

# Monitoring
PUSHGATEWAY_URL=pushgateway:9091
```

### 3. Run with Docker Compose

```bash
docker-compose up -d
```

This starts:
- PostgreSQL (port 5432)
- Redis (port 6379)
- FastAPI app (port 8000)
- Celery worker
- Prometheus (port 9090)
- Pushgateway (port 9091)
- Grafana (port 3000)

### 4. Run Database Migrations

```bash
docker-compose exec web alembic upgrade head
```

### 5. Access the Services

- **API Docs**: http://localhost:8000/docs
- **Grafana**: http://localhost:3000 (admin/admin)
- **Prometheus**: http://localhost:9090

## 📖 API Usage

### Create a User

```bash
curl -X POST "http://localhost:8000/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123",
    "phone": "+1234567890",
    "full_name": "John Doe",
    "preferences": {
      "email": true,
      "sms": false,
      "push": true,
      "in_app": true
    }
  }'
```

### Login

```bash
curl -X POST "http://localhost:8000/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@example.com&password=password123"
```

Response:
```json
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer"
}
```

### Send a Notification

```bash
curl -X POST "http://localhost:8000/notifications/" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1,
    "title": "Welcome!",
    "message": "Thanks for joining NotifyX",
    "channels": ["email", "in_app"]
  }'
```

### Check Notification Status

```bash
curl -X GET "http://localhost:8000/notifications/{notification_id}" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### WebSocket Connection (Real-time Updates)

```javascript
const ws = new WebSocket('ws://localhost:8000/notifications/ws/1');

ws.onmessage = (event) => {
  const notification = JSON.parse(event.data);
  console.log('New notification:', notification);
};
```

## 🗂️ Project Structure

```
notifyx/
├── alembic/                 # Database migrations
│   └── versions/            # Migration files
├── app/
│   ├── routers/            # API endpoints
│   │   ├── auth.py         # Login/authentication
│   │   ├── users.py        # User management
│   │   └── notifications.py # Notification endpoints
│   ├── services/           # Business logic
│   │   ├── email_service.py
│   │   ├── sms_service.py
│   │   ├── redis_pubsub.py
│   │   └── metrics.py      # Prometheus metrics
│   ├── workers/            # Celery tasks
│   │   └── notification_tasks.py
│   ├── models.py           # SQLAlchemy models
│   ├── schemas.py          # Pydantic schemas
│   ├── database.py         # DB connection
│   ├── oauth2.py           # JWT logic
│   └── main.py             # FastAPI app
├── tests/                  # Unit tests (WIP)
├── docker-compose.yml      # Local development
├── Dockerfile              # Container image
├── fly.toml                # Fly.io deployment
└── requirements.txt        # Python dependencies
```

## 📊 Monitoring

### Prometheus Metrics

Available at `http://localhost:8000/metrics`:

- `notifications_sent_total` - Total notifications sent (by channel, status)
- `notification_duration_seconds` - Time to send notification
- `pending_notifications` - Current queue depth

### Grafana Dashboard

1. Open http://localhost:3000
2. Login with `admin/admin`
3. Add Prometheus datasource: `http://prometheus:9090`
4. Import dashboard (or create custom panels)

**Key Panels**:
- Notification success rate by channel
- P95 latency per channel
- Failed notifications over time
- Queue depth monitoring

## 🧪 Testing

```bash
# Run tests (WIP)
pytest tests/

# Check test coverage
pytest --cov=app tests/
```

## 🔧 Development

### Run Locally (Without Docker)

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
alembic upgrade head

# Start FastAPI
uvicorn app.main:app --reload

# Start Celery worker (separate terminal)
celery -A app.celery_app worker --loglevel=info
```

### Create a New Migration

```bash
alembic revision --autogenerate -m "Add new column"
alembic upgrade head
```

## 🚀 Deployment

### Deploy to Fly.io

```bash
# Install flyctl
curl -L https://fly.io/install.sh | sh

# Login
flyctl auth login

# Create app
flyctl launch

# Set secrets
flyctl secrets set DATABASE_URL=postgres://...
flyctl secrets set REDIS_URL=rediss://...
flyctl secrets set SECRET_KEY=...

# Deploy
flyctl deploy
```

## 🐛 Known Issues / TODs

- [ ] Push notification service not implemented (need Firebase integration)
- [ ] SMS requires paid Twilio account
- [ ] No unit tests yet (tests/ folder empty)
- [ ] WebSocket polling could be more efficient
- [ ] Need to add idempotency keys for retry safety
- [ ] Rate limiting needs fine-tuning for production load

## 🤔 What I Learned

Building this project taught me:
- How to structure a FastAPI application with proper separation of concerns
- Working with Celery for background jobs and understanding worker patterns
- Database migrations with Alembic
- Real-time communication with WebSockets
- Setting up observability with Prometheus and Grafana
- Containerization and orchestration with Docker
- JWT authentication and OAuth2 flows

**Challenges faced**:
- Getting Celery to work with Redis SSL (Upstash) required special config
- WebSocket connection management and Redis pub/sub integration
- Prometheus Pushgateway setup for ephemeral workers
- Alembic migrations with enums in PostgreSQL

## 📚 Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Celery Best Practices](https://docs.celeryq.dev/en/stable/userguide/tasks.html)
- [SQLAlchemy ORM Tutorial](https://docs.sqlalchemy.org/en/20/orm/tutorial.html)
- [Prometheus Python Client](https://github.com/prometheus/client_python)

## 📄 License

MIT License - feel free to use this for learning!

## 🙋 Contributing

This is a learning project, but suggestions and improvements are welcome! Open an issue or PR.

## 📬 Contact

Built by HARSHA - [harshaa7654@gmail.com]

---

⭐ If this helped you learn something new, consider giving it a star!
