import tkinter as tk
from .api import get_patient_history, search_history_by_date

def history_loader_to_front(area, id, date, diagnosis, detail_history, note, doc_name):
    area.config(state="normal")
    area.insert("1.0", "──────────────────────────────────────\n", "divider")
    area.insert("1.0", f"Notes     : {note}\n", "body")
    area.insert("1.0", f"History   : {detail_history}\n", "body")
    area.insert("1.0", f"Diagnosis : {diagnosis}\n\n", "label")
    area.insert("1.0", f"Doctor    : {doc_name}\n", "label")
    area.insert("1.0", f"Date      : {date}\n", "label")
    area.insert("1.0", "──────────────────────────────────────\n", "divider")

    area.tag_config("label", font=("Arial", 10, "bold"), foreground="blue")
    area.tag_config("body", foreground="black")
    area.tag_config("divider", foreground="#C71585")
    area.see("1.0")
    area.config(state="disabled")
   
def history_fecher(id, area):
    ok, patient_histories = get_patient_history(id)

    if not ok or not patient_histories:
        return False
    for history in patient_histories:
        history_loader_to_front(
            area,
            id,
            history["created_at"],
            history["diagnosis"],
            history["detail_history"],
            history.get("note"),
            history["doctor_name"]
        )
    return True

def print_history(area, id, date, entry, filter):
    filter_choose = filter.get().strip()
    area.config(state="normal")

    if filter_choose == "All histories":
        ok, all_histories = get_patient_history(id)

        if not ok or not all_histories:
            return False

        area.delete("1.0", tk.END)

        for history in all_histories:
            history_loader_to_front(
                area,
                id,
                history["created_at"],
                history["diagnosis"],
                history["detail_history"],
                history.get("note"),
                history["doctor_name"]
            )

    if filter_choose == "Date":
        ok, histories = search_history_by_date(id, date)
        area.delete("1.0", tk.END)

        if not ok or not histories:
            area.insert("1.0", f"No history at date:{date}")
            area.tag_add("new", "1.0", "2.0")
            area.tag_config("new", foreground="red", font=("arial", 14, "bold"))
            return

        for history in histories:
            history_loader_to_front(
                area,
                id,
                history["created_at"],
                history["diagnosis"],
                history["detail_history"],
                history.get("note"),
                history["doctor_name"]
            )

    entry.delete(0, tk.END)
    area.config(state="disabled")


    
    
        