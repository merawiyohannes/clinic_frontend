import tkinter as tk
from tkinter.ttk import Scrollbar, Treeview
from tkinter import ttk
from .api import list_all_patients, diagnosis_filler
from gui.patient_tool_gui import update_patient_gui, delete_patient_gui
from gui import history_gui
from tkinter import Menu

# Professional color scheme
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
    'even_row': '#f8f9fa',
    'odd_row': '#ffffff'
}

FONTS = {
    'heading': ('Segoe UI', 12, 'bold'),
    'body': ('Segoe UI', 10),
    'small': ('Segoe UI', 9)
}

def tree_value(tree):
    return tree

def reset_tree(tree, entry, status_label=None):
    """Reset tree view with all patients"""
    for item in tree.get_children():
        tree.delete(item)

    ok, patients = list_all_patients()

    if ok and patients:
        for i, p in enumerate(patients):
            item = tree.insert("", "end", values=[
                p.get('id'),
                p.get('created_at'),
                p.get('first_name'),
                p.get('middle_name'),
                p.get('last_name'),
                p.get('age'),
                p.get('gender'),
                p.get('city'),
                p.get('sub_city'),
                p.get('wereda'),
                p.get('house_number'),
                p.get('phone'),
                p.get('created_by'),
                p.get('diagnosis')
            ])
            # Alternate row colors
            if i % 2 == 0:
                tree.tag_configure('evenrow', background=COLORS['even_row'])
                tree.item(item, tags=('evenrow',))
            else:
                tree.tag_configure('oddrow', background=COLORS['odd_row'])
                tree.item(item, tags=('oddrow',))
        
        if status_label:
            status_label.config(text=f"Total patients: {len(patients)}", fg=COLORS['success'])
    else:
        if status_label:
            status_label.config(text="No patients found", fg=COLORS['warning'])

    if entry:
        entry.delete(0, tk.END)
    diagnosis_filler()

def on_row_right_click(event, tree, status_label=None):
    """Handle right-click on tree row"""
    # Get the row ID that was clicked
    row_id = tree.identify_row(event.y)
    
    if not row_id:
        return
    
    # Select the row
    tree.selection_set(row_id)
    
    # Get the values of the selected row
    values = tree.item(row_id)["values"]
    
    # Create context menu
    context_menu = Menu(tree, tearoff=0, bg=COLORS['white'], fg=COLORS['dark'])
    
    # Style the menu
    context_menu.add_command(
        label="✏️ Edit Patient",
        command=lambda: update_patient_gui(values[0]),
        font=FONTS['body']
    )
    context_menu.add_separator()
    context_menu.add_command(
        label="🗑️ Delete Patient",
        command=lambda: delete_patient_gui(values[0]),
        font=FONTS['body']
    )
    context_menu.add_separator()
    context_menu.add_command(
        label="📜 View History",
        command=lambda: history_gui.history_view(values[0]),
        font=FONTS['body']
    )
    
    # Display the menu at mouse position
    context_menu.post(event.x_root, event.y_root)

def tree_view(parent):
    """Create and return a styled treeview"""
    # Create frame with padding
    tree_frame = tk.Frame(parent, bg=COLORS['white'])
    tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # Create scrollbars
    x_scroll = Scrollbar(tree_frame, orient="horizontal")
    y_scroll = Scrollbar(tree_frame, orient="vertical")
    
    # Define columns
    columns = ['Id', "CREATED_AT", 'FIRST_NAME', 'MIDDLE_NAME', 'LAST_NAME', 
               'AGE', 'GENDER', 'CITY', 'SUB_CITY', 'WEREDA', 'HOUSE_No', 
               'PHONE', 'CREATED_BY', 'DIAGNOSIS']
    
    # Create treeview with custom style
    style = ttk.Style()
    style.theme_use('clam')
    
    # Configure treeview style
    style.configure(
        "Custom.Treeview",
        background=COLORS['white'],
        foreground=COLORS['dark'],
        rowheight=30,
        fieldbackground=COLORS['white'],
        font=FONTS['body']
    )
    style.configure(
        "Custom.Treeview.Heading",
        background=COLORS['primary'],
        foreground=COLORS['white'],
        relief="flat",
        font=FONTS['heading']
    )
    style.map(
        "Custom.Treeview.Heading",
        background=[('active', COLORS['secondary'])]
    )
    
    tree = ttk.Treeview(
        tree_frame,
        columns=columns,
        show="headings",
        yscrollcommand=y_scroll.set,
        xscrollcommand=x_scroll.set,
        style="Custom.Treeview",
        selectmode="browse"
    )
    
    # Configure scrollbars
    x_scroll.config(command=tree.xview)
    x_scroll.pack(side="bottom", fill="x")
    
    y_scroll.config(command=tree.yview)
    y_scroll.pack(side='right', fill="y")
    
    tree.pack(fill='both', expand=True)

    # Configure columns
    column_widths = {
        'Id': 60,
        'CREATED_AT': 150,
        'FIRST_NAME': 120,
        'MIDDLE_NAME': 120,
        'LAST_NAME': 120,
        'AGE': 50,
        'GENDER': 70,
        'CITY': 100,
        'SUB_CITY': 100,
        'WEREDA': 80,
        'HOUSE_No': 80,
        'PHONE': 100,
        'CREATED_BY': 100,
        'DIAGNOSIS': 200
    }
    
    for col in columns:
        tree.heading(col, text=col.upper(), anchor="center")
        tree.column(col, anchor="center", width=column_widths.get(col, 100))

    # Load initial data
    ok, patients = list_all_patients()

    if ok and patients:
        for i, p in enumerate(patients):
            item = tree.insert("", "end", values=[
                p.get('id'),
                p.get('created_at'),
                p.get('first_name'),
                p.get('middle_name'),
                p.get('last_name'),
                p.get('age'),
                p.get('gender'),
                p.get('city'),
                p.get('sub_city'),
                p.get('wereda'),
                p.get('house_number'),
                p.get('phone'),
                p.get('created_by'),
                p.get('diagnosis')
            ])
            # Alternate row colors
            if i % 2 == 0:
                tree.tag_configure('evenrow', background=COLORS['even_row'])
                tree.item(item, tags=('evenrow',))
    
    return tree