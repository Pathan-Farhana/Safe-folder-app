# import tkinter as tk
# from tkinter import filedialog, messagebox, simpledialog
# from password_manager import create_master_password, verify_password
# from encryption import encrypt_file, decrypt_file
# from encryption import encrypt_file, decrypt_file, derive_key
# import os
# import shutil

# SAFE_VAULT_DIR = "Safe_Vault"

# class SafeFolderApp:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("Safe Folder App")
#         self.password_key = None
#         self.salt = b'a_secure_random_salt_for_your_app' # Change this to a truly random salt

#         if not os.path.exists(os.path.join(SAFE_VAULT_DIR, "password_hash.txt")):
#             self.show_create_password_dialog()
#         else:
#             self.show_login_dialog()

#     def show_create_password_dialog(self):
#         password = simpledialog.askstring("Create Password", "Create a Master Password:", show='*')
#         if password:
#             create_master_password(password)
#             self.show_login_dialog()

#     def show_login_dialog(self):
#         password = simpledialog.askstring("Login", "Enter Master Password:", show='*')
#         if password and verify_password(password):
#             self.password_key = self.get_encryption_key(password)
#             self.build_main_app_gui()
#         else:
#             messagebox.showerror("Error", "Invalid password.")
#             self.root.destroy()

#     def get_encryption_key(self, password):
#         return derive_key(password, self.salt)
    
#     def build_main_app_gui(self):
#         # This will contain the main application window and its components
#         # (buttons for add, view, delete, etc.)
#         self.root.title("Safe Folder")
        
#         # We can display the files in the Safe_Vault folder here
#         self.file_listbox = tk.Listbox(self.root)
#         self.file_listbox.pack(pady=10)
#         self.refresh_file_list()

#         add_btn = tk.Button(self.root, text="Add File", command=self.add_file_to_vault)
#         add_btn.pack(pady=5)

#         view_btn = tk.Button(self.root, text="View File", command=self.view_file)
#         view_btn.pack(pady=5)
        
#         delete_btn = tk.Button(self.root, text="Delete File", command=self.delete_file)
#         delete_btn.pack(pady=5)

#     def refresh_file_list(self):
#         self.file_listbox.delete(0, tk.END)
#         for filename in os.listdir(SAFE_VAULT_DIR):
#             if filename.endswith(".encrypted"):
#                 self.file_listbox.insert(tk.END, filename)

#     def add_file_to_vault(self):
#         file_path = filedialog.askopenfilename()
#         if file_path:
#             encrypted_path = encrypt_file(file_path, self.password_key)
#             shutil.move(encrypted_path, os.path.join(SAFE_VAULT_DIR, os.path.basename(encrypted_path)))
#             self.refresh_file_list()
#             messagebox.showinfo("Success", "File added to vault.")

#     def view_file(self):
#         selected_file = self.file_listbox.get(tk.ACTIVE)
#         if selected_file:
#             encrypted_path = os.path.join(SAFE_VAULT_DIR, selected_file)
#             temp_dir = "temp_decrypted"
#             os.makedirs(temp_dir, exist_ok=True)
            
#             try:
#                 decrypted_path = decrypt_file(encrypted_path, self.password_key, temp_dir)
#                 messagebox.showinfo("File Decrypted", f"File decrypted to: {decrypted_path}\nOpen it to view.")
                
#                 # You might want to automatically open the file here
#                 # os.startfile(decrypted_path) on Windows
#                 # import subprocess; subprocess.call(('open', decrypted_path)) on Mac
                
#             except Exception as e:
#                 messagebox.showerror("Decryption Error", f"Failed to decrypt file: {e}")
#             finally:
#                 # Clean up the temporary file after a certain action or when the app closes
#                 pass

#     def delete_file(self):
#         selected_file = self.file_listbox.get(tk.ACTIVE)
#         if selected_file:
#             if messagebox.askyesno("Delete File", f"Are you sure you want to delete {selected_file}?"):
#                 file_path = os.path.join(SAFE_VAULT_DIR, selected_file)
#                 os.remove(file_path)
#                 self.refresh_file_list()
#                 messagebox.showinfo("Success", "File deleted successfully.")

# if __name__ == "__main__":
#     root = tk.Tk()
#     app = SafeFolderApp(root)
#     root.mainloop()

import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from password_manager import create_master_password, verify_password
from encryption import encrypt_file, decrypt_file, derive_key
import os
import shutil

# This should be a truly random, non-guessable value
# It should be the same for all users and installations
SALT = b'a_secure_random_salt_for_your_app'
SAFE_VAULT_DIR = "Safe_Vault"

class SafeFolderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Safe Folder App")
        self.password_key = None

        if not os.path.exists(os.path.join(SAFE_VAULT_DIR, "password_hash.txt")):
            self.show_create_password_dialog()
        else:
            self.show_login_dialog()

    def show_create_password_dialog(self):
        password = simpledialog.askstring("Create Password", "Create a Master Password:", show='*')
        if password:
            create_master_password(password)
            messagebox.showinfo("Success", "Master password created successfully!")
            self.show_login_dialog()
        else:
            self.root.destroy()

    def show_login_dialog(self):
        # We need to make sure the main window doesn't show up before a successful login
        self.root.withdraw()
        
        password = simpledialog.askstring("Login", "Enter Master Password:", show='*')
        if password and verify_password(password):
            self.password_key = derive_key(password, SALT)
            self.root.deiconify()  # Show the main window after successful login
            self.build_main_app_gui()
        else:
            messagebox.showerror("Error", "Invalid password.")
            self.root.destroy()
            
    def build_main_app_gui(self):
        self.root.title("Safe Folder")
        self.file_listbox = tk.Listbox(self.root)
        self.file_listbox.pack(pady=10)
        self.refresh_file_list()

        add_btn = tk.Button(self.root, text="Add File", command=self.add_file_to_vault)
        add_btn.pack(pady=5)

        view_btn = tk.Button(self.root, text="View File", command=self.view_file)
        view_btn.pack(pady=5)

        delete_btn = tk.Button(self.root, text="Delete File", command=self.delete_file)
        delete_btn.pack(pady=5)
    
    def refresh_file_list(self):
        self.file_listbox.delete(0, tk.END)
        # Check if the vault directory exists before listing files
        if os.path.exists(SAFE_VAULT_DIR):
            for filename in os.listdir(SAFE_VAULT_DIR):
                if filename.endswith(".encrypted"):
                    self.file_listbox.insert(tk.END, filename.replace(".encrypted", ""))

    def add_file_to_vault(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            encrypted_path = encrypt_file(file_path, self.password_key)
            shutil.move(encrypted_path, os.path.join(SAFE_VAULT_DIR, os.path.basename(encrypted_path)))
            self.refresh_file_list()
            messagebox.showinfo("Success", "File added to vault.")

    def view_file(self):
        selected_file_name = self.file_listbox.get(tk.ACTIVE)
        if selected_file_name:
            encrypted_path = os.path.join(SAFE_VAULT_DIR, selected_file_name + ".encrypted")
            temp_dir = "temp_decrypted"
            os.makedirs(temp_dir, exist_ok=True)
            
            try:
                decrypted_path = decrypt_file(encrypted_path, self.password_key, temp_dir)
                messagebox.showinfo("File Decrypted", f"File decrypted to: {decrypted_path}\nOpen it to view.")
            except Exception as e:
                messagebox.showerror("Decryption Error", f"Failed to decrypt file: {e}")
            
    def delete_file(self):
        selected_file_name = self.file_listbox.get(tk.ACTIVE)
        if selected_file_name:
            if messagebox.askyesno("Delete File", f"Are you sure you want to delete {selected_file_name}?"):
                file_path = os.path.join(SAFE_VAULT_DIR, selected_file_name + ".encrypted")
                os.remove(file_path)
                self.refresh_file_list()
                messagebox.showinfo("Success", "File deleted successfully.")

if __name__ == "__main__":
    root = tk.Tk()
    app = SafeFolderApp(root)
    root.mainloop()