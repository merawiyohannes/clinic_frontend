from models.database import connect_db
from models.database import date_checker



def search_history_by_date(date):
    if date_checker(date):
        new_date = date_checker(date)
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM history WHERE created_at=?", (new_date,))
        history = cur.fetchall()
        conn.close()
        return history

def patient_history_table():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
                CREATE TABLE IF NOT EXISTS history(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    patient_id INTEGER,
                    created_at TEXT,
                    diagnosis TEXT,
                    detail_history TEXT,
                    note TEXT,
                    doctor_name TEXT,
                    FOREIGN KEY(patient_id) REFERENCES patients(id)
                )
                """)
    conn.commit()
    conn.close()
    
def select_patient_history(id):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM history WHERE patient_id=? ORDER BY created_at DESC', (id,))
    patient_histories = cur.fetchall()
    conn.close()
    return patient_histories

def insert_history(patient_id, created_at, diagnosis, detail_history, note, doctor_name):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
                INSERT INTO history(patient_id,  created_at, diagnosis, detail_history, note, doctor_name)
                VALUES(?,?,?,?,?,?)
                """,(patient_id, created_at, diagnosis, detail_history, note, doctor_name))
    conn.commit()
    conn.close()
    