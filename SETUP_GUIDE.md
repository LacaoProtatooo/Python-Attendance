# Face Recognition Attendance System - Setup & Usage Guide

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher installed
- Webcam connected to your computer

### Required Python Packages
```bash
pip install opencv-python opencv-contrib-python numpy pillow
```

### Run the Application
```bash
python main.py
```

---

## 📋 System Overview

This is a complete attendance system with 4 main components:

1. **Main Application** - Face registration and basic attendance
2. **Attendance Page** - Mark daily attendance with confirmation
3. **Admin Dashboard** - Manage students and view records
4. **Student Dashboard** - View personal attendance history

---

## 🎯 Step-by-Step Usage

### STEP 1: Register New Students

**From Main Window:**
1. Enter student name in the "Name:" field
2. Click **"Start Registration"** button
3. Face the camera (wait for green rectangle)
4. System captures 30 samples automatically
5. Model trains automatically after completion
6. **Student is added to database automatically**

✅ After registration:
- Student data saved to database
- Face model trained and saved
- Ready to mark attendance

---

### STEP 2: Mark Daily Attendance

**Method 1: Simple Attendance (Built-in)**
1. From Main Window → Click **"Start Attendance"**
2. Face the camera
3. Attendance marked automatically when face recognized
4. CSV file created with records

**Method 2: Attendance Page (Recommended)**
1. From Main Window → Click **"Start Camera"** (under Attendance Page section)
2. Camera starts → Shows detected face with confidence
3. Click **"✓ Accept & Mark Attendance"** to confirm
4. Attendance saved to database with exact time
5. Shows if already marked today
6. Click **"Stop Camera"** to finish

✅ What happens:
- Database updated with attendance record
- Timestamp recorded for entry time
- Cannot mark twice on same day
- Works offline if database exists

---

### STEP 3: Admin Dashboard

**Access:** Main Window → **"📊 Admin Dashboard"** button

**Features:**
- **View Students:** See all registered students in list
- **Add Students Manually:** 
  - Enter Name, Email, Student ID
  - Click "+ Add Student"
  - Added to database immediately
- **Manage Records:**
  - Select student and click "👁️ View Attendance"
  - See detailed attendance history
  - Click "🗑️ Delete Student" to remove
- **Refresh:** Click "🔄 Refresh" to reload list

---

### STEP 4: Student Dashboard

**Access:** Main Window → **"👤 Student Dashboard"** button

**Steps:**
1. Select student name from list
2. Click **"Open Dashboard"**
3. See their attendance statistics:
   - **Present:** Green box showing count
   - **Absent:** Red box showing count
   - **Late:** Yellow box showing count
   - **Total:** Blue box showing count

**Additional Options:**
- **View Records:** Detailed table of all attendance dates and times
- **🔄 Refresh:** Update data from database
- **📥 Export to CSV:** Download attendance records as Excel file
- **← Back:** Return to main menu

Color coding:
- 🟢 Green = Present
- 🔴 Red = Absent
- 🟡 Yellow = Late

---

## 🗂️ File Descriptions

| File | Purpose |
|------|---------|
| `main.py` | Main application entry point - Run this to start |
| `database.py` | SQLite database manager for students and attendance |
| `attendance_page.py` | Dedicated attendance marking interface |
| `admin_dashboard.py` | Admin interface to manage students |
| `student_dashboard.py` | Student interface to view records |
| `attendance.db` | SQLite database (auto-created) |
| `face_recognizer.yml` | Trained face recognition model |
| `labels.pkl` | Student label mappings for faces |
| `images/` | Folder storing captured face samples |

---

## 💾 Database Information

### Students Table
```
- ID (auto-generated)
- Name (unique)
- Email (optional)
- Student ID (optional)
- Status (active/inactive)
- Created At (timestamp)
```

### Attendance Table
```
- ID (auto-generated)
- Student ID (links to Students)
- Date (YYYY-MM-DD format)
- Time In (HH:MM:SS format)
- Status (present/absent/late)
- Created At (timestamp)
```

**Auto-created on first run!** No manual setup needed.

---

## ⚙️ Complete Workflow Example

### Day 1: Setup
```
1. Run: python main.py
2. Enter "John Doe" → Click "Start Registration"
3. Capture 30 samples by facing camera
4. Model trains automatically
5. John Doe added to database
6. Ready to mark attendance
```

### Day 2: Mark Attendance
```
1. Run: python main.py
2. From Main → Click "Mark Attendance" page
3. Click "Start Camera"
4. Face camera → System detects "John Doe"
5. Click "✓ Accept & Mark Attendance"
6. Recorded in database with timestamp
7. Attendance marked successfully
```

### Day 3: Check Records
```
1. Run: python main.py
2. Click "👤 Student Dashboard"
3. Select "John Doe" → Click "Open Dashboard"
4. See:
   - 2 days Present ✓
   - Statistics updated
   - Timeline of attendance
5. Export to CSV if needed
```

---

## 🔧 Troubleshooting

### Issue: "Camera not opening"
**Solution:**
- Close other apps using camera (Zoom, Teams, etc.)
- Unplug/replug webcam
- Check Windows camera permissions
- Restart application

### Issue: "Face not detected"
**Solution:**
- Increase room lighting
- Move closer to camera (30-60 cm)
- Remove sunglasses/masks
- Ensure face is fully visible

### Issue: "No trained model found"
**Solution:**
- Register at least one student first
- Model created automatically after first registration
- Ensure registration process completes fully

### Issue: "Student already marked today"
**Solution:**
- Expected! Each student marks once per day
- Different students can mark on same system
- Next day they can mark again

### Issue: "Database errors"
**Solution:**
- Delete `attendance.db` file to reset
- Application creates new database on restart
- CSV files remain unchanged

### Issue: "GUI looks strange"
**Solution:**
- Check Python version: `python --version`
- Reinstall: `pip install pillow --upgrade`
- Check screen resolution (works on 1280x720+)

---

## 📊 Reports & Exports

### CSV Export
1. Student Dashboard → **"📥 Export to CSV"**
2. Creates file: `Attendance_StudentName_YYYYMMDD.csv`
3. Contains: Name, Date, Time, Status
4. Open in Excel or Google Sheets

### Daily Attendance CSV
- Also creates: `Attendance_YYYY-MM-DD.csv` automatically
- Contains all attendance for the day

---

## 🔐 Security Notes

- Database is local SQLite (not online)
- Face samples stored locally in `images/` folder
- No data sent to external servers
- Admin access not password protected (for local use)
- Keep `attendance.db` file backed up

---

## 📱 Button Reference Guide

| Location | Button | Action |
|----------|--------|--------|
| Main Window | Start Registration | Begin face capture for new student |
| Main Window | Start Attendance (old) | Quick attendance marking |
| Main Window | Stop Camera | Stop camera feed |
| Main Window | Re-train Model | Rebuild ML model from saved images |
| Main Window | 📊 Admin Dashboard | Open admin panel |
| Main Window | 👤 Student Dashboard | Open student view |
| Attendance Page | Start Camera | Turn on camera |
| Attendance Page | Stop Camera | Turn off camera |
| Attendance Page | ✓ Accept & Mark Attendance | Confirm and save attendance |
| Attendance Page | Back to Main | Return to main window |
| Admin Panel | + Add Student | Add new student manually |
| Admin Panel | 👁️ View Attendance | View student's records |
| Admin Panel | 🗑️ Delete Student | Remove student and records |
| Admin Panel | 🔄 Refresh | Reload student list |
| Student Dashboard | 🔄 Refresh | Update attendance data |
| Student Dashboard | 📥 Export to CSV | Download records |

---

## 🎓 Example Scenarios

### Scenario 1: School Attendance
```
- Register all students on Day 1
- Students mark attendance daily
- Admin checks records weekly
- Export monthly reports for records
```

### Scenario 2: Company Attendance
```
- Register employees once
- Daily attendance marking
- Admin dashboard for management
- Monthly export for payroll
```

### Scenario 3: Class Attendance
```
- Start of semester: Register students
- Each class: Students mark attendance
- Mid-semester: Check attendance rates
- End: Export final attendance report
```

---

## 💡 Tips & Best Practices

1. **Good Lighting:** Position light source in front of camera
2. **Clear Face:** No large obstacles, glasses okay
3. **Consistent Distance:** Stay 30-60 cm from camera
4. **One Face Per Camera:** System recognizes one face at a time
5. **Regular Backups:** Copy `attendance.db` regularly
6. **Accurate Names:** Use full, consistent names
7. **Re-train if Needed:** Update model if recognition fails
8. **Check Records:** Review attendance weekly

---

## 📞 Support

For issues:
1. Check Troubleshooting section above
2. Verify all packages installed: `pip list`
3. Check Python version: `python --version`
4. Restart application
5. Check camera works with other apps first

---

## ✨ Features Summary

✅ Face Recognition - Real-time detection  
✅ Database Storage - SQLite persistence  
✅ Student Management - Add/Edit/Delete  
✅ Attendance Marking - One-click confirmation  
✅ Statistics - View attendance summary  
✅ Export - CSV file generation  
✅ Offline - Works without internet  
✅ User-Friendly - Modern GUI interface  
✅ Fast - Instant recognition and marking  
✅ Secure - Local data storage  

---

**Last Updated:** November 2025  
**Version:** 2.0 with Database Support
