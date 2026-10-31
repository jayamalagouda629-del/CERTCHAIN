import time
import streamlit as st
from core import verifier, ipfs

st.title("🔍 Verifier Portal (no wallet, no gas)")
MSG = {"GENUINE": ("success", "✅ GENUINE: hash matches the on-chain record."),
       "REVOKED": ("error", "⛔ REVOKED: this certificate was cancelled by the institution."),
       "NOT_FOUND": ("error", "❌ FORGED / TAMPERED / NOT ISSUED: no matching record on-chain.")}

def show(r, secs):
    getattr(st, MSG[r["verdict"]][0])(MSG[r["verdict"]][1])
    st.caption(f"Checked in {secs:.2f}s")
    if r.get("exists"):
        st.write(f"**USN:** {r['usn']}  |  **Issued (unix):** {r['issued_at']}")
        st.markdown(f"[View original on IPFS]({ipfs.gateway_url(r['cid'])})")
    if r.get("hash"):
        st.code(r["hash"])

usn_q = st.query_params.get("usn")
tab1, tab2 = st.tabs(["Upload PDF", "QR / USN lookup"])
with tab1:
    f = st.file_uploader("Drop certificate PDF", type="pdf")
    if f:
        t = time.time()
        try: show(verifier.verify_pdf(f.getvalue()), time.time() - t)
        except Exception as e: st.error(f"Could not reach blockchain: {e}")
with tab2:
    usn = st.text_input("USN (auto-filled from QR link)", usn_q or "")
    if usn:
        t = time.time()
        try: show(verifier.verify_usn(usn.strip()), time.time() - t)
        except Exception as e: st.error(f"Could not reach blockchain: {e}")
    st.caption("QR lookup shows on-chain status. For tamper detection, also upload the PDF.")
