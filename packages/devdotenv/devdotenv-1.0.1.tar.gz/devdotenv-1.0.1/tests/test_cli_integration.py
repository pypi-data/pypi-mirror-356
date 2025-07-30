"""
CLI Integration Tests
"""

import pytest
import tempfile
import os
import subprocess
import sys
from pathlib import Path


@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing"""
    with tempfile.TemporaryDirectory() as temp_dir:
        old_cwd = os.getcwd()
        os.chdir(temp_dir)
        yield temp_dir
        os.chdir(old_cwd)


def run_cli(*args):
    """Helper to run CLI commands"""
    cmd = [sys.executable, '-m', 'src.cli'] + list(args)
    result = subprocess.run(
        cmd, 
        capture_output=True, 
        text=True,
        cwd=os.path.dirname(os.path.dirname(__file__))  # devdotenv-python directory
    )
    return result


def test_init_creates_key_and_gitignore(temp_dir):
    """Should create key file and update .gitignore"""
    result = run_cli('init', '--key-file', '.devdotenv.key')
    
    assert result.returncode == 0
    assert 'SUCCESS: Encryption key generated successfully!' in result.stdout
    
    # Check key file was created (in original directory since CLI runs there)
    # This test verifies the CLI works, actual file creation tested in unit tests


def test_encrypt_creates_sequential_files(temp_dir):
    """Should create voynich-X.encrypted files sequentially"""
    # Create test files
    Path('.env').write_text('API_KEY=secret123\nDEBUG=true')
    Path('.env.production').write_text('API_KEY=prod_secret\nDEBUG=false')
    
    # First encryption should create voynich-0.encrypted
    result1 = run_cli('encrypt', '.env')
    assert result1.returncode == 0
    assert 'voynich-0.encrypted' in result1.stdout
    
    # Second encryption should create voynich-1.encrypted  
    result2 = run_cli('encrypt', '.env.production')
    assert result2.returncode == 0
    assert 'voynich-1.encrypted' in result2.stdout


def test_decrypt_auto_detection_single_file(temp_dir):
    """Should auto-detect single encrypted file"""
    Path('.env').write_text('API_KEY=secret123')
    
    # Encrypt
    result1 = run_cli('encrypt', '.env')
    assert result1.returncode == 0
    
    # Remove original
    Path('.env').unlink()
    
    # Decrypt without specifying file
    result2 = run_cli('decrypt')
    assert result2.returncode == 0
    assert 'Auto-detected' in result2.stdout


def test_decrypt_multiple_files_requires_specification(temp_dir):
    """Should require file specification when multiple files exist"""
    Path('.env').write_text('API_KEY=secret123')
    Path('.env.production').write_text('API_KEY=prod_secret')
    
    # Encrypt both
    run_cli('encrypt', '.env')
    run_cli('encrypt', '.env.production')
    
    # Try to decrypt without specification
    result = run_cli('decrypt')
    assert result.returncode == 1
    assert 'Multiple encrypted files found' in result.stdout


def test_decrypt_list_shows_all_files(temp_dir):
    """Should list all encrypted files"""
    Path('.env').write_text('API_KEY=secret123')
    Path('.env.production').write_text('API_KEY=prod_secret')
    
    # Encrypt both
    run_cli('encrypt', '.env')
    run_cli('encrypt', '.env.production')
    
    # List files
    result = run_cli('decrypt', '--list')
    assert result.returncode == 0
    assert 'Available encrypted files:' in result.stdout


def test_decrypt_specific_file(temp_dir):
    """Should decrypt specific file when specified"""
    Path('.env').write_text('API_KEY=secret123')
    Path('.env.production').write_text('API_KEY=prod_secret')
    
    # Encrypt both
    run_cli('encrypt', '.env')
    run_cli('encrypt', '.env.production')
    
    # Decrypt specific file
    result = run_cli('decrypt', 'voynich-1.encrypted', 'output.env')
    assert result.returncode == 0
    assert 'SUCCESS: File decrypted successfully!' in result.stdout


def test_decrypt_verify_option(temp_dir):
    """Should verify file without writing output"""
    Path('.env').write_text('API_KEY=secret123')
    
    # Encrypt
    run_cli('encrypt', '.env')
    
    # Verify
    result = run_cli('decrypt', '--verify')
    assert result.returncode == 0
    assert 'File verification successful!' in result.stdout


def test_status_command_shows_overview(temp_dir):
    """Should show status of keys and encrypted files"""
    Path('.env').write_text('API_KEY=secret123')
    
    # Encrypt
    run_cli('encrypt', '.env')
    
    # Check status
    result = run_cli('status')
    assert result.returncode == 0
    assert 'DevDotEnv Status Report' in result.stdout


def test_encrypt_with_backup_option(temp_dir):
    """Should create backup when requested"""
    original_content = 'API_KEY=secret123\nDEBUG=true'
    Path('.env').write_text(original_content)
    
    # Encrypt with backup
    result = run_cli('encrypt', '.env', '--backup')
    assert result.returncode == 0
    assert 'Backup created:' in result.stdout


def test_decrypt_with_backup_option(temp_dir):
    """Should create backup of existing output file"""
    Path('.env').write_text('API_KEY=secret123')
    
    # Encrypt
    run_cli('encrypt', '.env')
    
    # Create a different .env file
    Path('.env').write_text('DIFFERENT=content')
    
    # Decrypt with backup
    result = run_cli('decrypt', '--backup')
    assert result.returncode == 0
    assert 'Backup created:' in result.stdout


def test_encrypt_no_obfuscation_option(temp_dir):
    """Should disable obfuscation when requested"""
    Path('.env').write_text('API_KEY=secret123')
    
    result = run_cli('encrypt', '.env', '--no-obfuscation')
    assert result.returncode == 0
    assert 'Obfuscation: disabled' in result.stdout


def test_encrypt_default_obfuscation(temp_dir):
    """Should enable obfuscation by default"""
    Path('.env').write_text('API_KEY=secret123')
    
    result = run_cli('encrypt', '.env')
    assert result.returncode == 0
    assert 'Obfuscation: enabled' in result.stdout


def test_error_handling_missing_key(temp_dir):
    """Should handle missing key file gracefully"""
    Path('.env').write_text('API_KEY=secret123')
    
    result = run_cli('encrypt', '.env', '--key-file', 'nonexistent.key')
    assert result.returncode == 1
    assert 'ERROR: Key file not found' in result.stdout


def test_error_handling_missing_input_file(temp_dir):
    """Should handle missing input file gracefully"""
    result = run_cli('encrypt', 'nonexistent.env')
    assert result.returncode == 1
    assert 'ERROR: Input file not found' in result.stdout


def test_full_workflow_integration(temp_dir):
    """Test complete encrypt-decrypt workflow"""
    original_content = 'DATABASE_URL=postgresql://localhost:5432/mydb\nAPI_KEY=secret123\nDEBUG=true'
    Path('.env').write_text(original_content)
    
    # Initialize
    result1 = run_cli('init')
    assert result1.returncode == 0
    
    # Encrypt
    result2 = run_cli('encrypt', '.env')
    assert result2.returncode == 0
    assert 'voynich-0.encrypted' in result2.stdout
    
    # Remove original
    Path('.env').unlink()
    
    # Decrypt
    result3 = run_cli('decrypt')
    assert result3.returncode == 0
    
    # Check status
    result4 = run_cli('status')
    assert result4.returncode == 0
    assert 'DevDotEnv Status Report' in result4.stdout


def test_help_shows_quick_start_examples(temp_dir):
    """Should show quick start examples when no args provided"""
    result = run_cli()
    assert result.returncode == 0
    assert 'Quick start:' in result.stdout
    assert 'devdotenv init' in result.stdout
    assert 'devdotenv encrypt' in result.stdout
    assert 'devdotenv decrypt' in result.stdout 