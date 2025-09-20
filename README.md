# Safe-folder-app


### **Safe Folder App** 🔒

A simple Python application that allows you to securely store and manage your files with password protection and encryption.

-----

### **How It Works**

This app provides a secure "vault" for your files. When you add a file, it's encrypted using a key derived from your password and moved to a hidden folder. When you want to access a file, the app uses your password to decrypt it temporarily for viewing.

  * **Password Protection:** Your password is never stored in plain text. Instead, a secure hash is saved to verify your identity.
  * **Encryption:** The app uses the industry-standard **Fernet** cipher to keep your files safe.

-----

### **Features**

  * **Secure Storage:** Add and store any file type in a protected vault.
  * **Password Login:** Access your files with a master password.
  * **File Management:** View, add, and delete items from your secure folder.

-----

### **Getting Started**

#### **Prerequisites**

  * **Python 3.x**
  * **Cryptography** library. Install it with pip:
    ```bash
    pip install cryptography
    ```

#### **How to Run**

1.  Make sure all the project files (`safe_folder_app.py`, `encryption.py`, `password_manager.py`) are in the same folder.
2.  Open your terminal or command prompt in the project directory.
3.  Run the main application script:
    ```bash
    python safe_folder_app.py
    ```

-----

### **File Structure**

```
safe_folder_app/
├── Safe_Vault/             # Encrypted files are stored here
├── encryption.py           # Handles all encryption/decryption logic
├── password_manager.py     # Manages password hashing and verification
└── safe_folder_app.py      # The main application with the GUI
```
