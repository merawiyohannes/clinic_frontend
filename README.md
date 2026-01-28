# Health Clinic Management - Frontend (Tkinter)

This is the **Tkinter-based frontend** for the Health Clinic Management system.  
It works with a **Flask backend API** for patient, user, history, and backup management.

---

## Features

- **User Management**
  - Register new users
  - Login with email/password
  - Change password

- **Patient Management**
  - Add, edit, delete patients
  - View patients in a Treeview
  - Search patients by Name or ID
  - Diagnosis auto-filled from last history

- **History Management**
  - Add new patient history
  - Filter history by date or view all
  - Print or extract patient history

- **Backup Utilities**
  - Backup Patients, History, and Users (via Flask API)
  - Helper functions for printing and extracting files

---

## Requirements

- Python 
- `requests` module  

Install dependencies:

```bash
pip install requests

Project Structure

frontend/
│
├── api.py                 # API calls to Flask backend
├── dashboard_gui.py       # Main dashboard UI
├── patient_tool_gui.py    # Patient CRUD forms
├── history_gui.py         # Patient history forms and display
├── tree_gui.py            # Treeview creation and handling
├── backups.py             # Backup and helper functions
├── search_gui.py          # (Deprecated - optional)
└── main.py                # Entry point to launch the GUI

Running the Frontend

1 Ensure Flask backend is running

The frontend uses BASE_URL in api.py to connect to the backend.

2 Start the frontend

python test.py

3 Login or Register to access the main dashboard.

4 Use the buttons and Treeview to manage patients, history, and backups.

Notes

All patient and history data is stored in the backend database.

backups.py contains helper functions like printer and extract_file that do not require the backend.

date_checker ensures dates are in the correct format.

The GUI uses Treeview to display patients and aligns all columns properly.

Author

Merawi – Full-stack developer, building a practical health clinic system with Python Tkinter & Flask.
