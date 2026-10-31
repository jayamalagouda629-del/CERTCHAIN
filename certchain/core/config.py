"""FEATURE 0: Central configuration. Every other module reads settings only from here."""
import os
from pathlib import Path
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

RPC_URL = os.getenv("RPC_URL", "https://rpc-amoy.polygon.technology")
CHAIN_ID = int(os.getenv("CHAIN_ID", "80002"))
PRIVATE_KEY = os.getenv("PRIVATE_KEY", "")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS", "")
PINATA_JWT = os.getenv("PINATA_JWT", "")
IPFS_GATEWAY = os.getenv("IPFS_GATEWAY", "https://gateway.pinata.cloud/ipfs/")
VERIFY_BASE_URL = os.getenv("VERIFY_BASE_URL", "http://localhost:8501")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "")
INSTITUTION_NAME = os.getenv("INSTITUTION_NAME", "Sir M. Visvesvaraya Institute of Technology")
ABI_PATH = ROOT / "build" / "CertificateRegistry.abi.json"
DB_PATH = ROOT / "data" / "audit.db"
