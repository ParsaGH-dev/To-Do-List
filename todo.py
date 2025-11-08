import tkinter as tk
from tkinter import ttk, messagebox

# --- Settings ---
FONT = ("Segoe UI", 11)
LIGHT_BG = "#f8f9fa"
DARK_BG = "#2b2b2b"
LIGHT_FG = "#212529"
DARK_FG = "#ffffff"
TASK_FILE = "tasks.txt"

# --- Main App Window ---
root = tk.Tk()
root.title("Professional To-Do List")
root.geometry("500x550")
root.config(bg=LIGHT_BG)

# --- Theme Control ---
is_dark = False

def toggle_theme():
    global is_dark
    is_dark = not is_dark
    bg = DARK_BG if is_dark else LIGHT_BG
    fg = DARK_FG if is_dark else LIGHT_FG
    root.config(bg=bg)
    lbl_title.config(bg=bg, fg=fg)
    frame_buttons.config(bg=bg)
    frame_tasks.config(bg=bg)
    for widget in frame_tasks.winfo_children():
        widget.config(bg=bg, fg=fg)
    btn_theme.config(text="Light Mode" if is_dark else "Dark Mode")

# --- Task Functions ---
tasks = []

def add_task():
    task_text = entry_task.get().strip()
    if task_text:
        var = tk.BooleanVar()
        cb = tk.Checkbutton(frame_tasks, text=task_text, variable=var, font=FONT,
                            bg=LIGHT_BG, fg=LIGHT_FG, anchor="w")
        cb.pack(fill="x", pady=2, padx=5)
        tasks.append((cb, var))
        entry_task.delete(0, tk.END)
    else:
        messagebox.showwarning("Warning", "Please enter a task!")

def delete_task():
    for cb, var in tasks.copy():
        if var.get():
            cb.destroy()
            tasks.remove((cb, var))

def save_tasks():
    with open(TASK_FILE, "w", encoding="utf-8") as file:
        for cb, var in tasks:
            status = "1" if var.get() else "0"
            file.write(f"{status}|{cb.cget('text')}\n")
    messagebox.showinfo("Saved", "Tasks saved successfully!")

def load_tasks():
    try:
        with open(TASK_FILE, "r", encoding="utf-8") as file:
            for line in file:
                status, text = line.strip().split("|")
                var = tk.BooleanVar(value=(status=="1"))
                cb = tk.Checkbutton(frame_tasks, text=text, variable=var, font=FONT,
                                    bg=LIGHT_BG, fg=LIGHT_FG, anchor="w")
                cb.pack(fill="x", pady=2, padx=5)
                tasks.append((cb, var))
    except FileNotFoundError:
        messagebox.showwarning("File Missing", "No saved tasks found.")

# --- UI Elements ---
lbl_title = tk.Label(root, text="Professional To-Do List", 
                     font=("Segoe UI Semibold", 16), bg=LIGHT_BG, fg=LIGHT_FG)
lbl_title.pack(pady=15)

frame_entry = tk.Frame(root, bg=LIGHT_BG)
frame_entry.pack(pady=5)

entry_task = ttk.Entry(frame_entry, width=35, font=FONT)
entry_task.pack(side=tk.LEFT, padx=5)

btn_add = ttk.Button(frame_entry, text="Add Task", command=add_task)
btn_add.pack(side=tk.LEFT)

frame_buttons = tk.Frame(root, bg=LIGHT_BG)
frame_buttons.pack(pady=10)

btn_delete = ttk.Button(frame_buttons, text="Delete Completed", command=delete_task)
btn_delete.pack(side=tk.LEFT, padx=5)

btn_save = ttk.Button(frame_buttons, text="Save Tasks", command=save_tasks)
btn_save.pack(side=tk.LEFT, padx=5)

btn_load = ttk.Button(frame_buttons, text="Load Tasks", command=load_tasks)
btn_load.pack(side=tk.LEFT, padx=5)

btn_theme = ttk.Button(frame_buttons, text="Dark Mode", command=toggle_theme)
btn_theme.pack(side=tk.LEFT, padx=5)

frame_tasks = tk.Frame(root, bg=LIGHT_BG)
frame_tasks.pack(fill="both", expand=True, padx=15, pady=10)

# --- Run ---
root.mainloop()
