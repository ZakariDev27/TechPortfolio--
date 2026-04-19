import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

# ---------- LOG FUNCTION ----------
def log_message(msg):
    log_box.insert(tk.END, msg + "\n")
    log_box.see(tk.END)
    app.update()

# ---------- ORGANIZER ----------
def organize_files(folder_path, file_choice):
    file_types = {
        "Documents": [".docx", ".txt"],
        "CSV Files": [".csv"],
        "All Supported": [".docx", ".txt", ".csv"]
    }

    selected_extensions = file_types[file_choice]
    files = os.listdir(folder_path)

    total_files = len(files)
    progress["maximum"] = total_files
    progress["value"] = 0

    for index, filename in enumerate(files):
        file_path = os.path.join(folder_path, filename)

        if os.path.isfile(file_path):
            _, extension = os.path.splitext(filename)

            if extension.lower() in selected_extensions:
                destination = os.path.join(folder_path, file_choice)
                os.makedirs(destination, exist_ok=True)

                new_path = os.path.join(destination, filename)
                shutil.move(file_path, new_path)

                log_message(f"Moved: {filename} → {file_choice}")

        progress["value"] = index + 1
        app.update()

    log_message("Done organizing.\n")

# ---------- BUTTON ACTION ----------
def select_folder():
    folder = filedialog.askdirectory()
    if not folder:
        return

    choice = dropdown.get()

    try:
        log_message(f"\nOrganizing {choice}...\n")
        organize_files(folder, choice)
        messagebox.showinfo("Success", "Files organized successfully!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# ---------- UI ----------
app = tk.Tk()
app.title("File Organizer Pro")
app.geometry("500x400")
app.configure(bg="#1e1e1e")

# Title
title = tk.Label(app, text="File Organizer Pro", font=("Arial", 16, "bold"), bg="#1e1e1e", fg="white")
title.pack(pady=10)

# Dropdown Label
label = tk.Label(app, text="Select File Type:", bg="#1e1e1e", fg="white")
label.pack()

# Dropdown
options = ["Documents", "CSV Files", "All Supported"]
dropdown = ttk.Combobox(app, values=options, state="readonly")
dropdown.set("Documents")
dropdown.pack(pady=10)

# Button
button = tk.Button(app, text="Select Folder & Organize",
                   command=select_folder,
                   height=2, width=25,
                   bg="#007acc", fg="white")
button.pack(pady=10)

# Progress Bar
progress = ttk.Progressbar(app, orient="horizontal", length=400, mode="determinate")
progress.pack(pady=10)

# Log Box
log_box = tk.Text(app, height=10, bg="#121212", fg="#00ff9c")
log_box.pack(padx=10, pady=10, fill="both", expand=True)

app.mainloop()

