# CertChain: Blockchain-Based Academic Certificate Verification

## Module map (each feature = one file, fix errors in one place)
| Feature | File | Test it alone |
|---|---|---|
| Config | core/config.py | `python -c "from core import config; print(config.RPC_URL)"` |
| SHA-256 | core/hashing.py | `pytest tests -k hash` |
| QR | core/qr.py | `python -c "from core.qr import make_qr_image as m; m('1MV25MC030').save('qr.png')"` |
| PDF | core/pdf_generator.py | `pytest tests -k pdf` |
| IPFS | core/ipfs.py | check PINATA_JWT, pin a test PDF |
| Blockchain | core/blockchain.py + contracts/ | deploy, then call verify() |
| Audit | core/audit.py | open data/audit.db |
| Verify logic | core/verifier.py | called by pages/2_Verifier.py |
| UI | app.py, pages/ | `streamlit run app.py` |

## Setup
1. `python -m venv venv && source venv/bin/activate` (Windows: `venv\Scripts\activate`)
2. `pip install -r requirements.txt`
3. `cp .env.example .env`, then fill PRIVATE_KEY (MetaMask test wallet only), PINATA_JWT, ADMIN_PASSWORD
4. Get free test POL from the Polygon Amoy faucet
5. `python -m scripts.deploy`, then copy the printed address into .env as CONTRACT_ADDRESS
6. `pytest tests`, then `streamlit run app.py`

## Debug order if something fails
Step 1 PDF/hash (pytest) -> Step 2 IPFS -> Step 3 deploy -> Step 4 issue -> Step 5 verify.

## Before going public
- Use a dedicated issuer wallet; never reuse a personal wallet key.
- Deploy to Streamlit Cloud/Render and set VERIFY_BASE_URL to the public URL so QR codes work.
- Moving from Amoy testnet to Polygon mainnet costs real (small) gas.
