import os
import csv
import tempfile
from models.database import connect_db
from tkinter import messagebox
from tkinter import filedialog

def extract_file(area, name, last_name, age):
    content = area.get("1.0", "end-1c")
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt")],
        title="Save History As..."
    )
    if not file_path:
        return
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(f"Name: {name} {last_name} | Age: {age}  Medical History\n\n{content}")
    messagebox.showinfo("successfull", f"You are successfully extract the file\n{file_path}")


def printer(area, name, last_name, age):
    content = area.get("1.0", "end-1c")
    with tempfile.NamedTemporaryFile(delete=False, suffix='.txt', mode='w', encoding='utf-8') as tmpfile:
        tmpfile.write(f"HEALTH FOR ALL CLINIC                      healthforall@gmail.com | +251955936438\n\nName: {name} {last_name} | Age:{age}  Medical History\n\n{content}" )
        tmpfile_path = tmpfile.name
    os.startfile(tmpfile_path, "print")

def get_backup_folder():
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    backup_folder = os.path.join(desktop, "Backup")
    if not os.path.exists(backup_folder):
        os.makedirs(backup_folder)
    return backup_folder

def backup_patients_data():
    backup_folder = get_backup_folder()
    filename = os.path.join(backup_folder, "backup_patients.csv")

    # Delete old backup if it exists
    if os.path.exists(filename):
        os.remove(filename)

    # Fetch data from DB
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM patients")
    data = cur.fetchall()
    conn.close()

    # Write to CSV
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([
            "id", "created_at", "first_name", "middle_name", "last_name", "age", "gender",
            "city", "sub_city", "wereda", "house_number", "phone", "created_by", "diagnosis"
        ])
        writer.writerows(data)
        messagebox.showinfo("success", f"you are successfully backeup patient datas to:\n{os.path.abspath(filename)}")

def backup_history_data():
    backup_folder = get_backup_folder()
    filename = os.path.join(backup_folder, "backup_history.csv")

    # Delete old backup if exists
    if os.path.exists(filename):
        os.remove(filename)

    # Fetch data
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM history")
    data = cur.fetchall()
    conn.close()

    # Write to CSV
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([
            "id", "patient_id", "created_at", "diagnosis", "detail_history", "note", "doctor_name"
        ])
        writer.writerows(data)
        messagebox.showinfo("success", f"you are successfully backeup patient's history to:\n{os.path.abspath(filename)}")
        
def backup_users_data():
    backup_folder = get_backup_folder()
    filename = os.path.join(backup_folder, "backup_users.csv")

    # Delete old backup if exists
    if os.path.exists(filename):
        os.remove(filename)

    # Fetch data
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")
    data = cur.fetchall()
    conn.close()

    # Write to CSV
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([
            "id", "first_name", "last_name", "phone", "email",
            "password_hash", "created_at", "last_login", "is_active"
        ])
        writer.writerows(data)
        messagebox.showinfo("success", f"you are successfully signedup users data to:\n{os.path.abspath(filename)}")