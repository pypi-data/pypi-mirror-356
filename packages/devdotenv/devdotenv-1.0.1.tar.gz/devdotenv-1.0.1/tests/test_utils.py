"""
Tests for utility functions
"""

import pytest
import tempfile
import os
from pathlib import Path
from src.utils import (
    get_next_encrypted_filename,
    get_existing_encrypted_files,
    ensure_gitignore,
    get_default_decrypted_filename
)


@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing"""
    with tempfile.TemporaryDirectory() as temp_dir:
        old_cwd = os.getcwd()
        os.chdir(temp_dir)
        yield temp_dir
        os.chdir(old_cwd)


def test_get_next_encrypted_filename_starts_at_zero(temp_dir):
    """Should start with voynich-0.encrypted"""
    filename = get_next_encrypted_filename('.')
    assert filename == 'voynich-0.encrypted'


def test_get_next_encrypted_filename_sequential(temp_dir):
    """Should return sequential filenames"""
    # Create some encrypted files
    Path('voynich-0.encrypted').touch()
    Path('voynich-1.encrypted').touch()
    
    filename = get_next_encrypted_filename('.')
    assert filename == 'voynich-2.encrypted'


def test_get_next_encrypted_filename_skips_gaps(temp_dir):
    """Should skip gaps and find next available number"""
    # Create files with gaps
    Path('voynich-0.encrypted').touch()
    Path('voynich-2.encrypted').touch()
    Path('voynich-4.encrypted').touch()
    
    filename = get_next_encrypted_filename('.')
    assert filename == 'voynich-1.encrypted'


def test_get_existing_encrypted_files_empty(temp_dir):
    """Should return empty list when no encrypted files exist"""
    files = get_existing_encrypted_files('.')
    assert files == []


def test_get_existing_encrypted_files_returns_sorted(temp_dir):
    """Should return encrypted files in sorted order"""
    # Create files in random order
    Path('voynich-2.encrypted').touch()
    Path('voynich-0.encrypted').touch()
    Path('voynich-1.encrypted').touch()
    
    files = get_existing_encrypted_files('.')
    assert files == ['voynich-0.encrypted', 'voynich-1.encrypted', 'voynich-2.encrypted']


def test_get_existing_encrypted_files_ignores_other_files(temp_dir):
    """Should ignore non-encrypted files"""
    Path('voynich-0.encrypted').touch()
    Path('other-file.txt').touch()
    Path('voynich-1.txt').touch()
    Path('voynich-1.encrypted').touch()
    
    files = get_existing_encrypted_files('.')
    assert files == ['voynich-0.encrypted', 'voynich-1.encrypted']


def test_get_default_decrypted_filename():
    """Should return .env for voynich files"""
    assert get_default_decrypted_filename('voynich-0.encrypted') == '.env'
    assert get_default_decrypted_filename('voynich-123.encrypted') == '.env'
    assert get_default_decrypted_filename('other.encrypted') == 'other.decrypted'


def test_ensure_gitignore_creates_new_file(temp_dir):
    """Should create .gitignore if it doesn't exist"""
    updated = ensure_gitignore('.')
    assert updated is True
    
    gitignore_path = Path('.gitignore')
    assert gitignore_path.exists()
    
    content = gitignore_path.read_text()
    assert '# DevDotEnv - never commit these files!' in content
    assert '.devdotenv.key' in content
    assert '.devdotenv.key.backup' in content


def test_ensure_gitignore_updates_existing_file(temp_dir):
    """Should update existing .gitignore"""
    # Create existing .gitignore
    gitignore_path = Path('.gitignore')
    gitignore_path.write_text('node_modules/\n*.log\n')
    
    updated = ensure_gitignore('.')
    assert updated is True
    
    content = gitignore_path.read_text()
    assert 'node_modules/' in content
    assert '*.log' in content
    assert '# DevDotEnv - never commit these files!' in content
    assert '.devdotenv.key' in content
    assert '.devdotenv.key.backup' in content


def test_ensure_gitignore_no_update_needed(temp_dir):
    """Should not update if entries already exist"""
    # Create .gitignore with DevDotEnv entries
    gitignore_path = Path('.gitignore')
    gitignore_path.write_text('''
node_modules/
*.log

# DevDotEnv - never commit these files!
.devdotenv.key
.devdotenv.key.backup
''')
    
    updated = ensure_gitignore('.')
    assert updated is False 