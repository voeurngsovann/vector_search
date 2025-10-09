@echo off
echo ========================================
echo Movie Quotes Vector Search Setup
echo ========================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)

echo ✅ Python found
echo.

:: Create virtual environment
echo 🔧 Creating virtual environment...
if exist venv (
    echo Virtual environment already exists
    choice /m "Do you want to recreate it"
    if errorlevel 2 goto :skip_venv_creation
    rmdir /s /q venv
)

python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)

:skip_venv_creation
echo ✅ Virtual environment ready
echo.

:: Activate virtual environment and install requirements
echo 📦 Installing requirements...
call venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt

if errorlevel 1 (
    echo ERROR: Failed to install requirements
    pause
    exit /b 1
)

echo ✅ Requirements installed
echo.

:: Create .env file if it doesn't exist
if not exist .env (
    if exist .env.template (
        echo 📝 Creating .env file...
        copy .env.template .env
        echo ⚠️  Please edit .env file with your database credentials
    ) else (
        echo WARNING: .env.template not found
    )
) else (
    echo ✅ .env file already exists
)

echo.
echo ========================================
echo 🎉 Setup completed successfully!
echo ========================================
echo.
echo Next steps:
echo 1. Edit .env file with your Oracle database credentials
echo 2. Run: venv\Scripts\activate.bat
echo 3. Run: streamlit run app.py
echo 4. Open browser to: http://localhost:8501
echo.
pause