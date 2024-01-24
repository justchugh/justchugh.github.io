import tkinter as tk
from tkinter import filedialog, messagebox, Spinbox, StringVar
from tkcalendar import Calendar
import shutil, os
from git import Repo
from datetime import datetime
import pytz

repo_dir = '/Users/snehalraj/Desktop/GITHUB/webfolio/'
sub_dir = 'assets/js/'  # Path to your target subdirectory
commit_message = 'working on js'  # Define your commit message
ny_tz = pytz.timezone('America/New_York')  # New York Timezone

# --------------------------------------------------------------------------------------------------------

def copy_file_or_folder(src, dst):
    if os.path.isdir(src):
        shutil.copytree(src, dst)
    else:
        shutil.copy2(src, dst)

def perform_commit(date, time, file_path, repo_dir):
    filename = os.path.basename(file_path)
    new_file_path = os.path.join(repo_dir, sub_dir, filename)
    copy_file_or_folder(file_path, new_file_path)
    repo = Repo(repo_dir)
    
    # Combine date and time and convert to UTC
    ny_time_str = f"{date} {time}"
    ny_time = datetime.strptime(ny_time_str, "%Y-%m-%d %I:%M %p")
    ny_time = ny_tz.localize(ny_time)
    utc_time = ny_time.astimezone(pytz.utc)
    
    # Commit using the UTC time
    date_time_str = utc_time.strftime("%Y-%m-%dT%H:%M:%S")
    repo.git.add(all=True)
    repo.index.commit(commit_message, author_date=date_time_str, commit_date=date_time_str)
    repo.git.push()

# --------------------------------------------------------------------------------------------------------

def open_file():
    options = {
        'title': 'Select a file',
        'initialdir': '/',
    }
    file_path_entry.delete(0, tk.END)
    selection = filedialog.askopenfilename(**options)
    file_path_entry.insert(0, selection)

def open_folder():
    options = {
        'title': 'Select a folder',
        'initialdir': '/',
    }
    file_path_entry.delete(0, tk.END)
    selection = filedialog.askdirectory(**options)
    file_path_entry.insert(0, selection)

# --------------------------------------------------------------------------------------------------------

def commit_changes():
    start_date_str, file_path = cal_start.get_date(), file_path_entry.get()
    hour, minute = hour_spinbox.get(), minute_spinbox.get()
    am_pm = am_pm_var.get().strip().upper()  # Force uppercase for AM/PM
    try:
        start_date = datetime.strptime(start_date_str, "%m/%d/%y")  # Use a 2-digit year format
        if start_date and file_path:
            hour = hour.zfill(2)  # Add leading zeros if necessary
            minute = minute.zfill(2)  # Add leading zeros if necessary
            time_str = f"{hour}:{minute} {am_pm}"  # Combine hour, minute, and am/pm
            print(f"Date: {start_date.strftime('%Y-%m-%d')}, Time: {time_str}, File Path: {file_path}, Repo Dir: {repo_dir}")
            perform_commit(start_date.strftime("%Y-%m-%d"), time_str, file_path, repo_dir)  # Call the function with correct arguments
            messagebox.showinfo("Success", f"Commit made for {start_date.strftime('%Y-%m-%d')} at {time_str} New York Time")
        else:
            messagebox.showerror("Error", "Start date, time, and file path are required.")
    except ValueError as e:
        messagebox.showerror("Error", f"Invalid input: {str(e)}")


# --------------------------------------------------------------------------------------------------------

# Create the main window
root = tk.Tk()
root.title("Git Committer")

# Add a start date calendar
tk.Label(root, text="Date for commit:").pack(anchor='w')
current_date = datetime.now()
cal_start = Calendar(root, selectmode='day', year=current_date.year, month=current_date.month, day=current_date.day)
cal_start.pack()

# Time for commit frame
tk.Label(root, text="Time for commit:").pack(anchor='w')
time_frame = tk.Frame(root)
time_frame.pack()

# Configure the size to match the AM/PM dropdown
spinbox_width = 5  # Adjust the width as needed to match your UI

# Get the current time
current_time = datetime.now(ny_tz)  # Get the current time in New York timezone

# Hour Spinbox
current_hour = current_time.strftime("%I")  # Get the current hour in 12-hour format
hour_spinbox = Spinbox(time_frame, from_=1, to=12, wrap=True, format="%02.0f", width=spinbox_width)
hour_spinbox.pack(side=tk.LEFT)
hour_spinbox.delete(0, tk.END)  # Clear default value
hour_spinbox.insert(0, current_hour)  # Insert current hour

# Minute Spinbox
current_minute = current_time.strftime("%M")  # Get the current minute
minute_spinbox = Spinbox(time_frame, from_=0, to=59, wrap=True, format="%02.0f", width=spinbox_width)
minute_spinbox.pack(side=tk.LEFT)
minute_spinbox.delete(0, tk.END)  # Clear default value
minute_spinbox.insert(0, current_minute)  # Insert current minute

# AM/PM Dropdown
current_am_pm = current_time.strftime("%p")  # Get AM/PM
am_pm_var = StringVar(value=current_am_pm)
am_pm_dropdown = tk.OptionMenu(time_frame, am_pm_var, "AM", "PM")
am_pm_dropdown.pack(side=tk.LEFT)

# Match the dropdown size with the Spinbox
am_pm_dropdown.config(width=spinbox_width)

# Add a file path entry
tk.Label(root, text="File or Folder to commit:").pack(anchor='w')
file_path_entry = tk.Entry(root, width=15)
file_path_entry.pack(fill='x')

# Add "Select File" and "Select Folder" buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=5)
select_file_button = tk.Button(button_frame, text="Select File", command=open_file)
select_file_button.pack(side=tk.LEFT, padx=5)
select_folder_button = tk.Button(button_frame, text="Select Folder", command=open_folder)
select_folder_button.pack(side=tk.LEFT, padx=5)

# Add a "Commit" button to perform the commit
commit_button = tk.Button(root, text="Commit", command=commit_changes)
commit_button.pack(pady=5)

# Start the Tkinter event loop
root.mainloop()
