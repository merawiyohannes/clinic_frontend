import sqlite3
import os
import hashlib
from tkinter import messagebox

def connect_db():
    app_dir = os.path.join(os.getenv('LOCALAPPDATA'), 'ClinicApp')
    os.makedirs(app_dir, exist_ok=True)  # Create folder if it doesn’t exist
    db_path = os.path.join(app_dir, "clinic.db")
    return sqlite3.connect(db_path)

def date_checker(date):
    """
    Validates Ethiopian-style date input (yyyy-mm-dd)
    - Must be numeric
    - Year 4 digits
    - Month 1-13
    - Day 1-30
    Returns date as-is if valid, otherwise shows error and returns None
    """
    try:
        parts = date.split("-")
        if len(parts) != 3:
            raise ValueError("Format must be yyyy-mm-dd, e.g., 2017-05-04")
        
        year, month, day = parts
        if not (year.isdigit() and month.isdigit() and day.isdigit()):
            raise ValueError("Only numbers allowed in date")
        
        if len(year) != 4:
            raise ValueError("Year must be 4 digits")
        
        month = int(month)
        day = int(day)

        if not (1 <= month <= 13):
            raise ValueError("Month must be between 1 and 13")
        if not (1 <= day <= 30):
            raise ValueError("Day must be between 1 and 30")
        
        return f"{year}-{str(month).zfill(2)}-{str(day).zfill(2)}"

    except ValueError as e:
        messagebox.showerror("Invalid date", str(e))
        return None



def password_hasher(password):
    password = hashlib.sha256(password.encode()).hexdigest()
    return password
    
    
def create_patient_table():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
                CREATE TABLE IF NOT EXISTS patients(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    created_at TEXT,
                    first_name TEXT,
                    middle_name TEXT,
                    last_name TEXT,
                    age INTEGER,
                    gender TEXT,
                    city TEXT,
                    sub_city TEXT,
                    wereda TEXT,
                    house_number TEXT,
                    phone TEXT,
                    created_by TEXT,
                    diagnosis TEXT  
                )
                """)
    conn.commit()
    conn.close()

    
def insert_patient(created_at, first_name, middle_name, last_name, age, gender, city, sub_city, wereda, house_number, phone, created_by, diagnosis):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
                INSERT INTO patients(created_at, first_name, middle_name, last_name, age, gender, city, sub_city, wereda, house_number, phone, created_by, diagnosis)
                VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)
                """,(created_at, first_name, middle_name, last_name, age, gender, city, sub_city, wereda, house_number, phone, created_by, diagnosis))
    conn.commit()
    conn.close()
    
def list_all_patients():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM patients ORDER BY created_at DESC")
    patients = cur.fetchall()
    conn.close()
    return patients

