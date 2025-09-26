import os
import random
from barcode import EAN13
from barcode.writer import ImageWriter
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk

#carpeta_destino = r"C:\Users\T5809\BarcodesLyA"
# Directions of the folder to save the barcodes
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

def generate_barcodes():
    n = int(config['input_value'])
    carpeta_destino = config['setting']
    bntGenerator.pack_forget()

    # Create progress window
    progress_win = tk.Toplevel(root)
    progress_win.title("Generating Barcodes")
    progress_win.geometry("300x100")
    tk.Label(progress_win, text="Generating barcodes, please wait...").pack(pady=10)

    progress = ttk.Progressbar(progress_win, orient="horizontal", length=250, mode="determinate")
    progress.pack(pady=10)
    progress["value"] = 0
    progress["maximum"] = n

    progress_win.update_idletasks()

    for i in range(n):
        # Generate random 12-digit number
        numero = ''.join([str(random.randint(0, 9)) for _ in range(12)])
        codigo = EAN13(numero, writer=ImageWriter())

        # Save in destination folder
        archive_name = f"Código_{i:02d}"
        ruta_completa = os.path.join(carpeta_destino, archive_name)
        codigo.save(ruta_completa)

        # Update progress bar
        progress["value"] = i + 1
        progress_win.update_idletasks()

    # Close progress window
    progress_win.destroy()

    # Show final success message
    messagebox.showinfo("Success", f"{n} barcodes successfully generated and saved in {carpeta_destino}")

    # Open folder automatically
    os.startfile(carpeta_destino)
        
    n=config['input_value']
    carpeta_destino=config['setting']
    bntGenerator.pack_forget()

    progress.pack(pady=10)
    progress['value'] = 0
    progress['maximum'] = int(n)

    root.update_idletasks()

    for i in range(0, nm := int(n)):
        # Generar número aleatorio de 12 dígitos (el 13° lo calcula EAN13)
        numero = ''.join([str(random.randint(0, 9)) for _ in range(12)])

        # Crear código de barras EAN13 con imagen PNG
        codigo = EAN13(numero, writer=ImageWriter())

        # Guardar en la carpeta especificada
        archive_name = f"Código_{i:02d}"
        ruta_completa = os.path.join(carpeta_destino, archive_name)

        progress["value"] = i + 1
        root.update_idletasks()

        codigo.save(ruta_completa)
    messagebox.showinfo("Success",f"{(nm)} barcodes succesfully generated and saved in {(carpeta_destino)}")

    os.startfile(carpeta_destino)  # Open the folder after generation
    progress.pack_forget() # Hide progress bar after completion

root = tk.Tk()
root.title("Configuration Window")
root.geometry("400x250")

#Selection of the quantity of barcodes to generate
tk.Label(root, text="Quantity of barcodes to generate:").pack(pady=5)
title_entry = tk.Entry(root)
title_entry.pack(pady=5)
title_entry.insert(0, config["input_value"])

#Selection of the folder that will save the barcodes
ttk.Button(root, text="Select Folder", command=select_folder).pack(pady=5)

label_folder = tk.Label(root, text="No folder selected.")
label_folder.pack(pady=10)

ttk.Button(root, text="Update Configuration", command=update_values).pack(pady=5)
bntGenerator = tk.Button(root, text="Generate Barcodes", command=generate_barcodes)
bntGenerator.pack_forget()


progress = ttk.Progressbar(root, orient=tk.HORIZONTAL, length=250, mode='determinate')
progress.pack(pady=10)
progress.pack_forget()


root.mainloop()
