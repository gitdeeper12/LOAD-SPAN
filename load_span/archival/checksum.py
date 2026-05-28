"""SHA-256 tamper-evidence layer for data integrity."""

import hashlib
from pathlib import Path
from typing import str


def compute_checksum(filepath: str, algorithm: str = "sha256") -> str:
    """Compute file checksum for integrity verification."""
    hash_func = hashlib.new(algorithm)
    
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_func.update(chunk)
    
    return hash_func.hexdigest()


def verify_integrity(filepath: str, expected_checksum: str) -> bool:
    """Verify file integrity against expected checksum."""
    actual = compute_checksum(filepath)
    return actual == expected_checksum
