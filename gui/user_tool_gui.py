import tkinter as tt
from tkinter import messagebox
from gui import main_gui, user_tool_gui
import re
from tkinter import ttk
from gui.api import login, signup, change_password

def edit_password():
    # Professional color scheme (matching dashboard)
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
        'border': '#dcdde1'
    }
    
    FONTS = {
        'heading': ('Segoe UI', 16, 'bold'),
        'subheading': ('Segoe UI', 12),
        'body': ('Segoe UI', 10),
        'small': ('Segoe UI', 9),
        'label': ('Segoe UI', 10, 'bold')
    }
    
    def clear():
        """Clear all form fields"""
        username_entry.delete(0, tt.END)
        old_password_entry.delete(0, tt.END)
        new_password_entry.delete(0, tt.END)
        confirm_new_password_entry.delete(0, tt.END)
        # Reset field borders
        for frame in [username_frame, old_frame, new_frame, confirm_frame]:
            frame.config(highlightbackground=COLORS['border'])
        username_entry.focus()
    
    def toggle_old_password():
        """Toggle old password visibility"""
        if show_old_password_var.get():
            old_password_entry.config(show="")
            toggle_old_btn.config(text="👁️ Hide")
        else:
            old_password_entry.config(show="●")
            toggle_old_btn.config(text="👁️ Show")
    
    def toggle_new_password():
        """Toggle new password visibility"""
        if show_new_password_var.get():
            new_password_entry.config(show="")
            confirm_new_password_entry.config(show="")
            toggle_new_btn.config(text="👁️ Hide")
        else:
            new_password_entry.config(show="●")
            confirm_new_password_entry.config(show="●")
            toggle_new_btn.config(text="👁️ Show")
    
    def change():
        """Change user password"""
        # Get values
        un = username_entry.get().strip()
        op = old_password_entry.get()
        np = new_password_entry.get()
        cnp = confirm_new_password_entry.get()
        
        # Reset field borders
        for frame in [username_frame, old_frame, new_frame, confirm_frame]:
            frame.config(highlightbackground=COLORS['border'])
        
        # Validate required fields
        if not all([un, op, np, cnp]):
            messagebox.showerror("Error", "All fields must be filled", parent=frame)
            # Highlight empty fields
            if not un:
                username_frame.config(highlightbackground=COLORS['warning'])
            if not op:
                old_frame.config(highlightbackground=COLORS['warning'])
            if not np:
                new_frame.config(highlightbackground=COLORS['warning'])
            if not cnp:
                confirm_frame.config(highlightbackground=COLORS['warning'])
            return
        
        # Check password match
        if np != cnp:
            messagebox.showerror(
                "Password Mismatch", 
                "New password and confirm password must be identical",
                parent=frame
            )
            new_frame.config(highlightbackground=COLORS['warning'])
            confirm_frame.config(highlightbackground=COLORS['warning'])
            return
        
        # Check password strength
        if len(np) < 6:
            if not messagebox.askyesno(
                "Weak Password",
                "Password is too weak. Continue anyway?",
                parent=frame
            ):
                new_frame.config(highlightbackground=COLORS['warning'])
                return
        
        try:
            # Show loading state
            change_btn.config(text="CHANGING...", state="disabled", bg=COLORS['gray'])
            frame.update()
            
            # Login via API
            ok, user = login(un, op)

            if not ok:
                messagebox.showerror("Error", "Check your username/email and password", parent=frame)
                username_frame.config(highlightbackground=COLORS['warning'])
                old_frame.config(highlightbackground=COLORS['warning'])
                change_btn.config(text="CHANGE PASSWORD", state="normal", bg=COLORS['accent'])
                return

            # Change password via API
            success, _ = change_password(user["id"], op, np)

            if success:
                messagebox.showinfo(
                    "Success",
                    f"{user['first_name']} {user['last_name']} successfully changed your password",
                    parent=frame
                )
                clear()
                frame.destroy()
                user_tool_gui.login_user("Enter")
            else:
                messagebox.showerror("Error", "Failed to change password", parent=frame)
                change_btn.config(text="CHANGE PASSWORD", state="normal", bg=COLORS['accent'])
            
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Failed to change password: {str(e)}",
                parent=frame
            )
            change_btn.config(text="CHANGE PASSWORD", state="normal", bg=COLORS['accent'])
    
    # Create main window - increased size
    frame = tt.Tk()
    frame.title("Health For All Clinic - Change Password")
    frame.geometry("550x750")  # Increased size
    frame.resizable(False, False)
    frame.configure(bg=COLORS['light'])
    
    # Center window
    frame.update_idletasks()
    width = 550
    height = 750
    x = (frame.winfo_screenwidth() // 2) - (width // 2)
    y = (frame.winfo_screenheight() // 2) - (height // 2)
    frame.geometry(f'{width}x{height}+{x}+{y}')
    
    # Configure grid weight for the main frame to expand properly
    frame.grid_rowconfigure(1, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    
    # Header (fixed height)
    header_frame = tt.Frame(frame, bg=COLORS['primary'], height=100)
    header_frame.grid(row=0, column=0, sticky="ew")
    header_frame.grid_propagate(False)
    
    # Header content with better spacing
    tt.Label(
        header_frame,
        text="🔐 Change Password",
        font=FONTS['heading'],
        bg=COLORS['primary'],
        fg=COLORS['white']
    ).pack(pady=(20, 5))
    
    tt.Label(
        header_frame,
        text="Update your account password securely",
        font=FONTS['small'],
        bg=COLORS['primary'],
        fg=COLORS['light']
    ).pack()
    
    # Create a canvas with scrollbar for content
    canvas_container = tt.Frame(frame, bg=COLORS['light'])
    canvas_container.grid(row=1, column=0, sticky="nsew")
    canvas_container.grid_rowconfigure(0, weight=1)
    canvas_container.grid_columnconfigure(0, weight=1)
    
    # Canvas and scrollbar
    canvas = tt.Canvas(canvas_container, bg=COLORS['light'], highlightthickness=0)
    scrollbar = tt.Scrollbar(canvas_container, orient="vertical", command=canvas.yview)
    scrollable_frame = tt.Frame(canvas, bg=COLORS['white'])
    
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=canvas.winfo_width())
    canvas.configure(yscrollcommand=scrollbar.set)
    
    # Update canvas width when window resizes
    def configure_canvas_width(event):
        canvas.itemconfig(1, width=event.width)
    
    canvas.bind('<Configure>', configure_canvas_width)
    
    canvas.grid(row=0, column=0, sticky="nsew")
    scrollbar.grid(row=0, column=1, sticky="ns")
    
    # Main content in scrollable frame
    content_frame = tt.Frame(scrollable_frame, bg=COLORS['white'])
    content_frame.pack(fill="both", expand=True, padx=30, pady=30)
    
    # Form title
    tt.Label(
        content_frame,
        text="Enter your credentials",
        font=FONTS['subheading'],
        bg=COLORS['white'],
        fg=COLORS['dark']
    ).pack(pady=(0, 25))
    
    # Username field
    tt.Label(
        content_frame,
        text="USERNAME",
        font=FONTS['label'],
        bg=COLORS['white'],
        fg=COLORS['dark'],
        anchor="w"
    ).pack(fill="x", pady=(0, 5))
    
    username_frame = tt.Frame(
        content_frame,
        bg=COLORS['white'],
        highlightbackground=COLORS['border'],
        highlightthickness=1,
        highlightcolor=COLORS['accent']
    )
    username_frame.pack(fill="x", pady=(0, 20))
    
    username_entry = tt.Entry(
        username_frame,
        font=FONTS['body'],
        bd=0,
        bg=COLORS['white'],
        fg=COLORS['dark'],
        insertbackground=COLORS['accent']
    )
    username_entry.pack(padx=12, pady=10, fill="x")
    
    # Old password field
    tt.Label(
        content_frame,
        text="OLD PASSWORD",
        font=FONTS['label'],
        bg=COLORS['white'],
        fg=COLORS['dark'],
        anchor="w"
    ).pack(fill="x", pady=(0, 5))
    
    old_frame = tt.Frame(
        content_frame,
        bg=COLORS['white'],
        highlightbackground=COLORS['border'],
        highlightthickness=1
    )
    old_frame.pack(fill="x", pady=(0, 5))
    
    old_password_entry = tt.Entry(
        old_frame,
        font=FONTS['body'],
        show="●",
        bd=0,
        bg=COLORS['white'],
        fg=COLORS['dark'],
        insertbackground=COLORS['accent']
    )
    old_password_entry.pack(padx=12, pady=10, fill="x")
    
    # Show old password option
    show_old_frame = tt.Frame(content_frame, bg=COLORS['white'])
    show_old_frame.pack(fill="x", pady=(0, 20))
    
    show_old_password_var = tt.BooleanVar()
    toggle_old_btn = tt.Checkbutton(
        show_old_frame,
        text="👁️ Show old password",
        variable=show_old_password_var,
        command=toggle_old_password,
        bg=COLORS['white'],
        fg=COLORS['dark'],
        activebackground=COLORS['white'],
        font=FONTS['small']
    )
    toggle_old_btn.pack(anchor="w")
    
    # New password field
    tt.Label(
        content_frame,
        text="NEW PASSWORD",
        font=FONTS['label'],
        bg=COLORS['white'],
        fg=COLORS['dark'],
        anchor="w"
    ).pack(fill="x", pady=(0, 5))
    
    new_frame = tt.Frame(
        content_frame,
        bg=COLORS['white'],
        highlightbackground=COLORS['border'],
        highlightthickness=1
    )
    new_frame.pack(fill="x", pady=(0, 5))
    
    new_password_entry = tt.Entry(
        new_frame,
        font=FONTS['body'],
        show="●",
        bd=0,
        bg=COLORS['white'],
        fg=COLORS['dark'],
        insertbackground=COLORS['accent']
    )
    new_password_entry.pack(padx=12, pady=10, fill="x")
    
    # Password strength indicator
    strength_container = tt.Frame(content_frame, bg=COLORS['white'])
    strength_container.pack(fill="x", pady=(5, 5))
    
    strength_label = tt.Label(
        strength_container,
        text="Not set",
        font=FONTS['small'],
        bg=COLORS['white'],
        fg=COLORS['gray']
    )
    strength_label.pack(side="left")
    
    # Confirm password field
    tt.Label(
        content_frame,
        text="CONFIRM NEW PASSWORD",
        font=FONTS['label'],
        bg=COLORS['white'],
        fg=COLORS['dark'],
        anchor="w"
    ).pack(fill="x", pady=(15, 5))
    
    confirm_frame = tt.Frame(
        content_frame,
        bg=COLORS['white'],
        highlightbackground=COLORS['border'],
        highlightthickness=1
    )
    confirm_frame.pack(fill="x", pady=(0, 5))
    
    confirm_new_password_entry = tt.Entry(
        confirm_frame,
        font=FONTS['body'],
        show="●",
        bd=0,
        bg=COLORS['white'],
        fg=COLORS['dark'],
        insertbackground=COLORS['accent']
    )
    confirm_new_password_entry.pack(padx=12, pady=10, fill="x")
    
    # Show new password option
    show_new_frame = tt.Frame(content_frame, bg=COLORS['white'])
    show_new_frame.pack(fill="x", pady=(5, 20))
    
    show_new_password_var = tt.BooleanVar()
    toggle_new_btn = tt.Checkbutton(
        show_new_frame,
        text="👁️ Show new password",
        variable=show_new_password_var,
        command=toggle_new_password,
        bg=COLORS['white'],
        fg=COLORS['dark'],
        activebackground=COLORS['white'],
        font=FONTS['small']
    )
    toggle_new_btn.pack(anchor="w")
    
    # Buttons
    button_frame = tt.Frame(content_frame, bg=COLORS['white'])
    button_frame.pack(fill="x", pady=25)
    
    # Create a sub-frame for buttons to center them
    button_container = tt.Frame(button_frame, bg=COLORS['white'])
    button_container.pack(anchor="center")
    
    change_btn = tt.Button(
        button_container,
        text="CHANGE PASSWORD",
        command=change,
        font=FONTS['label'],
        bg=COLORS['accent'],
        fg=COLORS['white'],
        width=18,
        height=2,
        bd=0,
        cursor="hand2",
        activebackground=COLORS['hover'],
        activeforeground=COLORS['white']
    )
    change_btn.pack(side="left", padx=5)
    
    clear_btn = tt.Button(
        button_container,
        text="CLEAR",
        command=clear,
        font=FONTS['body'],
        bg=COLORS['gray'],
        fg=COLORS['white'],
        width=10,
        height=2,
        bd=0,
        cursor="hand2",
        activebackground=COLORS['secondary'],
        activeforeground=COLORS['white']
    )
    clear_btn.pack(side="left", padx=5)
    
    cancel_btn = tt.Button(
        button_container,
        text="CANCEL",
        command=frame.destroy,
        font=FONTS['body'],
        bg=COLORS['gray'],
        fg=COLORS['white'],
        width=10,
        height=2,
        bd=0,
        cursor="hand2",
        activebackground=COLORS['secondary'],
        activeforeground=COLORS['white']
    )
    cancel_btn.pack(side="left", padx=5)
    
    # Login hint
    hint_frame = tt.Frame(content_frame, bg=COLORS['white'])
    hint_frame.pack(fill="x", pady=10)
    
    tt.Label(
        hint_frame,
        text="After successful password change, you'll be redirected to login.",
        font=FONTS['small'],
        bg=COLORS['white'],
        fg=COLORS['gray'],
        wraplength=450
    ).pack()
    
    # Set focus to username field
    username_entry.focus()
    
    # Enter key binding
    frame.bind('<Return>', lambda event: change())
    
    frame.mainloop()

def login_user(event):
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
        'hover': '#2980b9'
    }
    
    def check_auth():
        username = user_name_entry.get()
        psw = psw_entry.get()
        
        try:
            ok, data = login(username, psw)

            if ok:
                frame.destroy()
                main_gui.open_dashboard(username)
            else:
                messagebox.showerror("Authentication Failed", "Invalid username or password.\nPlease try again.")
                # Highlight fields
                username_frame.config(highlightbackground=COLORS['warning'])
                password_frame.config(highlightbackground=COLORS['warning'])
                
        except Exception as e:
            messagebox.showerror("System Error", f"An unexpected error occurred:\n{e}")
            
    frame = tt.Tk()
    frame.title("Clinic Management System - Enterprise Login")
    frame.geometry("1000x600")
    frame.resizable(False, False)
    frame.configure(bg=COLORS['light'])
    
    # ===== Create main container with modern split design =====
    # Left panel - Branding/Image side
    left_panel = tt.Frame(frame, bg=COLORS['primary'], width=400)
    left_panel.pack(side="left", fill="both", expand=False)
    left_panel.pack_propagate(False)
    
    # Right panel - Login form side
    right_panel = tt.Frame(frame, bg=COLORS['white'], width=600)
    right_panel.pack(side="right", fill="both", expand=True)
    right_panel.pack_propagate(False)
    
    # ===== Left Panel Content (Branding) =====
    logo_frame = tt.Frame(left_panel, bg=COLORS['primary'])
    logo_frame.pack(expand=True)
    
    tt.Label(
        logo_frame,
        text="🏥",
        font=("Segoe UI", 60),
        bg=COLORS['primary'],
        fg=COLORS['white']
    ).pack(pady=20)
    
    tt.Label(
        logo_frame,
        text="CLINIC PRO",
        font=("Segoe UI", 24, "bold"),
        bg=COLORS['primary'],
        fg=COLORS['white']
    ).pack()
    
    tt.Label(
        logo_frame,
        text="Enterprise Healthcare Management",
        font=("Segoe UI", 12),
        bg=COLORS['primary'],
        fg=COLORS['light']
    ).pack(pady=5)
    
    # Features list
    features_frame = tt.Frame(logo_frame, bg=COLORS['primary'])
    features_frame.pack(pady=40)
    
    features = [
        "✓ Secure Patient Records",
        "✓ Appointment Scheduling",
        "✓ Patient History",
        "✓ Advanced Search",
        "✓ Analytics Dashboard"
    ]
    
    for feature in features:
        tt.Label(
            features_frame,
            text=feature,
            font=("Segoe UI", 11),
            bg=COLORS['primary'],
            fg=COLORS['light'],
            anchor="w"
        ).pack(pady=3)
    
    # Version
    tt.Label(
        left_panel,
        text="Version 1.0.0 | Multi-User Edition",
        font=("Segoe UI", 8),
        bg=COLORS['primary'],
        fg=COLORS['gray']
    ).pack(side="bottom", pady=20)
    
    # ===== Right Panel Content (Login Form) =====
    login_container = tt.Frame(right_panel, bg=COLORS['white'])
    login_container.place(relx=0.5, rely=0.5, anchor="center")
    
    # Welcome message
    tt.Label(
        login_container,
        text="Welcome Back",
        font=("Segoe UI", 28, "bold"),
        bg=COLORS['white'],
        fg=COLORS['primary']
    ).grid(row=0, column=0, columnspan=2, pady=(0, 10))
    
    tt.Label(
        login_container,
        text="Please sign in to access your dashboard",
        font=("Segoe UI", 11),
        bg=COLORS['white'],
        fg=COLORS['gray']
    ).grid(row=1, column=0, columnspan=2, pady=(0, 30))
    
    # Username field
    tt.Label(
        login_container,
        text="Username",
        font=("Segoe UI", 11, "bold"),
        bg=COLORS['white'],
        fg=COLORS['dark'],
        anchor="w"
    ).grid(row=2, column=0, columnspan=2, sticky="w", pady=(0, 5))
    
    username_frame = tt.Frame(
        login_container, 
        bg=COLORS['white'], 
        highlightthickness=1,
        highlightcolor=COLORS['accent']
    )
    username_frame.grid(row=3, column=0, columnspan=2, pady=(0, 15), sticky="ew")
    
    user_name_entry = tt.Entry(
        username_frame,
        font=("Segoe UI", 12),
        width=30,
        bd=0,
        bg=COLORS['white'],
        fg=COLORS['dark'],
        insertbackground=COLORS['accent']
    )
    user_name_entry.pack(padx=10, pady=8, fill="x")
    user_name_entry.focus()
    
    # Password field
    tt.Label(
        login_container,
        text="Password",
        font=("Segoe UI", 11, "bold"),
        bg=COLORS['white'],
        fg=COLORS['dark'],
        anchor="w"
    ).grid(row=4, column=0, columnspan=2, sticky="w", pady=(0, 5))
    
    password_frame = tt.Frame(
        login_container, 
        bg=COLORS['white'], 
        highlightthickness=1
    )
    password_frame.grid(row=5, column=0, columnspan=2, pady=(0, 20), sticky="ew")
    
    psw_entry = tt.Entry(
        password_frame,
        font=("Segoe UI", 12),
        width=30,
        show="●",
        bd=0,
        bg=COLORS['white'],
        fg=COLORS['dark'],
        insertbackground=COLORS['accent']
    )
    psw_entry.pack(padx=10, pady=8, fill="x")
    
    # Remember me and Forgot password row
    options_frame = tt.Frame(login_container, bg=COLORS['white'])
    options_frame.grid(row=6, column=0, columnspan=2, sticky="ew", pady=(0, 20))
    
    remember_var = tt.BooleanVar()
    remember_check = tt.Checkbutton(
        options_frame,
        text="Remember me",
        variable=remember_var,
        bg=COLORS['white'],
        fg=COLORS['dark'],
        selectcolor=COLORS['white'],
        activebackground=COLORS['white'],
        font=("Segoe UI", 10)
    )
    remember_check.pack(side="left")
    
    forgot_btn = tt.Label(
        options_frame,
        text="Forgot Password?",
        font=("Segoe UI", 10),
        bg=COLORS['white'],
        fg=COLORS['accent'],
        cursor="hand2"
    )
    forgot_btn.pack(side="right")
    forgot_btn.bind("<Button-1>", lambda e: (frame.destroy(), edit_password()))
    
    # Login button
    login_btn = tt.Button(
        login_container,
        text="SIGN IN",
        command=check_auth,
        font=("Segoe UI", 12, "bold"),
        bg=COLORS['accent'],
        fg=COLORS['white'],
        width=25,
        height=2,
        bd=0,
        cursor="hand2",
        activebackground=COLORS['hover'],
        activeforeground=COLORS['white']
    )
    login_btn.grid(row=7, column=0, columnspan=2, pady=10)
    
    # Hover effect for login button
    def on_enter(e):
        login_btn['background'] = COLORS['hover']
    
    def on_leave(e):
        login_btn['background'] = COLORS['accent']
    
    login_btn.bind("<Enter>", on_enter)
    login_btn.bind("<Leave>", on_leave)
    
    # Sign up link
    signup_frame = tt.Frame(login_container, bg=COLORS['white'])
    signup_frame.grid(row=8, column=0, columnspan=2, pady=10)
    
    tt.Label(
        signup_frame,
        text="New to Clinic Pro? ",
        font=("Segoe UI", 10),
        bg=COLORS['white'],
        fg=COLORS['gray']
    ).pack(side="left")
    
    signup_lbl = tt.Label(
        signup_frame,
        text="Create an account",
        font=("Segoe UI", 10, "bold"),
        bg=COLORS['white'],
        fg=COLORS['success'],
        cursor="hand2"
    )
    signup_lbl.pack(side="left")
    signup_lbl.bind("<Button-1>", lambda event: (frame.destroy(), user_registration(event)))
    
    # Hover effect for signup link
    def on_signup_enter(e):
        signup_lbl['fg'] = '#219a52'
    
    def on_signup_leave(e):
        signup_lbl['fg'] = COLORS['success']
    
    signup_lbl.bind("<Enter>", on_signup_enter)
    signup_lbl.bind("<Leave>", on_signup_leave)
    
    # Enter key binding
    frame.bind('<Return>', lambda event: check_auth())
    
    frame.mainloop()

def user_registration(event=None):
    # Professional color scheme (matching dashboard)
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
        'border': '#dcdde1'
    }
    
    FONTS = {
        'heading': ('Segoe UI', 24, 'bold'),
        'subheading': ('Segoe UI', 12),
        'body': ('Segoe UI', 10),
        'small': ('Segoe UI', 9),
        'label': ('Segoe UI', 10, 'bold')
    }
    
    def clear_form():
        """Clear all form fields and reset validation state"""
        fn_entry.delete(0, tt.END)
        ln_entry.delete(0, tt.END)
        phone_entry.delete(0, tt.END)
        email_entry.delete(0, tt.END)
        psw_entry.delete(0, tt.END)
        confirm_psw_entry.delete(0, tt.END)
        terms_var.set(False)
        register_btn.config(state="disabled", bg=COLORS['gray'])
        validate_btn.config(state="normal", bg=COLORS['accent'])
        # Reset all field borders
        for frame in [fn_frame, ln_frame, phone_frame, email_frame, psw_frame, confirm_psw_frame]:
            frame.config(highlightbackground=COLORS['border'])
        fn_entry.focus()
    
    def validate_field(entry_frame, condition, error_message=""):
        """Helper function to validate individual fields"""
        if not condition:
            entry_frame.config(highlightbackground=COLORS['warning'])
            return False
        entry_frame.config(highlightbackground=COLORS['border'])
        return True
    
    def validate_form():
        """Validate all form fields before enabling registration"""
        # Get field values
        fn = fn_entry.get().strip()
        ln = ln_entry.get().strip()
        phone = phone_entry.get().strip()
        email = email_entry.get().strip()
        p1 = psw_entry.get()
        p2 = confirm_psw_entry.get()
        
        # Reset all field borders
        for frame in [fn_frame, ln_frame, phone_frame, email_frame, psw_frame, confirm_psw_frame]:
            frame.config(highlightbackground=COLORS['border'])
        
        # Validate all fields
        is_valid = True
        
        # Check required fields
        if not all([fn, ln, phone, email, p1, p2]):
            messagebox.showerror(
                "Incomplete Form",
                "Please fill in all required fields",
                parent=window
            )
            return
        
        # Validate each field
        if not validate_field(fn_frame, len(fn) >= 2, "First name must be at least 2 characters"):
            is_valid = False
        
        if not validate_field(ln_frame, len(ln) >= 2, "Last name must be at least 2 characters"):
            is_valid = False
        
        # Phone validation
        phone_valid = phone.isdigit() and len(phone) == 10
        if not validate_field(phone_frame, phone_valid, "Phone must be 10 digits"):
            messagebox.showerror("Invalid Phone", "Phone number must be 10 digits", parent=window)
            is_valid = False
        
        # Email validation
        email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        email_valid = re.match(email_pattern, email) is not None
        if not validate_field(email_frame, email_valid, "Invalid email format"):
            messagebox.showerror("Invalid Email", "Please enter a valid email address", parent=window)
            is_valid = False
        
        # Password match validation
        if not validate_field(psw_frame, p1 == p2, "Passwords don't match"):
            confirm_psw_frame.config(highlightbackground=COLORS['warning'])
            messagebox.showerror("Password Mismatch", "Passwords do not match", parent=window)
            is_valid = False
        
        # Password strength
        if len(p1) < 6:
            if not messagebox.askyesno(
                "Weak Password",
                "Password is weak. Continue anyway?",
                parent=window
            ):
                psw_frame.config(highlightbackground=COLORS['warning'])
                return
        elif len(p1) < 8:
            messagebox.showwarning(
                "Medium Password",
                "Consider using a stronger password for better security",
                parent=window
            )
        
        # Terms agreement
        if not terms_var.get():
            messagebox.showerror(
                "Terms Required",
                "Please agree to the Terms of Service to continue",
                parent=window
            )
            return
        
        if is_valid:
            validate_btn.config(state="disabled", bg=COLORS['gray'])
            register_btn.config(state="normal", bg=COLORS['success'], cursor="hand2")
            progress_label.config(text="✓ Validation Complete - Ready to Register", fg=COLORS['success'])
            messagebox.showinfo(
                "Validation Successful",
                "All information is valid. You may now complete your registration.",
                parent=window
            )
    
    def register_user():
        """Register the user via API"""
        if not terms_var.get():
            messagebox.showerror(
                "Terms Required",
                "Please agree to the Terms of Service",
                parent=window
            )
            return
        
        fn = fn_entry.get().strip()
        ln = ln_entry.get().strip()
        phone = phone_entry.get().strip()
        email = email_entry.get().strip()
        password = psw_entry.get()
        
        try:
            # Show loading state
            register_btn.config(text="CREATING ACCOUNT...", state="disabled", bg=COLORS['gray'])
            window.update()
            
            # Call your API function
            ok, msg = signup(fn, ln, phone, email, password)

            if ok:
                messagebox.showinfo(
                    "Registration Complete",
                    f"Welcome {fn} {ln}!\nYour account has been successfully created.",
                    parent=window
                )
                window.destroy()
                login_user("Enter")
            else:
                messagebox.showerror(
                    "Registration Error",
                    f"Unable to complete registration:\n{msg}",
                    parent=window
                )
                register_btn.config(text="CREATE ACCOUNT", state="normal", bg=COLORS['success'])
            
        except Exception as e:
            messagebox.showerror(
                "Registration Error",
                f"Unable to complete registration:\n{str(e)}",
                parent=window
            )
            register_btn.config(text="CREATE ACCOUNT", state="normal", bg=COLORS['success'])
    
    def check_password_strength(*args):
        """Real-time password strength indicator"""
        password = psw_entry.get()
        if len(password) == 0:
            strength_label.config(text="Not set", fg=COLORS['gray'])
            strength_bar.config(style="Strength.Weak.Horizontal.TProgressbar")
        elif len(password) < 6:
            strength_label.config(text="Weak", fg=COLORS['warning'])
            strength_bar.config(value=30, style="Strength.Weak.Horizontal.TProgressbar")
        elif len(password) < 10:
            strength_label.config(text="Medium", fg="#f39c12")
            strength_bar.config(value=60, style="Strength.Medium.Horizontal.TProgressbar")
        else:
            strength_label.config(text="Strong", fg=COLORS['success'])
            strength_bar.config(value=100, style="Strength.Strong.Horizontal.TProgressbar")
    
    def toggle_password():
        """Toggle password visibility"""
        if show_password_var.get():
            psw_entry.config(show="")
            confirm_psw_entry.config(show="")
            toggle_btn.config(text="👁️ Hide")
        else:
            psw_entry.config(show="●")
            confirm_psw_entry.config(show="●")
            toggle_btn.config(text="👁️ Show")
    
    # ===== Main Window =====
    window = tt.Tk()
    window.title("Health For All Clinic - User Registration")
    window.geometry("1000x700")
    window.configure(bg=COLORS['light'])
    
    # Center window
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')
    
    # Configure style for progress bar
    style = ttk.Style()
    style.theme_use('clam')
    style.configure("Strength.Weak.Horizontal.TProgressbar", background=COLORS['warning'])
    style.configure("Strength.Medium.Horizontal.TProgressbar", background="#f39c12")
    style.configure("Strength.Strong.Horizontal.TProgressbar", background=COLORS['success'])
    
    # ===== Header =====
    header_frame = tt.Frame(window, bg=COLORS['primary'], height=120)
    header_frame.pack(fill="x")
    header_frame.pack_propagate(False)
    
    # Logo/Icon placeholder
    tt.Label(
        header_frame,
        text="🏥",
        font=('Segoe UI', 32),
        bg=COLORS['primary'],
        fg=COLORS['white']
    ).pack(pady=(15, 5))
    
    tt.Label(
        header_frame,
        text="Create Your Account",
        font=FONTS['heading'],
        bg=COLORS['primary'],
        fg=COLORS['white']
    ).pack()
    
    tt.Label(
        header_frame,
        text="Join Health For All Clinic - Complete your registration below",
        font=FONTS['subheading'],
        bg=COLORS['primary'],
        fg=COLORS['light']
    ).pack(pady=(0, 10))
    
    # ===== Main Content =====
    main_frame = tt.Frame(window, bg=COLORS['white'])
    main_frame.pack(fill="both", expand=True, padx=40, pady=30)
    
    # Progress indicator
    progress_frame = tt.Frame(main_frame, bg=COLORS['white'])
    progress_frame.pack(fill="x", pady=(0, 20))
    
    progress_label = tt.Label(
        progress_frame,
        text="Step 1 of 2: Enter Your Information",
        font=FONTS['label'],
        bg=COLORS['white'],
        fg=COLORS['primary']
    )
    progress_label.pack(side="left")
    
    # ===== Form Container =====
    form_container = tt.Frame(main_frame, bg=COLORS['white'])
    form_container.pack(fill="both", expand=True)
    
    # Create two columns
    left_column = tt.Frame(form_container, bg=COLORS['white'])
    left_column.pack(side="left", fill="both", expand=True, padx=(0, 20))
    
    right_column = tt.Frame(form_container, bg=COLORS['white'])
    right_column.pack(side="right", fill="both", expand=True)
    
    # ===== LEFT COLUMN =====
    # First Name
    tt.Label(
        left_column,
        text="FIRST NAME *",
        font=FONTS['label'],
        bg=COLORS['white'],
        fg=COLORS['dark'],
        anchor="w"
    ).pack(fill="x", pady=(0, 5))
    
    fn_frame = tt.Frame(
        left_column,
        bg=COLORS['white'],
        highlightbackground=COLORS['border'],
        highlightthickness=1,
        highlightcolor=COLORS['accent']
    )
    fn_frame.pack(fill="x", pady=(0, 15))
    
    fn_entry = tt.Entry(
        fn_frame,
        font=FONTS['body'],
        bd=0,
        bg=COLORS['white'],
        fg=COLORS['dark'],
        insertbackground=COLORS['accent']
    )
    fn_entry.pack(padx=10, pady=8, fill="x")
    
    # Last Name
    tt.Label(
        left_column,
        text="LAST NAME *",
        font=FONTS['label'],
        bg=COLORS['white'],
        fg=COLORS['dark'],
        anchor="w"
    ).pack(fill="x", pady=(0, 5))
    
    ln_frame = tt.Frame(
        left_column,
        bg=COLORS['white'],
        highlightbackground=COLORS['border'],
        highlightthickness=1
    )
    ln_frame.pack(fill="x", pady=(0, 15))
    
    ln_entry = tt.Entry(
        ln_frame,
        font=FONTS['body'],
        bd=0,
        bg=COLORS['white'],
        fg=COLORS['dark'],
        insertbackground=COLORS['accent']
    )
    ln_entry.pack(padx=10, pady=8, fill="x")
    
    # Phone
    tt.Label(
        left_column,
        text="PHONE NUMBER *",
        font=FONTS['label'],
        bg=COLORS['white'],
        fg=COLORS['dark'],
        anchor="w"
    ).pack(fill="x", pady=(0, 5))
    
    phone_frame = tt.Frame(
        left_column,
        bg=COLORS['white'],
        highlightbackground=COLORS['border'],
        highlightthickness=1
    )
    phone_frame.pack(fill="x", pady=(0, 15))
    
    phone_entry = tt.Entry(
        phone_frame,
        font=FONTS['body'],
        bd=0,
        bg=COLORS['white'],
        fg=COLORS['dark'],
        insertbackground=COLORS['accent']
    )
    phone_entry.pack(padx=10, pady=8, fill="x")
    
    # ===== RIGHT COLUMN =====
    # Email
    tt.Label(
        right_column,
        text="EMAIL ADDRESS *",
        font=FONTS['label'],
        bg=COLORS['white'],
        fg=COLORS['dark'],
        anchor="w"
    ).pack(fill="x", pady=(0, 5))
    
    email_frame = tt.Frame(
        right_column,
        bg=COLORS['white'],
        highlightbackground=COLORS['border'],
        highlightthickness=1
    )
    email_frame.pack(fill="x", pady=(0, 15))
    
    email_entry = tt.Entry(
        email_frame,
        font=FONTS['body'],
        bd=0,
        bg=COLORS['white'],
        fg=COLORS['dark'],
        insertbackground=COLORS['accent']
    )
    email_entry.pack(padx=10, pady=8, fill="x")
    
    # Password
    tt.Label(
        right_column,
        text="PASSWORD *",
        font=FONTS['label'],
        bg=COLORS['white'],
        fg=COLORS['dark'],
        anchor="w"
    ).pack(fill="x", pady=(0, 5))
    
    psw_frame = tt.Frame(
        right_column,
        bg=COLORS['white'],
        highlightbackground=COLORS['border'],
        highlightthickness=1
    )
    psw_frame.pack(fill="x", pady=(0, 5))
    
    psw_entry = tt.Entry(
        psw_frame,
        font=FONTS['body'],
        show="●",
        bd=0,
        bg=COLORS['white'],
        fg=COLORS['dark'],
        insertbackground=COLORS['accent']
    )
    psw_entry.pack(padx=10, pady=8, fill="x")
    psw_entry.bind('<KeyRelease>', check_password_strength)
    
    # Password strength indicator
    strength_container = tt.Frame(right_column, bg=COLORS['white'])
    strength_container.pack(fill="x", pady=(0, 15))
    
    strength_bar = ttk.Progressbar(
        strength_container,
        length=100,
        mode='determinate',
        value=0,
        style="Strength.Weak.Horizontal.TProgressbar"
    )
    strength_bar.pack(side="left", fill="x", expand=True, padx=(0, 10))
    
    strength_label = tt.Label(
        strength_container,
        text="Not set",
        font=FONTS['small'],
        bg=COLORS['white'],
        fg=COLORS['gray']
    )
    strength_label.pack(side="left")
    
    # Confirm Password
    tt.Label(
        right_column,
        text="CONFIRM PASSWORD *",
        font=FONTS['label'],
        bg=COLORS['white'],
        fg=COLORS['dark'],
        anchor="w"
    ).pack(fill="x", pady=(0, 5))
    
    confirm_psw_frame = tt.Frame(
        right_column,
        bg=COLORS['white'],
        highlightbackground=COLORS['border'],
        highlightthickness=1
    )
    confirm_psw_frame.pack(fill="x", pady=(0, 5))
    
    confirm_psw_entry = tt.Entry(
        confirm_psw_frame,
        font=FONTS['body'],
        show="●",
        bd=0,
        bg=COLORS['white'],
        fg=COLORS['dark'],
        insertbackground=COLORS['accent']
    )
    confirm_psw_entry.pack(padx=10, pady=8, fill="x")
    
    # Show password option
    show_password_var = tt.BooleanVar()
    toggle_btn = tt.Checkbutton(
        right_column,
        text="👁️ Show Password",
        variable=show_password_var,
        command=toggle_password,
        bg=COLORS['white'],
        fg=COLORS['dark'],
        activebackground=COLORS['white'],
        font=FONTS['small']
    )
    toggle_btn.pack(anchor="w", pady=(5, 0))
    
    # ===== Terms and Conditions =====
    terms_frame = tt.Frame(main_frame, bg=COLORS['white'])
    terms_frame.pack(fill="x", pady=20)
    
    terms_var = tt.BooleanVar()
    terms_check = tt.Checkbutton(
        terms_frame,
        text="I agree to the Terms of Service and Privacy Policy",
        variable=terms_var,
        bg=COLORS['white'],
        fg=COLORS['dark'],
        activebackground=COLORS['white'],
        font=FONTS['body']
    )
    terms_check.pack()
    
    # ===== Action Buttons =====
    button_frame = tt.Frame(main_frame, bg=COLORS['white'])
    button_frame.pack(fill="x", pady=20)
    
    # Validate Button
    validate_btn = tt.Button(
        button_frame,
        text="VALIDATE INFORMATION",
        command=validate_form,
        font=FONTS['label'],
        bg=COLORS['accent'],
        fg=COLORS['white'],
        width=20,
        height=2,
        bd=0,
        cursor="hand2",
        activebackground=COLORS['hover'],
        activeforeground=COLORS['white']
    )
    validate_btn.pack(side="left", padx=5)
    
    # Register Button
    register_btn = tt.Button(
        button_frame,
        text="CREATE ACCOUNT",
        command=register_user,
        state="disabled",
        font=FONTS['label'],
        bg=COLORS['gray'],
        fg=COLORS['white'],
        width=20,
        height=2,
        bd=0,
        disabledforeground=COLORS['light']
    )
    register_btn.pack(side="left", padx=5)
    
    # Clear Button
    clear_btn = tt.Button(
        button_frame,
        text="CLEAR FORM",
        command=clear_form,
        font=FONTS['body'],
        bg=COLORS['gray'],
        fg=COLORS['white'],
        width=15,
        height=2,
        bd=0,
        cursor="hand2",
        activebackground=COLORS['secondary'],
        activeforeground=COLORS['white']
    )
    clear_btn.pack(side="left", padx=5)
    
    # ===== Login Link =====
    login_link_frame = tt.Frame(main_frame, bg=COLORS['white'])
    login_link_frame.pack(fill="x", pady=10)
    
    tt.Label(
        login_link_frame,
        text="Already have an account? ",
        font=FONTS['body'],
        bg=COLORS['white'],
        fg=COLORS['gray']
    ).pack(side="left")
    
    login_link = tt.Label(
        login_link_frame,
        text="Sign In",
        font=FONTS['label'],
        bg=COLORS['white'],
        fg=COLORS['accent'],
        cursor="hand2"
    )
    login_link.pack(side="left")
    
    # Hover effect for login link
    def on_login_enter(e):
        login_link.config(fg=COLORS['hover'])
    
    def on_login_leave(e):
        login_link.config(fg=COLORS['accent'])
    
    login_link.bind("<Enter>", on_login_enter)
    login_link.bind("<Leave>", on_login_leave)
    login_link.bind("<Button-1>", lambda e: (window.destroy(), login_user("Enter")))
    
    # Set focus to first field
    fn_entry.focus()
    
    # Enter key binding
    window.bind('<Return>', lambda e: validate_form())
    
    # Start main loop
    window.mainloop()

if __name__ == "__main__":
    # You can call login_user directly or let the user_tool_gui handle it
    login_user("Enter")