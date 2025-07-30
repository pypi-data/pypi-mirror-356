"""
Key management for DevDotEnv

This module handles the generation, storage, and loading of encryption keys
for the DevDotEnv tool. Keys are stored as Base64-encoded strings in files
with restricted permissions for security.
"""

import os
import base64
from pathlib import Path
from typing import Optional
from .crypto import generate_key


class KeyManager:
    """Manages encryption keys for DevDotEnv"""
    
    DEFAULT_KEY_FILE = '.devdotenv.key'
    
    def __init__(self, key_file: Optional[str] = None):
        """
        Initialize KeyManager.
        
        Args:
            key_file: Path to key file (defaults to .devdotenv.key)
        """
        self.key_file = Path(key_file) if key_file else Path(self.DEFAULT_KEY_FILE)
    
    def key_exists(self) -> bool:
        """
        Check if key file exists.
        
        Returns:
            True if key file exists
        """
        return self.key_file.exists()
    
    def generate_and_save_key(self) -> None:
        """
        Generate a new encryption key and save it to file.
        
        Raises:
            FileExistsError: If key file already exists
            OSError: If unable to write key file
        """
        if self.key_exists():
            raise FileExistsError(f"Key file already exists: {self.key_file}")
        
        # Generate new key
        key = generate_key()
        
        # Encode as base64 for storage
        key_b64 = base64.b64encode(key).decode('utf-8')
        
        # Write to file with restricted permissions
        try:
            self.key_file.write_text(key_b64)
            # Set restrictive permissions (owner read/write only)
            if os.name != 'nt':  # Not Windows
                os.chmod(self.key_file, 0o600)
        except Exception as e:
            # Clean up partial file if creation failed
            if self.key_file.exists():
                self.key_file.unlink()
            raise OSError(f"Failed to create key file: {str(e)}")
    
    def load_key(self) -> bytes:
        """
        Load encryption key from file.
        
        Returns:
            32-byte encryption key
            
        Raises:
            FileNotFoundError: If key file doesn't exist
            ValueError: If key file is invalid
        """
        if not self.key_exists():
            raise FileNotFoundError(f"Key file not found: {self.key_file}")
        
        try:
            key_b64 = self.key_file.read_text().strip()
            key = base64.b64decode(key_b64)
            
            if len(key) != 32:
                raise ValueError("Invalid key length")
                
            return key
        except Exception as e:
            raise ValueError(f"Invalid key file: {str(e)}")
    
    def rotate_key(self) -> None:
        """
        Generate a new key, replacing the existing one.
        
        Raises:
            FileNotFoundError: If key file doesn't exist
            OSError: If unable to write new key
        """
        if not self.key_exists():
            raise FileNotFoundError(f"Key file not found: {self.key_file}")
        
        # Generate new key
        key = generate_key()
        key_b64 = base64.b64encode(key).decode('utf-8')
        
        # Create backup of old key
        backup_file = self.key_file.with_suffix('.key.backup')
        if backup_file.exists():
            backup_file.unlink()
        
        try:
            # Backup current key
            self.key_file.rename(backup_file)
            
            # Write new key
            self.key_file.write_text(key_b64)
            if os.name != 'nt':  # Not Windows
                os.chmod(self.key_file, 0o600)
            
            # Remove backup on success
            backup_file.unlink()
            
        except Exception as e:
            # Restore backup on failure
            if backup_file.exists():
                backup_file.rename(self.key_file)
            raise OSError(f"Failed to rotate key: {str(e)}")
    
    def delete_key(self) -> None:
        """
        Delete the key file.
        
        Raises:
            FileNotFoundError: If key file doesn't exist
        """
        if not self.key_exists():
            raise FileNotFoundError(f"Key file not found: {self.key_file}")
        
        self.key_file.unlink()
    
    def get_key_file_path(self) -> Path:
        """
        Get the path to the key file.
        
        Returns:
            Path to key file
        """
        return self.key_file 