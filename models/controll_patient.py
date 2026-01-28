from models.database import connect_db, password_hasher, create_patient_table

def delete_patient(patient_id):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM patients WHERE id=?", (patient_id,))
    conn.commit()
    conn.close()
    

def update_patient_data(patient_id, created_at, first_name, middle_name, last_name, age, gender, city, sub_city, wereda, house_number, phone, created_by, diagnosis):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
                UPDATE patients SET created_at=?, first_name=?, middle_name=?, last_name=?, age=?, gender=?, city=?, sub_city=?, wereda=?, house_number=?, phone=?, created_by=?, diagnosis=? WHERE id=? 
                """,
                (created_at, first_name, middle_name, last_name, age, gender, city, sub_city, wereda, house_number, phone, created_by, diagnosis, patient_id)
                )
    conn.commit()
    conn.close()