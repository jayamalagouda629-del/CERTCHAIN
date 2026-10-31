"""FEATURE 1: SHA-256 hashing. Pure functions, no network."""
import hashlib

def sha256_hex(data: bytes) -> str:
    """Return 0x-prefixed 64-char hex digest (matches Solidity bytes32)."""
    return "0x" + hashlib.sha256(data).hexdigest()

def hex_to_bytes32(h: str) -> bytes:
    b = bytes.fromhex(h[2:] if h.startswith("0x") else h)
    if len(b) != 32:
        raise ValueError("Hash must be 32 bytes")
    return b
