"""Compile + deploy CertificateRegistry. Run from project root: python -m scripts.deploy"""
import json
from solcx import compile_source, install_solc
from web3 import Web3
from core import config

install_solc("0.8.20")
src = (config.ROOT / "contracts" / "CertificateRegistry.sol").read_text()
out = compile_source(src, output_values=["abi", "bin"], solc_version="0.8.20")
_, iface = out.popitem()
config.ABI_PATH.write_text(json.dumps(iface["abi"], indent=2))

w3 = Web3(Web3.HTTPProvider(config.RPC_URL))
acct = w3.eth.account.from_key(config.PRIVATE_KEY)
C = w3.eth.contract(abi=iface["abi"], bytecode=iface["bin"])
tx = C.constructor().build_transaction({"from": acct.address, "nonce": w3.eth.get_transaction_count(acct.address),
                                        "chainId": config.CHAIN_ID, "gasPrice": w3.eth.gas_price})
h = w3.eth.send_raw_transaction(acct.sign_transaction(tx).raw_transaction)
r = w3.eth.wait_for_transaction_receipt(h, timeout=180)
print("Deployed at:", r.contractAddress, "| gas used:", r.gasUsed)
print("Put this in .env as CONTRACT_ADDRESS")
