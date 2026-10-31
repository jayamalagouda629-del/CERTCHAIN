import streamlit as st
from core import config, blockchain, ipfs, audit
from core.hashing import sha256_hex
from core.pdf_generator import StudentData, generate_certificate

st.title("🏛️ Issuer Portal")
if not config.ADMIN_PASSWORD:
    st.error("Set ADMIN_PASSWORD in .env"); st.stop()
if st.sidebar.text_input("Admin password", type="password") != config.ADMIN_PASSWORD:
    st.info("Enter admin password in the sidebar."); st.stop()

issue_tab, revoke_tab = st.tabs(["Issue certificate", "Revoke certificate"])
with issue_tab:
    with st.form("f"):
        usn = st.text_input("USN"); name = st.text_input("Full name")
        program = st.text_input("Program", "Master of Computer Applications")
        credits = st.number_input("Total credits", 1, 300, 80)
        cgpa = st.number_input("CGPA", 0.0, 10.0, 8.0, 0.01)
        grad = st.date_input("Graduation date")
        go = st.form_submit_button("Generate, pin & anchor")
    if go:
        if not usn or not name:
            st.error("USN and name required"); st.stop()
        try:
            pdf = generate_certificate(StudentData(usn.strip(), name.strip(), program, int(credits), float(cgpa), str(grad)))
            h = sha256_hex(pdf); st.success(f"1/3 PDF built. Hash: {h}")
            cid = ipfs.pin_pdf(pdf, f"{usn}.pdf"); st.success(f"2/3 Pinned to IPFS: {cid}")
            res = blockchain.issue(h, usn.strip(), cid)
            st.success(f"3/3 Anchored in block {res['block']} (gas {res['gas_used']})")
            audit.log("issue", "OK", h, usn.strip(), res["tx_hash"])
            st.download_button("Download certificate PDF", pdf, f"{usn}.pdf", "application/pdf")
        except Exception as e:
            audit.log("issue", "ERROR", usn=usn, detail=str(e)[:200]); st.error(str(e))
with revoke_tab:
    rh = st.text_input("Certificate hash (0x...)")
    if st.button("Revoke") and rh:
        try:
            res = blockchain.revoke(rh.strip()); audit.log("revoke", "OK", rh, detail=res["tx_hash"])
            st.success(f"Revoked in block {res['block']}")
        except Exception as e:
            st.error(str(e))
