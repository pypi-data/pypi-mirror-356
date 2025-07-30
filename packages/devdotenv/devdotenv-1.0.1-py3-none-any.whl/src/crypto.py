"""
Cryptographic functions for DevDotEnv
"""

import os
import hashlib
import hmac
import struct
from typing import Tuple, Optional
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# Constants
ALGORITHM_VERSION = 1
FLAG_CUSTOM_OBFUSCATION = 0x01
AES_KEY_SIZE = 32  # 256 bits
GCM_IV_SIZE = 12   # 96 bits 
GCM_TAG_SIZE = 16  # 128 bits


def apply_custom_obfuscation(data: bytes, key: bytes) -> bytes:
    """
    Apply custom obfuscation using XOR and byte shuffling.
    
    Args:
        data: Data to obfuscate
        key: Encryption key for deriving obfuscation keys
        
    Returns:
        Obfuscated data
    """
    if len(data) == 0:
        return data
        
    # Derive XOR key using HMAC
    xor_key = hmac.new(key, b'xor_key', hashlib.sha256).digest()
    
    # XOR operation
    xor_data = bytearray()
    for i, byte in enumerate(data):
        xor_data.append(byte ^ xor_key[i % len(xor_key)])
    
    # Derive shuffle key
    shuffle_key = hmac.new(key, b'shuffle_key', hashlib.sha256).digest()
    
    # Create deterministic shuffle using Fisher-Yates
    indices = list(range(len(xor_data)))
    for i in range(len(indices) - 1, 0, -1):
        # Use shuffle key bytes to determine swap position
        key_byte = shuffle_key[i % len(shuffle_key)]
        j = key_byte % (i + 1)
        indices[i], indices[j] = indices[j], indices[i]
    
    # Apply shuffle
    shuffled_data = bytearray(len(xor_data))
    for i, source_idx in enumerate(indices):
        shuffled_data[i] = xor_data[source_idx]
    
    return bytes(shuffled_data)


def reverse_custom_obfuscation(data: bytes, key: bytes) -> bytes:
    """
    Reverse custom obfuscation.
    
    Args:
        data: Obfuscated data
        key: Encryption key for deriving obfuscation keys
        
    Returns:
        De-obfuscated data
    """
    if len(data) == 0:
        return data
        
    # Derive shuffle key
    shuffle_key = hmac.new(key, b'shuffle_key', hashlib.sha256).digest()
    
    # Recreate the same shuffle indices
    indices = list(range(len(data)))
    for i in range(len(indices) - 1, 0, -1):
        key_byte = shuffle_key[i % len(shuffle_key)]
        j = key_byte % (i + 1)
        indices[i], indices[j] = indices[j], indices[i]
    
    # Reverse the shuffle
    unshuffled_data = bytearray(len(data))
    for i, source_idx in enumerate(indices):
        unshuffled_data[source_idx] = data[i]
    
    # Derive XOR key
    xor_key = hmac.new(key, b'xor_key', hashlib.sha256).digest()
    
    # Reverse XOR operation
    original_data = bytearray()
    for i, byte in enumerate(unshuffled_data):
        original_data.append(byte ^ xor_key[i % len(xor_key)])
    
    return bytes(original_data)


def encrypt_data(data: bytes, key: bytes, use_custom_obfuscation: bool = False) -> bytes:
    """
    Encrypt data using AES-256-GCM with optional custom obfuscation.
    
    Args:
        data: Data to encrypt
        key: 256-bit encryption key
        use_custom_obfuscation: Whether to apply custom obfuscation
        
    Returns:
        Encrypted data with format: [version][flags][iv][tag][encrypted_data]
    """
    if len(key) != AES_KEY_SIZE:
        raise ValueError(f"Key must be exactly {AES_KEY_SIZE} bytes")
    
    # Apply custom obfuscation if requested
    if use_custom_obfuscation:
        data = apply_custom_obfuscation(data, key)
    
    # Generate random IV
    iv = os.urandom(GCM_IV_SIZE)
    
    # Encrypt with AES-256-GCM
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    
    ciphertext = encryptor.update(data) + encryptor.finalize()
    tag = encryptor.tag
    
    # Build header
    version = struct.pack('!I', ALGORITHM_VERSION)  # 4 bytes
    flags = struct.pack('!B', FLAG_CUSTOM_OBFUSCATION if use_custom_obfuscation else 0)  # 1 byte
    
    # Combine all parts
    return version + flags + iv + tag + ciphertext


def decrypt_data(encrypted_data: bytes, key: bytes) -> bytes:
    """
    Decrypt data encrypted with encrypt_data.
    
    Args:
        encrypted_data: Encrypted data with header
        key: 256-bit decryption key
        
    Returns:
        Decrypted data
    """
    if len(key) != AES_KEY_SIZE:
        raise ValueError(f"Key must be exactly {AES_KEY_SIZE} bytes")
    
    if len(encrypted_data) < 4 + 1 + GCM_IV_SIZE + GCM_TAG_SIZE:
        raise ValueError("Invalid encrypted data format")
    
    # Parse header
    version = struct.unpack('!I', encrypted_data[:4])[0]
    if version != ALGORITHM_VERSION:
        raise ValueError(f"Unsupported algorithm version: {version}")
    
    flags = struct.unpack('!B', encrypted_data[4:5])[0]
    use_custom_obfuscation = bool(flags & FLAG_CUSTOM_OBFUSCATION)
    
    # Extract components
    iv = encrypted_data[5:5 + GCM_IV_SIZE]
    tag = encrypted_data[5 + GCM_IV_SIZE:5 + GCM_IV_SIZE + GCM_TAG_SIZE]
    ciphertext = encrypted_data[5 + GCM_IV_SIZE + GCM_TAG_SIZE:]
    
    # Decrypt with AES-256-GCM
    cipher = Cipher(algorithms.AES(key), modes.GCM(iv, tag), backend=default_backend())
    decryptor = cipher.decryptor()
    
    try:
        data = decryptor.update(ciphertext) + decryptor.finalize()
    except Exception as e:
        raise ValueError(f"Decryption failed: {str(e)}")
    
    # Reverse custom obfuscation if it was applied
    if use_custom_obfuscation:
        data = reverse_custom_obfuscation(data, key)
    
    return data


def generate_key() -> bytes:
    """
    Generate a secure 256-bit encryption key.
    
    Returns:
        256-bit random key
    """
    return os.urandom(AES_KEY_SIZE) 