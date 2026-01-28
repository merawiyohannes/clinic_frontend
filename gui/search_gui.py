# import tkinter as tt
# from tkinter import messagebox
# from tkinter.ttk import Combobox
# from .api import search_by_name, search_patient_by_id


# def search_patient_gui():
    
#     def search_patient():
#         name = entry.get().strip()
#         filter_value = filter.get()

#         if not name:
#             messagebox.showwarning("Search", "Enter search value")
#             return

#         patient_list.delete(0, tt.END)

#         if filter_value == "Name":
#             ok, patients = search_by_name(name)
#             if ok and patients:
#                 for p in patients:
#                     patient_list.insert(
#                         tt.END,
#                         f'{p["id"]}-{p["first_name"]} {p["middle_name"]} {p["last_name"]} | Age:{p["age"]} | created_by:{p["created_by"]}'
#                     )
#             else:
#                 messagebox.showinfo("Not Found", f"No '{name}' match found")

#         elif filter_value == "Id":
#             ok, patient = search_patient_by_id(name)
#             if ok and patient:
#                 # Wrap single dict in a list to unify the logic
#                 patients = [patient]
#                 for p in patients:
#                     patient_list.insert(
#                         tt.END,
#                         f'{p["id"]}-{p["first_name"]} {p["middle_name"]} {p["last_name"]} | Age:{p["age"]} | created_by:{p["created_by"]}'
#                     )
#             else:
#                 messagebox.showinfo("Not Found", f"No '{name}' match found")


        
#     window = tt.Tk()
#     window.title("search patients")
    
#     tt.Label(window, text="select search by").pack(pady=5)
    
#     filter = Combobox(window,values=("Name", "Id"),)
#     filter.pack()
#     filter.set("Name")
    
#     entry = tt.Entry(window, width=20)
#     entry.pack(pady=5)
    
#     search_btn = tt.Button(window, text="search", command=search_patient)
#     search_btn.pack(pady=5)
    
#     patient_list = tt.Listbox(window, width=50)
#     patient_list.pack(pady=10)
    
    
#     window.mainloop()
    
# if __name__ == "__main__":
#     search_patient_gui()