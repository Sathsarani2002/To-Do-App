import tkinter as tk
from tkinter import messagebox
import os
import json
import re

# ---------------- Global ----------------
tasks = []
current_user = ""

BG_COLOR = "#f0f4ff"
CARD_COLOR = "#ffffff"
PRIMARY = "#4a6cff"
SUCCESS = "#2ecc71"
DANGER = "#e74c3c"
TEXT = "#2c3e50"

# ---------------- Validation Helpers ----------------
def is_valid_username(name):
    return bool(re.match("^[A-Za-z0-9]{3,}$", name))

def is_valid_task_name(name):
    return len(name.strip()) >= 3

def is_valid_date(date):
    return bool(re.match(r"^\d{4}-\d{2}-\d{2}$", date))

def is_valid_category(category):
    return bool(re.match("^[A-Za-z ]+$", category))

# ---------------- File Handling (JSON) ----------------
def user_file():
    return f"{current_user}_tasks.json"

def load_tasks():
    tasks.clear()
    if os.path.exists(user_file()):
        with open(user_file(), "r") as f:
            data = json.load(f)
            for task in data:
                tasks.append([
                    task["name"],
                    task["priority"],
                    task["due_date"],
                    task["category"],
                    task["status"]
                ])

def save_tasks():
    data = []
    for t in tasks:
        data.append({
            "name": t[0],
            "priority": t[1],
            "due_date": t[2],
            "category": t[3],
            "status": t[4]
        })
    with open(user_file(), "w") as f:
        json.dump(data, f, indent=4)

# ---------------- Login ----------------
def login():
    global current_user
    name = username_entry.get().strip()

    if not name:
        messagebox.showerror("Login Error", "Username is required")
        return

    if not is_valid_username(name):
        messagebox.showerror(
            "Login Error",
            "Username must be at least 3 characters\nOnly letters and numbers allowed"
        )
        return

    current_user = name
    welcome_label.config(text=f"Welcome, {current_user} 👋")
    load_tasks()
    login_frame.pack_forget()
    main_frame.pack(fill="both", expand=True)
    refresh_tasks()

# ---------------- Task Functions ----------------
def add_task():
    name = task_name.get().strip()
    date = due_date.get().strip()
    category = category_entry.get().strip()

    if not name or not date or not category:
        messagebox.showwarning("Input Error", "All fields are required")
        return

    if not is_valid_task_name(name):
        messagebox.showerror("Error", "Task name must be at least 3 characters")
        return

    if not is_valid_date(date):
        messagebox.showerror("Error", "Invalid date format\nUse YYYY-MM-DD")
        return

    if not is_valid_category(category):
        messagebox.showerror("Error", "Category should contain only letters")
        return

    tasks.append([
        name,
        priority_var.get(),
        date,
        category,
        "Pending"
    ])

    save_tasks()
    refresh_tasks()
    clear_inputs()

def update_task():
    selected = task_list.curselection()
    if not selected:
        messagebox.showerror("Update Error", "Select a task to update")
        return

    name = task_name.get().strip()
    date = due_date.get().strip()
    category = category_entry.get().strip()

    if not name or not date or not category:
        messagebox.showerror("Error", "All fields are required")
        return

    if not is_valid_date(date):
        messagebox.showerror("Error", "Use date format YYYY-MM-DD")
        return

    index = selected[0]
    tasks[index] = [
        name,
        priority_var.get(),
        date,
        category,
        tasks[index][4]
    ]

    save_tasks()
    refresh_tasks()
    clear_inputs()
    messagebox.showinfo("Success", "Task updated successfully")

def delete_task():
    if not task_list.curselection():
        messagebox.showerror("Error", "Select a task to delete")
        return

    tasks.pop(task_list.curselection()[0])
    save_tasks()
    refresh_tasks()
    clear_inputs()

def mark_done():
    if not task_list.curselection():
        messagebox.showerror("Error", "Select a task")
        return

    tasks[task_list.curselection()[0]][4] = "Completed"
    save_tasks()
    refresh_tasks()

def fill_inputs(event):
    if task_list.curselection():
        t = tasks[task_list.curselection()[0]]
        task_name.delete(0, tk.END)
        task_name.insert(0, t[0])
        priority_var.set(t[1])
        due_date.delete(0, tk.END)
        due_date.insert(0, t[2])
        category_entry.delete(0, tk.END)
        category_entry.insert(0, t[3])

# ---------------- Helpers ----------------
def refresh_tasks():
    task_list.delete(0, tk.END)

    for t in tasks:
        icon = "✅" if t[4] == "Completed" else "⏳"
        text = f"{icon}  {t[0]} | {t[1]} | {t[3]} | Due: {t[2]}"
        task_list.insert(tk.END, text)

    for i, t in enumerate(tasks):
        task_list.itemconfig(i, fg=SUCCESS if t[4] == "Completed" else TEXT)

def clear_inputs():
    task_name.delete(0, tk.END)
    due_date.delete(0, tk.END)
    category_entry.delete(0, tk.END)
    priority_var.set("Low")

# ---------------- GUI ----------------
root = tk.Tk()
root.title("To-Do List Management System")
root.geometry("850x600")
root.configure(bg=BG_COLOR)

# ---------------- Login Frame ----------------
login_frame = tk.Frame(root, bg=BG_COLOR)
login_frame.pack(pady=130)

tk.Label(login_frame, text="📝 To-Do List App",
         font=("Arial", 24, "bold"),
         bg=BG_COLOR, fg=PRIMARY).pack(pady=10)

tk.Label(login_frame, text="Enter Username",
         bg=BG_COLOR, fg=TEXT).pack()

username_entry = tk.Entry(login_frame, width=30)
username_entry.pack(pady=5)

tk.Button(login_frame, text="Login",
          width=18, bg=PRIMARY,
          fg="white", command=login).pack(pady=15)

# ---------------- Main Frame ----------------
main_frame = tk.Frame(root, bg=BG_COLOR)

welcome_label = tk.Label(main_frame, text="",
                         font=("Arial", 18, "bold"),
                         bg=BG_COLOR, fg=TEXT)
welcome_label.pack(pady=10)

# ---------------- Task Form ----------------
form = tk.LabelFrame(main_frame, text="Task Details",
                     bg=CARD_COLOR, fg=PRIMARY,
                     padx=15, pady=15)
form.pack(padx=25, pady=10, fill="x")

tk.Label(form, text="Task Name", bg=CARD_COLOR).grid(row=0, column=0, sticky="w")
task_name = tk.Entry(form, width=40)
task_name.grid(row=0, column=1, pady=5)

tk.Label(form, text="Priority", bg=CARD_COLOR).grid(row=1, column=0, sticky="w")
priority_var = tk.StringVar(value="Low")
tk.OptionMenu(form, priority_var, "High", "Low").grid(row=1, column=1, sticky="w")

tk.Label(form, text="Due Date", bg=CARD_COLOR).grid(row=2, column=0, sticky="w")
due_date = tk.Entry(form, width=40)
due_date.grid(row=2, column=1, pady=5)
tk.Label(form, text="YYYY-MM-DD", fg="gray", bg=CARD_COLOR).grid(row=2, column=2)

tk.Label(form, text="Category", bg=CARD_COLOR).grid(row=3, column=0, sticky="w")
category_entry = tk.Entry(form, width=40)
category_entry.grid(row=3, column=1, pady=5)

# ---------------- Buttons ----------------
btn_frame = tk.Frame(main_frame, bg=BG_COLOR)
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Add", bg=PRIMARY, fg="white",
          width=14, command=add_task).grid(row=0, column=0, padx=5)

tk.Button(btn_frame, text="Update", bg=SUCCESS, fg="white",
          width=14, command=update_task).grid(row=0, column=1, padx=5)

tk.Button(btn_frame, text="Delete", bg=DANGER, fg="white",
          width=14, command=delete_task).grid(row=0, column=2, padx=5)

tk.Button(btn_frame, text="Completed", bg="#8e44ad", fg="white",
          width=14, command=mark_done).grid(row=0, column=3, padx=5)

# ---------------- Task List ----------------
list_frame = tk.LabelFrame(main_frame, text="Your Tasks",
                           bg=CARD_COLOR, fg=PRIMARY,
                           padx=10, pady=10)
list_frame.pack(padx=25, pady=10, fill="both", expand=True)

scrollbar = tk.Scrollbar(list_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

task_list = tk.Listbox(list_frame,
                       font=("Segoe UI", 11),
                       yscrollcommand=scrollbar.set,
                       selectbackground=PRIMARY,
                       selectforeground="white",
                       activestyle="none")
task_list.pack(fill="both", expand=True)

scrollbar.config(command=task_list.yview)
task_list.bind("<<ListboxSelect>>", fill_inputs)

root.mainloop()
