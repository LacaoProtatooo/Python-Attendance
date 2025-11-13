import tkinter as tk
from tkinter import ttk, messagebox
from database import AttendanceDatabase
from datetime import datetime

class StudentDashboard:
    def __init__(self, root, student_id, student_name, main_app=None):
        self.root = root
        self.student_id = student_id
        self.student_name = student_name
        self.main_app = main_app
        self.db = AttendanceDatabase()
        
        self.root.title(f"Student Dashboard - {student_name}")
        self.root.geometry("900x700")
        self.root.configure(bg='#2c3e50')
        
        self.create_widgets()
        self.load_attendance_data()
    
    def create_widgets(self):
        # Title
        title_frame = tk.Frame(self.root, bg='#34495e', relief=tk.RAISED, borderwidth=2)
        title_frame.pack(fill=tk.X, padx=20, pady=20)
        
        tk.Label(title_frame, text="Student Dashboard", 
                font=("Arial", 24, "bold"), bg='#34495e', fg='white').pack(pady=10)
        
        tk.Label(title_frame, text=f"Welcome, {self.student_name}!", 
                font=("Arial", 14), bg='#34495e', fg='#3498db').pack(pady=(0, 10))
        
        # Stats frame
        stats_frame = tk.Frame(self.root, bg='#2c3e50')
        stats_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Summary statistics
        self.load_summary_stats(stats_frame)
        
        # Main content
        main_frame = tk.Frame(self.root, bg='#2c3e50')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Attendance records section
        records_label = tk.Label(main_frame, text="Attendance Records", 
                                font=("Arial", 14, "bold"), bg='#2c3e50', fg='white')
        records_label.pack(anchor='w', pady=(10, 5))
        
        # Create treeview for attendance records
        tree_frame = tk.Frame(main_frame, bg='#34495e', relief=tk.RAISED, borderwidth=2)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Treeview
        self.tree = ttk.Treeview(tree_frame, columns=("Date", "Time", "Status"), 
                                height=20, yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.tree.yview)
        
        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.column("Date", anchor=tk.W, width=200)
        self.tree.column("Time", anchor=tk.W, width=150)
        self.tree.column("Status", anchor=tk.CENTER, width=150)
        
        self.tree.heading("#0", text="", anchor=tk.W)
        self.tree.heading("Date", text="Date", anchor=tk.W)
        self.tree.heading("Time", text="Time In", anchor=tk.W)
        self.tree.heading("Status", text="Status", anchor=tk.CENTER)
        
        # Configure tag colors
        self.tree.tag_configure('present', background='#d5f4e6', foreground='#27ae60')
        self.tree.tag_configure('absent', background='#fadbd8', foreground='#c0392b')
        self.tree.tag_configure('late', background='#fef9e7', foreground='#f39c12')
        
        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Bottom buttons frame
        button_frame = tk.Frame(self.root, bg='#2c3e50')
        button_frame.pack(fill=tk.X, padx=20, pady=15)
        
        refresh_btn = tk.Button(button_frame, text="🔄 Refresh", 
                               font=("Arial", 10, "bold"), bg='#3498db', 
                               fg='white', command=self.refresh_data,
                               cursor='hand2', relief=tk.RAISED, borderwidth=2)
        refresh_btn.pack(side=tk.LEFT, padx=5)
        
        export_btn = tk.Button(button_frame, text="📥 Export to CSV", 
                              font=("Arial", 10, "bold"), bg='#27ae60', 
                              fg='white', command=self.export_to_csv,
                              cursor='hand2', relief=tk.RAISED, borderwidth=2)
        export_btn.pack(side=tk.LEFT, padx=5)
        
        back_btn = tk.Button(button_frame, text="← Back", 
                            font=("Arial", 10, "bold"), bg='#95a5a6', 
                            fg='white', command=self.go_back,
                            cursor='hand2', relief=tk.RAISED, borderwidth=2)
        back_btn.pack(side=tk.RIGHT, padx=5)
    
    def load_summary_stats(self, parent):
        """Load and display attendance summary statistics"""
        summary = self.db.get_attendance_summary(self.student_id)
        
        stats_dict = {}
        for status, count in summary:
            stats_dict[status] = count
        
        present_count = stats_dict.get('present', 0)
        absent_count = stats_dict.get('absent', 0)
        late_count = stats_dict.get('late', 0)
        total = present_count + absent_count + late_count
        
        # Create stat boxes
        stat_boxes = []
        
        # Present box
        present_box = tk.Frame(parent, bg='#d5f4e6', relief=tk.RAISED, borderwidth=2)
        present_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        tk.Label(present_box, text="Present", font=("Arial", 10, "bold"), 
                bg='#d5f4e6', fg='#27ae60').pack(pady=(5, 0))
        tk.Label(present_box, text=str(present_count), font=("Arial", 20, "bold"), 
                bg='#d5f4e6', fg='#27ae60').pack(pady=(0, 5))
        
        # Absent box
        absent_box = tk.Frame(parent, bg='#fadbd8', relief=tk.RAISED, borderwidth=2)
        absent_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        tk.Label(absent_box, text="Absent", font=("Arial", 10, "bold"), 
                bg='#fadbd8', fg='#c0392b').pack(pady=(5, 0))
        tk.Label(absent_box, text=str(absent_count), font=("Arial", 20, "bold"), 
                bg='#fadbd8', fg='#c0392b').pack(pady=(0, 5))
        
        # Late box
        late_box = tk.Frame(parent, bg='#fef9e7', relief=tk.RAISED, borderwidth=2)
        late_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        tk.Label(late_box, text="Late", font=("Arial", 10, "bold"), 
                bg='#fef9e7', fg='#f39c12').pack(pady=(5, 0))
        tk.Label(late_box, text=str(late_count), font=("Arial", 20, "bold"), 
                bg='#fef9e7', fg='#f39c12').pack(pady=(0, 5))
        
        # Total box
        total_box = tk.Frame(parent, bg='#ebf5fb', relief=tk.RAISED, borderwidth=2)
        total_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        tk.Label(total_box, text="Total", font=("Arial", 10, "bold"), 
                bg='#ebf5fb', fg='#3498db').pack(pady=(5, 0))
        tk.Label(total_box, text=str(total), font=("Arial", 20, "bold"), 
                bg='#ebf5fb', fg='#3498db').pack(pady=(0, 5))
    
    def load_attendance_data(self):
        """Load attendance records into treeview"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Get attendance records
        records = self.db.get_student_attendance(self.student_id)
        
        if not records:
            self.tree.insert("", "end", text="", values=("No records", "", ""))
        else:
            for date, time_in, status, name in records:
                tag = status.lower() if status in ['present', 'absent', 'late'] else 'present'
                display_time = time_in if time_in else "N/A"
                self.tree.insert("", "end", text="", 
                               values=(date, display_time, status),
                               tags=(tag,))
    
    def refresh_data(self):
        """Refresh the attendance data"""
        self.load_attendance_data()
        messagebox.showinfo("Success", "Attendance data refreshed!")
    
    def export_to_csv(self):
        """Export attendance records to CSV"""
        try:
            import csv
            filename = f"Attendance_{self.student_name}_{datetime.now().strftime('%Y%m%d')}.csv"
            
            records = self.db.get_student_attendance(self.student_id)
            
            with open(filename, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Name", "Date", "Time", "Status"])
                for date, time_in, status, name in records:
                    writer.writerow([name, date, time_in or "N/A", status])
            
            messagebox.showinfo("Success", f"Exported to {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export: {str(e)}")
    
    def go_back(self):
        self.db.close()
        self.root.destroy()
        if self.main_app:
            self.main_app.root.deiconify()
