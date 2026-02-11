# School Management System - Start Script
# This script starts both backend and frontend servers

Write-Host "==================================" -ForegroundColor Cyan
Write-Host "Starting School Management System" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""

# Start Backend in a new window
Write-Host "Starting Backend Server..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD\backend'; .\venv\Scripts\Activate.ps1; uvicorn app.main:app --reload"

# Wait a bit for backend to start
Start-Sleep -Seconds 3

# Start Frontend in a new window
Write-Host "Starting Frontend Server..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD\frontend'; npm start"

Write-Host ""
Write-Host "✓ Both servers are starting..." -ForegroundColor Green
Write-Host ""
Write-Host "Backend API: http://localhost:8000" -ForegroundColor Cyan
Write-Host "API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "Frontend App: http://localhost:4200" -ForegroundColor Cyan
Write-Host ""
Write-Host "Check the new terminal windows for server logs" -ForegroundColor Yellow
Write-Host "Press Ctrl+C in those windows to stop the servers" -ForegroundColor Yellow
