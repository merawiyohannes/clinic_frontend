import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import Combobox
from .api import create_patient, delete_patient, update_patient
from models.search import search_patient_by_id
from models.database import date_checker
from datetime import datetime

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
    'border': '#dcdde1',
    'form_bg': '#ffffff',
    'required': '#e74c3c'
}

FONTS = {
    'heading': ('Segoe UI', 16, 'bold'),
    'subheading': ('Segoe UI', 12),
    'body': ('Segoe UI', 10),
    'small': ('Segoe UI', 9),
    'label': ('Segoe UI', 10, 'bold'),
    'amharic': ('Noto Sans Ethiopic', 10, 'bold')
}

def update_patient_gui(id_number):
    patient = search_patient_by_id(id_number) 
       
    def update():
        id = id_number

        created_at = created_at_entry.get()
        first_name = fn_entry.get().strip()
        middle_name = mn_entry.get().strip()
        last_name = ln_entry.get().strip()
        age = age_entry.get().strip()
        gender = gender_entry.get().strip()
        city = city_entry.get().strip()
        sub_city = sub_city_entry.get().strip()
        wereda = wereda_entry.get().strip()
        house_number = house_number_entry.get().strip()
        phone = phone_entry.get().strip()
        created_by = created_by_entry.get().strip()
        diagnosis = diagnosis_entry.get().strip()

        # Reset field borders
        for frame in [created_at_frame, fn_frame, mn_frame, ln_frame, age_frame, 
                      gender_frame, city_frame, sub_city_frame, wereda_frame, 
                      house_frame, phone_frame, created_by_frame, diagnosis_frame]:
            frame.config(highlightbackground=COLORS['border'])

        # Validate required fields
        if not all([first_name, last_name, age, gender, phone, created_by]):
            messagebox.showwarning("Incomplete Data", "Please fill in all required fields before updating.", parent=window)
            if not first_name: fn_frame.config(highlightbackground=COLORS['warning'])
            if not last_name: ln_frame.config(highlightbackground=COLORS['warning'])
            if not age: age_frame.config(highlightbackground=COLORS['warning'])
            if not gender: gender_frame.config(highlightbackground=COLORS['warning'])
            if not phone: phone_frame.config(highlightbackground=COLORS['warning'])
            if not created_by: created_by_frame.config(highlightbackground=COLORS['warning'])
            return

        # Validate date
        formatted_date = date_checker(created_at.strip())
        if not formatted_date:
            created_at_frame.config(highlightbackground=COLORS['warning'])
            return

        # Validate phone
        if not phone.isdigit() or len(phone) != 10:
            messagebox.showerror("Invalid Phone", "Phone must be 10 digits and numeric only", parent=window)
            phone_frame.config(highlightbackground=COLORS['warning'])
            return

        try:
            # Show loading state
            update_btn.config(text="UPDATING...", state="disabled", bg=COLORS['gray'])
            window.update()
            
            ok, resp = update_patient(
                id,
                formatted_date,
                first_name,
                middle_name,
                last_name,
                int(age),
                gender,
                city,
                sub_city,
                wereda,
                house_number,
                phone,
                created_by,
                diagnosis
            )

            if ok:
                messagebox.showinfo("Success", "✅ Patient data successfully updated!", parent=window)
                window.destroy()
            else:
                messagebox.showerror("Error", str(resp), parent=window)
                update_btn.config(text="UPDATE PATIENT", state="normal", bg=COLORS['accent'])

        except Exception as e:
            messagebox.showerror("Error", f"Failed to update patient.\n{e}", parent=window)
            update_btn.config(text="UPDATE PATIENT", state="normal", bg=COLORS['accent'])

    def clear():
        fn_entry.delete(0, tk.END)
        city_entry.delete(0, tk.END)
        sub_city_entry.delete(0, tk.END)
        wereda_entry.delete(0, tk.END)
        house_number_entry.delete(0, tk.END)
        created_at_entry.delete(0, tk.END)
        diagnosis_entry.delete(0, tk.END)
        mn_entry.delete(0, tk.END)
        ln_entry.delete(0, tk.END)
        age_entry.delete(0, tk.END)
        gender_entry.set('')
        phone_entry.delete(0, tk.END)
        created_by_entry.delete(0, tk.END)

    # ===== Main Window =====
    window = tk.Toplevel()
    window.title("Health For All Clinic - Update Patient")
    window.geometry("600x800")
    window.resizable(False, False)
    window.configure(bg=COLORS['light'])
    
    # Center window
    window.update_idletasks()
    width = 600
    height = 800
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')

    # ===== Header =====
    header_frame = tk.Frame(window, bg=COLORS['primary'], height=80)
    header_frame.pack(fill=tk.X)
    header_frame.pack_propagate(False)

    tk.Label(
        header_frame,
        text="✏️ Update Patient Information",
        font=FONTS['heading'],
        bg=COLORS['primary'],
        fg=COLORS['white']
    ).pack(pady=(15, 5))

    tk.Label(
        header_frame,
        text="Modify patient details below",
        font=FONTS['small'],
        bg=COLORS['primary'],
        fg=COLORS['light']
    ).pack()

    # ===== Form Container =====
    form_container = tk.Frame(window, bg=COLORS['white'])
    form_container.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)

    # Create canvas for scrolling if needed
    canvas = tk.Canvas(form_container, bg=COLORS['white'], highlightthickness=0)
    scrollbar = tk.Scrollbar(form_container, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg=COLORS['white'])

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=canvas.winfo_width())
    canvas.configure(yscrollcommand=scrollbar.set)

    def configure_canvas_width(event):
        canvas.itemconfig(1, width=event.width)

    canvas.bind('<Configure>', configure_canvas_width)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # ===== Form Fields =====
    # Created At
    tk.Label(
        scrollable_frame,
        text="የተመዘገበበት ቀን / Created At *",
        font=FONTS['label'],
        bg=COLORS['white'],
        fg=COLORS['dark'],
        anchor="w"
    ).pack(fill=tk.X, pady=(0, 5))

    created_at_frame = tk.Frame(
        scrollable_frame,
        bg=COLORS['white'],
        highlightbackground=COLORS['border'],
        highlightthickness=1
    )
    created_at_frame.pack(fill=tk.X, pady=(0, 15))

    created_at_entry = tk.Entry(
        created_at_frame,
        font=FONTS['body'],
        bd=0,
        bg=COLORS['white'],
        fg=COLORS['dark'],
        insertbackground=COLORS['accent']
    )
    created_at_entry.pack(padx=10, pady=8, fill=tk.X)
    created_at_entry.insert(0, patient[1])

    # First Name
    tk.Label(
        scrollable_frame,
        text="ስም / First Name *",
        font=FONTS['label'],
        bg=COLORS['white'],
        fg=COLORS['dark'],
        anchor="w"
    ).pack(fill=tk.X, pady=(0, 5))

    fn_frame = tk.Frame(
        scrollable_frame,
        bg=COLORS['white'],
        highlightbackground=COLORS['border'],
        highlightthickness=1
    )
    fn_frame.pack(fill=tk.X, pady=(0, 15))

    fn_entry = tk.Entry(
        fn_frame,
        font=FONTS['body'],
        bd=0,
        bg=COLORS['white'],
        fg=COLORS['dark'],
        insertbackground=COLORS['accent']
    )
    fn_entry.pack(padx=10, pady=8, fill=tk.X)
    fn_entry.insert(0, patient[2])

    # Middle Name
    tk.Label(
        scrollable_frame,
        text="የአባት ስም / Middle Name",
        font=FONTS['label'],
        bg=COLORS['white'],
        fg=COLORS['dark'],
        anchor="w"
    ).pack(fill=tk.X, pady=(0, 5))

    mn_frame = tk.Frame(
        scrollable_frame,
        bg=COLORS['white'],
        highlightbackground=COLORS['border'],
        highlightthickness=1
    )
    mn_frame.pack(fill=tk.X, pady=(0, 15))

    mn_entry = tk.Entry(
        mn_frame,
        font=FONTS['body'],
        bd=0,
        bg=COLORS['white'],
        fg=COLORS['dark'],
        insertbackground=COLORS['accent']
    )
    mn_entry.pack(padx=10, pady=8, fill=tk.X)
    mn_entry.insert(0, patient[3])

    # Last Name
    tk.Label(
        scrollable_frame,
        text="የአያት ስም / Last Name *",
        font=FONTS['label'],
        bg=COLORS['white'],
        fg=COLORS['dark'],
        anchor="w"
    ).pack(fill=tk.X, pady=(0, 5))

    ln_frame = tk.Frame(
        scrollable_frame,
        bg=COLORS['white'],
        highlightbackground=COLORS['border'],
        highlightthickness=1
    )
    ln_frame.pack(fill=tk.X, pady=(0, 15))

    ln_entry = tk.Entry(
        ln_frame,
        font=FONTS['body'],
        bd=0,
        bg=COLORS['white'],
        fg=COLORS['dark'],
        insertbackground=COLORS['accent']
    )
    ln_entry.pack(padx=10, pady=8, fill=tk.X)
    ln_entry.insert(0, patient[4])

    # Age
    tk.Label(
        scrollable_frame,
        text="እድሜ / Age *",
        font=FONTS['label'],
        bg=COLORS['white'],
        fg=COLORS['dark'],
        anchor="w"
    ).pack(fill=tk.X, pady=(0, 5))

    age_frame = tk.Frame(
        scrollable_frame,
        bg=COLORS['white'],
        highlightbackground=COLORS['border'],
        highlightthickness=1
    )
    age_frame.pack(fill=tk.X, pady=(0, 15))

    age_entry = tk.Entry(
        age_frame,
        font=FONTS['body'],
        bd=0,
        bg=COLORS['white'],
        fg=COLORS['dark'],
        insertbackground=COLORS['accent']
    )
    age_entry.pack(padx=10, pady=8, fill=tk.X)
    age_entry.insert(0, patient[5])

    # Gender
    tk.Label(
        scrollable_frame,
        text="ፆታ / Gender *",
        font=FONTS['label'],
        bg=COLORS['white'],
        fg=COLORS['dark'],
        anchor="w"
    ).pack(fill=tk.X, pady=(0, 5))

    gender_frame = tk.Frame(
        scrollable_frame,
        bg=COLORS['white'],
        highlightbackground=COLORS['border'],
        highlightthickness=1
    )
    gender_frame.pack(fill=tk.X, pady=(0, 15))

    gender_entry = Combobox(
        gender_frame,
        values=['Male', 'Female'],
        font=FONTS['body'],
        state="readonly"
    )
    gender_entry.pack(padx=10, pady=8, fill=tk.X)
    gender_entry.set(patient[6])

    # City
    tk.Label(
        scrollable_frame,
        text="ከተማ / City",
        font=FONTS['label'],
        bg=COLORS['white'],
        fg=COLORS['dark'],
        anchor="w"
    ).pack(fill=tk.X, pady=(0, 5))

    city_frame = tk.Frame(
        scrollable_frame,
        bg=COLORS['white'],
        highlightbackground=COLORS['border'],
        highlightthickness=1
    )
    city_frame.pack(fill=tk.X, pady=(0, 15))

    city_entry = tk.Entry(
        city_frame,
        font=FONTS['body'],
        bd=0,
        bg=COLORS['white'],
        fg=COLORS['dark'],
        insertbackground=COLORS['accent']
    )
    city_entry.pack(padx=10, pady=8, fill=tk.X)
    city_entry.insert(0, patient[7])

    # Sub City
    tk.Label(
        scrollable_frame,
        text="ክ/ከተማ / Sub-City",
        font=FONTS['label'],
        bg=COLORS['white'],
        fg=COLORS['dark'],
        anchor="w"
    ).pack(fill=tk.X, pady=(0, 5))

    sub_city_frame = tk.Frame(
        scrollable_frame,
        bg=COLORS['white'],
        highlightbackground=COLORS['border'],
        highlightthickness=1
    )
    sub_city_frame.pack(fill=tk.X, pady=(0, 15))

    sub_city_entry = tk.Entry(
        sub_city_frame,
        font=FONTS['body'],
        bd=0,
        bg=COLORS['white'],
        fg=COLORS['dark'],
        insertbackground=COLORS['accent']
    )
    sub_city_entry.pack(padx=10, pady=8, fill=tk.X)
    sub_city_entry.insert(0, patient[8])

    # Wereda
    tk.Label(
        scrollable_frame,
        text="ወረዳ / Wereda",
        font=FONTS['label'],
        bg=COLORS['white'],
        fg=COLORS['dark'],
        anchor="w"
    ).pack(fill=tk.X, pady=(0, 5))

    wereda_frame = tk.Frame(
        scrollable_frame,
        bg=COLORS['white'],
        highlightbackground=COLORS['border'],
        highlightthickness=1
    )
    wereda_frame.pack(fill=tk.X, pady=(0, 15))

    wereda_entry = tk.Entry(
        wereda_frame,
        font=FONTS['body'],
        bd=0,
        bg=COLORS['white'],
        fg=COLORS['dark'],
        insertbackground=COLORS['accent']
    )
    wereda_entry.pack(padx=10, pady=8, fill=tk.X)
    wereda_entry.insert(0, patient[9])

    # House Number
    tk.Label(
        scrollable_frame,
        text="የቤት ቁጥር / House Number",
        font=FONTS['label'],
        bg=COLORS['white'],
        fg=COLORS['dark'],
        anchor="w"
    ).pack(fill=tk.X, pady=(0, 5))

    house_frame = tk.Frame(
        scrollable_frame,
        bg=COLORS['white'],
        highlightbackground=COLORS['border'],
        highlightthickness=1
    )
    house_frame.pack(fill=tk.X, pady=(0, 15))

    house_number_entry = tk.Entry(
        house_frame,
        font=FONTS['body'],
        bd=0,
        bg=COLORS['white'],
        fg=COLORS['dark'],
        insertbackground=COLORS['accent']
    )
    house_number_entry.pack(padx=10, pady=8, fill=tk.X)
    house_number_entry.insert(0, patient[10])

    # Phone
    tk.Label(
        scrollable_frame,
        text="ስልክ / Phone *",
        font=FONTS['label'],
        bg=COLORS['white'],
        fg=COLORS['dark'],
        anchor="w"
    ).pack(fill=tk.X, pady=(0, 5))

    phone_frame = tk.Frame(
        scrollable_frame,
        bg=COLORS['white'],
        highlightbackground=COLORS['border'],
        highlightthickness=1
    )
    phone_frame.pack(fill=tk.X, pady=(0, 15))

    phone_entry = tk.Entry(
        phone_frame,
        font=FONTS['body'],
        bd=0,
        bg=COLORS['white'],
        fg=COLORS['dark'],
        insertbackground=COLORS['accent']
    )
    phone_entry.pack(padx=10, pady=8, fill=tk.X)
    phone_entry.insert(0, patient[11])

    # Created By
    tk.Label(
        scrollable_frame,
        text="የተመዘገበበት ባለሙያ / Created By *",
        font=FONTS['label'],
        bg=COLORS['white'],
        fg=COLORS['dark'],
        anchor="w"
    ).pack(fill=tk.X, pady=(0, 5))

    created_by_frame = tk.Frame(
        scrollable_frame,
        bg=COLORS['white'],
        highlightbackground=COLORS['border'],
        highlightthickness=1
    )
    created_by_frame.pack(fill=tk.X, pady=(0, 15))

    created_by_entry = tk.Entry(
        created_by_frame,
        font=FONTS['body'],
        bd=0,
        bg=COLORS['white'],
        fg=COLORS['dark'],
        insertbackground=COLORS['accent']
    )
    created_by_entry.pack(padx=10, pady=8, fill=tk.X)
    created_by_entry.insert(0, patient[12])
    created_by_entry.config(state="readonly", readonlybackground=COLORS['light'])

    # Diagnosis
    tk.Label(
        scrollable_frame,
        text="ዲያግኖሲስ / Diagnosis",
        font=FONTS['label'],
        bg=COLORS['white'],
        fg=COLORS['dark'],
        anchor="w"
    ).pack(fill=tk.X, pady=(0, 5))

    diagnosis_frame = tk.Frame(
        scrollable_frame,
        bg=COLORS['white'],
        highlightbackground=COLORS['border'],
        highlightthickness=1
    )
    diagnosis_frame.pack(fill=tk.X, pady=(0, 15))

    diagnosis_entry = tk.Entry(
        diagnosis_frame,
        font=FONTS['body'],
        bd=0,
        bg=COLORS['white'],
        fg=COLORS['dark'],
        insertbackground=COLORS['accent']
    )
    diagnosis_entry.pack(padx=10, pady=8, fill=tk.X)
    diagnosis_entry.insert(0, patient[13])

    # Buttons
    button_frame = tk.Frame(scrollable_frame, bg=COLORS['white'])
    button_frame.pack(fill=tk.X, pady=20)

    button_container = tk.Frame(button_frame, bg=COLORS['white'])
    button_container.pack(anchor="center")

    update_btn = tk.Button(
        button_container,
        text="UPDATE PATIENT",
        command=update,
        font=FONTS['label'],
        bg=COLORS['accent'],
        fg=COLORS['white'],
        width=15,
        height=2,
        bd=0,
        cursor="hand2",
        activebackground=COLORS['hover'],
        activeforeground=COLORS['white']
    )
    update_btn.pack(side=tk.LEFT, padx=5)

    clear_btn = tk.Button(
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
    clear_btn.pack(side=tk.LEFT, padx=5)

    cancel_btn = tk.Button(
        button_container,
        text="CANCEL",
        command=window.destroy,
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
    cancel_btn.pack(side=tk.LEFT, padx=5)

    # Required fields note
    note_frame = tk.Frame(scrollable_frame, bg=COLORS['white'])
    note_frame.pack(fill=tk.X, pady=10)

    tk.Label(
        note_frame,
        text="* Required fields",
        font=FONTS['small'],
        bg=COLORS['white'],
        fg=COLORS['gray']
    ).pack()

    window.mainloop()

def add_patient_gui(created_by):
    def submit():
        created_at = entry_created_at.get().strip()
        fname = entry_fname.get().strip()
        mname = entry_mname.get().strip()
        lname = entry_lname.get().strip()
        age = entry_age.get().strip()
        gender = combo_gender.get().strip()
        city = entry_city.get().strip()
        subcity = entry_sub_city.get().strip()
        wereda = entry_wereda.get().strip()
        house_number = entry_house_number.get().strip()
        phone = entry_phone.get().strip()
        created_by_val = created_by_entry.get().strip()
        diagnosis = diagnosis_entry.get().strip()

        # Reset field borders
        for frame in [created_at_frame, fname_frame, mname_frame, lname_frame, 
                      age_frame, gender_frame, city_frame, sub_city_frame, 
                      wereda_frame, house_frame, phone_frame, diagnosis_frame]:
            frame.config(highlightbackground=COLORS['border'])

        # Validate required fields
        if not all([created_at, fname, lname, age, gender, phone, created_by_val]):
            messagebox.showwarning("Missing Data", "Please fill all the '*' fields.", parent=window)
            if not created_at: created_at_frame.config(highlightbackground=COLORS['warning'])
            if not fname: fname_frame.config(highlightbackground=COLORS['warning'])
            if not lname: lname_frame.config(highlightbackground=COLORS['warning'])
            if not age: age_frame.config(highlightbackground=COLORS['warning'])
            if not gender: gender_frame.config(highlightbackground=COLORS['warning'])
            if not phone: phone_frame.config(highlightbackground=COLORS['warning'])
            if not created_by_val: created_by_frame.config(highlightbackground=COLORS['warning'])
            return

        # Validate date
        formatted_date = date_checker(created_at.strip())
        if not formatted_date:
            created_at_frame.config(highlightbackground=COLORS['warning'])
            return

        # Validate phone
        if not phone.isdigit() or len(phone) != 10:
            messagebox.showerror("Invalid Phone", "Phone must be 10 digits and numeric only", parent=window)
            phone_frame.config(highlightbackground=COLORS['warning'])
            return

        try:
            # Show loading state
            add_btn.config(text="ADDING...", state="disabled", bg=COLORS['gray'])
            window.update()
            
            ok, resp = create_patient(
                formatted_date,
                fname,
                mname,
                lname,
                int(age),
                gender,
                city,
                subcity,
                wereda,
                house_number,
                phone,
                created_by_val,
                diagnosis
            )

            if ok:
                messagebox.showinfo("Success", "✅ Patient added successfully!", parent=window)
                window.destroy()
            else:
                messagebox.showerror("Error", str(resp), parent=window)
                add_btn.config(text="ADD PATIENT", state="normal", bg=COLORS['success'])

        except Exception as e:
            messagebox.showerror("Error", f"Failed to add patient.\n{e}", parent=window)
            add_btn.config(text="ADD PATIENT", state="normal", bg=COLORS['success'])

    def clear_form():
        entry_fname.delete(0, tk.END)
        entry_mname.delete(0, tk.END)
        entry_lname.delete(0, tk.END)
        entry_age.delete(0, tk.END)
        combo_gender.set("")
        entry_city.delete(0, tk.END)
        entry_sub_city.delete(0, tk.END)
        entry_wereda.delete(0, tk.END)
        entry_house_number.delete(0, tk.END)
        entry_phone.delete(0, tk.END)
        diagnosis_entry.delete(0, tk.END)

    # ===== Main Window =====
    window = tk.Toplevel()
    window.title("Health For All Clinic - Add New Patient")
    window.geometry("600x800")
    window.resizable(False, False)
    window.configure(bg=COLORS['light'])
    
    # Center window
    window.update_idletasks()
    width = 600
    height = 800
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')

    # ===== Header =====
    header_frame = tk.Frame(window, bg=COLORS['success'], height=80)
    header_frame.pack(fill=tk.X)
    header_frame.pack_propagate(False)

    tk.Label(
        header_frame,
        text="➕ Add New Patient",
        font=FONTS['heading'],
        bg=COLORS['success'],
        fg=COLORS['white']
    ).pack(pady=(15, 5))

    tk.Label(
        header_frame,
        text="Enter patient information below",
        font=FONTS['small'],
        bg=COLORS['success'],
        fg=COLORS['light']
    ).pack()

    # ===== Form Container =====
    form_container = tk.Frame(window, bg=COLORS['white'])
    form_container.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)

    # Create canvas for scrolling
    canvas = tk.Canvas(form_container, bg=COLORS['white'], highlightthickness=0)
    scrollbar = tk.Scrollbar(form_container, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg=COLORS['white'])

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=canvas.winfo_width())
    canvas.configure(yscrollcommand=scrollbar.set)

    def configure_canvas_width(event):
        canvas.itemconfig(1, width=event.width)

    canvas.bind('<Configure>', configure_canvas_width)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # ===== Form Fields =====
    # Created At
    tk.Label(
        scrollable_frame,
        text="የተመዘገበበት ቀን / Created At *",
        font=FONTS['label'],
        bg=COLORS['white'],
        fg=COLORS['dark'],
        anchor="w"
    ).pack(fill=tk.X, pady=(0, 5))

    created_at_frame = tk.Frame(
        scrollable_frame,
        bg=COLORS['white'],
        highlightbackground=COLORS['border'],
        highlightthickness=1
    )
    created_at_frame.pack(fill=tk.X, pady=(0, 15))

    entry_created_at = tk.Entry(
        created_at_frame,
        font=FONTS['body'],
        bd=0,
        bg=COLORS['white'],
        fg=COLORS['dark'],
        insertbackground=COLORS['accent']
    )
    entry_created_at.pack(padx=10, pady=8, fill=tk.X)
    today = datetime.now().strftime("%Y-%m-%d")
    entry_created_at.insert(0, today)

    # First Name
    tk.Label(
        scrollable_frame,
        text="ስም / First Name *",
        font=FONTS['label'],
        bg=COLORS['white'],
        fg=COLORS['dark'],
        anchor="w"
    ).pack(fill=tk.X, pady=(0, 5))

    fname_frame = tk.Frame(
        scrollable_frame,
        bg=COLORS['white'],
        highlightbackground=COLORS['border'],
        highlightthickness=1
    )
    fname_frame.pack(fill=tk.X, pady=(0, 15))

    entry_fname = tk.Entry(
        fname_frame,
        font=FONTS['body'],
        bd=0,
        bg=COLORS['white'],
        fg=COLORS['dark'],
        insertbackground=COLORS['accent']
    )
    entry_fname.pack(padx=10, pady=8, fill=tk.X)

    # Middle Name
    tk.Label(
        scrollable_frame,
        text="የአባት ስም / Middle Name",
        font=FONTS['label'],
        bg=COLORS['white'],
        fg=COLORS['dark'],
        anchor="w"
    ).pack(fill=tk.X, pady=(0, 5))

    mname_frame = tk.Frame(
        scrollable_frame,
        bg=COLORS['white'],
        highlightbackground=COLORS['border'],
        highlightthickness=1
    )
    mname_frame.pack(fill=tk.X, pady=(0, 15))

    entry_mname = tk.Entry(
        mname_frame,
        font=FONTS['body'],
        bd=0,
        bg=COLORS['white'],
        fg=COLORS['dark'],
        insertbackground=COLORS['accent']
    )
    entry_mname.pack(padx=10, pady=8, fill=tk.X)

    # Last Name
    tk.Label(
        scrollable_frame,
        text="የአያት ስም / Last Name *",
        font=FONTS['label'],
        bg=COLORS['white'],
        fg=COLORS['dark'],
        anchor="w"
    ).pack(fill=tk.X, pady=(0, 5))

    lname_frame = tk.Frame(
        scrollable_frame,
        bg=COLORS['white'],
        highlightbackground=COLORS['border'],
        highlightthickness=1
    )
    lname_frame.pack(fill=tk.X, pady=(0, 15))

    entry_lname = tk.Entry(
        lname_frame,
        font=FONTS['body'],
        bd=0,
        bg=COLORS['white'],
        fg=COLORS['dark'],
        insertbackground=COLORS['accent']
    )
    entry_lname.pack(padx=10, pady=8, fill=tk.X)

    # Age
    tk.Label(
        scrollable_frame,
        text="እድሜ / Age *",
        font=FONTS['label'],
        bg=COLORS['white'],
        fg=COLORS['dark'],
        anchor="w"
    ).pack(fill=tk.X, pady=(0, 5))

    age_frame = tk.Frame(
        scrollable_frame,
        bg=COLORS['white'],
        highlightbackground=COLORS['border'],
        highlightthickness=1
    )
    age_frame.pack(fill=tk.X, pady=(0, 15))

    entry_age = tk.Entry(
        age_frame,
        font=FONTS['body'],
        bd=0,
        bg=COLORS['white'],
        fg=COLORS['dark'],
        insertbackground=COLORS['accent']
    )
    entry_age.pack(padx=10, pady=8, fill=tk.X)

    # Gender
    tk.Label(
        scrollable_frame,
        text="ፆታ / Gender *",
        font=FONTS['label'],
        bg=COLORS['white'],
        fg=COLORS['dark'],
        anchor="w"
    ).pack(fill=tk.X, pady=(0, 5))

    gender_frame = tk.Frame(
        scrollable_frame,
        bg=COLORS['white'],
        highlightbackground=COLORS['border'],
        highlightthickness=1
    )
    gender_frame.pack(fill=tk.X, pady=(0, 15))

    combo_gender = Combobox(
        gender_frame,
        values=["Male", "Female"],
        font=FONTS['body'],
        state="readonly"
    )
    combo_gender.pack(padx=10, pady=8, fill=tk.X)

    # City
    tk.Label(
        scrollable_frame,
        text="ከተማ / City",
        font=FONTS['label'],
        bg=COLORS['white'],
        fg=COLORS['dark'],
        anchor="w"
    ).pack(fill=tk.X, pady=(0, 5))

    city_frame = tk.Frame(
        scrollable_frame,
        bg=COLORS['white'],
        highlightbackground=COLORS['border'],
        highlightthickness=1
    )
    city_frame.pack(fill=tk.X, pady=(0, 15))

    entry_city = tk.Entry(
        city_frame,
        font=FONTS['body'],
        bd=0,
        bg=COLORS['white'],
        fg=COLORS['dark'],
        insertbackground=COLORS['accent']
    )
    entry_city.pack(padx=10, pady=8, fill=tk.X)

    # Sub City
    tk.Label(
        scrollable_frame,
        text="ክ/ከተማ / Sub-City",
        font=FONTS['label'],
        bg=COLORS['white'],
        fg=COLORS['dark'],
        anchor="w"
    ).pack(fill=tk.X, pady=(0, 5))

    sub_city_frame = tk.Frame(
        scrollable_frame,
        bg=COLORS['white'],
        highlightbackground=COLORS['border'],
        highlightthickness=1
    )
    sub_city_frame.pack(fill=tk.X, pady=(0, 15))

    entry_sub_city = tk.Entry(
        sub_city_frame,
        font=FONTS['body'],
        bd=0,
        bg=COLORS['white'],
        fg=COLORS['dark'],
        insertbackground=COLORS['accent']
    )
    entry_sub_city.pack(padx=10, pady=8, fill=tk.X)

    # Wereda
    tk.Label(
        scrollable_frame,
        text="ወረዳ / Wereda",
        font=FONTS['label'],
        bg=COLORS['white'],
        fg=COLORS['dark'],
        anchor="w"
    ).pack(fill=tk.X, pady=(0, 5))

    wereda_frame = tk.Frame(
        scrollable_frame,
        bg=COLORS['white'],
        highlightbackground=COLORS['border'],
        highlightthickness=1
    )
    wereda_frame.pack(fill=tk.X, pady=(0, 15))

    entry_wereda = tk.Entry(
        wereda_frame,
        font=FONTS['body'],
        bd=0,
        bg=COLORS['white'],
        fg=COLORS['dark'],
        insertbackground=COLORS['accent']
    )
    entry_wereda.pack(padx=10, pady=8, fill=tk.X)

    # House Number
    tk.Label(
        scrollable_frame,
        text="የቤት ቁጥር / House Number",
        font=FONTS['label'],
        bg=COLORS['white'],
        fg=COLORS['dark'],
        anchor="w"
    ).pack(fill=tk.X, pady=(0, 5))

    house_frame = tk.Frame(
        scrollable_frame,
        bg=COLORS['white'],
        highlightbackground=COLORS['border'],
        highlightthickness=1
    )
    house_frame.pack(fill=tk.X, pady=(0, 15))

    entry_house_number = tk.Entry(
        house_frame,
        font=FONTS['body'],
        bd=0,
        bg=COLORS['white'],
        fg=COLORS['dark'],
        insertbackground=COLORS['accent']
    )
    entry_house_number.pack(padx=10, pady=8, fill=tk.X)

    # Phone
    tk.Label(
        scrollable_frame,
        text="ስልክ / Phone *",
        font=FONTS['label'],
        bg=COLORS['white'],
        fg=COLORS['dark'],
        anchor="w"
    ).pack(fill=tk.X, pady=(0, 5))

    phone_frame = tk.Frame(
        scrollable_frame,
        bg=COLORS['white'],
        highlightbackground=COLORS['border'],
        highlightthickness=1
    )
    phone_frame.pack(fill=tk.X, pady=(0, 15))

    entry_phone = tk.Entry(
        phone_frame,
        font=FONTS['body'],
        bd=0,
        bg=COLORS['white'],
        fg=COLORS['dark'],
        insertbackground=COLORS['accent']
    )
    entry_phone.pack(padx=10, pady=8, fill=tk.X)

    # Created By
    tk.Label(
        scrollable_frame,
        text="የተመዘገበበት ባለሙያ / Created By *",
        font=FONTS['label'],
        bg=COLORS['white'],
        fg=COLORS['dark'],
        anchor="w"
    ).pack(fill=tk.X, pady=(0, 5))

    created_by_frame = tk.Frame(
        scrollable_frame,
        bg=COLORS['white'],
        highlightbackground=COLORS['border'],
        highlightthickness=1
    )
    created_by_frame.pack(fill=tk.X, pady=(0, 15))

    created_by_entry = tk.Entry(
        created_by_frame,
        font=FONTS['body'],
        bd=0,
        bg=COLORS['white'],
        fg=COLORS['dark'],
        insertbackground=COLORS['accent']
    )
    created_by_entry.pack(padx=10, pady=8, fill=tk.X)
    created_by_entry.insert(tk.END, created_by)
    created_by_entry.config(state="readonly", readonlybackground=COLORS['light'])

    # Diagnosis
    tk.Label(
        scrollable_frame,
        text="ዲያግኖሲስ / Diagnosis",
        font=FONTS['label'],
        bg=COLORS['white'],
        fg=COLORS['dark'],
        anchor="w"
    ).pack(fill=tk.X, pady=(0, 5))

    diagnosis_frame = tk.Frame(
        scrollable_frame,
        bg=COLORS['white'],
        highlightbackground=COLORS['border'],
        highlightthickness=1
    )
    diagnosis_frame.pack(fill=tk.X, pady=(0, 15))

    diagnosis_entry = tk.Entry(
        diagnosis_frame,
        font=FONTS['body'],
        bd=0,
        bg=COLORS['white'],
        fg=COLORS['dark'],
        insertbackground=COLORS['accent']
    )
    diagnosis_entry.pack(padx=10, pady=8, fill=tk.X)

    # Buttons
    button_frame = tk.Frame(scrollable_frame, bg=COLORS['white'])
    button_frame.pack(fill=tk.X, pady=20)

    button_container = tk.Frame(button_frame, bg=COLORS['white'])
    button_container.pack(anchor="center")

    add_btn = tk.Button(
        button_container,
        text="ADD PATIENT",
        command=submit,
        font=FONTS['label'],
        bg=COLORS['success'],
        fg=COLORS['white'],
        width=15,
        height=2,
        bd=0,
        cursor="hand2",
        activebackground='#219a52',
        activeforeground=COLORS['white']
    )
    add_btn.pack(side=tk.LEFT, padx=5)

    clear_btn = tk.Button(
        button_container,
        text="CLEAR",
        command=clear_form,
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
    clear_btn.pack(side=tk.LEFT, padx=5)

    cancel_btn = tk.Button(
        button_container,
        text="CANCEL",
        command=window.destroy,
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
    cancel_btn.pack(side=tk.LEFT, padx=5)

    # Required fields note
    note_frame = tk.Frame(scrollable_frame, bg=COLORS['white'])
    note_frame.pack(fill=tk.X, pady=10)

    tk.Label(
        note_frame,
        text="* Required fields",
        font=FONTS['small'],
        bg=COLORS['white'],
        fg=COLORS['gray']
    ).pack()

    window.mainloop()

def delete_patient_gui(id):
    patient = search_patient_by_id(id)
        
    def delete():
        ans = messagebox.askyesno(
            "Confirm Deletion",
            f"Are you sure you want to delete {patient[2]} {patient[3]}?",
            parent=window
        )

        if not ans:
            return

        try:
            ok, resp = delete_patient(id)

            if ok:
                messagebox.showinfo("Success", "✅ Patient deleted successfully.", parent=window)
                window.destroy()
            else:
                messagebox.showerror("Error", str(resp), parent=window)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete patient.\n{e}", parent=window)

    # ===== Main Window =====
    window = tk.Toplevel()
    window.title("Delete Patient")
    window.geometry("600x300")
    window.resizable(False, False)
    window.configure(bg=COLORS['light'])
    
    # Center window
    window.update_idletasks()
    width = 600
    height = 300
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')

    # Content
    content_frame = tk.Frame(window, bg=COLORS['white'])
    content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    # Warning Icon
    tk.Label(
        content_frame,
        text="⚠️",
        font=('Segoe UI', 40),
        bg=COLORS['white'],
        fg=COLORS['warning']
    ).pack(pady=10)

    # Patient Info
    tk.Label(
        content_frame,
        text=f"Delete {patient[2]} {patient[3]} | Age: {patient[5]} | Phone: {patient[11]}",
        font=('Segoe UI', 11),
        bg=COLORS['white'],
        fg=COLORS['dark']
    ).pack(pady=10)

    # Buttons
    button_frame = tk.Frame(content_frame, bg=COLORS['white'])
    button_frame.pack(pady=15)

    delete_btn = tk.Button(
        button_frame,
        text="DELETE",
        command=delete,
        font=('Segoe UI', 10, 'bold'),
        bg=COLORS['danger'],
        fg=COLORS['white'],
        width=10,
        height=1,
        bd=0,
        cursor="hand2"
    )
    delete_btn.pack(side=tk.LEFT, padx=10)

    cancel_btn = tk.Button(
        button_frame,
        text="CANCEL",
        command=window.destroy,
        font=('Segoe UI', 10, 'bold'),
        bg=COLORS['gray'],
        fg=COLORS['white'],
        width=10,
        height=1,
        bd=0,
        cursor="hand2"
    )
    cancel_btn.pack(side=tk.LEFT, padx=10)

    window.mainloop()