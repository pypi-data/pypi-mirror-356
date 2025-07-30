"""
DevDotEnv - Secure .env file encryption/decryption tool

A Python CLI tool for encrypting and decrypting environment files
using AES-256-GCM encryption with optional custom obfuscation.
"""

__version__ = "1.0.0"
__author__ = "DevDotEnv"
__email__ = "contact@devdotenv.dev"

from .crypto import encrypt_data, decrypt_data
from .key_manager import KeyManager
from .utils import read_file, write_file, calculate_checksum

__all__ = [
    "encrypt_data",
    "decrypt_data", 
    "KeyManager",
    "read_file",
    "write_file",
    "calculate_checksum",
] 