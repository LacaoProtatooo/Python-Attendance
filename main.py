import cv2
import numpy as np
import os
from datetime import datetime
import pickle
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import threading
from database import AttendanceDatabase
from attendance_page import AttendancePage
from admin_dashboard import AdminDashboard
from student_dashboard import StudentDashboard

class AttendanceSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Recognition Attendance System")
        self.root.geometry("1000x700")
        self.root.configure(bg='#2c3e50')
        
        # Database
        self.db = AttendanceDatabase()
        
        # Variables
        self.camera_active = False
        self.cap = None
        self.current_mode = None  # 'register' or 'attendance'
        self.registration_name = ""
        self.samples_collected = 0
        self.samples_needed = 30
        self.frame_count = 0
        self.capture_interval = 10
        
        # Face cascade
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        # Create GUI
        self.create_widgets()
        
    def create_widgets(self):
        # Title
        title = tk.Label(self.root, text="Face Recognition Attendance System", 
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
        self.video_label.pack(padx=10, pady=10)
        
        # Status label
        self.status_label = tk.Label(left_frame, text="Camera Off", 
                                     font=("Arial", 12), bg='#34495e', fg='#e74c3c')
        self.status_label.pack(pady=5)
        
        # Progress bar (hidden initially)
        self.progress_frame = tk.Frame(left_frame, bg='#34495e')
        self.progress_frame.pack(pady=10, fill=tk.X, padx=20)
        
        self.progress_label = tk.Label(self.progress_frame, text="", 
                                       font=("Arial", 10), bg='#34495e', fg='white')
        self.progress_label.pack()
        
        self.progress_bar = ttk.Progressbar(self.progress_frame, length=400, mode='determinate')
        self.progress_bar.pack(pady=5)
        self.progress_frame.pack_forget()  # Hide initially
        
        # Right side - Controls
        right_frame = tk.Frame(main_frame, bg='#34495e', relief=tk.RAISED, borderwidth=2)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(10, 0))
        
        control_label = tk.Label(right_frame, text="Controls", 
                                font=("Arial", 14, "bold"), bg='#34495e', fg='white')
        control_label.pack(pady=20)
        
        # Register section
        register_frame = tk.LabelFrame(right_frame, text="Register New Person", 
                                       font=("Arial", 12, "bold"), bg='#34495e', 
                                       fg='white', relief=tk.GROOVE, borderwidth=2)
        register_frame.pack(pady=10, padx=20, fill=tk.X)
        
        tk.Label(register_frame, text="Name:", font=("Arial", 10), 
                bg='#34495e', fg='white').pack(pady=(10, 5))
        
        self.name_entry = tk.Entry(register_frame, font=("Arial", 12), width=20)
        self.name_entry.pack(pady=5)
        
        self.register_btn = tk.Button(register_frame, text="Start Registration", 
                                      font=("Arial", 11, "bold"), bg='#3498db', 
                                      fg='white', command=self.start_registration,
                                      cursor='hand2', relief=tk.RAISED, borderwidth=2)
        self.register_btn.pack(pady=10)
        
        # Attendance section
        attendance_frame = tk.LabelFrame(right_frame, text="Mark Attendance", 
                                        font=("Arial", 12, "bold"), bg='#34495e', 
                                        fg='white', relief=tk.GROOVE, borderwidth=2)
        attendance_frame.pack(pady=10, padx=20, fill=tk.X)
        
        quick_attend_btn = tk.Button(attendance_frame, text="⚡ Quick Attendance", 
                                     font=("Arial", 11, "bold"), bg='#2ecc71', 
                                     fg='white', command=self.start_attendance,
                                     cursor='hand2', relief=tk.RAISED, borderwidth=2)
        quick_attend_btn.pack(pady=10, fill=tk.X)
        
        advanced_attend_btn = tk.Button(attendance_frame, text="📱 Advanced Attendance Page", 
                                       font=("Arial", 10, "bold"), bg='#1abc9c', 
                                       fg='white', command=self.open_attendance_page,
                                       cursor='hand2', relief=tk.RAISED, borderwidth=2)
        advanced_attend_btn.pack(pady=5, fill=tk.X)
        
        # Dashboard section
        dashboard_frame = tk.LabelFrame(right_frame, text="Dashboard", 
                                       font=("Arial", 12, "bold"), bg='#34495e', 
                                       fg='white', relief=tk.GROOVE, borderwidth=2)
        dashboard_frame.pack(pady=10, padx=20, fill=tk.X)
        
        admin_btn = tk.Button(dashboard_frame, text="📊 Admin Dashboard", 
                            font=("Arial", 11, "bold"), bg='#9b59b6', 
                            fg='white', command=self.open_admin_dashboard,
                            cursor='hand2', relief=tk.RAISED, borderwidth=2)
        admin_btn.pack(pady=5, fill=tk.X)
        
        student_btn = tk.Button(dashboard_frame, text="👤 Student Dashboard", 
                              font=("Arial", 11, "bold"), bg='#16a085', 
                              fg='white', command=self.open_student_dashboard,
                              cursor='hand2', relief=tk.RAISED, borderwidth=2)
        student_btn.pack(pady=5, fill=tk.X)
        
        # Utility buttons
        utility_frame = tk.Frame(right_frame, bg='#34495e')
        utility_frame.pack(pady=10, padx=20, fill=tk.X)
        
        self.stop_btn = tk.Button(utility_frame, text="Stop Camera", 
                                  font=("Arial", 10, "bold"), bg='#e74c3c', 
                                  fg='white', command=self.stop_camera,
                                  cursor='hand2', state=tk.DISABLED)
        self.stop_btn.pack(pady=5, fill=tk.X)
        
        self.retrain_btn = tk.Button(utility_frame, text="Re-train Model", 
                                     font=("Arial", 10, "bold"), bg='#f39c12', 
                                     fg='white', command=self.train_model,
                                     cursor='hand2')
        self.retrain_btn.pack(pady=5, fill=tk.X)
        
        # Info text
        info_text = tk.Text(right_frame, height=8, width=30, font=("Arial", 9), 
                           bg='#2c3e50', fg='white', relief=tk.FLAT)
        info_text.pack(pady=20, padx=20)
        info_text.insert(tk.END, "Instructions:\n\n")
        info_text.insert(tk.END, "Registration:\n")
        info_text.insert(tk.END, "1. Enter name\n")
        info_text.insert(tk.END, "2. Click Start Registration\n")
        info_text.insert(tk.END, "3. Look at camera\n")
        info_text.insert(tk.END, "4. 30 samples will be captured\n\n")
        info_text.insert(tk.END, "Attendance:\n")
        info_text.insert(tk.END, "1. Click Start Attendance\n")
        info_text.insert(tk.END, "2. Face camera\n")
        info_text.config(state=tk.DISABLED)
        
    def start_registration(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Please enter a name!")
            return
        
        if self.camera_active:
            messagebox.showwarning("Warning", "Camera is already active!")
            return
        
        # Add student to database if not exists
        student_info = self.db.get_student_by_name(name)
        if not student_info:
            success, student_id = self.db.add_student(name)
            if not success:
                messagebox.showerror("Error", f"Failed to add student to database: {student_id}")
                return
        
        self.registration_name = name
        self.samples_collected = 0
        self.frame_count = 0
        self.current_mode = 'register'
        
        # Create images directory
        if not os.path.exists('images'):
            os.makedirs('images')
        
        # Show progress bar
        self.progress_frame.pack(pady=10, fill=tk.X, padx=20)
        self.progress_bar['value'] = 0
        self.progress_label.config(text=f"Samples: 0/{self.samples_needed}")
        
        self.start_camera()
        
    def start_attendance(self):
        if not os.path.exists('face_recognizer.yml'):
            messagebox.showerror("Error", "No trained model found!\nPlease register faces first.")
            return
        
        if self.camera_active:
            messagebox.showwarning("Warning", "Camera is already active!")
            return
        
        self.current_mode = 'attendance'
        self.progress_frame.pack_forget()
        self.start_camera()
    
    def open_attendance_page(self):
        """Open the attendance marking page"""
        if not os.path.exists('face_recognizer.yml'):
            messagebox.showerror("Error", "No trained model found!\nPlease register faces first.")
            return
        
        self.stop_camera()
        self.root.withdraw()
        
        new_window = tk.Toplevel(self.root)
        AttendancePage(new_window, self)
    
    def open_admin_dashboard(self):
        """Open the admin dashboard"""
        self.stop_camera()
        self.root.withdraw()
        
        new_window = tk.Toplevel(self.root)
        AdminDashboard(new_window, self)
    
    def open_student_dashboard(self):
        """Open student dashboard"""
        # Create a dialog to select student
        student_window = tk.Toplevel(self.root)
        student_window.title("Select Student")
        student_window.geometry("400x300")
        student_window.configure(bg='#2c3e50')
        
        tk.Label(student_window, text="Select Student", 
                font=("Arial", 14, "bold"), bg='#2c3e50', fg='white').pack(pady=20)
        
        # Get all students
        students = self.db.get_all_students()
        
        if not students:
            messagebox.showwarning("Warning", "No students registered!")
            student_window.destroy()
            return
        
        # Create listbox
        frame = tk.Frame(student_window, bg='#34495e')
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        scrollbar = ttk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        listbox = tk.Listbox(frame, font=("Arial", 10), yscrollcommand=scrollbar.set)
        scrollbar.config(command=listbox.yview)
        listbox.pack(fill=tk.BOTH, expand=True)
        
        for student_id, name, email, student_id_num, status, created_at in students:
            listbox.insert(tk.END, name)
        
        def open_dashboard():
            selection = listbox.curselection()
            if not selection:
                messagebox.showwarning("Warning", "Please select a student!")
                return
            
            index = selection[0]
            student_id = students[index][0]
            student_name = students[index][1]
            
            self.stop_camera()
            self.root.withdraw()
            student_window.destroy()
            
            new_window = tk.Toplevel(self.root)
            StudentDashboard(new_window, student_id, student_name, self)
        
        btn_frame = tk.Frame(student_window, bg='#2c3e50')
        btn_frame.pack(fill=tk.X, padx=20, pady=10)
        
        select_btn = tk.Button(btn_frame, text="Open Dashboard", 
                             font=("Arial", 10, "bold"), bg='#3498db', 
                             fg='white', command=open_dashboard,
                             cursor='hand2')
        select_btn.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        close_btn = tk.Button(btn_frame, text="Cancel", 
                            font=("Arial", 10, "bold"), bg='#95a5a6', 
                            fg='white', command=student_window.destroy,
                            cursor='hand2')
        close_btn.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
    def start_camera(self):
        self.camera_active = True
        self.cap = cv2.VideoCapture(0)
        
        if not self.cap.isOpened():
            messagebox.showerror("Error", "Could not open camera!")
            self.camera_active = False
            return
        
        self.status_label.config(text="Camera Active", fg='#2ecc71')
        self.stop_btn.config(state=tk.NORMAL)
        self.register_btn.config(state=tk.DISABLED)
        
        self.update_frame()
        
    def stop_camera(self):
        self.camera_active = False
        if self.cap:
            self.cap.release()
        
        self.video_label.config(image='', bg='black')
        self.status_label.config(text="Camera Off", fg='#e74c3c')
        self.stop_btn.config(state=tk.DISABLED)
        self.register_btn.config(state=tk.NORMAL)
        
        self.current_mode = None
        
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
        
        if self.current_mode == 'register':
            self.process_registration(frame, gray, faces)
        elif self.current_mode == 'attendance':
            self.process_attendance(frame, gray, faces)
        
        # Convert frame for display
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (640, 480))
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)
        
        self.video_label.imgtk = imgtk
        self.video_label.configure(image=imgtk)
        
        if self.camera_active:
            self.video_label.after(10, self.update_frame)
    
    def process_registration(self, frame, gray, faces):
        face_detected = len(faces) > 0
        
        if face_detected:
            for (x, y, w, h) in faces:
                # Draw green rectangle
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
                cv2.putText(frame, "Face Detected", (x, y-10),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            # Capture sample at intervals
            if self.frame_count % self.capture_interval == 0 and self.samples_collected < self.samples_needed:
                x, y, w, h = faces[0]
                img_name = os.path.join('images', f"{self.registration_name}_{self.samples_collected}.jpg")
                cv2.imwrite(img_name, gray[y:y+h, x:x+w])
                self.samples_collected += 1
                
                # Update progress
                progress = (self.samples_collected / self.samples_needed) * 100
                self.progress_bar['value'] = progress
                self.progress_label.config(text=f"Samples: {self.samples_collected}/{self.samples_needed}")
                
                # Flash effect
                cv2.rectangle(frame, (0, 0), (frame.shape[1]-1, frame.shape[0]-1), 
                            (255, 255, 255), 15)
                
                if self.samples_collected >= self.samples_needed:
                    self.stop_camera()
                    messagebox.showinfo("Success", f"Registration complete!\nCollected {self.samples_needed} samples.")
                    threading.Thread(target=self.train_model, daemon=True).start()
            
            self.frame_count += 1
        else:
            # Draw red warning
            cv2.putText(frame, "No Face Detected!", (20, 40),
                       cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 3)
            cv2.putText(frame, "Please position your face", (20, 80),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        
        # Status text
        status = "CAPTURING..." if face_detected else "WAITING FOR FACE..."
        color = (0, 255, 0) if face_detected else (0, 0, 255)
        cv2.putText(frame, status, (10, frame.shape[0] - 20),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
    
    def process_attendance(self, frame, gray, faces):
        if not os.path.exists('face_recognizer.yml') or not os.path.exists('labels.pkl'):
            return
        
        # Load recognizer
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read('face_recognizer.yml')
        
        with open('labels.pkl', 'rb') as f:
            label_dict = pickle.load(f)
        
        id_to_name = {v: k for k, v in label_dict.items()}
        
        # Create attendance file
        attendance_file = f'Attendance_{datetime.now().strftime("%Y-%m-%d")}.csv'
        if not os.path.exists(attendance_file):
            with open(attendance_file, 'w') as f:
                f.write("Name,Date,Time\n")
        
        # Load marked today
        marked_today = set()
        with open(attendance_file, 'r') as f:
            for line in f:
                if line.strip() and ',' in line:
                    marked_today.add(line.split(',')[0])
        
        for (x, y, w, h) in faces:
            face_region = gray[y:y+h, x:x+w]
            id_, confidence = recognizer.predict(face_region)
            
            if confidence < 100:
                name = id_to_name.get(id_, "Unknown")
                color = (0, 255, 0)
                
                # Mark attendance
                if name != "Unknown" and name not in marked_today:
                    with open(attendance_file, 'a') as f:
                        now = datetime.now()
                        f.write(f"{name},{now.strftime('%Y-%m-%d')},{now.strftime('%H:%M:%S')}\n")
                    marked_today.add(name)
                    self.status_label.config(text=f"Attendance marked: {name}")
            else:
                name = "Unknown"
                color = (0, 0, 255)
            
            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
            cv2.rectangle(frame, (x, y+h-35), (x+w, y+h), color, cv2.FILLED)
            cv2.putText(frame, f"{name} ({int(confidence)})", (x+6, y+h-6),
                       cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 255, 255), 1)
        
        # Show marked count
        cv2.putText(frame, f"Marked Today: {len(marked_today)}", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    
    def train_model(self):
        images_path = 'images'
        if not os.path.exists(images_path):
            messagebox.showerror("Error", "No images directory found!")
            return
        
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        
        faces = []
        labels = []
        label_dict = {}
        current_id = 0
        
        for img_name in os.listdir(images_path):
            img_path = os.path.join(images_path, img_name)
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            
            if img is None:
                continue
            
            name = '_'.join(img_name.split('_')[:-1])
            
            if name not in label_dict:
                label_dict[name] = current_id
                current_id += 1
            
            faces.append(img)
            labels.append(label_dict[name])
        
        if len(faces) == 0:
            messagebox.showerror("Error", "No faces found for training!")
            return
        
        recognizer.train(faces, np.array(labels))
        recognizer.save('face_recognizer.yml')
        
        with open('labels.pkl', 'wb') as f:
            pickle.dump(label_dict, f)
        
        messagebox.showinfo("Success", f"Model trained with {len(label_dict)} people!")

def main():
    root = tk.Tk()
    app = AttendanceSystem(root)
    root.mainloop()

if __name__ == "__main__":
    main()
