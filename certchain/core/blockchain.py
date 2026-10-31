"""FEATURE 5: Blockchain bridge (web3.py). Read = free eth_call, write = signed tx."""
import json
from web3 import Web3
from . import config
from .hashing import hex_to_bytes32

class ChainError(Exception): ...

def _contract():
    if not config.CONTRACT_ADDRESS:
        raise ChainError("CONTRACT_ADDRESS missing. Run: python -m scripts.deploy")
    w3 = Web3(Web3.HTTPProvider(config.RPC_URL, request_kwargs={"timeout": 20}))
    abi = json.loads(config.ABI_PATH.read_text())
    return w3, w3.eth.contract(address=Web3.to_checksum_address(config.CONTRACT_ADDRESS), abi=abi)

def verify(cert_hash: str) -> dict:
    """Gasless. Returns {exists, revoked, usn, cid, issued_at, revoked_at}."""
    _, c = _contract()
    ex, rev, usn, cid, ts, rts = c.functions.verifyCertificate(hex_to_bytes32(cert_hash)).call()
    return dict(exists=ex, revoked=rev, usn=usn, cid=cid, issued_at=ts, revoked_at=rts)

def hash_for_usn(usn: str):
    _, c = _contract()
    b = c.functions.latestHashOfUSN(usn).call()
    return None if int.from_bytes(b, "big") == 0 else "0x" + b.hex()

def _send(fn) -> dict:
    if not config.PRIVATE_KEY:
        raise ChainError("PRIVATE_KEY missing in .env")
    w3, _ = _contract()
    acct = w3.eth.account.from_key(config.PRIVATE_KEY)
    try:
        tx = fn.build_transaction({
            "from": acct.address, "nonce": w3.eth.get_transaction_count(acct.address),
            "chainId": config.CHAIN_ID, "gasPrice": w3.eth.gas_price})
        signed = acct.sign_transaction(tx)
        h = w3.eth.send_raw_transaction(signed.raw_transaction)
        rcpt = w3.eth.wait_for_transaction_receipt(h, timeout=120)
    except Exception as e:
        raise ChainError(f"Transaction failed: {e}") from e
    return dict(tx_hash=h.hex(), block=rcpt.blockNumber, gas_used=rcpt.gasUsed, ok=rcpt.status == 1)

def issue(cert_hash: str, usn: str, cid: str) -> dict:
    _, c = _contract()
    return _send(c.functions.issueCertificate(hex_to_bytes32(cert_hash), usn, cid))

def revoke(cert_hash: str) -> dict:
    _, c = _contract()
    return _send(c.functions.revokeCertificate(hex_to_bytes32(cert_hash)))
