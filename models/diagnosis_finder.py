from models.database import list_all_patients
from models.patient_history import select_patient_history
from models.database import connect_db

def diagnosis_filler():
    patients_last_history = []
    conn = connect_db()
    cur = conn.cursor()
    for patient in list_all_patients():
        try:
            patients_last_history.append(select_patient_history(patient[0])[0])  
        except IndexError:
            continue  
    for last_history in patients_last_history: 
        cur.execute("UPDATE patients SET diagnosis=? WHERE id=?",(last_history[3],last_history[1]))
        conn.commit()
    conn.close()
