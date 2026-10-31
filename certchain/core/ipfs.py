"""FEATURE 4: IPFS pinning via Pinata. Only talks to Pinata; nothing else."""
import requests
from . import config

class IPFSError(Exception): ...

def pin_pdf(pdf_bytes: bytes, filename: str) -> str:
    if not config.PINATA_JWT:
        raise IPFSError("PINATA_JWT missing in .env")
    r = requests.post(
        "https://api.pinata.cloud/pinning/pinFileToIPFS",
        headers={"Authorization": f"Bearer {config.PINATA_JWT}"},
        files={"file": (filename, pdf_bytes, "application/pdf")}, timeout=60)
    if r.status_code != 200:
        raise IPFSError(f"Pinata error {r.status_code}: {r.text[:200]}")
    return r.json()["IpfsHash"]

def gateway_url(cid: str) -> str:
    return config.IPFS_GATEWAY + cid
