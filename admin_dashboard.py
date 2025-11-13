import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from database import AttendanceDatabase
from datetime import datetime

class AdminDashboard:
    def __init__(self, root, main_app=None):
        self.root = root
        self.main_app = main_app
        self.db = AttendanceDatabase()
        
        self.root.title("Admin Dashboard")
        self.root.geometry("1000x700")
        self.root.configure(bg='#2c3e50')
        
        self.create_widgets()
        self.load_students()
    
    def create_widgets(self):
        # Title
        title_frame = tk.Frame(self.root, bg='#34495e', relief=tk.RAISED, borderwidth=2)
        title_frame.pack(fill=tk.X, padx=20, pady=20)
        
        tk.Label(title_frame, text="Admin Dashboard", 
                font=("Arial", 24, "bold"), bg='#34495e', fg='white').pack(pady=10)
        
        tk.Label(title_frame, text="Manage Students and Attendance", 
                font=("Arial", 12), bg='#34495e', fg='#3498db').pack(pady=(0, 10))
        
        # Main content
        main_frame = tk.Frame(self.root, bg='#2c3e50')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Left side - Students list
        left_frame = tk.Frame(main_frame, bg='#2c3e50')
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        list_label = tk.Label(left_frame, text="Registered Students", 
                             font=("Arial", 12, "bold"), bg='#2c3e50', fg='white')
        list_label.pack(anchor='w', pady=(0, 5))
        
        # Treeview frame
        tree_frame = tk.Frame(left_frame, bg='#34495e', relief=tk.RAISED, borderwidth=2)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree = ttk.Treeview(tree_frame, columns=("Name", "Email", "ID", "Status"), 
                                height=20, yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.tree.yview)
        
        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.column("Name", anchor=tk.W, width=150)
        self.tree.column("Email", anchor=tk.W, width=150)
        self.tree.column("ID", anchor=tk.W, width=100)
        self.tree.column("Status", anchor=tk.CENTER, width=80)
        
        self.tree.heading("#0", text="", anchor=tk.W)
        self.tree.heading("Name", text="Name", anchor=tk.W)
        self.tree.heading("Email", text="Email", anchor=tk.W)
        self.tree.heading("ID", text="Student ID", anchor=tk.W)
        self.tree.heading("Status", text="Status", anchor=tk.CENTER)
        
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Bind selection
        self.tree.bind('<<TreeviewSelect>>', self.on_student_select)
        
        # Right side - Controls
        right_frame = tk.Frame(main_frame, bg='#34495e', relief=tk.RAISED, borderwidth=2)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(10, 0), ipadx=15)
        
        control_label = tk.Label(right_frame, text="Controls", 
                                font=("Arial", 12, "bold"), bg='#34495e', fg='white')
        control_label.pack(pady=20)
        
        # Add student section
        add_frame = tk.LabelFrame(right_frame, text="Add New Student", 
                                 font=("Arial", 10, "bold"), bg='#34495e', 
                                 fg='white', relief=tk.GROOVE, borderwidth=2)
        add_frame.pack(pady=10, padx=5, fill=tk.X)
        
        tk.Label(add_frame, text="Name:", font=("Arial", 9), 
                bg='#34495e', fg='white').pack(pady=(5, 2), anchor='w', padx=10)
        self.name_entry = tk.Entry(add_frame, font=("Arial", 10), width=20)
        self.name_entry.pack(pady=2, padx=10, fill=tk.X)
        
        tk.Label(add_frame, text="Email:", font=("Arial", 9), 
                bg='#34495e', fg='white').pack(pady=(5, 2), anchor='w', padx=10)
        self.email_entry = tk.Entry(add_frame, font=("Arial", 10), width=20)
        self.email_entry.pack(pady=2, padx=10, fill=tk.X)
        
        tk.Label(add_frame, text="Student ID:", font=("Arial", 9), 
                bg='#34495e', fg='white').pack(pady=(5, 2), anchor='w', padx=10)
        self.id_entry = tk.Entry(add_frame, font=("Arial", 10), width=20)
        self.id_entry.pack(pady=2, padx=10, fill=tk.X)
        
        add_btn = tk.Button(add_frame, text="+ Add Student", 
                           font=("Arial", 9, "bold"), bg='#2ecc71', 
                           fg='white', command=self.add_student,
                           cursor='hand2', relief=tk.RAISED, borderwidth=2)
        add_btn.pack(pady=10, padx=5, fill=tk.X)
        
        # Student actions section
        actions_frame = tk.LabelFrame(right_frame, text="Student Actions", 
                                     font=("Arial", 10, "bold"), bg='#34495e', 
                                     fg='white', relief=tk.GROOVE, borderwidth=2)
        actions_frame.pack(pady=10, padx=5, fill=tk.X)
        
        view_btn = tk.Button(actions_frame, text="👁️ View Attendance", 
                            font=("Arial", 9, "bold"), bg='#3498db', 
                            fg='white', command=self.view_attendance,
                            cursor='hand2', state=tk.DISABLED)
        view_btn.pack(pady=5, padx=5, fill=tk.X)
        self.view_btn = view_btn
        
        delete_btn = tk.Button(actions_frame, text="🗑️ Delete Student", 
                              font=("Arial", 9, "bold"), bg='#e74c3c', 
                              fg='white', command=self.delete_student,
                              cursor='hand2', state=tk.DISABLED)
        delete_btn.pack(pady=5, padx=5, fill=tk.X)
        self.delete_btn = delete_btn
        
        # Bottom buttons
        bottom_frame = tk.Frame(right_frame, bg='#34495e')
        bottom_frame.pack(pady=15, padx=5, fill=tk.X)
        
        refresh_btn = tk.Button(bottom_frame, text="🔄 Refresh", 
                               font=("Arial", 9, "bold"), bg='#95a5a6', 
                               fg='white', command=self.load_students,
                               cursor='hand2')
        refresh_btn.pack(pady=5, fill=tk.X)
        
        back_btn = tk.Button(bottom_frame, text="← Back to Main", 
                            font=("Arial", 9, "bold"), bg='#7f8c8d', 
                            fg='white', command=self.go_back,
                            cursor='hand2')
        back_btn.pack(pady=5, fill=tk.X)
        
        # Status label
        self.status_label = tk.Label(right_frame, text="Ready", 
                                    font=("Arial", 9), bg='#34495e', 
                                    fg='#2ecc71')
        self.status_label.pack(pady=10)
    
    def load_students(self):
        """Load all students into treeview"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Get all students
        students = self.db.get_all_students()
        
        if not students:
            self.tree.insert("", "end", text="", 
                           values=("No students", "", "", ""))
        else:
            for student_id, name, email, student_id_num, status, created_at in students:
                self.tree.insert("", "end", text="", 
                               values=(name, email or "N/A", student_id_num or "N/A", status),
                               tags=(student_id,))
    
    def on_student_select(self, event):
        """Handle student selection"""
        selected = self.tree.selection()
        if selected:
            self.view_btn.config(state=tk.NORMAL)
            self.delete_btn.config(state=tk.NORMAL)
        else:
            self.view_btn.config(state=tk.DISABLED)
            self.delete_btn.config(state=tk.DISABLED)
    
    def add_student(self):
        """Add a new student"""
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        student_id = self.id_entry.get().strip()
        
        if not name:
            messagebox.showerror("Error", "Please enter student name!")
            return
        
        success, result = self.db.add_student(name, email, student_id)
        
        if success:
            messagebox.showinfo("Success", f"Student '{name}' added successfully!")
            self.name_entry.delete(0, tk.END)
            self.email_entry.delete(0, tk.END)
            self.id_entry.delete(0, tk.END)
            self.load_students()
            self.status_label.config(text="Student added successfully")
        else:
            messagebox.showerror("Error", f"Failed to add student: {result}")
            self.status_label.config(text="Failed to add student", fg='#e74c3c')
    
    def view_attendance(self):
        """View attendance for selected student"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a student!")
            return
        
        item = self.tree.item(selected[0])
        student_id = item['tags'][0] if item['tags'] else None
        student_name = item['values'][0]
        
        if not student_id or student_id == "No students":
            return
        
        # Open student dashboard
        from student_dashboard import StudentDashboard
        
        new_window = tk.Toplevel(self.root)
        self.root.withdraw()
        StudentDashboard(new_window, int(student_id), student_name, self)
    
    def delete_student(self):
        """Delete selected student"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a student!")
            return
        
        item = self.tree.item(selected[0])
        student_id = item['tags'][0] if item['tags'] else None
        student_name = item['values'][0]
        
        if not student_id or student_id == "No students":
            return
        
        # Confirm deletion
        if messagebox.askyesno("Confirm", f"Are you sure you want to delete {student_name} and all their attendance records?"):
            success, message = self.db.delete_student(int(student_id))
            
            if success:
                messagebox.showinfo("Success", message)
                self.load_students()
                self.status_label.config(text="Student deleted successfully")
            else:
                messagebox.showerror("Error", f"Failed to delete student: {message}")
                self.status_label.config(text="Failed to delete", fg='#e74c3c')
    
    def go_back(self):
        self.db.close()
        self.root.destroy()
        if self.main_app:
            self.main_app.root.deiconify()
