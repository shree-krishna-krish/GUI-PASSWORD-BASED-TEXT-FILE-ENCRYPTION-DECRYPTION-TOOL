# Libraries Used
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os, base64

# Create an encryption key from the password function
def get_cipher(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(), length=32,
        salt=salt, iterations=600000
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return Fernet(key)

# Encrypt or decrypt text

def process_text(mode):
    text, password = text_input.get("1.0", "end-1c"), password_box.get()
    if not text or not password:
        messagebox.showerror("Error", "Enter text and password.")
        return

    try:
        if mode == "encrypt":
            salt = os.urandom(16)
            token = get_cipher(password, salt).encrypt(text.encode())
            result = base64.urlsafe_b64encode(salt + token).decode()
        else:
            data = base64.urlsafe_b64decode(text.encode())
            if len(data) <= 16:
                raise ValueError("Invalid text")
            result = get_cipher(password, data[:16]).decrypt(data[16:]).decode()

        text_output.delete("1.0", tk.END)
        text_output.insert("1.0", result)
    except Exception:
        messagebox.showerror("Error", "Wrong password or invalid text.")

# Encrypt or decrypt a file

def process_file(mode):
    password = password_box.get()
    if not password:
        messagebox.showerror("Error", "Enter a password first.")
        return

    source = filedialog.askopenfilename(title="Choose a file")
    if not source:
        return

    try:
        with open(source, "rb") as file:
            data = file.read()

        if mode == "encrypt":
            salt = os.urandom(16)
            result = salt + get_cipher(password, salt).encrypt(data)
            name = os.path.basename(source) + ".encrypted"
        else:
            if len(data) <= 16:
                raise ValueError("Invalid file")
            result = get_cipher(password, data[:16]).decrypt(data[16:])
            name = os.path.basename(source)
            name = name[:-10] if name.endswith(".encrypted") else "decrypted_" + name
            if not name:
                name = "decrypted_file"

        destination = filedialog.asksaveasfilename(
            title="Save result as", initialfile=name
        )
        if not destination:
            return
        if os.path.abspath(source) == os.path.abspath(destination):
            messagebox.showerror("Error", "Choose a different output file.")
            return

        with open(destination, "wb") as file:
            file.write(result)
        messagebox.showinfo("Success", "File processed successfully.")
    except Exception:
        messagebox.showerror("Error", "Wrong password or invalid file.")

# Main window
root = tk.Tk()
root.title("Text and File Encryption")
root.geometry("560x620")

# Shared password field
tk.Label(root, text="Password").pack(pady=(12, 3))
password_box = tk.Entry(root, show="*", width=40)
password_box.pack(pady=(0, 10))

# Use separate tabs so text and file buttons do not clutter each other
tabs = ttk.Notebook(root)
tabs.pack(fill="both", expand=True, padx=12, pady=8)
text_tab = tk.Frame(tabs, padx=12, pady=12)
file_tab = tk.Frame(tabs, padx=12, pady=12)
tabs.add(text_tab, text="Text")
tabs.add(file_tab, text="Files")

# Text tab
tk.Label(text_tab, text="Input text / encrypted text").pack(anchor="w")
text_input = tk.Text(text_tab, height=8, wrap="word")
text_input.pack(fill="x", pady=5)
tk.Button(text_tab, text="Encrypt Text", command=lambda: process_text("encrypt")).pack(fill="x", pady=3)
tk.Button(text_tab, text="Decrypt Text", command=lambda: process_text("decrypt")).pack(fill="x", pady=3)
tk.Label(text_tab, text="Output").pack(anchor="w", pady=(10, 0))
text_output = tk.Text(text_tab, height=8, wrap="word")
text_output.pack(fill="both", expand=True, pady=5)

# File tab
tk.Label(file_tab, text="Select a file and choose where to save the result.", wraplength=400).pack(pady=(25, 15))
tk.Button(file_tab, text="Encrypt File", command=lambda: process_file("encrypt")).pack(fill="x", pady=6)
tk.Button(file_tab, text="Decrypt File", command=lambda: process_file("decrypt")).pack(fill="x", pady=6)
tk.Label(file_tab, text="Your original file is not intentionally modified.", wraplength=400).pack(pady=15)

root.mainloop()
