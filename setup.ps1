# Windows Setup Script for School Management System
# Run this script in PowerShell as Administrator

Write-Host "==================================" -ForegroundColor Cyan
Write-Host "School Management System - Setup" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version
    Write-Host "✓ $pythonVersion found" -ForegroundColor Green
}
catch {
    Write-Host "✗ Python is not installed!" -ForegroundColor Red
    Write-Host "Please install Python 3.11+ from https://www.python.org/downloads/" -ForegroundColor Red
    exit 1
}

# Check if Node.js is installed
Write-Host "Checking Node.js installation..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version
    Write-Host "✓ Node.js $nodeVersion found" -ForegroundColor Green
}
catch {
    Write-Host "✗ Node.js is not installed!" -ForegroundColor Red
    Write-Host "Please install Node.js 18+ from https://nodejs.org/" -ForegroundColor Red
    exit 1
}

# Check if PostgreSQL is installed
Write-Host "Checking PostgreSQL installation..." -ForegroundColor Yellow
try {
    $pgVersion = psql --version
    Write-Host "✓ $pgVersion found" -ForegroundColor Green
}
catch {
    Write-Host "⚠ PostgreSQL not found in PATH" -ForegroundColor Yellow
    Write-Host "Please ensure PostgreSQL is installed and running" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "==================================" -ForegroundColor Cyan
Write-Host "Setting up Backend..." -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan

# Navigate to backend directory
Set-Location -Path "backend"

# Create virtual environment
Write-Host "Creating Python virtual environment..." -ForegroundColor Yellow
python -m venv venv

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
.\venv\Scripts\Activate.ps1

# Install requirements
Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file if it doesn't exist
if (-not (Test-Path ".env")) {
    Write-Host "Creating .env file from template..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    Write-Host "⚠ Please edit backend\.env with your database credentials" -ForegroundColor Yellow
}

Write-Host "✓ Backend setup complete!" -ForegroundColor Green
Write-Host ""

# Go back to root
Set-Location -Path ".."

Write-Host "==================================" -ForegroundColor Cyan
Write-Host "Setting up Frontend..." -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan

# Navigate to frontend directory
Set-Location -Path "frontend"

# Install npm dependencies
Write-Host "Installing Node.js dependencies..." -ForegroundColor Yellow
npm install

Write-Host "✓ Frontend setup complete!" -ForegroundColor Green
Write-Host ""

# Go back to root
Set-Location -Path ".."

Write-Host "==================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Ensure PostgreSQL is running and create the database" -ForegroundColor White
Write-Host "2. Edit backend\.env with your database credentials" -ForegroundColor White
Write-Host "3. Run database migrations: cd backend; .\venv\Scripts\activate; alembic upgrade head" -ForegroundColor White
Write-Host "4. Start backend: cd backend; .\venv\Scripts\activate; uvicorn app.main:app --reload" -ForegroundColor White
Write-Host "5. Start frontend (new terminal): cd frontend; npm start" -ForegroundColor White
Write-Host ""
Write-Host "Full instructions: See SETUP_GUIDE.md" -ForegroundColor Cyan
