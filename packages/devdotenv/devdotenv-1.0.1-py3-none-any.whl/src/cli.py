"""
CLI interface for DevDotEnv
"""

import sys
import click
from pathlib import Path
from typing import Optional

from .key_manager import KeyManager
from .crypto import encrypt_data, decrypt_data
from .utils import (
    read_file, write_file, file_exists, get_file_size, format_file_size,
    get_next_encrypted_filename, get_existing_encrypted_files,
    get_default_encrypted_filename, get_default_decrypted_filename,
    ensure_gitignore, calculate_checksum
)

# Initialize colorama for Windows
try:
    import colorama
    colorama.init()
except ImportError:
    pass


def print_success(message: str) -> None:
    """Print success message in green"""
    click.echo(click.style(f"SUCCESS: {message}", fg='green'))


def print_error(message: str) -> None:
    """Print error message in red"""
    click.echo(click.style(f"ERROR: {message}", fg='red'), err=True)


def print_warning(message: str) -> None:
    """Print warning message in yellow"""
    click.echo(click.style(f"WARNING: {message}", fg='yellow'))


def print_info(message: str) -> None:
    """Print info message in blue"""
    click.echo(click.style(message, fg='blue'))


def print_gray(message: str) -> None:
    """Print info message in gray"""
    click.echo(click.style(message, fg='bright_black'))


@click.group()
@click.version_option(version="1.0.1")
def cli():
    """
    DevDotEnv - Secure .env file encryption/decryption tool
    
    A CLI tool for encrypting and decrypting environment files using
    AES-256-GCM encryption with optional custom obfuscation.
    
    WARNING: This tool is designed for development use only. For production
    environments, use dedicated secret management solutions.
    """
    pass


@cli.command()
@click.option('--key-file', '-k', default='.devdotenv.key', help='Path to key file')
@click.option('--force', '-f', is_flag=True, help='Overwrite existing key file')
def init(key_file: str, force: bool):
    """Initialize a new encryption key and setup .gitignore"""
    try:
        key_manager = KeyManager(key_file)
        
        if key_manager.key_exists() and not force:
            print_warning(f"WARNING: Key file already exists: {key_file}")
            print_warning("Use --force to overwrite the existing key")
            sys.exit(1)
        
        if force and key_manager.key_exists():
            key_manager.delete_key()
        
        # Generate new key
        key_manager.generate_and_save_key()
        
        # Update .gitignore
        gitignore_updated = ensure_gitignore('.')
        
        print_success("Encryption key generated successfully!")
        print_info(f"Key saved to: {key_file}")
        
        if gitignore_updated:
            print_info(".gitignore updated with DevDotEnv entries")
        else:
            print_gray(".gitignore already contains DevDotEnv entries")
        
        print_warning("WARNING: Keep this key file secure and never commit it to version control!")
        
        # Get key size for display
        key = key_manager.load_key()
        print_gray(f"Key size: {len(key) * 8} bits")
        
    except Exception as e:
        print_error(f"Failed to initialize key: {str(e)}")
        sys.exit(1)


@cli.command()
@click.argument('input_file', default='.env', type=click.Path())
@click.option('--key-file', '-k', default='.devdotenv.key', help='Path to key file')
@click.option('--no-obfuscation', is_flag=True, help='Disable custom obfuscation')
@click.option('--backup', '-b', is_flag=True, help='Create backup of original file')
def encrypt(input_file: str, key_file: str, no_obfuscation: bool, backup: bool):
    """Encrypt file to next available voynich-X.encrypted"""
    try:
        # Find next available encrypted filename
        output_file = get_next_encrypted_filename('.')
        use_obfuscation = not no_obfuscation
        
        # Check if input file exists
        if not file_exists(input_file):
            print_error(f"Input file not found: {input_file}")
            sys.exit(1)
        
        # Load encryption key
        key_manager = KeyManager(key_file)
        if not key_manager.key_exists():
            print_error(f"Key file not found: {key_file}")
            print_warning("Run 'devdotenv init' to create a new key")
            sys.exit(1)
        
        key = key_manager.load_key()
        
        # Create backup if requested
        if backup:
            from datetime import datetime
            timestamp = datetime.now().isoformat().replace(':', '-').replace('.', '-')
            backup_path = f"{input_file}.backup-{timestamp}"
            content = read_file(input_file)
            write_file(backup_path, content)
            print_info(f"Backup created: {backup_path}")
        
        # Read and encrypt the file
        content = read_file(input_file)
        encrypted_content = encrypt_data(content, key, use_obfuscation)
        
        # Write encrypted content
        write_file(output_file, encrypted_content)
        
        # Update .gitignore to ensure encrypted files are ignored
        ensure_gitignore('.')
        
        print_success("File encrypted successfully!")
        print_info(f"Input:  {input_file} ({len(content)} bytes)")
        print_info(f"Output: {output_file} ({len(encrypted_content)} bytes)")
        print_gray(f"Obfuscation: {'enabled' if use_obfuscation else 'disabled'}")
        
    except Exception as e:
        print_error(f"Failed to encrypt file: {str(e)}")
        sys.exit(1)


@cli.command()
@click.argument('input_file', required=False)
@click.argument('output_file', default='.env', required=False)
@click.option('--key-file', '-k', default='.devdotenv.key', help='Path to key file')
@click.option('--backup', '-b', is_flag=True, help='Create backup of existing output file')
@click.option('--verify', is_flag=True, help='Verify integrity without writing output')
@click.option('--list', 'list_files', is_flag=True, help='List all available encrypted files')
def decrypt(input_file: Optional[str], output_file: str, key_file: str, 
           backup: bool, verify: bool, list_files: bool):
    """Decrypt specified voynich-X.encrypted file"""
    try:
        # List available encrypted files if requested
        if list_files:
            encrypted_files = get_existing_encrypted_files('.')
            if not encrypted_files:
                print_warning("No encrypted files found.")
                print_gray("Run 'devdotenv encrypt [file]' to create one.")
            else:
                print_info("Available encrypted files:")
                for file in encrypted_files:
                    print_gray(f"  {file}")
            return
        
        # Auto-detect input file if not provided
        final_input_file = input_file
        if not final_input_file:
            encrypted_files = get_existing_encrypted_files('.')
            if not encrypted_files:
                print_error("No encrypted files found")
                print_warning("Run 'devdotenv encrypt [file]' first to create an encrypted file")
                sys.exit(1)
            elif len(encrypted_files) == 1:
                final_input_file = encrypted_files[0]
                print_gray(f"Auto-detected: {final_input_file}")
            else:
                print_error("Multiple encrypted files found, please specify which one:")
                for file in encrypted_files:
                    print_gray(f"  devdotenv decrypt {file}")
                print_warning("Or use --list to see all available files")
                sys.exit(1)
        
        # Check if input file exists
        if not file_exists(final_input_file):
            print_error(f"Encrypted file not found: {final_input_file}")
            print_warning("Use --list to see available encrypted files")
            sys.exit(1)
        
        # Load encryption key
        key_manager = KeyManager(key_file)
        if not key_manager.key_exists():
            print_error(f"Key file not found: {key_file}")
            sys.exit(1)
        
        key = key_manager.load_key()
        
        # Read and decrypt the file
        encrypted_content = read_file(final_input_file)
        decrypted_content = decrypt_data(encrypted_content, key)
        
        if verify:
            print_success("File verification successful!")
            print_info("Metadata:")
            print_gray(f"   Original size: {len(decrypted_content)} bytes")
            print_gray(f"   Encrypted size: {len(encrypted_content)} bytes")
            checksum = calculate_checksum(decrypted_content)
            print_gray(f"   Checksum: {checksum[:16]}...")
            return
        
        # Create backup if requested and output file exists
        if backup and file_exists(output_file):
            from datetime import datetime
            timestamp = datetime.now().isoformat().replace(':', '-').replace('.', '-')
            backup_path = f"{output_file}.backup-{timestamp}"
            existing_content = read_file(output_file)
            write_file(backup_path, existing_content)
            print_info(f"Backup created: {backup_path}")
        
        # Write decrypted content
        write_file(output_file, decrypted_content)
        
        print_success("File decrypted successfully!")
        print_info(f"Input:  {final_input_file}")
        print_info(f"Output: {output_file} ({len(decrypted_content)} bytes)")
        
    except Exception as e:
        print_error(f"Failed to decrypt file: {str(e)}")
        sys.exit(1)


@cli.command()
@click.option('--key-file', '-k', default='.devdotenv.key', help='Path to key file')
def status(key_file: str):
    """Check status and integrity of encryption files"""
    try:
        print_info("DevDotEnv Status Report")
        print_gray("======================")
        
        # Check key file
        key_manager = KeyManager(key_file)
        if key_manager.key_exists():
            print_success(f"[OK] Key file: {key_file}")
            try:
                key = key_manager.load_key()
                print_gray(f"     Size: {len(key) * 8} bits")
            except Exception as e:
                print_error(f"     Error: {str(e)}")
        else:
            print_error(f"[MISSING] Key file: {key_file}")
        
        # Check encrypted files
        encrypted_files = get_existing_encrypted_files('.')
        if encrypted_files:
            print_info(f"[OK] Found {len(encrypted_files)} encrypted file(s):")
            for file in encrypted_files:
                if file_exists(file):
                    size = get_file_size(file)
                    print_info(f"     {file} ({format_file_size(size)})")
                    
                    # Try to verify integrity if key exists
                    if key_manager.key_exists():
                        try:
                            key = key_manager.load_key()
                            encrypted_content = read_file(file)
                            decrypted_content = decrypt_data(encrypted_content, key)
                            checksum = calculate_checksum(decrypted_content)
                            print_gray(f"       Integrity: OK")
                            print_gray(f"       Checksum: {checksum[:16]}...")
                        except Exception as e:
                            print_error(f"       Integrity: FAILED ({str(e)})")
        else:
            print_warning("[WARNING] No encrypted files found")
            print_gray("         Run 'devdotenv encrypt [file]' to create encrypted files")
        
    except Exception as e:
        print_error(f"Failed to check status: {str(e)}")
        sys.exit(1)


def main():
    """Main CLI entry point"""
    if len(sys.argv) == 1:
        # No arguments provided, show help and examples
        ctx = click.Context(cli)
        click.echo(ctx.get_help())
        click.echo()
        print_info("Quick start:")
        print_gray("  devdotenv init                        # Initialize key and .gitignore")
        print_gray("  devdotenv encrypt .env                # Encrypt .env to voynich-0.encrypted")
        print_gray("  devdotenv encrypt .env.production     # Encrypt to voynich-1.encrypted")
        print_gray("  devdotenv decrypt                     # Auto-decrypt if only one file")
        print_gray("  devdotenv decrypt --list              # List all encrypted files")
        print_gray("  devdotenv decrypt voynich-1.encrypted # Decrypt specific file")
    else:
        cli()


if __name__ == "__main__":
    main() 