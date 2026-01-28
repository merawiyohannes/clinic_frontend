from models.database import connect_db, password_hasher

def search_patient_by_id(patient_id):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM patients WHERE id=?",(patient_id,))
    patient = cur.fetchone()
    conn.close()
    return patient


def search_by_name(name):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
                SELECT * FROM patients 
                WHERE first_name LIKE ? OR middle_name LIKE ? OR last_name LIKE ?
                """, (f'%{name}%', f'%{name}%', f'%{name}%'))
    results = cur.fetchall()
    conn.close()
    return results