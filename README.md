# School Management System

A comprehensive school management platform built with Angular, Python FastAPI, and PostgreSQL.

## 🚀 Features

### Phase 1 (Current Implementation)
- ✅ Student Information System
- ✅ Attendance Management
- ✅ Gradebook & Assessment

### Upcoming Phases
- Parent Portal
- Fee Management
- Timetable & Scheduling
- And 25+ more modules...

## 🛠️ Technology Stack

**Frontend:**
- Angular 17+
- Angular Material UI
- RxJS
- TypeScript

**Backend:**
- Python 3.11+
- FastAPI
- SQLAlchemy ORM
- Pydantic
- JWT Authentication

**Database:**
- PostgreSQL 15+

**DevOps:**
- Docker & Docker Compose
- Nginx (reverse proxy)

## 📋 Prerequisites

- Node.js 18+ and npm
- Python 3.11+
- PostgreSQL 15+
- Docker Desktop (optional, for containerized setup)

## 🏁 Quick Start

### Option 1: Docker Setup (Recommended)

```bash
# Clone and navigate to project
cd "School Management System - Feature Ideas"

# Start all services
docker-compose up -d

# Frontend: http://localhost:4200
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Option 2: Local Development

#### Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Set environment variables
copy .env.example .env
# Edit .env with your database credentials

# Run migrations
alembic upgrade head

# Start server
uvicorn app.main:app --reload
```

#### Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
ng serve
```

## 📊 Database Schema

See `backend/app/models/` for complete schema definitions.

## 🔐 Default Credentials

**Super Admin:**
- Email: admin@school.com
- Password: Admin@123

## 📖 API Documentation

Access interactive API docs at: http://localhost:8000/docs

## 🗂️ Project Structure

```
school-management-system/
├── backend/
│   ├── app/
│   │   ├── api/          # API endpoints
│   │   ├── models/       # Database models
│   │   ├── schemas/      # Pydantic schemas
│   │   ├── services/     # Business logic
│   │   ├── core/         # Configuration
│   │   └── utils/        # Utilities
│   ├── alembic/          # Database migrations
│   └── tests/            # Backend tests
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── modules/  # Feature modules
│   │   │   ├── shared/   # Shared components
│   │   │   ├── core/     # Core services
│   │   │   └── models/   # TypeScript models
└── docker-compose.yml
```

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
ng test
```

## 🎯 What's Included

### ✅ Modules Implemented (Phase 1)

1. **Student Information System**
   - Complete student profiles with demographics
   - Medical records and emergency contacts
   - Enrollment history and status tracking
   - Search and filter functionality
   - CRUD operations with role-based access

2. **Attendance Management**
   - Daily attendance marking (individual/bulk)
   - Multiple status types (Present, Absent, Late, Sick Leave, etc.)
   - Real-time attendance statistics
   - Date range reports and analytics
   - Automated percentage calculations

3. **Gradebook & Assessment**
   - Multiple assessment types (Quiz, Test, Assignment, etc.)
   - Automated grade calculation
   - Weighted grading support
   - Student performance tracking
   - Teacher-specific assessment management

### 🔐 Security Features

- JWT-based authentication
- Role-based access control (RBAC)
- Password hashing with bcrypt
- Secure API endpoints
- CORS configuration
- SQL injection prevention with ORM

### 📊 API Features

- RESTful API design
- Interactive API documentation (Swagger/OpenAPI)
- Request validation with Pydantic
- Async database operations
- Pagination support
- Error handling and logging

### 🎨 Frontend Features

- Modern Angular 17+ with standalone components
- Material Design UI components
- Responsive layout
- Form validation
- Real-time data updates
- Route guards for protected pages

## 📈 Performance

- Async/await for non-blocking operations
- Database connection pooling
- Optimized queries with SQLAlchemy
- Lazy loading for Angular modules
- Efficient state management

## 🔮 Coming Soon (Phase 2+)

- Parent Portal with real-time notifications
- Fee Management with payment gateway integration
- Timetable & Scheduling with conflict detection
- Library Management System
- Staff Management & Payroll
- AI-Powered Learning Analytics
- Virtual Classroom Integration
- Mobile Apps (iOS & Android)
- SMS & Email Notifications
- Transportation Management with GPS tracking

See [ROADMAP.md](ROADMAP.md) for detailed future plans.

## 🤝 Contributing

This is a proprietary project. For collaboration opportunities, please contact the project owner.

## 📝 License

Proprietary - All Rights Reserved

## 🆘 Support & Issues

### Common Issues & Solutions

**Database Connection Failed**
- Verify PostgreSQL is running
- Check credentials in `.env` file
- Ensure database exists

**Port Already in Use**
- Kill process on port 8000 (backend) or 4200 (frontend)
- Or change port in configuration files

**Module Not Found Errors**
- Backend: Activate venv and reinstall: `pip install -r requirements.txt`
- Frontend: Delete node_modules and reinstall: `npm install`

For detailed setup instructions, see [SETUP_GUIDE.md](SETUP_GUIDE.md)

## 👥 Contact

For questions, support, or collaboration:
- Email: support@schoolmanagementsystem.com
- Issues: Create an issue in the repository

## 🙏 Acknowledgments

Built with:
- FastAPI - Modern Python web framework
- Angular - Platform for building web applications
- PostgreSQL - World's most advanced open source database
- Material Design - Google's design system
- SQLAlchemy - Python SQL toolkit and ORM

---

**Made with ❤️ for better education management**
