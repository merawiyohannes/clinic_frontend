import tkinter as tk
from tkinter.ttk import Combobox
from tkinter import messagebox
from .api import search_by_name, search_patient_by_id, backup_history, backup_patients,backup_users
from gui.patient_tool_gui import add_patient_gui
from gui import tree_gui
from . import user_tool_gui



def open_dashboard(user):
    def backup_patients_gui():
        ok, resp = backup_patients()
        if ok:
            messagebox.showinfo("Backup", "Patients backup completed")
        else:
            messagebox.showerror("Backup failed", resp)


    def backup_history_gui():
        ok, resp = backup_history()
        if ok:
            messagebox.showinfo("Backup", "History backup completed")
        else:
            messagebox.showerror("Backup failed", resp)


    def backup_users_gui():
        ok, resp = backup_users()
        if ok:
            messagebox.showinfo("Backup", "Users backup completed")
        else:
            messagebox.showerror("Backup failed", resp)

    def logout():
        answ = messagebox.askyesno("Logout", "Do you want to Log-out?")
        if answ:
            window.destroy()
            user_tool_gui.login_user("Enter")
        
    def search_patient():
        name = entry.get()

        if not name.strip():
            messagebox.showwarning("Empty Search", "Please enter a name or ID to search.")
            return

        filter_value = filter.get()

        # clear tree
        for item in tree.get_children():
            tree.delete(item)

        if filter_value == "Name":
            ok, patients = search_by_name(name)

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

            else:
                messagebox.showinfo("Not Found", f"No '{name}' match found")

        elif filter_value == "Id":
            ok, p = search_patient_by_id(name)

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
            else:
                messagebox.showinfo("Not Found", f"No '{name}' match found")

                
    window = tk.Tk()
    window.title("WELCOME TO HEALTH FOR ALL CLINIC")

    tk.Label(window, text="Patient Management").pack(fill=tk.BOTH)
    
    search_frame = tk.Frame(window, bg="#e0e0e0", padx=10, pady=10)
    search_frame.pack(fill=tk.X)
    
    
    filter_label = tk.Label(search_frame, text="search patient by👉")
    filter_label.config(bg="gray", fg="white")
    filter_label.pack(side=tk.LEFT, padx=5)
    
    filter = Combobox(search_frame,values=("Name", "Id"), width=8)
    filter.set("Name") 
    filter.pack(side=tk.LEFT, padx=5)
    
    entry = tk.Entry(search_frame, width=20)
    entry.pack(side=tk.LEFT, padx=5)
    
    search = tk.Button(search_frame, text="🔍 Search", command=search_patient, width=15)
    search.pack(side=tk.LEFT, padx=5)
    search.config(bg="#24A0ED")
    
    cancle_btn = tk.Button(search_frame, text="🔁 Refresh", command=lambda: tree_gui.reset_tree(tree, entry), width=15)
    cancle_btn.pack(side=tk.LEFT)
    cancle_btn.config(bg="red", fg="white")
    
    add = tk.Button(search_frame, text="➕ Add new patient", command=lambda: add_patient_gui(user), width=20, pady=10)
    add.pack(side=tk.RIGHT, pady=5)
    add.config(bg="green", fg="white")
    

    
    tools_frame = tk.Frame(window)
    tools_frame.pack(fill=tk.BOTH, padx=10, pady=5)

    tree = tree_gui.tree_view(window)
    tree
    tree.bind("<Button-3>", lambda event: tree_gui.on_row_right_click(event, tree))
    
    btns_frame = tk.Frame(window, bg="#e0e0e0")
    btns_frame.pack(fill=tk.X)
    
    bu_btn = tk.Menubutton(btns_frame, text="BackUp", bg="#FFFF00", fg="black")
    bu_btn.grid(row=0, column=0, padx=5)
    bu_menu = tk.Menu(bu_btn, tearoff=0)
    bu_btn.config(menu=bu_menu)
    bu_menu.add_command(label="Backup Patient", command=backup_patients_gui)
    bu_menu.add_command(label="Backup History", command=backup_history_gui)
    bu_menu.add_command(label="Backup User", command=backup_users_gui)
    
    setting_btn = tk.Menubutton(btns_frame, text="Settings", bg="#2196F3")
    setting_btn.grid(row=0, column=4, padx=5)
    
    setting_menu = tk.Menu(setting_btn, tearoff=0)
    setting_btn.config(menu=setting_menu)
    
    setting_menu.add_command(label="Change Password", command=user_tool_gui.edit_password)
    setting_menu.add_command(label="Logout", command=logout)
    
    
    footer_frame = tk.Frame(window, bg="#87CEEB")
    footer_frame.pack(fill=tk.X, side=tk.BOTTOM)
    
    tk.Label(footer_frame, text=f"user: {user}", font=("arial", 8, "bold")).pack(side=tk.LEFT, padx=10) 
    tk.Button(footer_frame, text="Logout",
              bg="red", fg="white",
              command=logout,
              padx=4, pady=4).pack(side=tk.RIGHT, padx=10, pady=4)
       
    window.mainloop()
                
