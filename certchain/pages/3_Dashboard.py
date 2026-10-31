import streamlit as st, plotly.express as px
from core import audit
st.title("📊 Integrity & Audit Dashboard")
df = audit.all_events()
if df.empty:
    st.info("No events yet."); st.stop()
v = df[df.kind.isin(["pdf", "qr"])]
c1, c2, c3 = st.columns(3)
c1.metric("Verifications", len(v)); c2.metric("Genuine", int((v.verdict == "GENUINE").sum()))
c3.metric("Suspicious (not found/revoked)", int(v.verdict.isin(["NOT_FOUND", "REVOKED"]).sum()))
if len(v):
    st.plotly_chart(px.pie(v, names="verdict", title="Verdicts"))
sus = v[v.verdict == "NOT_FOUND"]
if len(sus):
    st.subheader("Repeated mismatch hashes")
    st.dataframe(sus.groupby("cert_hash").size().sort_values(ascending=False).rename("attempts"))
st.subheader("Audit trail"); st.dataframe(df)
