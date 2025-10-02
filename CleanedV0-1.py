import os
import random
from barcode import EAN13
from barcode.writer import ImageWriter
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk
import threading
import time
import subprocess
import platform
from datetime import datetime

config = {
    "input_value": "1",
    "setting": ""
}

def only_integer(char):
    return char.isdigit()

def select_folder():
    folder_selected = filedialog.askdirectory(title="Select Folder")
    if folder_selected:
        config["setting"] = folder_selected
        messagebox.showinfo("Folder Selected", f"Selected Folder: {config['setting']}")
        label_folder.config(text=f"Selected Folder:\n {shorten_path(config['setting'])}")

def update_values():
    config["input_value"] = title_entry.get()
    messagebox.showinfo("Configuration Updated", f"Barcode(s) to generate: {config['input_value']}\nFolder selected: {config['setting']}")
    bntGenerator.pack(pady=5)

def shorten_path(path, max_length=30):
    if len(path) <= max_length:
        return path
    else:
        part_length = (max_length - 3) // 2
        return f"{path[:part_length]}...{path[-part_length:]}"

def generate_barcodes_thread(n, target_folder, progress_window, progress_bar, status_label):
    """Function to run barcode generation in a separate thread"""
    try:
        nm = int(n)
        
        for i in range(nm):
            # Update progress
            progress_percentage = (i / nm) * 100
            progress_bar['value'] = progress_percentage
            status_label.config(text=f"Generating barcode {i+1} of {nm}...")
            progress_window.update()
            
            # Generate random 12-digit number (EAN13 calculates the 13th)
            number = ''.join([str(random.randint(0, 9)) for _ in range(12)])
            
            # Create EAN13 barcode with PNG image
            barcode = EAN13(number, writer=ImageWriter())
            
            # Save to specified folder
            archive_name = f"Code_{i+1:03d}"
            full_destination_path = os.path.join(target_folder, archive_name)
            barcode.save(full_destination_path)
            
        
        # Complete progress
        progress_bar['value'] = 100
        status_label.config(text=f"Complete! Generated {nm} barcodes.")
        progress_window.update()
        
        # Wait a moment before closing
        time.sleep(1)
        
        # Close progress window and show success message
        progress_window.destroy()
        messagebox.showinfo("Success", f"{nm} barcodes successfully generated and saved in {target_folder}")
        
        # Open the folder automatically based on OS
        try:
            if platform.system() == "Windows":
                os.startfile(target_folder)
            elif platform.system() == "Darwin":  # macOS
                subprocess.Popen(["open", target_folder])
            else:  # Linux and other Unix-like systems
                subprocess.Popen(["xdg-open", target_folder])
        except Exception as e:
            print(f"Could not open folder: {e}")
            
    except Exception as e:
        progress_window.destroy()
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def generate_barcodes():
    n = config['input_value']
    target_folder = config['setting']
    
    # Validate inputs
    if not target_folder:
        messagebox.showerror("Error", "Please select a folder first.")
        return
    
    try:
        nm = int(n)
        if nm <= 0:
            messagebox.showerror("Error", "Please enter a positive number.")
            return
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number.")
        return
    
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    subfolder_name = f"Barcodes_{timestamp}"
    final_destination = os.path.join(target_folder, subfolder_name)
    
    try:
        os.makedirs(final_destination, exist_ok=True)
    except Exception as e:
        messagebox.showerror("Error", f"Could not create subfolder: {str(e)}")
        return
     
    # Hide the generate button
    bntGenerator.pack_forget()
    
    # Create progress window
    progress_window = tk.Toplevel(root)
    progress_window.title("Generating Barcodes")
    progress_window.geometry("400x150")
    progress_window.resizable(False, False)
    progress_window.transient(root)
    progress_window.grab_set()
    
    # Center the progress window
    progress_window.geometry("+%d+%d" % (root.winfo_rootx() + 50, root.winfo_rooty() + 50))
    
    # Progress window content
    tk.Label(progress_window, text="Generating Barcodes...", font=("Arial", 12, "bold")).pack(pady=10)
    
    # Progress bar
    progress_bar = ttk.Progressbar(progress_window, length=300, mode='determinate')
    progress_bar.pack(pady=10)
    
    # Status label
    status_label = tk.Label(progress_window, text="Starting generation...")
    status_label.pack(pady=5)
    
    # Cancel button (optional)
    def cancel_generation():
        progress_window.destroy()
        bntGenerator.pack(pady=5)  # Show the generate button again
    
    tk.Button(progress_window, text="Cancel", command=cancel_generation).pack(pady=5)
    
    # Start generation in a separate thread
    thread = threading.Thread(
        target=generate_barcodes_thread, 
        args=(n, final_destination, progress_window, progress_bar, status_label)
    )
    thread.daemon = True
    thread.start()
    
    # Function to check if thread is still alive and re-enable button if needed
    def check_thread():
        if thread.is_alive():
            root.after(100, check_thread)
    
    check_thread()

# Main window
root = tk.Tk()
root.title("Barcode Generator-beta")
root.geometry("450x680")
root.resizable(False, False)

# Title
title_frame = tk.Frame(root, bg="#4CAF50", height=120)
title_frame.pack(fill=tk.X, pady=0)
title_frame.pack_propagate(False)

icon_label = tk.Label(title_frame, text="📊", font=("Arial", 30), 
                      fg="white",
                      bg="#4CAF50")
icon_label.pack(pady=(15, 0))

title_label = tk.Label(title_frame, text="Barcode Generator", 
                      font=("Arial", 18, "bold"), 
                      fg="white", 
                      bg="#4CAF50")
title_label.pack(pady=(0, 15))

# Quantity section
quantity_frame = tk.Frame(root, bg="#f5f7fa", height=100)
quantity_frame.pack(fill=tk.X,)
quantity_frame.pack_propagate(False)

quantity_label = tk.Label(quantity_frame, 
                         text="Quantity of barcodes to generate:", 
                         font=("Arial", 11, "bold"),
                         fg="#2c3e50",
                         bg="#f5f7fa")
quantity_label.pack(anchor="w", pady=(10, 0))

# Entry with border
entry_container = tk.Frame(quantity_frame, 
                          bg="white", 
                          highlightbackground="#dcdde1",
                          highlightthickness=2)
entry_container.pack(fill=tk.X)

title_entry = tk.Entry(entry_container, 
                      font=("Arial", 12), 
                      fg="#2c3e50",
                      bg="white",
                      relief=tk.FLAT,
                      bd=8)
title_entry.pack(fill=tk.X, padx=5, pady=5)
title_entry.insert(0, config["input_value"])

# Validate that only integers can be entered
vcmd = (root.register(only_integer), '%S')
title_entry.config(validate='key', validatecommand=vcmd)

# Folder selection section
folder_frame = tk.Frame(root, bg="#f5f7fa")
folder_frame.pack(fill=tk.X, padx=30, pady=20)

folder_label_title = tk.Label(folder_frame, 
                             text="Destination Folder:", 
                             font=("Arial", 11, "bold"),
                             fg="#2c3e50",
                             bg="#f5f7fa")
folder_label_title.pack(anchor="w", pady=(0, 8))

# Button with modern style
folder_button = tk.Button(folder_frame, 
                         text="📁 Select Folder", 
                         command=select_folder,
                         font=("Arial", 11, "bold"),
                         fg="white",
                         bg="#4CAF50",  # Blue
                         activebackground="#ff0000",  # Darker blue on click
                         activeforeground="white",
                         relief=tk.FLAT,
                         bd=0,
                         padx=20,
                         pady=10,)
folder_button.pack(pady=(0, 10))

label_folder = tk.Label(folder_frame, 
                       text="No folder selected", 
                       font=("Arial", 9),
                       fg="#000000",
                       bg="#f5f7fa",
                       wraplength=400)
label_folder.pack(pady=(0, 20))

# Update button
update_button = tk.Button(folder_frame, 
                         text="✓ Update Configuration", 
                         command=update_values,
                         font=("Arial", 11, "bold"),
                         fg="white",
                         bg="#4CAF50",
                         activebackground="#ff0000",
                         activeforeground="white",
                         relief=tk.FLAT,
                         bd=0,
                         padx=20,
                         pady=10,)
update_button.pack()

# Generate barcodes button (initially hidden)
bntGenerator = tk.Button(root, 
                         text="Generate Barcodes", 
                         command=generate_barcodes, 
                         font=("Arial", 11, "bold"), 
                         fg="white",
                         bg="#4CAF50",
                         activebackground="#ff0000",
                         activeforeground="white",
                         relief=tk.FLAT,
                         bd=0,
                         padx=20,
                         pady=10,)
bntGenerator.pack_forget()

# Instructions
instructions = tk.Label(root, text="\nInstructions:\n1. Enter the number of barcodes to generate\n2. Select destination folder\n3. Click 'Update Configuration'\n4. Click 'Generate Barcodes'", 
                       font=("Arial", 9), justify="left", fg="gray")
instructions.pack(pady=20)

root.mainloop()