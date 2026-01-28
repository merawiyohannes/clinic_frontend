import requests
from .ip_detector import get_local_ip

IP = get_local_ip()
BASE_URL = f"http://{IP}:5000"

# user realted api calls

def login(email, password):
    r = requests.post(
        f"{BASE_URL}/login",
        json={
            "email": email,
            "password": password
        }
    )

    if r.status_code == 200:
        return True, r.json()

    return False, r.text


def signup(fn, ln, phone, email, password):
    url = f"{BASE_URL}/register"

    payload = {
        "first_name": fn,
        "last_name": ln,
        "phone": phone,
        "email": email,
        "password": password
    }

    try:
        r = requests.post(url, json=payload, timeout=10)

        # IMPORTANT: check status BEFORE json
        if r.status_code == 200:
            return True, "Registered successfully"

        return False, r.text

    except Exception as e:
        raise Exception(f"Cannot connect to server: {e}")



def change_password(user_id, old_password, new_password):
    url = f"{BASE_URL}/change-password"
    payload = {
        "user_id": user_id,
        "password": old_password,
        "new_password": new_password
    }
    try:
        r = requests.post(url, json=payload, timeout=10)
        data = r.json()

        if r.status_code == 200:
            return data.get("success", False), data

        return False, r.text

    except Exception as e:
        raise Exception(f"Cannot change password: {e}")


#  patient realted api calls

def create_patient(formatted_date, fname, mname, lname, age, gender,
                   city, subcity, wereda, house_number, phone, created_by, diagnosis):

    url = f"{BASE_URL}/patients"

    payload = {
        "created_at": formatted_date,
        "first_name": fname,
        "middle_name": mname,
        "last_name": lname,
        "age": age,
        "gender": gender,
        "city": city,
        "sub_city": subcity,
        "wereda": wereda,
        "house_number": house_number,
        "phone": phone,
        "created_by": created_by,
        "diagnosis": diagnosis
    }

    try:
        r = requests.post(url, json=payload, timeout=10)

        if r.status_code == 200:
            return True, r.json()

        return False, r.text

    except Exception as e:
        raise Exception(f"Cannot connect to server: {e}")

            

def delete_patient(id):
    url = f"{BASE_URL}/patients/{id}"

    try:
        r = requests.delete(url, timeout=10)

        if r.status_code == 200:
            return True, r.json()

        return False, r.text

    except Exception as e:
        raise Exception(f"Cannot delete patient: {e}")

    
    
def update_patient(id, formatted_date, fname, mname, lname, age, gender,
                   city, subcity, wereda, house_number, phone, created_by, diagnosis):

    url = f"{BASE_URL}/patients/{id}"

    payload = {
        "created_at": formatted_date,
        "first_name": fname,
        "middle_name": mname,
        "last_name": lname,
        "age": age,
        "gender": gender,
        "city": city,
        "sub_city": subcity,
        "wereda": wereda,
        "house_number": house_number,
        "phone": phone,
        "created_by": created_by,
        "diagnosis": diagnosis
    }

    try:
        r = requests.put(url, json=payload, timeout=10)

        if r.status_code == 200:
            return True, r.json()

        return False, r.text

    except Exception as e:
        raise Exception(f"Cannot update patient: {e}")


def search_by_name(name):
    url = f"{BASE_URL}/patients/search"
    r = requests.get(url, params={"name": name}, timeout=10)

    if r.status_code == 200:
        return True, r.json()

    return False, r.text


def search_patient_by_id(pid):
    url = f"{BASE_URL}/patients/{pid}"
    r = requests.get(url, timeout=10)

    if r.status_code == 200:
        return True, r.json()

    return False, r.text


def list_all_patients():
    url = f"{BASE_URL}/patients"
    r = requests.get(url, timeout=10)

    if r.status_code == 200:
        return True, r.json()

    return False, r.text


def diagnosis_filler():
    url = f"{BASE_URL}/patients/diagnosis-filler"
    r = requests.get(url, timeout=10)

    if r.status_code == 200:
        return True

    return False

def backup_patients():
    r = requests.get(f"{BASE_URL}/backup/patients", timeout=20)

    if r.status_code == 200:
        return True, r.text

    return False, r.text


def backup_history():
    r = requests.get(f"{BASE_URL}/backup/history", timeout=20)

    if r.status_code == 200:
        return True, r.text

    return False, r.text


def backup_users():
    r = requests.get(f"{BASE_URL}/backup/users", timeout=20)

    if r.status_code == 200:
        return True, r.text

    return False, r.text

# ================= HISTORY =================

def get_patient_history(patient_id):
    r = requests.get(f"{BASE_URL}/history/{patient_id}", timeout=10)

    if r.status_code == 200:
        return True, r.json()

    return False, r.text


def search_history_by_date(patient_id, date):
    # reuse same endpoint then filter locally (simplest)
    ok, histories = get_patient_history(patient_id)

    if not ok:
        return False, histories

    filtered = [h for h in histories if h["created_at"] == date]
    return True, filtered

# ================= HISTORY =================

def add_history(patient_id, created_at, diagnosis, detail_history, note, doctor_name):
    url = f"{BASE_URL}/history"

    payload = {
        "patient_id": patient_id,
        "created_at": created_at,
        "diagnosis": diagnosis,
        "detail_history": detail_history,
        "note": note,
        "doctor_name": doctor_name
    }

    try:
        r = requests.post(url, json=payload, timeout=10)

        if r.status_code == 200:
            return True, r.json()

        return False, r.text

    except Exception as e:
        raise Exception(f"Cannot connect to server: {e}")


