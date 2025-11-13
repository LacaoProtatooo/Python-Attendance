import sqlite3
import os
from datetime import datetime
from pathlib import Path

class AttendanceDatabase:
    def __init__(self, db_name='attendance.db'):
        self.db_path = db_name
        self.conn = None
        self.cursor = None
        self.init_database()
    
    def init_database(self):
        """Initialize the database and create tables if they don't exist"""
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        
        # Create students table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                email TEXT,
                student_id TEXT UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'active'
            )
        ''')
        
        # Create attendance table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                date DATE NOT NULL,
                time_in TEXT,
                status TEXT DEFAULT 'present',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (student_id) REFERENCES students(id),
                UNIQUE(student_id, date)
            )
        ''')
        
        self.conn.commit()
    
    def add_student(self, name, email="", student_id=""):
        """Add a new student to the database"""
        try:
            self.cursor.execute('''
                INSERT INTO students (name, email, student_id)
                VALUES (?, ?, ?)
            ''', (name, email, student_id))
            self.conn.commit()
            return True, self.cursor.lastrowid
        except sqlite3.IntegrityError as e:
            return False, str(e)
    
    def get_student_by_name(self, name):
        """Get student information by name"""
        self.cursor.execute('''
            SELECT id, name, email, student_id, status 
            FROM students WHERE name = ?
        ''', (name,))
        result = self.cursor.fetchone()
        return result
    
    def get_all_students(self):
        """Get all students"""
        self.cursor.execute('''
            SELECT id, name, email, student_id, status, created_at 
            FROM students ORDER BY name
        ''')
        return self.cursor.fetchall()
    
    def mark_attendance(self, student_id, date, time_in, status='present'):
        """Mark attendance for a student"""
        try:
            self.cursor.execute('''
                INSERT OR REPLACE INTO attendance (student_id, date, time_in, status)
                VALUES (?, ?, ?, ?)
            ''', (student_id, date, time_in, status))
            self.conn.commit()
            return True, "Attendance marked successfully"
        except Exception as e:
            return False, str(e)
    
    def check_attendance_today(self, student_id, date):
        """Check if student has already marked attendance today"""
        self.cursor.execute('''
            SELECT id, status FROM attendance 
            WHERE student_id = ? AND date = ?
        ''', (student_id, date))
        result = self.cursor.fetchone()
        return result
    
    def get_student_attendance(self, student_id, limit=None):
        """Get attendance records for a student"""
        if limit:
            self.cursor.execute('''
                SELECT a.date, a.time_in, a.status, s.name
                FROM attendance a
                JOIN students s ON a.student_id = s.id
                WHERE a.student_id = ?
                ORDER BY a.date DESC
                LIMIT ?
            ''', (student_id, limit))
        else:
            self.cursor.execute('''
                SELECT a.date, a.time_in, a.status, s.name
                FROM attendance a
                JOIN students s ON a.student_id = s.id
                WHERE a.student_id = ?
                ORDER BY a.date DESC
            ''', (student_id,))
        return self.cursor.fetchall()
    
    def get_attendance_summary(self, student_id):
        """Get attendance summary for a student"""
        self.cursor.execute('''
            SELECT status, COUNT(*) as count
            FROM attendance
            WHERE student_id = ?
            GROUP BY status
        ''', (student_id,))
        return self.cursor.fetchall()
    
    def get_daily_attendance(self, date):
        """Get all attendance records for a specific date"""
        self.cursor.execute('''
            SELECT s.id, s.name, s.student_id, a.time_in, a.status
            FROM students s
            LEFT JOIN attendance a ON s.id = a.student_id AND a.date = ?
            ORDER BY s.name
        ''', (date,))
        return self.cursor.fetchall()
    
    def update_student(self, student_id, name=None, email=None, student_id_num=None, status=None):
        """Update student information"""
        updates = []
        params = []
        
        if name:
            updates.append("name = ?")
            params.append(name)
        if email:
            updates.append("email = ?")
            params.append(email)
        if student_id_num:
            updates.append("student_id = ?")
            params.append(student_id_num)
        if status:
            updates.append("status = ?")
            params.append(status)
        
        if not updates:
            return False, "No updates provided"
        
        params.append(student_id)
        
        try:
            query = f"UPDATE students SET {', '.join(updates)} WHERE id = ?"
            self.cursor.execute(query, params)
            self.conn.commit()
            return True, "Student updated successfully"
        except Exception as e:
            return False, str(e)
    
    def delete_student(self, student_id):
        """Delete a student and their records"""
        try:
            # Delete attendance records first
            self.cursor.execute('DELETE FROM attendance WHERE student_id = ?', (student_id,))
            # Delete student
            self.cursor.execute('DELETE FROM students WHERE id = ?', (student_id,))
            self.conn.commit()
            return True, "Student deleted successfully"
        except Exception as e:
            return False, str(e)
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
