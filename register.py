import tkinter as tk
from tkinter import messagebox
import pyodbc
from md5_utils import md5

conn = pyodbc.connect(
    'DRIVER={SQL Server};'
    'SERVER=.\SQLEXPRESS;'
    'DATABASE=Register_data;'
    'Trusted_connection=yes;'
)

def register(username, password):
    hashed_password = md5(password)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM Users WHERE Username = ?", (username,))
    row = cursor.fetchone()
    if not (username and password):
        messagebox.showerror("Error", "Please enter both username and password.")
    elif row[0] == 0 :
        cursor.execute("INSERT INTO Users(Username, PasswordHash) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        messagebox.showinfo("Success", "Registration is successful.")
    else:
        messagebox.showerror("Error", "The username is already taken.")

def login(username, password):
    cursor = conn.cursor()
    cursor.execute("SELECT PasswordHash FROM Users WHERE Username = ?", (username,))
    row = cursor.fetchone()
    if not (username and password):
        messagebox.showerror("Error", "Please enter both username and password.")
    elif row:
        hashed_password = row.PasswordHash
        if md5(password) == hashed_password:
            messagebox.showinfo("Success", "Login succeeded.")
        else:
            messagebox.showerror("Error", "Incorrect password.")
    else:
        messagebox.showerror("Error", "User not found.")

root = tk.Tk()
root.title("Login System")
root.geometry("1000x7500")

# Background Image
bg_image = tk.PhotoImage(file="Python_GUI_Login.png")
bg_label = tk.Label(root, image=bg_image)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)



# Styling
root.configure(bg="#f0f0f0")
root.attributes('-alpha', 0.95)

# Create a frame for the content with rounded corners and subtle shadow
content_frame = tk.Frame(root, bg="#ffffff", bd=2, relief=tk.SOLID)
content_frame.place(relx=0.5, rely=0.5, anchor="center")

# Username Label and Entry
username_label = tk.Label(content_frame, text="Username:", bg="#ffffff", fg="#333333", font=("Helvetica", 12))
username_label.grid(row=0, column=0, padx=10, pady=(20, 5), sticky="w")
username_entry = tk.Entry(content_frame, font=("Helvetica", 12))
username_entry.grid(row=0, column=1, padx=10, pady=(20, 5), sticky="we")

# Password Label and Entry
password_label = tk.Label(content_frame, text="Password:", bg="#ffffff", fg="#333333", font=("Helvetica", 12))
password_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
password_entry = tk.Entry(content_frame, show="*", font=("Helvetica", 12))
password_entry.grid(row=1, column=1, padx=10, pady=5, sticky="we")

# Login Button with hover effect
def on_login_enter(e):
    login_button['background'] = '#45a049'

def on_login_leave(e):
    login_button['background'] = '#4CAF50'

login_button = tk.Button(content_frame, text="Login", command=lambda: login(username_entry.get(), password_entry.get()), bg="#4CAF50", fg="white", font=("Helvetica", 12))
login_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="we")
login_button.bind("<Enter>", on_login_enter)
login_button.bind("<Leave>", on_login_leave)

# Register Button with hover effect
def on_register_enter(e):
    register_button['background'] = '#1e90ff'

def on_register_leave(e):
    register_button['background'] = '#2196F3'

register_button = tk.Button(content_frame, text="Register", command=lambda: register(username_entry.get(), password_entry.get()), bg="#2196F3", fg="white", font=("Helvetica", 12))
register_button.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="we")
register_button.bind("<Enter>", on_register_enter)
register_button.bind("<Leave>", on_register_leave)

root.mainloop()
conn.close()
