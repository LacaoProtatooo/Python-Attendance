@echo off
REM Face Recognition Attendance System - Quick Start Script
REM This script checks requirements and runs the application

echo.
echo ============================================
echo Face Recognition Attendance System
echo ============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://www.python.org/
    pause
    exit /b 1
)

echo [✓] Python found
python --version

REM Check if required packages are installed
echo.
echo Checking required packages...
echo.

REM Check opencv-python
python -c "import cv2" >nul 2>&1
if errorlevel 1 (
    echo [!] opencv-python not found
    echo Installing: pip install opencv-python
    pip install opencv-python
)
echo [✓] opencv-python found

REM Check opencv-contrib-python
python -c "import cv2; cv2.face.LBPHFaceRecognizer_create()" >nul 2>&1
if errorlevel 1 (
    echo [!] opencv-contrib-python not found
    echo Installing: pip install opencv-contrib-python
    pip install opencv-contrib-python
)
echo [✓] opencv-contrib-python found

REM Check numpy
python -c "import numpy" >nul 2>&1
if errorlevel 1 (
    echo [!] numpy not found
    echo Installing: pip install numpy
    pip install numpy
)
echo [✓] numpy found

REM Check pillow
python -c "import PIL" >nul 2>&1
if errorlevel 1 (
    echo [!] pillow not found
    echo Installing: pip install pillow
    pip install pillow
)
echo [✓] pillow found

REM All requirements satisfied
echo.
echo ============================================
echo All requirements satisfied!
echo Launching Face Recognition Attendance System...
echo ============================================
echo.

REM Run the main application
python main.py

REM If application closes, show message
echo.
echo Application closed.
pause
