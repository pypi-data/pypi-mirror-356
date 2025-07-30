"""
Utility functions for DevDotEnv
"""

import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List


def read_file(file_path: str) -> bytes:
    """
    Read file content as bytes.
    
    Args:
        file_path: Path to file
        
    Returns:
        File content as bytes
        
    Raises:
        FileNotFoundError: If file doesn't exist
        OSError: If unable to read file
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    try:
        return path.read_bytes()
    except Exception as e:
        raise OSError(f"Failed to read file {file_path}: {str(e)}")


def write_file(file_path: str, content: bytes) -> None:
    """
    Write bytes content to file.
    
    Args:
        file_path: Path to file
        content: Content to write
        
    Raises:
        OSError: If unable to write file
    """
    path = Path(file_path)
    
    try:
        path.write_bytes(content)
    except Exception as e:
        raise OSError(f"Failed to write file {file_path}: {str(e)}")


def calculate_checksum(data: bytes) -> str:
    """
    Calculate SHA-256 checksum of data.
    
    Args:
        data: Data to checksum
        
    Returns:
        Hex-encoded SHA-256 checksum
    """
    return hashlib.sha256(data).hexdigest()


def file_exists(file_path: str) -> bool:
    """
    Check if file exists.
    
    Args:
        file_path: Path to file
        
    Returns:
        True if file exists
    """
    return Path(file_path).exists()


def get_file_size(file_path: str) -> int:
    """
    Get file size in bytes.
    
    Args:
        file_path: Path to file
        
    Returns:
        File size in bytes
        
    Raises:
        FileNotFoundError: If file doesn't exist
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    return path.stat().st_size


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human-readable format.
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Formatted size string
    """
    if size_bytes == 0:
        return "0 B"
    
    units = ['B', 'KB', 'MB', 'GB', 'TB']
    unit_index = 0
    size = float(size_bytes)
    
    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024
        unit_index += 1
    
    if unit_index == 0:
        return f"{int(size)} {units[unit_index]}"
    else:
        return f"{size:.1f} {units[unit_index]}"


def create_metadata(file_path: str, encrypted_file_path: str, 
                   use_custom_obfuscation: bool = False) -> Dict[str, Any]:
    """
    Create metadata for encrypted file.
    
    Args:
        file_path: Original file path
        encrypted_file_path: Encrypted file path
        use_custom_obfuscation: Whether custom obfuscation was used
        
    Returns:
        Metadata dictionary
    """
    original_content = read_file(file_path)
    encrypted_content = read_file(encrypted_file_path)
    
    return {
        'version': '1.0.0',
        'timestamp': datetime.now().isoformat(),
        'original_file': file_path,
        'encrypted_file': encrypted_file_path,
        'original_size': len(original_content),
        'encrypted_size': len(encrypted_content),
        'original_checksum': calculate_checksum(original_content),
        'encrypted_checksum': calculate_checksum(encrypted_content),
        'custom_obfuscation': use_custom_obfuscation,
        'algorithm': 'AES-256-GCM'
    }


def save_metadata(metadata: Dict[str, Any], metadata_file: str) -> None:
    """
    Save metadata to JSON file.
    
    Args:
        metadata: Metadata dictionary
        metadata_file: Path to metadata file
    """
    try:
        Path(metadata_file).write_text(json.dumps(metadata, indent=2))
    except Exception as e:
        raise OSError(f"Failed to save metadata: {str(e)}")


def load_metadata(metadata_file: str) -> Dict[str, Any]:
    """
    Load metadata from JSON file.
    
    Args:
        metadata_file: Path to metadata file
        
    Returns:
        Metadata dictionary
        
    Raises:
        FileNotFoundError: If metadata file doesn't exist
        ValueError: If metadata file is invalid
    """
    path = Path(metadata_file)
    if not path.exists():
        raise FileNotFoundError(f"Metadata file not found: {metadata_file}")
    
    try:
        return json.loads(path.read_text())
    except Exception as e:
        raise ValueError(f"Invalid metadata file: {str(e)}")


def verify_file_integrity(file_path: str, expected_checksum: str) -> bool:
    """
    Verify file integrity using checksum.
    
    Args:
        file_path: Path to file
        expected_checksum: Expected SHA-256 checksum
        
    Returns:
        True if checksum matches
    """
    if not file_exists(file_path):
        return False
    
    try:
        content = read_file(file_path)
        actual_checksum = calculate_checksum(content)
        return actual_checksum == expected_checksum
    except Exception:
        return False


def get_next_encrypted_filename(project_path: str = ".") -> str:
    """
    Find the next available encrypted filename with sequential numbering.
    
    Args:
        project_path: Project root path
        
    Returns:
        Next available encrypted filename
        
    Raises:
        OSError: If too many encrypted files (max 1000)
    """
    index = 0
    while index < 1000:  # Safety limit
        filename = f"voynich-{index}.encrypted"
        file_path = Path(project_path) / filename
        if not file_path.exists():
            return filename
        index += 1
    
    raise OSError("Too many encrypted files (max 1000)")


def get_existing_encrypted_files(project_path: str = ".") -> List[str]:
    """
    Get all existing encrypted files sorted by index.
    
    Args:
        project_path: Project root path
        
    Returns:
        List of encrypted filenames
    """
    files = []
    
    for index in range(1000):  # Safety limit
        filename = f"voynich-{index}.encrypted"
        file_path = Path(project_path) / filename
        if file_path.exists():
            files.append(filename)
    
    return files


def get_default_encrypted_filename(original_file: str) -> str:
    """
    Get default encrypted filename (finds next available number).
    
    Args:
        original_file: Original file path (for reference)
        
    Returns:
        Next available encrypted filename
    """
    return get_next_encrypted_filename(".")


def get_default_decrypted_filename(encrypted_file: str) -> str:
    """
    Get default decrypted filename for an encrypted file.
    
    Args:
        encrypted_file: Encrypted file path (should be voynich-X.encrypted)
        
    Returns:
        Default decrypted filename
    """
    import re
    
    # Default to .env for any voynich-X.encrypted file
    if re.match(r'^voynich-\d+\.encrypted$', encrypted_file):
        return '.env'
    
    # Fallback for other files
    path = Path(encrypted_file)
    return f"{path.stem}.decrypted"


def ensure_gitignore(project_path: str = ".") -> bool:
    """
    Ensure .gitignore contains necessary DevDotEnv entries.
    
    Args:
        project_path: Project root path
        
    Returns:
        True if .gitignore was updated, False if no update needed
    """
    gitignore_path = Path(project_path) / ".gitignore"
    
    required_entries = [
        '# DevDotEnv - never commit these files!',
        '.devdotenv.key',
        '.devdotenv.key.backup'
    ]
    
    existing_content = ""
    needs_update = False
    
    # Read existing .gitignore if it exists
    if gitignore_path.exists():
        existing_content = gitignore_path.read_text()
        
        # Check if our entries are missing
        for entry in required_entries:
            if entry != required_entries[0]:  # Skip comment line for search
                if entry.strip() not in existing_content:
                    needs_update = True
                    break
    else:
        needs_update = True
    
    if needs_update:
        new_content = existing_content
        
        # Add a section for DevDotEnv if not present
        if 'DevDotEnv' not in existing_content:
            if existing_content and not existing_content.endswith('\n'):
                new_content += '\n'
            new_content += '\n' + '\n'.join(required_entries) + '\n'
        
        gitignore_path.write_text(new_content)
        return True  # Updated
    
    return False  # No update needed


# Legacy functions for backward compatibility
def get_encrypted_file_path(original_file: str) -> str:
    """
    Get the standard encrypted file path for an original file.
    
    Args:
        original_file: Path to original file
        
    Returns:
        Path to encrypted file
    """
    return get_default_encrypted_filename(original_file)


def get_metadata_file_path(original_file: str) -> str:
    """
    Get the standard metadata file path for an original file.
    
    Args:
        original_file: Path to original file
        
    Returns:
        Path to metadata file
    """
    return f"{original_file}.meta" 