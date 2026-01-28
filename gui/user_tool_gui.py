import tkinter as tt
from tkinter import messagebox
from gui import main_gui, user_tool_gui
import re
from .api import login, signup, change_password


def edit_password():
    def clear():
        username_entry.delete(0, tt.END)
        old_password_entry.delete(0, tt.END)
        new_password_entry.delete(0, tt.END)
        confirm_new_password_entry.delete(0, tt.END)

        
    def change():
        un = username_entry.get()
        op = old_password_entry.get()
        np = new_password_entry.get()
        cnp = confirm_new_password_entry.get()

        if not all([un, op, np, cnp]):
            messagebox.showerror("Error", "All the fields must be filled")
            return

        if np != cnp:
            messagebox.showerror("New password", "Your new password and confirm new password must be identical")
            return

        # Login via API
        ok, user = login(un, op)  # `login` is your api.py function

        if not ok:
            messagebox.showerror("Error", "Check your username/email and password")
            return

        # Change password via API
        success, _ = change_password(user["id"], op, np)  # add this API wrapper in api.py

        if success:
            messagebox.showinfo("Success", f"{user['first_name']} {user['last_name']} successfully changed your password")
            clear()
            frame.destroy()
            user_tool_gui.login_user("Enter")
        else:
            messagebox.showerror("Error", "Failed to change password")

        
    
    frame = tt.Tk()
    frame.title("change password")
    frame.geometry("400x300") 
    frame.resizable(False, False)
    frame.configure(bg="#f0f0f0")
    
    tt.Label(frame, text="Change your password", font=("arial", 10, "bold")).pack(fill="both", pady=17)
    
    form_frame = tt.Frame(frame)
    form_frame.place(relx=0.5, rely=0.5, anchor="center")
     
    labels = ["username", "old_password", "new_password", "confirm_new_password"]
    for i, label in enumerate(labels):
        tt.Label(form_frame, text=label).grid(row=i, column=0, padx=5, pady=5)
        
    username_entry = tt.Entry(form_frame)
    old_password_entry = tt.Entry(form_frame, show="*")
    new_password_entry = tt.Entry(form_frame, show="*")
    confirm_new_password_entry = tt.Entry(form_frame, show="*")
    
    username_entry.grid(row=0, column=1)
    old_password_entry.grid(row=1, column=1)
    new_password_entry.grid(row=2, column=1)
    confirm_new_password_entry.grid(row=3, column=1)
    
    
    change_btn = tt.Button(form_frame, text="change-password", command=change, bg="#4CAF50", fg="white")
    change_btn.grid(row=4, column=0, columnspan=2, padx=4, pady=4)
    
        
    frame.mainloop()
    
    if __name__ == "__main__":
        edit_password()
        
        
def login_user(event):
    def check_auth():
        email = user_name_entry.get()
        psw = psw_entry.get()

        try:
            ok, data = login(email, psw)

            if ok:
                frame.destroy()
                main_gui.open_dashboard(email)
            else:
                messagebox.showerror("Invalid", "use correct username and password")

        except Exception as e:
            messagebox.showerror("Error", f"something went wrong\n{e}")
            
    frame = tt.Tk()
    frame.title("Clinic App Login")
    frame.geometry("400x300")  # Smaller fixed size
    frame.resizable(False, False)
    frame.configure(bg="#f0f0f0")  # Light gray background

    # ===== Centered Frame =====
    login_frame = tt.Frame(frame, )
    login_frame.place(relx=0.5, rely=0.5, anchor="center")  # Perfect center

    # ===== UI Elements =====
    # Title
    tt.Label(
        login_frame, 
        text="Login", 
        font=("Arial", 14, "bold")
    ).grid(row=0, column=0, columnspan=2, pady=10)

    # Username
    tt.Label(login_frame, text="Username:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
    user_name_entry = tt.Entry(login_frame, width=25)
    user_name_entry.grid(row=1, column=1, sticky="w", pady=5)

    # Password
    tt.Label(login_frame, text="Password:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
    psw_entry = tt.Entry(login_frame, show="•", width=25)  # • is prettier than *
    psw_entry.grid(row=2, column=1, sticky="w", pady=5)

    # Login Button
    login_btn = tt.Button(
        login_frame, 
        text="Login", 
        command=check_auth, 
        width=15
    )
    login_btn.grid(row=3, column=0, columnspan=2, pady=15)

    # Signup Link (optional)
    signup_lbl = tt.Label(
        login_frame, 
        text="No account? Sign up", 
        foreground="blue", 
        cursor="hand2"
    )
    signup_lbl.grid(row=4, column=0, columnspan=2)
    signup_lbl.bind("<Button-1>", lambda event:( frame.destroy(), user_registration(event) ))  # Add your signup function

    # ===== Run Application =====
    frame.mainloop()

        

def user_registration(event):

    def clear():
        fn_entry.delete(0, tt.END)
        ln_entry.delete(0, tt.END)
        phone_entry.delete(0, tt.END)
        email_entry.delete(0, tt.END)
        psw_entry.delete(0, tt.END)
        confirm_psw_entry.delete(0, tt.END)
        register.config(state="disabled")
        
    def check_data():
        fn = fn_entry.get()
        ln = ln_entry.get()
        phone = phone_entry.get()
        email = email_entry.get()
        p1 = psw_entry.get()
        p2 = confirm_psw_entry.get()
        
        if not all([fn, ln, phone, email, p1, p2]):
            messagebox.showerror("Empty ", "Please fil all the data")
            return False
        if p1 != p2:
            messagebox.showerror("password", "the two passwords must be identical")
            return False
        if not phone.isdigit() or len(phone) != 10:
            messagebox.showerror("Phone", "Phone must be at least 9 digits and numeric only start with 09")
            return False
        email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(email_pattern, email):
            messagebox.showerror("Email", "Please enter a valid email address")
            return False
    
        check_button.config(state="disabled")
        register.config(state="active")
        messagebox.showinfo("The datas are filled", "All datas are filled correctly. click register to finish")
        
    
    def register_user():
        fn = fn_entry.get()
        ln = ln_entry.get()
        phone = phone_entry.get()
        email = email_entry.get()
        p1 = psw_entry.get()

        if not all([fn, ln, phone, email, p1]):
            messagebox.showerror("Error", "Please fill all fields")
            return

        try:
            ok, msg = signup(fn, ln, phone, email, p1)

            if ok:
                clear()
                messagebox.showinfo("Success", f"Welcome {fn} {ln}! You are successfully registered")
                window.destroy()
                login_user("Enter")

            else:
                messagebox.showerror("Error", msg)

        except Exception as e:
            messagebox.showerror("Error", f"Something went wrong\n{e}")
            
    
    window = tt.Tk()
    window.title("user-registrstion")
    window.geometry("400x400")
    window.resizable(False,False)
    window.configure(bg="#f0f0f0")
    
    tt.Label(window, text="User Registration Form", font=("arial", 14, "bold"), padx=10, pady=20).pack(anchor='center')
    
    frame = tt.Frame(window)
    frame.place(relx=0.5, rely=0.5, anchor='center')
    
    labels = ["first_name", "last_name", "phone", "email", "password", "confirm-password"]
    for i, label in enumerate(labels):
        tt.Label(frame, text=label).grid(row=i, column=0, padx=5, pady=5, sticky="e")
    
    fn_entry = tt.Entry(frame)
    ln_entry = tt.Entry(frame)
    phone_entry = tt.Entry(frame)
    email_entry = tt.Entry(frame)
    psw_entry = tt.Entry(frame, show="•")
    confirm_psw_entry = tt.Entry(frame, show="•")
    
    fn_entry.grid(row=0, column=1)
    ln_entry.grid(row=1, column=1)
    phone_entry.grid(row=2, column=1)
    email_entry.grid(row=3, column=1)
    psw_entry.grid(row=4, column=1)
    confirm_psw_entry.grid(row=5, column=1)
    
    check_button = tt.Button(frame, text="check-data", command=check_data, width=15)
    check_button.config(bg="yellow")
    check_button.grid(row=6, column=0, columnspan=2, pady=15)
    
    register = tt.Button(frame, text="Register", state="disabled" ,command=register_user, width=15, fg="white")
    register.grid(row=7, column=0, columnspan=2, pady=5)
    
    login_label = tt.Label(frame, text="Have an account? Login here", fg="blue", cursor="hand2")
    login_label.grid(row=9, column=0, columnspan=2)
    login_label.bind("<Button-1>", lambda event:(window.destroy(), login_user(event)))
    
    
    window.mainloop()
    
    if __name__ == "__main__":
        user_registration()