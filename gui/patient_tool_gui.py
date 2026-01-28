import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import Combobox
from .api import create_patient, delete_patient, update_patient
from models.search import search_patient_by_id
from models.database import date_checker
from datetime import datetime

def update_patient_gui(id_number):
    patient = search_patient_by_id(id_number) 
       
    def update():
        id = id_number

        created_at = created_at_entry.get()
        first_name = fn_entry.get()
        middle_name = mn_entry.get()
        last_name = ln_entry.get()
        age = age_entry.get()
        gender = gender_entry.get()
        city = city_entry.get()
        sub_city = sub_city_entry.get()
        wereda = wereda_entry.get()
        house_number = house_number_entry.get()
        phone = phone_entry.get()
        created_by = created_by_entry.get()
        diagnosis = diagnosis_entry.get()

        formatted_date = date_checker(created_at.strip())
        if not formatted_date:
            return

        if not all([first_name, last_name, age, gender, phone, created_by]):
            messagebox.showwarning("Incomplete Data", "Please fill in all required fields before updating.")
            return

        if not phone.isdigit() or len(phone) != 10:
            messagebox.showerror("Phone", "Phone must be 10 digits and numeric only start with 09")
            return

        try:
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
                messagebox.showinfo("Success", "Patient data successfully updated!")
                clear()
                window.destroy()
            else:
                messagebox.showerror("Error", str(resp))

        except Exception as e:
            messagebox.showerror("Error", f"Failed to update patient.\n{e}")

        
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
        gender_entry.delete(0, tk.END)
        phone_entry.delete(0, tk.END)
        created_by_entry.delete(0, tk.END)

    window = tk.Toplevel()
    window.title("Update patient data")
    window.geometry("450x600")
    window.resizable(False,False)
    window.configure(bg="#f0f0f0")
    
    tk.Label(window, text="Update Patient's Data Form", font=("arial", 14, "bold")).pack(fill="both", pady=20)
    
    frame = tk.Frame(window,)
    frame.place(relx=0.5, rely=0.5, anchor="center")    
   
    
    label = ["የተመዘገበበት ቀን / Created At",
        "ስም / First Name",
        "የአባት ስም / Middle Name",
        "የአያት ስም / Last Name",
        "እድሜ / Age",
        "ፆታ / Gender",
        "ከተማ / City",
        "ክ/ከተማ / Sub-City",
        "ወረዳ / Wereda",
        "የቤት ቁጥር / House Number",
        "ስልክ / Phone",
        "የተመዘገበበት ባለሙያ / Created By",
        "ዲያግኖሲስ / Diagnosis"]
    for i, title in enumerate(label):
        tk.Label(frame, text=title, font=("arial", 10, "bold")).grid(row=i, column=0, padx=10, pady=5, sticky="e")
        
    created_at_entry = tk.Entry(frame)   
    fn_entry = tk.Entry(frame)
    mn_entry = tk.Entry(frame)
    ln_entry = tk.Entry(frame)
    age_entry = tk.Entry(frame)
    gender_entry = Combobox(frame, values=['male', 'female'])
    city_entry = tk.Entry(frame)
    sub_city_entry = tk.Entry(frame)
    wereda_entry = tk.Entry(frame)
    house_number_entry = tk.Entry(frame)
    phone_entry = tk.Entry(frame)
    created_by_entry = tk.Entry(frame)
    diagnosis_entry = tk.Entry(frame)
    
        
    created_at_entry.grid(row=0, column=1)
    fn_entry.grid(row=1, column=1)
    mn_entry.grid(row=2, column=1)
    ln_entry.grid(row=3, column=1)
    age_entry.grid(row=4, column=1)
    gender_entry.grid(row=5, column=1)
    city_entry.grid(row=6, column=1)
    sub_city_entry.grid(row=7, column=1)
    wereda_entry.grid(row=8, column=1)
    house_number_entry.grid(row=9, column=1)
    phone_entry.grid(row=10, column=1)
    created_by_entry.grid(row=11, column=1)
    diagnosis_entry.grid(row=12, column=1)
    
    created_at_entry.insert(0, patient[1])
    fn_entry.insert(0, patient[2])
    mn_entry.insert(0, patient[3])
    ln_entry.insert(0, patient[4])
    age_entry.insert(0, patient[5])
    gender_entry.set(patient[6])
    city_entry.insert(0, patient[7])
    sub_city_entry.insert(0, patient[8])
    wereda_entry.insert(0, patient[9])
    house_number_entry.insert(0, patient[10])
    phone_entry.insert(0, patient[11])
    created_by_entry.insert(0, patient[12])
    created_by_entry.config(state="readonly")
    diagnosis_entry.insert(0, patient[13])
    
    
    update_btn = tk.Button(frame, text='UPDATE', command=update, fg="white", padx=4, pady=4)
    update_btn.config(bg="blue")
    update_btn.grid(row=13, column=0, columnspan=2, pady=20)
    window.mainloop()

def add_patient_gui(created_by):
    def submit():
        created_at = entry_created_at.get()
        fname = entry_fname.get()
        mname = entry_mname.get()
        lname = entry_lname.get()
        age = entry_age.get()
        gender = combo_gender.get()
        city = entry_city.get()
        subcity = entry_sub_city.get()
        wereda = entry_wereda.get()
        house_number = entry_house_number.get()
        phone = entry_phone.get()
        created_by = created_by_entry.get()
        diagnosis = diagnosis_entry.get()

        formatted_date = date_checker(created_at.strip())
        if not formatted_date:
            return

        if not all([created_at, fname, lname, age, gender, phone, created_by]):
            messagebox.showwarning("Missing Data", "Please fill all the '*' fields.")
            return

        if not phone.isdigit() or len(phone) != 10:
            messagebox.showerror("Phone", "Phone must be 10 digits and numeric only start with 09")
            return

        try:
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
                created_by,
                diagnosis
            )

            if ok:
                messagebox.showinfo("Success", "Patient added successfully!")
                clear_form()
                window.destroy()
            else:
                messagebox.showerror("Error", str(resp))

        except Exception as e:
            messagebox.showerror("Error", f"Failed to add patient.\n{e}")


    def clear_form():
        entry_created_at.delete(0, tk.END)
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
        created_by_entry.delete(0, tk.END)
        diagnosis_entry.delete(0, tk.END)

    window = tk.Toplevel()
    window.title("Add New Patient")
    window.geometry("450x600")
    window.resizable(False,False)
    window.configure(bg="#f0f0f0")
    
    tk.Label(window, text="New Patient Form", font=("arial", 14, "bold")).pack(fill="both")

    frame = tk.Frame(window)
    frame.place(relx=0.5, rely=0.5, anchor="center")
    
    labels = ["የተመዘገበበት ቀን / Created At *",
        "ስም / First Name *",
        "የአባት ስም / Middle Name *",
        "የአያት ስም / Last Name *",
        "እድሜ / Age *",
        "ፆታ / Gender *",
        "ከተማ / City",
        "ክ/ከተማ / Sub-City",
        "ወረዳ / Wereda",
        "የቤት ቁጥር / House Number",
        "ስልክ / Phone *",
        "የተመዘገበበት ባለሙያ / Created By",
        "ዲያግኖሲስ / Diagnosis"]
    for i, label in enumerate(labels):
        tk.Label(frame, text=label, font=("arial", 10, "bold")).grid(row=i, column=0, padx=10, pady=7, sticky="e")
    entry_created_at = tk.Entry(frame)
    today = datetime.now().strftime("%Y-%m-%d")
    entry_created_at.insert(0, today)
    entry_fname = tk.Entry(frame)
    entry_mname = tk.Entry(frame)
    entry_lname = tk.Entry(frame)
    entry_age = tk.Entry(frame)
    combo_gender = Combobox(frame, values=["Male", "Female"])
    entry_city = tk.Entry(frame)
    entry_sub_city = tk.Entry(frame)
    entry_wereda = tk.Entry(frame)
    entry_house_number = tk.Entry(frame)
    entry_phone = tk.Entry(frame)
    created_by_entry = tk.Entry(frame,)
    created_by_entry.insert(tk.END, created_by)
    created_by_entry.config(state="readonly")
    diagnosis_entry = tk.Entry(frame,)
    

    entry_created_at.grid(row=0, column=1)
    entry_fname.grid(row=1, column=1)
    entry_mname.grid(row=2, column=1)
    entry_lname.grid(row=3, column=1)
    entry_age.grid(row=4, column=1)
    combo_gender.grid(row=5, column=1)
    entry_city.grid(row=6, column=1)
    entry_sub_city.grid(row=7, column=1)
    entry_wereda.grid(row=8, column=1)
    entry_house_number.grid(row=9, column=1)
    entry_phone.grid(row=10, column=1)
    created_by_entry.grid(row=11, column=1)
    diagnosis_entry.grid(row=12, column=1)

    # Submit Button
    add_btn = tk.Button(frame, text="Add Patient", fg="white", command=submit, padx=4, pady=4)
    add_btn.config(bg="green")
    add_btn.grid(row=13, column=0, columnspan=2, pady=15)
    window.mainloop()

def delete_patient_gui(id):
    patient = search_patient_by_id(id)
        
    def delete():
        ans = messagebox.askyesno(
            "Confirm Deletion",
            f"Are you sure you want to delete {patient[1]} {patient[2]}?"
        )

        if not ans:
            return

        try:
            ok, resp = delete_patient(id)

            if ok:
                messagebox.showinfo("Deleted", "Patient deleted successfully.")
                window.destroy()
            else:
                messagebox.showerror("Error", str(resp))

        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete patient.\n{e}")

    
    # GUI setup
    window = tk.Toplevel()
    window.title("Delete Patient")
    window.geometry("300x200")
    window.resizable(False, False)
    window.configure(bg="#f0f0f0")
    
    frame = tk.Frame(window)
    frame.place(relx=0.5, rely=0.5, anchor="center")
    
    tk.Label(frame, 
             text=f"Do you want to Delete '{patient[1]} {patient[2]}'",
             fg="red", font=("arial", 10, "bold")).pack(fill="both", pady=10)
    
    patient_detail = tk.Label(frame, width=50, wraplength=300)
    patient_detail.pack()
    patient_detail.config(text=f"{patient[1]} {patient[2]} | Age: {patient[4]} | created_by: {patient[8]}")


    delete_btn = tk.Button(frame, text="Delete", command=delete, padx=4, pady=4)
    delete_btn.config(bg="red", fg='white')
    delete_btn.pack(pady=10)
    window.mainloop()