import cv2
import numpy as np
import os
import pickle
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from database import AttendanceDatabase

class AttendancePage:
    def __init__(self, root, main_app=None):
        self.root = root
        self.main_app = main_app
        self.root.title("Mark Attendance")
        self.root.geometry("1500x800")
        self.root.configure(bg='#2c3e50')
        
        # Variables
        self.camera_active = False
        self.cap = None
        self.detected_person = None
        self.detected_confidence = 100
        self.db = AttendanceDatabase()
        
        # Face cascade
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        
        self.create_widgets()
        
        # Show instructions
        messagebox.showinfo("Instructions", 
            "ATTENDANCE PAGE\n\n"
            "1. Click 'Start Camera' button on the right\n"
            "2. Face the camera\n"
            "3. Wait for face detection\n"
            "4. Click 'Accept & Mark Attendance'\n"
            "5. Your attendance is saved!\n\n"
            "The black area will show camera when started.")
    
    def create_widgets(self):
        # Title
        title = tk.Label(self.root, text="Mark Daily Attendance", 
                        font=("Arial", 24, "bold"), bg='#2c3e50', fg='white')
        title.pack(pady=20)
        
        # Main container
        main_frame = tk.Frame(self.root, bg='#2c3e50')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Left side - Camera feed
        left_frame = tk.Frame(main_frame, bg='#34495e', relief=tk.RAISED, borderwidth=2)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        camera_label = tk.Label(left_frame, text="Camera Feed", 
                               font=("Arial", 14, "bold"), bg='#34495e', fg='white')
        camera_label.pack(pady=10)
        
        self.video_label = tk.Label(left_frame, bg='black')
        self.video_label.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Status label
        self.status_label = tk.Label(left_frame, text="Camera Off", 
                                     font=("Arial", 12), bg='#34495e', fg='#e74c3c')
        self.status_label.pack(pady=5)
        
        # Right side - Controls (with fixed width)
        right_frame = tk.Frame(main_frame, bg='#34495e', relief=tk.RAISED, borderwidth=2, width=300)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        right_frame.pack_propagate(False)
        
        control_label = tk.Label(right_frame, text="Attendance Control", 
                                font=("Arial", 14, "bold"), bg='#34495e', fg='white')
        control_label.pack(pady=10)
        
        # Create scrollable content
        canvas = tk.Canvas(right_frame, bg='#34495e', highlightthickness=0)
        scrollbar = ttk.Scrollbar(right_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#34495e')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True, padx=10)
        scrollbar.pack(side="right", fill="y")
        
        # Detected person info
        info_frame = tk.LabelFrame(scrollable_frame, text="Detected Person", 
                                   font=("Arial", 10, "bold"), bg='#34495e', 
                                   fg='white', relief=tk.GROOVE, borderwidth=2)
        info_frame.pack(pady=5, padx=5, fill=tk.X)
        
        tk.Label(info_frame, text="Name:", font=("Arial", 9), 
                bg='#34495e', fg='white').pack(pady=(5, 2), anchor='w', padx=10)
        
        self.person_name_label = tk.Label(info_frame, text="Not Detected", 
                                          font=("Arial", 11, "bold"), 
                                          bg='#34495e', fg='#e74c3c')
        self.person_name_label.pack(pady=2, anchor='w', padx=15)
        
        tk.Label(info_frame, text="Confidence:", font=("Arial", 9), 
                bg='#34495e', fg='white').pack(pady=(5, 2), anchor='w', padx=10)
        
        self.confidence_label = tk.Label(info_frame, text="0%", 
                                        font=("Arial", 11), bg='#34495e', fg='white')
        self.confidence_label.pack(pady=2, anchor='w', padx=15)
        
        # Attendance status
        status_frame = tk.LabelFrame(scrollable_frame, text="Attendance Status", 
                                    font=("Arial", 10, "bold"), bg='#34495e', 
                                    fg='white', relief=tk.GROOVE, borderwidth=2)
        status_frame.pack(pady=5, padx=5, fill=tk.X)
        
        self.attendance_status_label = tk.Label(status_frame, text="--", 
                                               font=("Arial", 10), 
                                               bg='#34495e', fg='#f39c12')
        self.attendance_status_label.pack(pady=10)
        
        # Control buttons
        button_frame = tk.Frame(scrollable_frame, bg='#34495e')
        button_frame.pack(pady=10, padx=5, fill=tk.X)
        
        self.start_btn = tk.Button(button_frame, text="Start Camera", 
                                   font=("Arial", 10, "bold"), bg='#2ecc71', 
                                   fg='white', command=self.start_camera,
                                   cursor='hand2', relief=tk.RAISED, borderwidth=2)
        self.start_btn.pack(pady=3, fill=tk.X)
        
        self.stop_btn = tk.Button(button_frame, text="Stop Camera", 
                                  font=("Arial", 10, "bold"), bg='#e74c3c', 
                                  fg='white', command=self.stop_camera,
                                  cursor='hand2', state=tk.DISABLED)
        self.stop_btn.pack(pady=3, fill=tk.X)
        
        # Accept attendance button
        self.accept_btn = tk.Button(button_frame, text="✓ Accept & Mark", 
                                    font=("Arial", 10, "bold"), bg='#27ae60', 
                                    fg='white', command=self.accept_attendance,
                                    cursor='hand2', state=tk.DISABLED, relief=tk.RAISED, borderwidth=2)
        self.accept_btn.pack(pady=3, fill=tk.X)
        
        # Back button
        back_btn = tk.Button(button_frame, text="Back to Main", 
                            font=("Arial", 9, "bold"), bg='#95a5a6', 
                            fg='white', command=self.go_back,
                            cursor='hand2')
        back_btn.pack(pady=3, fill=tk.X)
    
    def start_camera(self):
        if not os.path.exists('face_recognizer.yml'):
            messagebox.showerror("Error", "No trained model found!\nPlease register faces first in Main page.")
            return
        
        self.camera_active = True
        self.cap = cv2.VideoCapture(0)
        
        if not self.cap.isOpened():
            messagebox.showerror("Error", "Could not open camera!")
            self.camera_active = False
            return
        
        self.status_label.config(text="Camera Active", fg='#2ecc71')
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        
        self.update_frame()
    
    def stop_camera(self):
        self.camera_active = False
        if self.cap:
            self.cap.release()
        
        self.video_label.config(image='', bg='black')
        self.status_label.config(text="Camera Off", fg='#e74c3c')
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.accept_btn.config(state=tk.DISABLED)
    
    def update_frame(self):
        if not self.camera_active:
            return
        
        ret, frame = self.cap.read()
        if not ret:
            self.stop_camera()
            return
        
        frame = cv2.flip(frame, 1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        
        self.process_frame(frame, gray, faces)
        
        # Convert frame for display
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (640, 480))
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)
        
        self.video_label.imgtk = imgtk
        self.video_label.configure(image=imgtk)
        
        if self.camera_active:
            self.video_label.after(10, self.update_frame)
    
    def process_frame(self, frame, gray, faces):
        if len(faces) == 0:
            self.detected_person = None
            self.person_name_label.config(text="Not Detected", fg='#e74c3c')
            self.confidence_label.config(text="0%")
            self.accept_btn.config(state=tk.DISABLED)
            cv2.putText(frame, "No Face Detected", (20, 40),
                       cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 3)
            return
        
        # Load recognizer
        try:
            recognizer = cv2.face.LBPHFaceRecognizer_create()
            recognizer.read('face_recognizer.yml')
            
            with open('labels.pkl', 'rb') as f:
                label_dict = pickle.load(f)
            
            id_to_name = {v: k for k, v in label_dict.items()}
        except Exception as e:
            print(f"Error loading recognizer: {e}")
            return
        
        # Process largest face
        x, y, w, h = faces[0]
        face_region = gray[y:y+h, x:x+w]
        
        try:
            id_, confidence = recognizer.predict(face_region)
        except Exception as e:
            print(f"Error predicting: {e}")
            return
        
        if confidence < 100:
            name = id_to_name.get(id_, "Unknown")
            self.detected_person = name
            self.detected_confidence = confidence
            
            if name == "Unknown":
                color = (0, 0, 255)
                self.person_name_label.config(text="Unknown", fg='#e74c3c')
                self.accept_btn.config(state=tk.DISABLED)
            else:
                color = (0, 255, 0)
                self.person_name_label.config(text=name, fg='#2ecc71')
                self.accept_btn.config(state=tk.NORMAL)
            
            confidence_score = int(100 - confidence)
            self.confidence_label.config(text=f"{confidence_score}%")
        else:
            color = (0, 0, 255)
            self.detected_person = None
            self.person_name_label.config(text="Unknown", fg='#e74c3c')
            self.confidence_label.config(text="Low")
            self.accept_btn.config(state=tk.DISABLED)
        
        # Draw rectangle
        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
        cv2.rectangle(frame, (x, y+h-35), (x+w, y+h), color, cv2.FILLED)
        display_name = self.detected_person if self.detected_person else "Unknown"
        cv2.putText(frame, f"{display_name}", (x+6, y+h-6),
                   cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 255, 255), 1)
    
    def accept_attendance(self):
        if not self.detected_person or self.detected_person == "Unknown":
            messagebox.showwarning("Warning", "Please ensure a valid person is detected!")
            return
        
        # Get student info from database - try exact match first, then case-insensitive
        student_info = self.db.get_student_by_name(self.detected_person)
        
        if not student_info:
            # Try case-insensitive search if exact match fails
            all_students = self.db.get_all_students()
            for student_id, name, email, student_id_num, status, created_at in all_students:
                if name.lower() == self.detected_person.lower():
                    student_info = (student_id, name, email, student_id_num, status)
                    break
        
        if not student_info:
            messagebox.showerror("Error", f"Student '{self.detected_person}' not found in database!\n\nPlease register this student first.")
            return
        
        student_id = student_info[0]
        today = datetime.now().strftime("%Y-%m-%d")
        
        # Check if already marked today
        existing = self.db.check_attendance_today(student_id, today)
        if existing:
            messagebox.showinfo("Info", f"Attendance already marked today for {self.detected_person}!")
            self.attendance_status_label.config(text="Already Marked Today", fg='#e74c3c')
            return
        
        # Mark attendance
        time_now = datetime.now().strftime("%H:%M:%S")
        success, message = self.db.mark_attendance(student_id, today, time_now, 'present')
        
        if success:
            messagebox.showinfo("Success", f"Attendance marked for {self.detected_person}!\n\nTime: {time_now}")
            self.attendance_status_label.config(text=f"✓ Marked at {time_now}", fg='#2ecc71')
        else:
            messagebox.showerror("Error", f"Failed to mark attendance: {message}")
            self.attendance_status_label.config(text="Failed to mark attendance", fg='#e74c3c')
    
    def go_back(self):
        self.stop_camera()
        self.db.close()
        self.root.destroy()
        if self.main_app:
            self.main_app.root.deiconify()
    
    def on_closing(self):
        self.stop_camera()
        self.db.close()
