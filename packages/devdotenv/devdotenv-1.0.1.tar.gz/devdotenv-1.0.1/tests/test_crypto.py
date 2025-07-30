"""
Tests for the crypto module
"""

import pytest
from src.crypto import (
    encrypt_data, decrypt_data, generate_key,
    apply_custom_obfuscation, reverse_custom_obfuscation
)


class TestBasicEncryption:
    """Test basic encryption/decryption functionality"""
    
    def test_generate_key(self):
        """Test key generation"""
        key = generate_key()
        assert len(key) == 32
        assert isinstance(key, bytes)
        
        # Generate another key and ensure they're different
        key2 = generate_key()
        assert key != key2
    
    def test_encrypt_decrypt_basic(self):
        """Test basic encryption and decryption"""
        key = generate_key()
        data = b"Hello, World!"
        
        encrypted = encrypt_data(data, key, use_custom_obfuscation=False)
        decrypted = decrypt_data(encrypted, key)
        
        assert decrypted == data
    
    def test_encrypt_decrypt_with_obfuscation(self):
        """Test encryption and decryption with custom obfuscation"""
        key = generate_key()
        data = b"Hello, World! This is a longer test message."
        
        encrypted = encrypt_data(data, key, use_custom_obfuscation=True)
        decrypted = decrypt_data(encrypted, key)
        
        assert decrypted == data
    
    def test_empty_data(self):
        """Test encryption of empty data"""
        key = generate_key()
        data = b""
        
        encrypted = encrypt_data(data, key)
        decrypted = decrypt_data(encrypted, key)
        
        assert decrypted == data
    
    def test_large_data(self):
        """Test encryption of large data"""
        key = generate_key()
        data = b"x" * 10000  # 10KB of data
        
        encrypted = encrypt_data(data, key)
        decrypted = decrypt_data(encrypted, key)
        
        assert decrypted == data


class TestCustomObfuscation:
    """Test custom obfuscation functionality"""
    
    def test_obfuscation_reversible(self):
        """Test that obfuscation is reversible"""
        key = generate_key()
        data = b"Test data for obfuscation"
        
        obfuscated = apply_custom_obfuscation(data, key)
        deobfuscated = reverse_custom_obfuscation(obfuscated, key)
        
        assert deobfuscated == data
        assert obfuscated != data  # Should be different
    
    def test_obfuscation_empty_data(self):
        """Test obfuscation with empty data"""
        key = generate_key()
        data = b""
        
        obfuscated = apply_custom_obfuscation(data, key)
        deobfuscated = reverse_custom_obfuscation(obfuscated, key)
        
        assert deobfuscated == data
        assert obfuscated == data  # Empty data should remain empty
    
    def test_obfuscation_deterministic(self):
        """Test that obfuscation is deterministic with same key"""
        key = generate_key()
        data = b"Deterministic test data"
        
        obfuscated1 = apply_custom_obfuscation(data, key)
        obfuscated2 = apply_custom_obfuscation(data, key)
        
        assert obfuscated1 == obfuscated2
    
    def test_obfuscation_different_keys(self):
        """Test that different keys produce different obfuscation"""
        key1 = generate_key()
        key2 = generate_key()
        data = b"Test data for different keys"
        
        obfuscated1 = apply_custom_obfuscation(data, key1)
        obfuscated2 = apply_custom_obfuscation(data, key2)
        
        assert obfuscated1 != obfuscated2


class TestErrorHandling:
    """Test error handling"""
    
    def test_invalid_key_length_encrypt(self):
        """Test encryption with invalid key length"""
        key = b"short"  # Too short
        data = b"test data"
        
        with pytest.raises(ValueError, match="Key must be exactly 32 bytes"):
            encrypt_data(data, key)
    
    def test_invalid_key_length_decrypt(self):
        """Test decryption with invalid key length"""
        key = b"short"  # Too short
        encrypted_data = b"fake encrypted data"
        
        with pytest.raises(ValueError, match="Key must be exactly 32 bytes"):
            decrypt_data(encrypted_data, key)
    
    def test_invalid_encrypted_data_format(self):
        """Test decryption with invalid data format"""
        key = generate_key()
        invalid_data = b"not encrypted data"
        
        with pytest.raises(ValueError, match="Invalid encrypted data format"):
            decrypt_data(invalid_data, key)
    
    def test_wrong_key_decrypt(self):
        """Test decryption with wrong key"""
        key1 = generate_key()
        key2 = generate_key()
        data = b"test data"
        
        encrypted = encrypt_data(data, key1)
        
        with pytest.raises(ValueError, match="Decryption failed"):
            decrypt_data(encrypted, key2)
    
    def test_unsupported_version(self):
        """Test decryption with unsupported version"""
        key = generate_key()
        data = b"test data"
        
        encrypted = encrypt_data(data, key)
        # Modify the version bytes to simulate unsupported version
        corrupted = b"\x00\x00\x00\x02" + encrypted[4:]  # Version 2
        
        with pytest.raises(ValueError, match="Unsupported algorithm version"):
            decrypt_data(corrupted, key)


class TestFileFormat:
    """Test encrypted file format"""
    
    def test_encrypted_format_structure(self):
        """Test that encrypted data has correct structure"""
        key = generate_key()
        data = b"test data"
        
        encrypted = encrypt_data(data, key, use_custom_obfuscation=False)
        
        # Check minimum length (4 + 1 + 12 + 16 + data_length)
        assert len(encrypted) >= 33
        
        # Check version (first 4 bytes)
        version = int.from_bytes(encrypted[:4], byteorder='big')
        assert version == 1
        
        # Check flags (5th byte)
        flags = encrypted[4]
        assert flags & 0x01 == 0  # No custom obfuscation
    
    def test_encrypted_format_with_obfuscation(self):
        """Test that encrypted data has correct structure with obfuscation"""
        key = generate_key()
        data = b"test data"
        
        encrypted = encrypt_data(data, key, use_custom_obfuscation=True)
        
        # Check flags (5th byte)
        flags = encrypted[4]
        assert flags & 0x01 == 1  # Custom obfuscation enabled 