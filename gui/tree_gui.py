import tkinter as tk
from tkinter.ttk import Scrollbar
from tkinter import ttk
from .api import list_all_patients, diagnosis_filler
from gui.patient_tool_gui import update_patient_gui, delete_patient_gui
from gui import history_gui

import tkinter as tk
from tkinter import Menu


def tree_value(tree):
    return tree

def reset_tree(tree, entry):
    for item in tree.get_children():
        tree.delete(item)

    ok, patients = list_all_patients()

    if ok:
        for p in patients:
            tree.insert("", "end", values=[
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

    entry.delete(0, tk.END)
    diagnosis_filler()



def on_row_right_click(event,tree):
    context_menu = Menu(tree, tearoff=0)

    context_menu.add_command(label="✏️ Edit", command=lambda: update_patient_gui(tree.item(tree.selection()[0])["values"][0]))
    context_menu.add_command(label="🗑️ Delete", command=lambda: delete_patient_gui(tree.item(tree.selection()[0])["values"][0]))
    context_menu.add_command(label="📜 History", command=lambda: history_gui.history_view(tree.item(tree.selection()[0])["values"][0]))
    
    row_id = tree.identify_row(event.y)
    if row_id:
        tree.selection_set(row_id)
        context_menu.post(event.x_root, event.y_root)
    else:
        context_menu.unpost()

    
def tree_view(window):
    tree_frame = tk.Frame(window)
    tree_frame.pack(fill=tk.BOTH, expand=True)
    
    x_scroll = Scrollbar(tree_frame, orient="horizontal")
    y_scroll = Scrollbar(tree_frame, orient="vertical")
    
    tree = ttk.Treeview(tree_frame,
                        columns=['Id', "CREATED_AT", 'FIRST_NAME', 'MIDDLE_NAME', 'LAST_NAME', 'AGE', 'GENDER', 'CITY', 'SUB_CITY', 'WEREDA', 'HOUSE_No', 'PHONE', 'CREATED_BY', 'DIAGNOSIS'],
                        show="headings",
                        yscrollcommand=y_scroll.set,
                        xscrollcommand=x_scroll.set)
    x_scroll.config(command=tree.xview)
    x_scroll.pack(side="bottom", fill="x")
    
    y_scroll.config(command=tree.yview)
    y_scroll.pack(side='right', fill="y")
        
    tree.pack(fill='both', expand=True)

    for col in tree["columns"]:
        tree.heading(col, text=col.upper(),anchor="center")
        tree.column(col, anchor="center")

        
    ok, patients = list_all_patients()

    if ok:
        for p in patients:
            tree.insert("", "end", values=[
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
        
    return tree