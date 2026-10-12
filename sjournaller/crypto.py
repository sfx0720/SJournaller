"""
Encryption / decryption helpers built on top of the *cryptography* library.

- PBKDF2-HMAC-SHA256 key derivation → Fernet symmetric encryption
- Separate password hashing for config-storage verification
- File-level encrypt / decrypt for the SQLite database
"""

import os
import base64
import hashlib

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

from sjournaller.constants import PBKDF2_ITERATIONS, SALT_LENGTH


# ── Key derivation ────────────────────────────────────────

def derive_key(password: str, salt: bytes) -> bytes:
    """Derive a Fernet-compatible 32-byte key from *password* + *salt*."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=PBKDF2_ITERATIONS,
    )
    raw = kdf.derive(password.encode("utf-8"))
    return base64.urlsafe_b64encode(raw)


def generate_salt() -> bytes:
    return os.urandom(SALT_LENGTH)


# ── Fernet encrypt / decrypt ──────────────────────────────

def encrypt_data(data: bytes, key: bytes) -> bytes:
    return Fernet(key).encrypt(data)


def decrypt_data(data: bytes, key: bytes) -> bytes:
    return Fernet(key).decrypt(data)


def encrypt_file(src: str, dst: str, key: bytes) -> None:
    with open(src, "rb") as f:
        plaintext = f.read()
    with open(dst, "wb") as f:
        f.write(encrypt_data(plaintext, key))


def decrypt_file(src: str, dst: str, key: bytes) -> None:
    with open(src, "rb") as f:
        ciphertext = f.read()
    with open(dst, "wb") as f:
        f.write(decrypt_data(ciphertext, key))


# ── Password hashing (for config verification) ───────────

def hash_password(password: str, salt: bytes | None = None) -> tuple[str, str]:
    """Return *(hash_hex, salt_hex)* for storage in config."""
    if salt is None:
        salt = generate_salt()
    h = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, PBKDF2_ITERATIONS
    )
    return h.hex(), salt.hex()


def verify_password(password: str, hash_hex: str, salt_hex: str) -> bool:
    salt = bytes.fromhex(salt_hex)
    h = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, PBKDF2_ITERATIONS
    )
    return h.hex() == hash_hex