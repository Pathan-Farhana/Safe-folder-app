import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend

def derive_key(password, salt):
    """Derives a key from a password and salt using PBKDF2HMAC."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))

def encrypt_file(file_path, key):
    """Encrypts a file and saves it with a .encrypted extension."""
    f = Fernet(key)
    with open(file_path, "rb") as original_file:
        original_data = original_file.read()
    
    encrypted_data = f.encrypt(original_data)
    
    encrypted_file_path = file_path + ".encrypted"
    with open(encrypted_file_path, "wb") as encrypted_file:
        encrypted_file.write(encrypted_data)
        
    return encrypted_file_path

def decrypt_file(file_path, key, output_dir):
    """Decrypts a file and saves it to the specified output directory."""
    f = Fernet(key)
    with open(file_path, "rb") as encrypted_file:
        encrypted_data = encrypted_file.read()
        
    decrypted_data = f.decrypt(encrypted_data)
    
    original_file_name = os.path.basename(file_path).replace(".encrypted", "")
    decrypted_file_path = os.path.join(output_dir, original_file_name)
    
    with open(decrypted_file_path, "wb") as decrypted_file:
        decrypted_file.write(decrypted_data)
        
    return decrypted_file_path