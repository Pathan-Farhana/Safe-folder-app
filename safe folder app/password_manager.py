import hashlib
import os

# Create a hidden folder to store the password hash and encryption key
SAFE_VAULT_DIR = "Safe_Vault"
PASSWORD_HASH_FILE = os.path.join(SAFE_VAULT_DIR, "password_hash.txt")

def hash_password(password):
    """Hashes a password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def create_master_password(password):
    """Hashes and saves the master password for the first time."""
    os.makedirs(SAFE_VAULT_DIR, exist_ok=True)
    hashed_password = hash_password(password)
    with open(PASSWORD_HASH_FILE, "w") as f:
        f.write(hashed_password)
    print("Master password created successfully!")

def verify_password(password):
    """Verifies a password against the stored hash."""
    if not os.path.exists(PASSWORD_HASH_FILE):
        return False
    
    with open(PASSWORD_HASH_FILE, "r") as f:
        stored_hash = f.read()
    
    return hash_password(password) == stored_hash