import streamlit as st
from crawler import crawl_website
from ai_engine import generate_audit_report

st.set_page_config(page_title="ArvixAI Website Auditor", layout="wide")

st.title("🔍 ArvixAI – AI Website Auditor")
st.caption("First autonomous AI agent demo by Ioan Mihai Popoviciu (18) – Founder @ArvixAI")

url = st.text_input("Enter website URL", placeholder="example.com or https://...")
go = st.button("Run Audit", type="primary", use_container_width=True)

if go and url:
    with st.spinner("Crawling website + AI analysis..."):
        data = crawl_website(url.strip())
        report = generate_audit_report(data)

    st.success("Audit finished!")

    st.metric("Overall Score", f"{report.get('overall_score', 0)} / 100")

    cols = st.columns(5)
    for i, (cat, info) in enumerate(report.get("categories", {}).items()):
        with cols[i % 5]:
            st.metric(cat, f"{info.get('score', 0)} / 100")

    for category, info in report.get("categories", {}).items():
        with st.expander(f"📊 {category} (Score: {info.get('score', '?')})"):
            st.subheader("Issues")
            for issue in info.get("issues", []):
                st.markdown(f"• {issue}")
            st.subheader("Suggestions")
            for sug in info.get("suggestions", []):
                st.markdown(f"• {sug}")

    with st.expander("Raw crawled data"):
        st.json(data)