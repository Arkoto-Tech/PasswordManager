import tkinter as tk
from tkinter import messagebox, filedialog
from cryptography.fernet import Fernet
import os


class PasswordManager:
    def __init__(self):
        self.key = None
        self.password_file = None
        self.password_dict = {}

    def create_key(self, path):
        self.key = Fernet.generate_key()
        with open(path, 'wb') as f:
            f.write(self.key)

    def load_key(self, path):
        if not os.path.exists(path):
            return False
        with open(path, 'rb') as f:
            self.key = f.read()
        return True

    def create_password_file(self, path, initial_values=None):
        self.password_file = path
        if initial_values is not None:
            for key, value in initial_values.items():
                self.add_password(key, value)

    def load_password_file(self, path):
        if not self.key:
            return False
        if not os.path.exists(path):
            return False

        self.password_file = path
        self.password_dict.clear()
        with open(path, 'r') as f:
            for line in f:
                site, encrypted = line.strip().split(":")
                try:
                    decrypted = Fernet(self.key).decrypt(encrypted.encode()).decode()
                    self.password_dict[site] = decrypted
                except:
                    continue
        return True

    def add_password(self, site, password):
        if not self.key:
            return False

        self.password_dict[site] = password

        if self.password_file:
            with open(self.password_file, 'a') as f:
                encrypted = Fernet(self.key).encrypt(password.encode())
                f.write(f"{site}:{encrypted.decode()}\n")
        return True

    def get_password(self, site):
        return self.password_dict.get(site, "Password not found.")


class PasswordManagerGUI:
    def __init__(self, root):
        self.pm = PasswordManager()
        self.root = root
        self.root.title("Password Manager")

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Path to Key/Password File:").pack()
        self.path_entry = tk.Entry(self.root, width=50)
        self.path_entry.pack()

        tk.Button(self.root, text="Create New Key", command=self.create_key).pack()
        tk.Button(self.root, text="Load Existing Key", command=self.load_key).pack()
        tk.Button(self.root, text="Create New Password File", command=self.create_password_file).pack()
        tk.Button(self.root, text="Load Existing Password File", command=self.load_password_file).pack()

        tk.Label(self.root, text="Site:").pack()
        self.site_entry = tk.Entry(self.root, width=50)
        self.site_entry.pack()

        tk.Label(self.root, text="Password:").pack()
        self.password_entry = tk.Entry(self.root, width=50, show='*')
        self.password_entry.pack()

        tk.Button(self.root, text="Add Password", command=self.add_password).pack()
        tk.Button(self.root, text="Get Password", command=self.get_password).pack()

    def create_key(self):
        path = filedialog.asksaveasfilename(defaultextension=".key", filetypes=[("Key files", "*.key")])
        if path:
            self.pm.create_key(path)
            messagebox.showinfo("Success", "Key created and saved.")

    def load_key(self):
        path = filedialog.askopenfilename(filetypes=[("Key files", "*.key")])
        if path and self.pm.load_key(path):
            messagebox.showinfo("Success", "Key loaded.")
        else:
            messagebox.showerror("Error", "Failed to load key.")

    def create_password_file(self):
        path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if path:
            self.pm.create_password_file(path)
            messagebox.showinfo("Success", "Password file created.")

    def load_password_file(self):
        path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if path and self.pm.load_password_file(path):
            messagebox.showinfo("Success", "Password file loaded.")
        else:
            messagebox.showerror("Error", "Failed to load password file or no key loaded.")

    def add_password(self):
        site = self.site_entry.get()
        password = self.password_entry.get()
        if self.pm.add_password(site, password):
            messagebox.showinfo("Success", f"Password for {site} added.")
        else:
            messagebox.showerror("Error", "Failed to add password or no key loaded.")

    def get_password(self):
        site = self.site_entry.get()
        password = self.pm.get_password(site)
        messagebox.showinfo("Password", f"Password for {site} is: {password}")


if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordManagerGUI(root)
    root.mainloop()
