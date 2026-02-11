# 🚀 Quick Start Guide - School Management System

## Prerequisites

Before you begin, ensure you have the following installed:
- **Python 3.11+** - [Download](https://www.python.org/downloads/)
- **Node.js 18+** and npm - [Download](https://nodejs.org/)
- **PostgreSQL 15+** - [Download](https://www.postgresql.org/download/)
- **Git** - [Download](https://git-scm.com/downloads)

## Step 1: Database Setup

1. Install and start PostgreSQL server

2. Create the database and user:
```sql
-- Open PostgreSQL command line or pgAdmin and run:
CREATE DATABASE school_management;
CREATE USER school_admin WITH PASSWORD 'school_password_123';
GRANT ALL PRIVILEGES ON DATABASE school_management TO school_admin;
```

## Step 2: Backend Setup

1. Navigate to backend directory:
```powershell
cd "c:\School Management System - Feature Ideas\backend"
```

2. Create and activate virtual environment:
```powershell
python -m venv venv
.\venv\Scripts\activate
```

3. Install dependencies:
```powershell
pip install -r requirements.txt
```

4. Create environment file:
```powershell
copy .env.example .env
```

5. **IMPORTANT:** Edit the `.env` file with your settings (database URL, etc.)

6. Initialize database with Alembic:
```powershell
# Create initial migration
alembic revision --autogenerate -m "Initial migration"

# Apply migrations
alembic upgrade head
```

7. Start the backend server:
```powershell
uvicorn app.main:app --reload
```

✅ Backend should now be running at: **http://localhost:8000**
📖 API Documentation: **http://localhost:8000/docs**

## Step 3: Frontend Setup

1. Open a NEW terminal/PowerShell window

2. Navigate to frontend directory:
```powershell
cd "c:\School Management System - Feature Ideas\frontend"
```

3. Install dependencies:
```powershell
npm install
```

4. Start the development server:
```powershell
npm start
```

✅ Frontend should now be running at: **http://localhost:4200**

## Step 4: Create Initial Admin User

You need to create an admin user through the API. You can use the Swagger UI at http://localhost:8000/docs

1. Go to **http://localhost:8000/docs**
2. Find the **POST /api/v1/auth/register** endpoint
3. Click "Try it out"
4. Use this JSON body:

```json
{
  "email": "admin@school.com",
  "username": "admin",
  "password": "Admin@123",
  "first_name": "System",
  "last_name": "Administrator",
  "phone": "1234567890",
  "role": "super_admin"
}
```

5. Click "Execute"

## Step 5: Login

1. Open http://localhost:4200 in your browser
2. Login with:
   - **Username:** admin
   - **Password:** Admin@123

## 🎉 You're All Set!

The application should now be fully functional with:
- ✅ Student Information System
- ✅ Attendance Management
- ✅ Gradebook & Assessment

## 🔧 Troubleshooting

### Database Connection Errors
- Make sure PostgreSQL is running
- Check your database credentials in `.env` file
- Verify the database exists: `psql -U school_admin -d school_management`

### Port Already in Use
- Backend (8000): Stop other processes using port 8000
- Frontend (4200): Stop other Angular apps or change port in `angular.json`

### Python Package Errors
- Make sure you're in the virtual environment (you should see `(venv)` in your terminal)
- Try: `pip install --upgrade pip` then reinstall requirements

### Node Module Errors
- Delete `node_modules` folder and `package-lock.json`
- Run `npm install` again

## 📁 Project Structure

```
School Management System - Feature Ideas/
├── backend/                # Python FastAPI backend
│   ├── app/
│   │   ├── api/           # API endpoints
│   │   ├── models/        # Database models
│   │   ├── schemas/       # Pydantic schemas
│   │   └── core/          # Configuration & security
│   ├── alembic/           # Database migrations
│   └── requirements.txt   # Python dependencies
├── frontend/              # Angular frontend
│   ├── src/
│   │   ├── app/          # Angular application
│   │   └── environments/ # Environment configs
│   └── package.json      # Node dependencies
├── docker-compose.yml    # Docker configuration
└── README.md             # Main documentation
```

## 🐳 Docker Alternative (Optional)

If you prefer Docker:

```powershell
docker-compose up -d
```

This will start all services (database, backend, frontend) automatically.

## 📚 Next Steps

1. **Add Students:** Go to Students → Add Student
2. **Mark Attendance:** Go to Attendance → Select date → Mark attendance
3. **Create Assessments:** Go to Gradebook → Create Assessment
4. **Explore API:** Visit http://localhost:8000/docs for interactive API documentation

## 🆘 Need Help?

- Check the main README.md for detailed documentation
- API documentation: http://localhost:8000/docs
- Check backend logs in the terminal where uvicorn is running
- Check frontend logs in browser Developer Console (F12)

---

**Happy Managing! 🎓**
