import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from models.search import search_patient_by_id
from models.database import date_checker
from gui import history_loader
from models import backups
from .api import add_history
from datetime import datetime

today = datetime.now().strftime("%Y-%m-%d")

def history_view(id):
    patient = search_patient_by_id(id)
    if not patient:
        messagebox.showerror("No patient", "Please select only one patient an try again")
    def clear():
        date_entry.delete(0, tk.END)
        diagnosis_entry.delete(0, tk.END)
        history_text.delete(1.0, tk.END)
        note_text.delete(1.0, tk.END)
        dr_name_entry.delete(0, tk.END)
        
    
    def add_new_history():
        date = date_entry.get()
        diagnosis = diagnosis_entry.get()
        detail_history = history_text.get(1.0, tk.END)
        note = note_text.get(1.0, tk.END)
        doc_name = dr_name_entry.get()

        formatted_date = date_checker(date.strip())

        if formatted_date:
            if old_history_text.get("1.0", tk.END).strip() == "No Previous History !!":
                old_history_text.config(state="normal")
                old_history_text.delete("1.0", tk.END)
                old_history_text.config(state="disabled")

            if not diagnosis.strip() or not doc_name.strip():
                messagebox.showwarning("Missing Fields", "Doctor name and Diagnosis are required!")
                return

            ans = messagebox.askyesno(
                "Are you sure?",
                "If you are sure about the Datas,\nclick 'yes' to save the history and display it in the above patient history area"
            )

            if ans:
                try:
                    ok, resp = add_history(id, formatted_date, diagnosis, detail_history, note, doc_name)

                    if ok:
                        messagebox.showinfo(
                            "Success Message",
                            f"You successfully added '{patient[2]} {patient[3]}' History"
                        )

                        history_loader.history_loader_to_front(
                            old_history_text,
                            id,
                            formatted_date,
                            diagnosis,
                            detail_history,
                            note,
                            doc_name
                        )

                        clear()
                        date_entry.insert(tk.END, today)
                        dr_name_entry.insert(tk.END, "Dr. ")

                    else:
                        messagebox.showerror("Error", resp)

                except Exception as e:
                    messagebox.showerror("Error", f"Sorry! something went wrong\n{e}")


        
        
    window = tk.Tk()
    window.title("Patients History Page")

    tk.Label(window,
              text=f"{patient[2]} {patient[3]} | Age:{patient[5]}  Medical History",
              font=("arial", 11, "bold"), background="red", foreground="white").pack(fill="both", padx=5, pady=5)
    upper_frame = ttk.Labelframe(window, text="Patient History(Previous)", padding=10)
    upper_frame.pack(padx=10, pady=10, fill="both", expand=True)
    upper_frame.columnconfigure(0, weight=1)
    upper_frame.columnconfigure(1, weight=1)
    text_frame = tk.Frame(upper_frame,)
    text_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
    
    scroll_y = tk.Scrollbar(text_frame, orient="vertical")
    scroll_x = tk.Scrollbar(text_frame, orient="horizontal")
    
    old_history_text = tk.Text(text_frame, wrap=None, height=11,
                           yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set, )
    
    scroll_y.config(command=old_history_text.yview)
    scroll_y.pack(fill="y", side="right")
    scroll_x.config(command=old_history_text.xview)
    scroll_x.pack(fill="x", side="bottom")
    has_history = history_loader.history_fecher(id, old_history_text)
    if not has_history:
        old_history_text.config(state="normal")
        old_history_text.insert("1.0", "No Previous History !!")
        old_history_text.tag_add("new", "1.0","2.0")
        old_history_text.tag_config("new", foreground="red", font=("arial", 14, "bold"))
        old_history_text.config(state="disabled")
        
    old_history_text.pack(side='left', fill="both", expand=True)
    # print_frame = tk.Frame(upper_frame)
    # print_frame.pack(fill="both", expand=True)
    # tk.Button(print_frame, text="Print-History",bg="#FF851B", fg="black", padx=10, pady=5, command=lambda: backups.printer(old_history_text, patient[2], patient[3], patient[5])).pack(side="left")

    search_frame = tk.Frame(upper_frame)
    search_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
    data_frame = tk.Frame(search_frame, background="#ADD8E6")
    data_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
    tk.Label(data_frame, text="choose history filter options", bg="#ADD8E6").pack(side=tk.LEFT)
    filter_choose = ttk.Combobox(data_frame, values=('All histories', 'Date'))
    filter_choose.set("All histories")
    filter_choose.pack(side=tk.LEFT)
    history_date_entry = tk.Entry(data_frame,)
    history_date_entry.pack(side=tk.LEFT)
    
    
    
    inside_frame = tk.Frame(search_frame)
    inside_frame.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)
    search_x = tk.Scrollbar(inside_frame, orient="horizontal")
    search_y = tk.Scrollbar(inside_frame, orient="vertical")
    search_text = tk.Text(inside_frame, wrap=None, height=11, xscrollcommand=search_x.set, yscrollcommand=search_y.set)
    search_text.config(state="normal")
    search_text.insert("1.0", "Choose 'all histories' to get all the history, or Choose 'date' enter the specific date you want and click search!")
    search_text.tag_add("new", "1.0","4.0")
    search_text.tag_config("new", foreground="green", font=("arial", 14, "bold"))
    search_text.config(state="disabled")
    search_x.config(command=search_text.xview)
    search_y.config(command=search_text.yview)
    search_x.pack(fill="x", side="bottom")
    search_y.pack(fill="y", side="right")
    search_text.pack(fill="both", expand=True)
    search_btn  = ttk.Button(data_frame, text="search",
                             command=lambda: history_loader.print_history(search_text, id, history_date_entry.get().strip(), history_date_entry, filter_choose))
    search_btn.pack(side=tk.LEFT)
    button_frame = tk.Frame(search_frame)
    button_frame.grid(row=3, column=0, columnspan=2, pady=5)

    tk.Button(button_frame, text="Print", bg="#e40c0c",
            fg="white", width=10,
            command=lambda:backups.printer(search_text, patient[2], patient[3], patient[5])
    ).pack(side=tk.LEFT, padx=5)

    tk.Button(button_frame, text="Extract File", bg="#0cb375",
            fg="white", width=10,
            command=lambda:backups.extract_file(search_text, patient[2], patient[3], patient[5])
    ).pack(side=tk.LEFT, padx=5)
    

# add history form

    lower_frame = ttk.Labelframe(window, text="Add New History Form", padding=10)
    lower_frame.pack(padx=10, pady=10, fill="both", expand=True)
    
    form_frame = tk.Frame(lower_frame,)
    form_frame.pack(fill="both", expand=True)
    tk.Label(form_frame, text="Date").grid(row=0, column=0, padx=5, pady=5)
    tk.Label(form_frame, text="Dr's Name").grid(row=0, column=2, padx=5, pady=5)
    tk.Label(form_frame, text="Diagnosis").grid(row=0, column=4, padx=5, pady=5)
    
    
    date_entry = tk.Entry(form_frame, )
    date_entry.insert(0, today)
    diagnosis_entry = tk.Entry(form_frame, width=30)
    dr_name_entry = tk.Entry(form_frame, width=30)
    dr_name_entry.insert(tk.END, "Dr ")
    
    date_entry.grid(row=0, column=1, padx=10, pady=5)
    dr_name_entry.grid(row=0, column=3, padx=10, pady=5)
    diagnosis_entry.grid(row=0, column=5, padx=5, pady=5)
    
    texts_frame = tk.Frame(lower_frame)
    texts_frame.pack(fill="both", expand=True)
    
    history_label_frame = ttk.Labelframe(texts_frame, text="History")
    history_label_frame.pack(side="left", pady=5, fill="both", expand=True)
    history_x = tk.Scrollbar(history_label_frame, orient="horizontal")
    history_y = tk.Scrollbar(history_label_frame, orient="vertical")
    history_text = tk.Text(history_label_frame, bg="yellow", wrap=None, height=11, xscrollcommand=history_x.set, yscrollcommand=history_y.set)
    history_x.config(command=history_text.xview)
    history_y.config(command=history_text.yview)
    history_x.pack(fill="x", side="bottom")
    history_y.pack(fill="y", side="right")
    history_text.pack(fill="both", expand=True, padx=5, pady=5)
    
    note_label_frame = ttk.Labelframe(texts_frame, text="Note")
    note_label_frame.pack(side="left", pady=5, fill="both", expand=True)
    note_x = tk.Scrollbar(note_label_frame, orient="horizontal")
    note_y = tk.Scrollbar(note_label_frame, orient="vertical")
    note_text = tk.Text(note_label_frame, bg="#D3D3D3", fg="black", height=11, xscrollcommand=note_x.set, yscrollcommand=note_y.set)
    note_x.config(command=note_text.xview)
    note_y.config(command=note_text.yview)
    note_x.pack(fill="x", side="bottom")
    note_y.pack(fill="y", side="right")
    note_text.pack(fill="both", expand=True, padx=5, pady=5)
    
    btn_frame = tk.Frame(lower_frame)
    btn_frame.pack(fill="both", expand=True)
    add_history_btn = tk.Button(btn_frame, width=30,
                                text="Add History", bg="green",
                                fg="white", padx=5, pady=5,
                                command=add_new_history)
    add_history_btn.pack(side="bottom", pady=10)
    window.mainloop()