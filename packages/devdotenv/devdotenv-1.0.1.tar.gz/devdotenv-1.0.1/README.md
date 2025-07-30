# DevDotEnv (Python Version)

A secure CLI tool for encrypting and decrypting .env files using AES-256-GCM encryption with optional custom obfuscation.

## Features

- **AES-256-GCM Encryption**: Military-grade encryption with authenticated encryption
- **Custom Obfuscation**: Optional XOR + byte shuffling for additional security layer
- **Key Management**: Secure 256-bit Base64 key storage in `.devdotenv.key`
- **File Integrity**: SHA-256 checksums for data integrity verification
- **Metadata Tracking**: Detailed encryption metadata with timestamps
- **Cross-Platform**: Works on Windows, macOS, and Linux

## Installation

### Using uv (Recommended)

```bash
# Install from source
git clone https://github.com/guinat/devdotenv-python.git
cd devdotenv-python
uv sync
uv run devdotenv --help
```

### Using pip

```bash
# Install from source
git clone https://github.com/guinat/devdotenv-python.git
cd devdotenv-python
pip install -e .
devdotenv --help
```

## Quick Start

```bash
# 1. Initialize encryption key
devdotenv init

# 2. Encrypt your .env file
devdotenv encrypt .env

# 3. Check status
devdotenv status .env

# 4. Decrypt when needed
devdotenv decrypt .env.encrypted
```

## Commands

### `devdotenv init`

Initialize a new encryption key.

```bash
devdotenv init                    # Create .devdotenv.key
devdotenv init --force            # Overwrite existing key
devdotenv init --key-file my.key  # Use custom key file
```

### `devdotenv encrypt`

Encrypt a file.

```bash
devdotenv encrypt .env                           # Encrypt to .env.encrypted
devdotenv encrypt .env --output secret.enc      # Custom output file
devdotenv encrypt .env --custom-obfuscation     # Enable custom obfuscation
devdotenv encrypt .env --force                  # Overwrite existing file
```

### `devdotenv decrypt`

Decrypt a file.

```bash
devdotenv decrypt .env.encrypted                # Auto-detect output name
devdotenv decrypt .env.encrypted --output .env # Specify output file
devdotenv decrypt secret.enc --force           # Overwrite existing file
```

### `devdotenv rotate`

Generate a new encryption key (makes existing encrypted files unreadable).

```bash
devdotenv rotate                    # Rotate default key
devdotenv rotate --key-file my.key  # Rotate custom key
```

### `devdotenv status`

Show encryption status and file integrity.

```bash
devdotenv status           # Show general status
devdotenv status .env      # Check specific file
```

## Security Features

### Encryption Algorithm

- **AES-256-GCM**: Authenticated encryption providing both confidentiality and integrity
- **Random IV**: 96-bit initialization vector generated for each encryption
- **Authentication Tag**: 128-bit tag for tampering detection

### Custom Obfuscation (Optional)

- **XOR Encryption**: Data XORed with HMAC-derived key
- **Byte Shuffling**: Deterministic Fisher-Yates shuffle using HMAC-derived seed
- **Key Derivation**: HMAC-SHA256 for generating obfuscation keys

### File Format

```
[4 bytes: Version][1 byte: Flags][12 bytes: IV][16 bytes: Auth Tag][Encrypted Data]
```

## Configuration

### Key File Location

- Default: `.devdotenv.key` in current directory
- Custom: Use `--key-file` option
- Permissions: Automatically set to 600 (owner read/write only) on Unix systems

### Environment Variables

- `DEVDOTENV_KEY_FILE`: Default key file path
- `DEVDOTENV_FORCE`: Skip confirmation prompts (set to "1")

## Development

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/guinat/devdotenv-python.git
cd devdotenv-python

# Install with development dependencies
uv sync --extra dev

# Run tests
uv run pytest

# Run linting
uv run black .
uv run isort .
uv run flake8
uv run mypy devdotenv
```

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=devdotenv --cov-report=html

# Run specific test file
uv run pytest tests/test_crypto.py
```

## Security Considerations

### Development Use Only

This tool is designed for development environments. For production use:

- Use dedicated secret management solutions (AWS Secrets Manager, HashiCorp Vault, etc.)
- Implement proper key rotation policies
- Use hardware security modules (HSMs) for key storage

### Best Practices

1. **Never commit** `.devdotenv.key` to version control
2. **Backup keys securely** in a separate location
3. **Rotate keys regularly** in development environments
4. **Use strong access controls** on key files
5. **Monitor key file access** and modifications

### Known Limitations

- Keys stored in plaintext files (Base64 encoded)
- No built-in key derivation from passwords
- No network-based key management
- Custom obfuscation provides limited additional security

## File Structure

```
devdotenv/
├── devdotenv/
│   ├── __init__.py         # Package initialization
│   ├── cli.py              # Command-line interface
│   ├── crypto.py           # Encryption/decryption functions
│   ├── key_manager.py      # Key management
│   └── utils.py            # Utility functions
├── tests/                  # Test files
├── pyproject.toml          # Project configuration
├── README.md               # This file
└── .gitignore              # Git ignore rules
```

## Troubleshooting

### Common Issues

**Key file not found**

```bash
ERROR: Key file not found: .devdotenv.key
# Solution: Run `devdotenv init` to create a new key
```

**Permission denied**

```bash
ERROR: Failed to create key file: Permission denied
# Solution: Check directory permissions or use different location
```

**Invalid encrypted file**

```bash
ERROR: Invalid encrypted data format
# Solution: Verify file integrity, may be corrupted
```

**Decryption failed**

```bash
ERROR: Decryption failed: authentication tag verification failed
# Solution: Check if correct key is being used
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Make your changes
4. Add tests for new functionality
5. Run the test suite (`uv run pytest`)
6. Run linting (`uv run black . && uv run isort . && uv run flake8`)
7. Commit your changes (`git commit -am 'Add new feature'`)
8. Push to the branch (`git push origin feature/new-feature`)
9. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Changelog

### v1.0.0

- Initial Python implementation
- AES-256-GCM encryption
- Custom obfuscation support
- CLI interface with Click
- Comprehensive test suite
- Cross-platform support

## Acknowledgments

- [cryptography](https://cryptography.io/) - Python cryptographic library
- [click](https://click.palletsprojects.com/) - Command-line interface framework
- [colorama](https://pypi.org/project/colorama/) - Cross-platform colored terminal output
