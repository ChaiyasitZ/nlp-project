@echo off
echo Starting NewsTimelineAI Development Environment...
echo.

echo ============================================
echo MongoDB Atlas Configuration Required
echo ============================================
echo Please ensure you have:
echo 1. Created a MongoDB Atlas account
echo 2. Set up a cluster (free tier is fine)
echo 3. Created a database user
echo 4. Configured network access
echo 5. Updated .env file with your Atlas connection string
echo.
echo See MONGODB_ATLAS_SETUP.md for detailed instructions
echo ============================================
echo.

echo Starting Backend (Flask)...
cd backend
if not exist .env (
    echo Error: .env file not found!
    echo Please copy .env.example to .env and configure your MongoDB Atlas connection
    pause
    exit /b 1
)
start "Backend" cmd /k "venv\Scripts\activate && python app.py"

echo.
echo Starting Frontend (React + Vite)...
cd ..\frontend
start "Frontend" cmd /k "npm run dev"

echo.
echo All services started!
echo Frontend: http://localhost:5173
echo Backend: http://localhost:5000
echo Health Check: http://localhost:5000/api/health
echo.
echo Check the Backend terminal for MongoDB Atlas connection status
echo.
pause
