# Face Recognition Attendance System - PowerShell Quick Start

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Face Recognition Attendance System" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "[✓] Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Python not found. Please install Python 3.7+" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "Checking required packages..." -ForegroundColor Yellow
Write-Host ""

# Check opencv-python
try {
    python -c "import cv2" 2>$null
    Write-Host "[✓] opencv-python found" -ForegroundColor Green
} catch {
    Write-Host "[!] Installing opencv-python..." -ForegroundColor Yellow
    pip install opencv-python
}

# Check opencv-contrib-python
try {
    python -c "import cv2; cv2.face.LBPHFaceRecognizer_create()" 2>$null
    Write-Host "[✓] opencv-contrib-python found" -ForegroundColor Green
} catch {
    Write-Host "[!] Installing opencv-contrib-python..." -ForegroundColor Yellow
    pip install opencv-contrib-python
}

# Check numpy
try {
    python -c "import numpy" 2>$null
    Write-Host "[✓] numpy found" -ForegroundColor Green
} catch {
    Write-Host "[!] Installing numpy..." -ForegroundColor Yellow
    pip install numpy
}

# Check pillow
try {
    python -c "import PIL" 2>$null
    Write-Host "[✓] pillow found" -ForegroundColor Green
} catch {
    Write-Host "[!] Installing pillow..." -ForegroundColor Yellow
    pip install pillow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "All requirements satisfied!" -ForegroundColor Green
Write-Host "Launching application..." -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

# Run the application
python main.py
