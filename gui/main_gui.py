import tkinter as tk
from tkinter.ttk import Combobox
from tkinter import messagebox
from .api import search_by_name, search_patient_by_id, backup_history, backup_patients, backup_users
from gui.patient_tool_gui import add_patient_gui
from gui import tree_gui
from . import user_tool_gui

def open_dashboard(user):
    # Professional color scheme (matching authentication screens)
    COLORS = {
        'primary': '#2c3e50',
        'secondary': '#34495e',
        'accent': '#3498db',
        'success': '#27ae60',
        'warning': '#e74c3c',
        'danger': '#c0392b',
        'light': '#ecf0f1',
        'dark': '#2c3e50',
        'white': '#ffffff',
        'gray': '#95a5a6',
        'hover': '#2980b9',
        'border': '#dcdde1',
        'header_bg': '#34495e',
        'footer_bg': '#2c3e50'
    }
    
    FONTS = {
        'heading': ('Segoe UI', 16, 'bold'),
        'subheading': ('Segoe UI', 12),
        'body': ('Segoe UI', 10),
        'small': ('Segoe UI', 9),
        'label': ('Segoe UI', 10, 'bold')
    }

    def backup_patients_gui():
        ok, resp = backup_patients()
        if ok:
            messagebox.showinfo("Success", "✅ Patients backup completed successfully", parent=window)
        else:
            messagebox.showerror("Backup Failed", f"❌ {resp}", parent=window)

    def backup_history_gui():
        ok, resp = backup_history()
        if ok:
            messagebox.showinfo("Success", "✅ History backup completed successfully", parent=window)
        else:
            messagebox.showerror("Backup Failed", f"❌ {resp}", parent=window)

    def backup_users_gui():
        ok, resp = backup_users()
        if ok:
            messagebox.showinfo("Success", "✅ Users backup completed successfully", parent=window)
        else:
            messagebox.showerror("Backup Failed", f"❌ {resp}", parent=window)

    def logout():
        answ = messagebox.askyesno("Logout", "Are you sure you want to logout?", parent=window)
        if answ:
            window.destroy()
            user_tool_gui.login_user("Enter")
    
    # Real-time search function
    def on_search_change(*args):
        """Trigger search when user types in entry field"""
        search_term = entry.get().strip()
        
        # Don't search if term is too short (optional - can remove if you want real-time on every keystroke)
        if len(search_term) < 1:
            # If search is empty, show all patients
            tree_gui.reset_tree(tree, entry)
            return
            
        # Use after idle to prevent too many API calls while typing
        window.after(300, perform_search)  # 300ms delay
    
    def perform_search():
        """Actual search function called after delay"""
        search_term = entry.get().strip()
        
        # If search term changed during delay, skip
        if not search_term:
            return
            
        filter_value = filter_combo.get()

        # Clear tree
        for item in tree.get_children():
            tree.delete(item)

        if filter_value == "Name":
            ok, patients = search_by_name(search_term)

            if ok and patients:
                for p in patients:
                    tree.insert("", "end", values=[
                        p.get("id"),
                        p.get("created_at", ""),
                        p.get("first_name", ""),
                        p.get("middle_name", ""),
                        p.get("last_name", ""),
                        p.get("age", ""),
                        p.get("gender", ""),
                        p.get("city", ""),
                        p.get("sub_city", ""),
                        p.get("wereda", ""),
                        p.get("house_number", ""),
                        p.get("phone", ""),
                        p.get("created_by", ""),
                        p.get("diagnosis", "")
                    ])
                # Update status
                status_label.config(text=f"Found {len(patients)} patient(s)", fg=COLORS['success'])
            else:
                status_label.config(text="No patients found", fg=COLORS['warning'])

        elif filter_value == "Id":
            ok, p = search_patient_by_id(search_term)

            if ok and p:
                tree.insert("", "end", values=[
                        p.get("id"),
                        p.get("created_at", ""),
                        p.get("first_name", ""),
                        p.get("middle_name", ""),
                        p.get("last_name", ""),
                        p.get("age", ""),
                        p.get("gender", ""),
                        p.get("city", ""),
                        p.get("sub_city", ""),
                        p.get("wereda", ""),
                        p.get("house_number", ""),
                        p.get("phone", ""),
                        p.get("created_by", ""),
                        p.get("diagnosis", "")
                    ])
                status_label.config(text="Found 1 patient", fg=COLORS['success'])
            else:
                status_label.config(text="Patient ID not found", fg=COLORS['warning'])
    
    # Manual search function (for button click)
    def search_patient():
        search_term = entry.get().strip()

        if not search_term:
            messagebox.showwarning("Empty Search", "Please enter a name or ID to search.", parent=window)
            return

        # Clear tree and perform search
        for item in tree.get_children():
            tree.delete(item)

        filter_value = filter_combo.get()

        if filter_value == "Name":
            ok, patients = search_by_name(search_term)

            if ok and patients:
                for p in patients:
                    tree.insert("", "end", values=[
                        p.get("id"),
                        p.get("created_at", ""),
                        p.get("first_name", ""),
                        p.get("middle_name", ""),
                        p.get("last_name", ""),
                        p.get("age", ""),
                        p.get("gender", ""),
                        p.get("city", ""),
                        p.get("sub_city", ""),
                        p.get("wereda", ""),
                        p.get("house_number", ""),
                        p.get("phone", ""),
                        p.get("created_by", ""),
                        p.get("diagnosis", "")
                    ])
                status_label.config(text=f"Found {len(patients)} patient(s)", fg=COLORS['success'])
            else:
                status_label.config(text=f"No '{search_term}' match found", fg=COLORS['warning'])

        elif filter_value == "Id":
            ok, p = search_patient_by_id(search_term)

            if ok and p:
                tree.insert("", "end", values=[
                        p.get("id"),
                        p.get("created_at", ""),
                        p.get("first_name", ""),
                        p.get("middle_name", ""),
                        p.get("last_name", ""),
                        p.get("age", ""),
                        p.get("gender", ""),
                        p.get("city", ""),
                        p.get("sub_city", ""),
                        p.get("wereda", ""),
                        p.get("house_number", ""),
                        p.get("phone", ""),
                        p.get("created_by", ""),
                        p.get("diagnosis", "")
                    ])
                status_label.config(text="Found 1 patient", fg=COLORS['success'])
            else:
                status_label.config(text=f"ID '{search_term}' not found", fg=COLORS['warning'])

    # ===== Main Window =====
    window = tk.Tk()
    window.title("Health For All Clinic - Patient Management Dashboard")
    window.geometry("1400x800")
    window.configure(bg=COLORS['light'])
    
    # Center window
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')

    # ===== Header =====
    header_frame = tk.Frame(window, bg=COLORS['primary'], height=80)
    header_frame.pack(fill=tk.X)
    header_frame.pack_propagate(False)

    # Logo and title
    title_frame = tk.Frame(header_frame, bg=COLORS['primary'])
    title_frame.pack(side=tk.LEFT, padx=20, pady=10)

    tk.Label(
        title_frame,
        text="🏥",
        font=('Segoe UI', 24),
        bg=COLORS['primary'],
        fg=COLORS['white']
    ).pack(side=tk.LEFT, padx=(0, 10))

    tk.Label(
        title_frame,
        text="Patient Management System",
        font=FONTS['heading'],
        bg=COLORS['primary'],
        fg=COLORS['white']
    ).pack(side=tk.LEFT)

    # User info in header
    user_frame = tk.Frame(header_frame, bg=COLORS['primary'])
    user_frame.pack(side=tk.RIGHT, padx=20)

    tk.Label(
        user_frame,
        text=f"👤 {user}",
        font=FONTS['body'],
        bg=COLORS['primary'],
        fg=COLORS['light']
    ).pack(side=tk.LEFT, padx=10)

    # ===== Search Section =====
    search_frame = tk.Frame(window, bg=COLORS['white'], height=70)
    search_frame.pack(fill=tk.X, padx=20, pady=(20, 10))
    search_frame.pack_propagate(False)

    # Search container
    search_container = tk.Frame(search_frame, bg=COLORS['white'])
    search_container.pack(expand=True)

    # Filter label
    filter_label = tk.Label(
        search_container,
        text="Search by:",
        font=FONTS['label'],
        bg=COLORS['white'],
        fg=COLORS['dark']
    )
    filter_label.pack(side=tk.LEFT, padx=(0, 5))

    # Filter combobox
    filter_combo = Combobox(
        search_container,
        values=("Name", "Id"),
        width=8,
        font=FONTS['body'],
        state="readonly"
    )
    filter_combo.set("Name")
    filter_combo.pack(side=tk.LEFT, padx=(0, 10))

    # Search entry with real-time binding
    entry_frame = tk.Frame(
        search_container,
        bg=COLORS['white'],
        highlightbackground=COLORS['border'],
        highlightthickness=1,
        highlightcolor=COLORS['accent']
    )
    entry_frame.pack(side=tk.LEFT, padx=(0, 10))

    entry = tk.Entry(
        entry_frame,
        font=FONTS['body'],
        width=30,
        bd=0,
        bg=COLORS['white'],
        fg=COLORS['dark'],
        insertbackground=COLORS['accent']
    )
    entry.pack(padx=10, pady=8)
    
    # Bind key release event for real-time search
    entry.bind('<KeyRelease>', on_search_change)

    # Search button
    search_btn = tk.Button(
        search_container,
        text="🔍 Search",
        command=search_patient,
        font=FONTS['body'],
        bg=COLORS['accent'],
        fg=COLORS['white'],
        width=12,
        height=1,
        bd=0,
        cursor="hand2",
        activebackground=COLORS['hover'],
        activeforeground=COLORS['white']
    )
    search_btn.pack(side=tk.LEFT, padx=(0, 10))

    # Refresh button
    refresh_btn = tk.Button(
        search_container,
        text="🔄 Refresh",
        command=lambda: tree_gui.reset_tree(tree, entry, status_label),
        font=FONTS['body'],
        bg=COLORS['gray'],
        fg=COLORS['white'],
        width=10,
        height=1,
        bd=0,
        cursor="hand2",
        activebackground=COLORS['secondary'],
        activeforeground=COLORS['white']
    )
    refresh_btn.pack(side=tk.LEFT, padx=(0, 10))

    # Add patient button
    add_btn = tk.Button(
        search_container,
        text="➕ Add New Patient",
        command=lambda: add_patient_gui(user),
        font=FONTS['body'],
        bg=COLORS['success'],
        fg=COLORS['white'],
        width=18,
        height=1,
        bd=0,
        cursor="hand2",
        activebackground='#219a52',
        activeforeground=COLORS['white']
    )
    add_btn.pack(side=tk.LEFT)

    # ===== Tree View Section =====
    tree_container = tk.Frame(window, bg=COLORS['white'])
    tree_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 10))

    # Create tree view with scrollbars
    tree_frame = tk.Frame(tree_container, bg=COLORS['white'])
    tree_frame.pack(fill=tk.BOTH, expand=True)

    # Create tree
    tree = tree_gui.tree_view(tree_frame)
    
    # Bind right-click event
    tree.bind("<Button-3>", lambda event: tree_gui.on_row_right_click(event, tree, status_label))

    # ===== Tools and Status Bar =====
    bottom_frame = tk.Frame(window, bg=COLORS['white'], height=50)
    bottom_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
    bottom_frame.pack_propagate(False)

    # Left side - Tools
    tools_frame = tk.Frame(bottom_frame, bg=COLORS['white'])
    tools_frame.pack(side=tk.LEFT)

    # Backup Menu
    bu_btn = tk.Menubutton(
        tools_frame,
        text="📦 Backup",
        font=FONTS['body'],
        bg=COLORS['accent'],
        fg=COLORS['white'],
        bd=0,
        cursor="hand2",
        activebackground=COLORS['hover'],
        activeforeground=COLORS['white']
    )
    bu_btn.pack(side=tk.LEFT, padx=5)
    
    bu_menu = tk.Menu(bu_btn, tearoff=0, bg=COLORS['white'], fg=COLORS['dark'])
    bu_btn.config(menu=bu_menu)
    bu_menu.add_command(label="Backup Patients", command=backup_patients_gui)
    bu_menu.add_separator()
    bu_menu.add_command(label="Backup History", command=backup_history_gui)
    bu_menu.add_separator()
    bu_menu.add_command(label="Backup Users", command=backup_users_gui)

    # Settings Menu
    setting_btn = tk.Menubutton(
        tools_frame,
        text="⚙️ Settings",
        font=FONTS['body'],
        bg=COLORS['gray'],
        fg=COLORS['white'],
        bd=0,
        cursor="hand2",
        activebackground=COLORS['secondary'],
        activeforeground=COLORS['white']
    )
    setting_btn.pack(side=tk.LEFT, padx=5)
    
    setting_menu = tk.Menu(setting_btn, tearoff=0, bg=COLORS['white'], fg=COLORS['dark'])
    setting_btn.config(menu=setting_menu)
    setting_menu.add_command(label="Change Password", command=user_tool_gui.edit_password)
    setting_menu.add_separator()
    setting_menu.add_command(label="Logout", command=logout)

    # Right side - Status
    status_frame = tk.Frame(bottom_frame, bg=COLORS['white'])
    status_frame.pack(side=tk.RIGHT)

    status_label = tk.Label(
        status_frame,
        text="Ready",
        font=FONTS['small'],
        bg=COLORS['white'],
        fg=COLORS['gray']
    )
    status_label.pack()

    # ===== Footer =====
    footer_frame = tk.Frame(window, bg=COLORS['footer_bg'], height=30)
    footer_frame.pack(fill=tk.X, side=tk.BOTTOM)
    footer_frame.pack_propagate(False)

    tk.Label(
        footer_frame,
        text=f"© 2024 Health For All Clinic | Logged in as: {user}",
        font=FONTS['small'],
        bg=COLORS['footer_bg'],
        fg=COLORS['light']
    ).pack(side=tk.LEFT, padx=10)

    # Load initial data
    tree_gui.reset_tree(tree, entry, status_label)

    window.mainloop()