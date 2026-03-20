import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from models.patient_history import insert_history
from models.search import search_patient_by_id
from models.database import date_checker
from gui import history_loader
from models import backups
from datetime import datetime

today = datetime.now().strftime("%Y-%m-%d")

def history_view(id):
    # Professional medical color scheme
    COLORS = {
        'primary': '#2c3e50',
        'secondary': '#34495e',
        'accent': '#3498db',
        'success': '#27ae60',
        'warning': '#e74c3c',
        'danger': '#c0392b',
        'light': '#f8f9fa',
        'dark': '#2c3e50',
        'white': '#ffffff',
        'gray': '#6c757d',
        'hover': '#2980b9',
        'border': '#dee2e6',
        'history_bg': '#fff9e6',  # Soft cream for history
        'note_bg': '#e8f5e9',      # Soft green for notes
        'clinical_bg': '#e3f2fd',   # Soft blue for clinical
        'header_bg': '#2c3e50'
    }
    
    FONTS = {
        'heading': ('Segoe UI', 16, 'bold'),
        'subheading': ('Segoe UI', 12, 'bold'),
        'body': ('Segoe UI', 10),
        'small': ('Segoe UI', 9),
        'label': ('Segoe UI', 10, 'bold'),
        'button': ('Segoe UI', 10, 'bold')
    }
    
    patient = search_patient_by_id(id)
    if not patient:
        messagebox.showerror("No patient", "Please select only one patient and try again")
        return
    
    def clear():
        date_entry.delete(0, tk.END)
        diagnosis_entry.delete(0, tk.END)
        history_text.delete(1.0, tk.END)
        note_text.delete(1.0, tk.END)
        dr_name_entry.delete(0, tk.END)
        date_entry.insert(0, today)
        dr_name_entry.insert(0, "Dr. ")
    
    def add_new_history():
        date = date_entry.get().strip()
        diagnosis = diagnosis_entry.get().strip()
        detail_history = history_text.get(1.0, tk.END).strip()
        note = note_text.get(1.0, tk.END).strip()
        doc_name = dr_name_entry.get().strip()
        
        formatted_date = date_checker(date)
        if formatted_date:
            if old_history_text.get("1.0", tk.END).strip() == "No Previous History !!":
                old_history_text.config(state="normal")
                old_history_text.delete("1.0", tk.END)
                old_history_text.config(state="disabled")
            
            if not diagnosis or not doc_name:
                messagebox.showwarning("Missing Fields", "Doctor name and Diagnosis are required!")
                return
            
            ans = messagebox.askyesno("Are you sure?", "Click 'yes' to save the history")
            if ans:
                try:
                    insert_history(id, formatted_date, diagnosis, detail_history, note, doc_name)
                    messagebox.showinfo("Success", f"✅ Successfully added {patient[2]} {patient[3]}'s History")
                    
                    # Refresh history display
                    history_loader.history_loader_to_front(
                        old_history_text, id, formatted_date, 
                        diagnosis, detail_history, note, doc_name
                    )
                    clear()
                    
                except Exception as e:
                    messagebox.showerror("Error", f"Something went wrong: {str(e)}")
    
    # Create main window
    window = tk.Tk()
    window.title(f"Health For All Clinic - Medical History: {patient[2]} {patient[3]}")
    
    # Get screen dimensions
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    
    # Set window size
    window_width = min(1400, screen_width - 100)
    window_height = min(900, screen_height - 100)
    
    # Calculate position to center the window
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    
    window.geometry(f'{window_width}x{window_height}+{x}+{y}')
    window.configure(bg=COLORS['light'])
    
    # Create main canvas with scrollbar for entire window
    main_canvas = tk.Canvas(window, bg=COLORS['light'], highlightthickness=0)
    main_canvas.pack(side="left", fill="both", expand=True)
    
    v_scrollbar = tk.Scrollbar(window, orient="vertical", command=main_canvas.yview)
    v_scrollbar.pack(side="right", fill="y")
    
    main_canvas.configure(yscrollcommand=v_scrollbar.set)
    
    # Frame inside canvas
    main_frame = tk.Frame(main_canvas, bg=COLORS['light'])
    main_canvas.create_window((0, 0), window=main_frame, anchor="nw")
    
    def configure_scroll(event):
        main_canvas.configure(scrollregion=main_canvas.bbox("all"))
        main_canvas.itemconfig(1, width=main_canvas.winfo_width())
    
    main_frame.bind("<Configure>", configure_scroll)
    main_canvas.bind('<Configure>', configure_scroll)
    
    # ===== HEADER =====
    header_frame = tk.Frame(main_frame, bg=COLORS['header_bg'], height=80)
    header_frame.pack(fill="x", padx=10, pady=5)
    header_frame.pack_propagate(False)
    
    # Patient info in header
    header_content = tk.Frame(header_frame, bg=COLORS['header_bg'])
    header_content.pack(expand=True)
    
    tk.Label(
        header_content,
        text="🏥",
        font=('Segoe UI', 28),
        bg=COLORS['header_bg'],
        fg=COLORS['white']
    ).pack(side="left", padx=(0, 15))
    
    patient_info = f"{patient[2]} {patient[3]} {patient[4]}"
    tk.Label(
        header_content,
        text=patient_info,
        font=FONTS['heading'],
        bg=COLORS['header_bg'],
        fg=COLORS['white']
    ).pack(side="left")
    
    tk.Label(
        header_content,
        text=f" | Age: {patient[5]} | Gender: {patient[6]} | Phone: {patient[11]}",
        font=FONTS['body'],
        bg=COLORS['header_bg'],
        fg=COLORS['light']
    ).pack(side="left")
    
    # ===== UPPER SECTION - History Records =====
    upper_frame = ttk.LabelFrame(main_frame, text="📜 PATIENT HISTORY RECORDS", padding=10)
    upper_frame.pack(padx=10, pady=10, fill="both", expand=True)
    upper_frame.columnconfigure(0, weight=1)
    upper_frame.columnconfigure(1, weight=1)
    upper_frame.rowconfigure(0, weight=1)
    
    # LEFT PANEL - Previous History
    text_frame = tk.Frame(upper_frame, bg=COLORS['white'], relief="groove", bd=1)
    text_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
    text_frame.rowconfigure(0, weight=1)
    text_frame.columnconfigure(0, weight=1)
    
    # Title for left panel
    tk.Label(
        text_frame,
        text="📋 COMPLETE HISTORY",
        font=FONTS['label'],
        bg=COLORS['primary'],
        fg=COLORS['white'],
        pady=5
    ).pack(fill="x")
    
    # Text container
    history_container = tk.Frame(text_frame, bg=COLORS['white'])
    history_container.pack(fill="both", expand=True, padx=5, pady=5)
    history_container.rowconfigure(0, weight=1)
    history_container.columnconfigure(0, weight=1)
    
    scroll_y = tk.Scrollbar(history_container, orient="vertical")
    scroll_y.grid(row=0, column=1, sticky="ns")
    
    scroll_x = tk.Scrollbar(history_container, orient="horizontal")
    scroll_x.grid(row=1, column=0, sticky="ew")
    
    old_history_text = tk.Text(
        history_container,
        wrap="word",
        font=('Consolas', 10),
        bg=COLORS['history_bg'],
        fg=COLORS['dark'],
        yscrollcommand=scroll_y.set,
        xscrollcommand=scroll_x.set
    )
    old_history_text.grid(row=0, column=0, sticky="nsew")
    
    scroll_y.config(command=old_history_text.yview)
    scroll_x.config(command=old_history_text.xview)
    
    # Load history
    has_history = history_loader.history_fecher(id, old_history_text)
    if not has_history:
        old_history_text.config(state="normal")
        old_history_text.delete("1.0", tk.END)
        old_history_text.insert("1.0", "📭 NO PREVIOUS HISTORY FOUND")
        old_history_text.tag_add("no_history", "1.0", "end")
        old_history_text.tag_config(
            "no_history",
            foreground=COLORS['gray'],
            font=('Segoe UI', 14, 'bold'),
            justify='center'
        )
        old_history_text.config(state="disabled")
    
    # RIGHT PANEL - Search Section
    search_frame = tk.Frame(upper_frame, bg=COLORS['white'], relief="groove", bd=1)
    search_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
    search_frame.rowconfigure(1, weight=1)
    search_frame.columnconfigure(0, weight=1)
    
    # Title for right panel
    tk.Label(
        search_frame,
        text="🔍 SEARCH & FILTER",
        font=FONTS['label'],
        bg=COLORS['accent'],
        fg=COLORS['white'],
        pady=5
    ).pack(fill="x")
    
    # Search controls
    data_frame = tk.Frame(search_frame, bg=COLORS['clinical_bg'], pady=10)
    data_frame.pack(fill="x", padx=10, pady=5)
    
    tk.Label(
        data_frame,
        text="Filter by:",
        bg=COLORS['clinical_bg'],
        font=FONTS['label']
    ).pack(side="left", padx=5)
    
    filter_choose = ttk.Combobox(
        data_frame,
        values=('All histories', 'Date'),
        width=12,
        font=FONTS['body']
    )
    filter_choose.set("All histories")
    filter_choose.pack(side="left", padx=5)
    
    history_date_entry = tk.Entry(
        data_frame,
        width=12,
        font=FONTS['body'],
        state="disabled"
    )
    history_date_entry.pack(side="left", padx=5)
    
    def on_filter_change(event=None):
        if filter_choose.get() == "Date":
            history_date_entry.config(state="normal")
        else:
            history_date_entry.config(state="disabled")
            history_date_entry.delete(0, tk.END)
    
    filter_choose.bind('<<ComboboxSelected>>', on_filter_change)
    
    search_btn = tk.Button(
        data_frame,
        text="🔍 SEARCH",
        command=lambda: history_loader.print_history(
            search_text, id, history_date_entry.get().strip(),
            history_date_entry, filter_choose
        ),
        bg=COLORS['accent'],
        fg=COLORS['white'],
        font=FONTS['button'],
        bd=0,
        cursor="hand2",
        padx=10
    )
    search_btn.pack(side="left", padx=5)
    
    # Search results area
    results_container = tk.Frame(search_frame, bg=COLORS['white'])
    results_container.pack(fill="both", expand=True, padx=10, pady=10)
    results_container.rowconfigure(0, weight=1)
    results_container.columnconfigure(0, weight=1)
    
    search_x = tk.Scrollbar(results_container, orient="horizontal")
    search_x.grid(row=1, column=0, sticky="ew")
    
    search_y = tk.Scrollbar(results_container, orient="vertical")
    search_y.grid(row=0, column=1, sticky="ns")
    
    search_text = tk.Text(
        results_container,
        wrap="word",
        font=('Consolas', 10),
        bg=COLORS['clinical_bg'],
        fg=COLORS['dark'],
        xscrollcommand=search_x.set,
        yscrollcommand=search_y.set
    )
    search_text.grid(row=0, column=0, sticky="nsew")
    
    search_x.config(command=search_text.xview)
    search_y.config(command=search_text.yview)
    
    # Initial instruction
    search_text.config(state="normal")
    search_text.delete("1.0", tk.END)
    search_text.insert("1.0", "🔍 Select filter and click SEARCH to view history records")
    search_text.tag_add("instruction", "1.0", "end")
    search_text.tag_config(
        "instruction",
        foreground=COLORS['accent'],
        font=('Segoe UI', 11, 'bold'),
        justify='center'
    )
    search_text.config(state="disabled")
    
    # Action buttons - Centered
    action_center = tk.Frame(search_frame, bg=COLORS['white'])
    action_center.pack(fill="x", pady=10)
    
    button_center = tk.Frame(action_center, bg=COLORS['white'])
    button_center.pack(anchor="center")
    
    tk.Button(
        button_center,
        text="🖨️ PRINT",
        bg=COLORS['warning'],
        fg=COLORS['white'],
        width=12,
        font=FONTS['button'],
        bd=0,
        cursor="hand2",
        command=lambda: backups.printer(search_text, patient[2], patient[3], patient[5])
    ).pack(side="left", padx=5)
    
    tk.Button(
        button_center,
        text="📄 EXTRACT FILE",
        bg=COLORS['success'],
        fg=COLORS['white'],
        width=12,
        font=FONTS['button'],
        bd=0,
        cursor="hand2",
        command=lambda: backups.extract_file(search_text, patient[2], patient[3], patient[5])
    ).pack(side="left", padx=5)
    
    # ===== LOWER SECTION =====
    lower_frame = ttk.LabelFrame(main_frame, text="➕ ADD NEW MEDICAL HISTORY", padding=10)
    lower_frame.pack(padx=10, pady=10, fill="both", expand=True)
    
    # Form row
    form_frame = tk.Frame(lower_frame, bg=COLORS['white'])
    form_frame.pack(fill="x", pady=10, padx=10)
    
    # Date
    tk.Label(
        form_frame,
        text="📅 Date:",
        font=FONTS['label'],
        bg=COLORS['white'],
        fg=COLORS['dark']
    ).grid(row=0, column=0, padx=10, pady=8, sticky="e")
    
    date_entry = tk.Entry(form_frame, width=15, font=FONTS['body'])
    date_entry.grid(row=0, column=1, padx=10, pady=8)
    date_entry.insert(0, today)
    
    # Dr's Name
    tk.Label(
        form_frame,
        text="👨‍⚕️ Doctor's Name:",
        font=FONTS['label'],
        bg=COLORS['white'],
        fg=COLORS['dark']
    ).grid(row=0, column=2, padx=10, pady=8, sticky="e")
    
    dr_name_entry = tk.Entry(form_frame, width=20, font=FONTS['body'])
    dr_name_entry.grid(row=0, column=3, padx=10, pady=8)
    dr_name_entry.insert(0, "Dr. ")
    
    # Diagnosis
    tk.Label(
        form_frame,
        text="🏥 Diagnosis:",
        font=FONTS['label'],
        bg=COLORS['white'],
        fg=COLORS['dark']
    ).grid(row=0, column=4, padx=10, pady=8, sticky="e")
    
    diagnosis_entry = tk.Entry(form_frame, width=25, font=FONTS['body'], bg=COLORS['clinical_bg'])
    diagnosis_entry.grid(row=0, column=5, padx=10, pady=8)
    
    # Text areas
    texts_frame = tk.Frame(lower_frame, bg=COLORS['white'])
    texts_frame.pack(fill="both", expand=True, pady=10, padx=10)
    texts_frame.columnconfigure(0, weight=1)
    texts_frame.columnconfigure(1, weight=1)
    texts_frame.rowconfigure(0, weight=1)
    
    # History text area
    history_label_frame = ttk.LabelFrame(texts_frame, text="📝 DETAILED HISTORY", padding=5)
    history_label_frame.grid(row=0, column=0, sticky="nsew", padx=5)
    history_label_frame.rowconfigure(0, weight=1)
    history_label_frame.columnconfigure(0, weight=1)
    
    history_container = tk.Frame(history_label_frame)
    history_container.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
    history_container.rowconfigure(0, weight=1)
    history_container.columnconfigure(0, weight=1)
    
    history_x = tk.Scrollbar(history_container, orient="horizontal")
    history_x.grid(row=1, column=0, sticky="ew")
    
    history_y = tk.Scrollbar(history_container, orient="vertical")
    history_y.grid(row=0, column=1, sticky="ns")
    
    history_text = tk.Text(
        history_container,
        bg=COLORS['history_bg'],
        font=('Consolas', 10),
        wrap="word",
        xscrollcommand=history_x.set,
        yscrollcommand=history_y.set
    )
    history_text.grid(row=0, column=0, sticky="nsew")
    
    history_x.config(command=history_text.xview)
    history_y.config(command=history_text.yview)
    
    # Note text area
    note_label_frame = ttk.LabelFrame(texts_frame, text="📌 ADDITIONAL NOTES", padding=5)
    note_label_frame.grid(row=0, column=1, sticky="nsew", padx=5)
    note_label_frame.rowconfigure(0, weight=1)
    note_label_frame.columnconfigure(0, weight=1)
    
    note_container = tk.Frame(note_label_frame)
    note_container.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
    note_container.rowconfigure(0, weight=1)
    note_container.columnconfigure(0, weight=1)
    
    note_x = tk.Scrollbar(note_container, orient="horizontal")
    note_x.grid(row=1, column=0, sticky="ew")
    
    note_y = tk.Scrollbar(note_container, orient="vertical")
    note_y.grid(row=0, column=1, sticky="ns")
    
    note_text = tk.Text(
        note_container,
        bg=COLORS['note_bg'],
        font=('Consolas', 10),
        wrap="word",
        xscrollcommand=note_x.set,
        yscrollcommand=note_y.set
    )
    note_text.grid(row=0, column=0, sticky="nsew")
    
    note_x.config(command=note_text.xview)
    note_y.config(command=note_text.yview)
    
    # Button frame - Centered
    btn_center = tk.Frame(lower_frame, bg=COLORS['white'])
    btn_center.pack(fill="x", pady=15)
    
    center_container = tk.Frame(btn_center, bg=COLORS['white'])
    center_container.pack(anchor="center")
    
    add_history_btn = tk.Button(
        center_container,
        text="➕ ADD HISTORY RECORD",
        bg=COLORS['success'],
        fg=COLORS['white'],
        font=('Segoe UI', 11, 'bold'),
        padx=30,
        pady=8,
        bd=0,
        cursor="hand2",
        command=add_new_history
    )
    add_history_btn.pack(side="left", padx=10)
    
    tk.Button(
        center_container,
        text="🗑️ CLEAR FORM",
        bg=COLORS['gray'],
        fg=COLORS['white'],
        font=FONTS['button'],
        padx=25,
        pady=8,
        bd=0,
        cursor="hand2",
        command=clear
    ).pack(side="left", padx=10)
    
    # ===== FOOTER =====
    footer_frame = tk.Frame(main_frame, bg=COLORS['secondary'], height=30)
    footer_frame.pack(fill="x", padx=10, pady=5)
    footer_frame.pack_propagate(False)
    
    tk.Label(
        footer_frame,
        text=f"Patient ID: {id} • Registered: {patient[1]} • Last Update: {today}",
        font=FONTS['small'],
        bg=COLORS['secondary'],
        fg=COLORS['light']
    ).pack(side="left", padx=10, pady=5)
    
    # Mouse wheel scrolling
    def on_mousewheel(event):
        main_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    
    main_canvas.bind_all("<MouseWheel>", on_mousewheel)
    
    window.mainloop()