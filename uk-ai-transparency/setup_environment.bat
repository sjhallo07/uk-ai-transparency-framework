@echo off
REM Creates a virtual environment and installs requirements
if not exist venv python -m venv venv
call venv\Scripts\activate
python -m pip install --upgrade pip
if exist requirements.txt (
    pip install -r requirements.txt
)
echo Environment setup complete.
pause
echo Setting up UK AI Transparency Framework Environment...

:: Check Python version
python --version
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    pause
    exit /b 1
)

:: Create virtual environment
echo Creating virtual environment...
python -m venv venv

:: Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

:: Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

:: Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Environment setup complete!
echo.
echo To activate the environment in the future, run:
echo venv\Scripts\activate
echo.
echo To run the dashboard:
echo streamlit run src/transparency_dashboard.py

pause
