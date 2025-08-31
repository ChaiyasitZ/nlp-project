@echo off
echo ============================================
echo MongoDB Atlas Initialization Script
echo ============================================
echo.

echo Activating Python virtual environment...
call venv\Scripts\activate.bat

echo.
echo Running MongoDB initialization...
python init_mongodb.py

echo.
echo Initialization complete!
pause
