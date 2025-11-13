#!/usr/bin/env python3
"""
Database Migration Script
Adds students from existing images to the database
Run this once if you have existing registered students
"""

import os
from database import AttendanceDatabase

def migrate_students():
    """Migrate students from images folder to database"""
    
    print("=" * 50)
    print("Database Migration - Adding Students")
    print("=" * 50)
    print()
    
    db = AttendanceDatabase()
    
    # Get list of unique student names from images folder
    if not os.path.exists('images'):
        print("No 'images' folder found!")
        return
    
    student_names = set()
    for img_file in os.listdir('images'):
        if img_file.endswith('.jpg') or img_file.endswith('.png'):
            # Extract name from filename (e.g., "Josh_0.jpg" -> "Josh")
            name = '_'.join(img_file.split('_')[:-1])
            if name:
                student_names.add(name)
    
    if not student_names:
        print("No student images found in 'images' folder")
        return
    
    print(f"Found {len(student_names)} student(s) in images folder:")
    print()
    
    added_count = 0
    existing_count = 0
    
    for name in sorted(student_names):
        # Check if student already exists
        existing = db.get_student_by_name(name)
        
        if existing:
            print(f"  ✓ {name} - Already in database")
            existing_count += 1
        else:
            # Add to database
            success, result = db.add_student(name)
            if success:
                print(f"  ✓ {name} - Added to database")
                added_count += 1
            else:
                print(f"  ✗ {name} - Error: {result}")
    
    print()
    print("=" * 50)
    print(f"Migration complete!")
    print(f"  Added: {added_count} student(s)")
    print(f"  Already in database: {existing_count} student(s)")
    print("=" * 50)
    print()
    print("All students are now in the database.")
    print("You can now use the attendance system!")
    
    db.close()

if __name__ == "__main__":
    migrate_students()
