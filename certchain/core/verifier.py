"""FEATURE 7: Verification logic (hashing + blockchain + audit). No UI code here."""
from . import blockchain, audit
from .hashing import sha256_hex

def verify_pdf(pdf_bytes: bytes) -> dict:
    h = sha256_hex(pdf_bytes)
    try:
        r = blockchain.verify(h)
    except Exception as e:
        audit.log("pdf", "ERROR", h, detail=str(e)[:200]); raise
    verdict = "NOT_FOUND" if not r["exists"] else ("REVOKED" if r["revoked"] else "GENUINE")
    audit.log("pdf", verdict, h, r["usn"])
    return dict(verdict=verdict, hash=h, **r)

def verify_usn(usn: str) -> dict:
    h = blockchain.hash_for_usn(usn)
    if not h:
        audit.log("qr", "NOT_FOUND", usn=usn); return dict(verdict="NOT_FOUND", hash=None)
    r = blockchain.verify(h)
    verdict = "REVOKED" if r["revoked"] else "GENUINE"
    audit.log("qr", verdict, h, usn)
    return dict(verdict=verdict, hash=h, **r)
