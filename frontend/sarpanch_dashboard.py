import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import json
from utils import (
    fetch_api,
    post_api,
    is_authenticated,
    get_current_user_role,
    render_auth_sidebar,
    render_privacy_badge,
    display_success,
    display_warning,
    display_info
)

# Configuration - Support environment variables for deployment
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000/api/v1")

st.set_page_config(
    page_title="Smart Panchayat - Sarpanch & Admin Dashboard",
    page_icon="🏛️",
    layout="wide"
)

# Sidebar
st.sidebar.title("🏛️ Gram Panchayat Portal")
st.sidebar.markdown("**Alandi Gram Panchayat**, Pune, Maharashtra")

lang = st.sidebar.selectbox(
    "🌐 Language / भाषा",
    ["en", "hi", "mr"],
    format_func=lambda x: {"en": "English", "hi": "हिंदी (Hindi)", "mr": "मराठी (Marathi)"}[x]
)

# Render Authentication Box in sidebar
render_auth_sidebar(API_BASE_URL)

menu = st.sidebar.radio("Navigation", [
    "📊 Overview Dashboard",
    "👥 Population & Demographics",
    "🏘️ Ward Analytics",
    "📝 Reported Village Issues",
    "🤖 AI Decision Support",
    "📚 Government Schemes (RAG)",
    "📄 Panchayat Meeting Reports",
    "🛡️ Security & Privacy Audit Trail"
])

# Privacy Banner
render_privacy_badge()

user_role = get_current_user_role()
if user_role in ["Sarpanch", "Panchayat Admin", "System Admin"]:
    st.sidebar.success(f"🔓 Authorized as `{user_role}` (Full Administrative Access)")
elif is_authenticated():
    st.sidebar.info(f"ℹ️ Signed in as `{user_role}` (Resident View)")
else:
    st.sidebar.warning("⚠️ Public / Guest Mode (Sign in for administrative actions)")

# =============================================================
# 1. OVERVIEW DASHBOARD
# =============================================================
if menu == "📊 Overview Dashboard":
    st.title("📊 Panchayat Decision Support Dashboard")

    data = fetch_api(API_BASE_URL, "sarpanch/dashboard/overview")

    if data:
        pop = data.get("population_summary", {})
        issues = data.get("issue_statistics", {})

        # Key Metrics Row
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Population", pop.get("total_population", 0), delta="Calculated automatically")
        col2.metric("Total Households", pop.get("total_households", 0))
        col3.metric("Total Issues Reported", issues.get("total_issues", 0))
        col4.metric("Avg Household Size", f"{pop.get('avg_household_size', 0)} members")

        st.markdown("---")

        c1, c2 = st.columns(2)

        with c1:
            st.subheader("Gender Distribution")
            gender_data = {
                "Gender": ["Male", "Female", "Other"],
                "Count": [pop.get("male_population", 0), pop.get("female_population", 0), pop.get("other_population", 0)]
            }
            fig_gender = px.pie(
                gender_data,
                names="Gender",
                values="Count",
                color="Gender",
                color_discrete_map={"Male": "#1f77b4", "Female": "#e377c2", "Other": "#7f7f7f"},
                hole=0.3
            )
            st.plotly_chart(fig_gender, use_container_width=True)

        with c2:
            st.subheader("Issues by Category")
            by_cat = issues.get("by_category", {})
            if by_cat:
                cat_df = pd.DataFrame(list(by_cat.items()), columns=["Category", "Count"])
                fig_cat = px.bar(cat_df, x="Category", y="Count", color="Count", color_continuous_scale="Viridis")
                st.plotly_chart(fig_cat, use_container_width=True)
            else:
                st.info("No issues reported yet")

        # Age Breakdown
        st.subheader("Age Group Demographics")
        age_data = {
            "Age Group": ["Children (<18)", "Adults (18-59)", "Senior Citizens (60+)"],
            "Count": [pop.get("children", 0), pop.get("adults", 0), pop.get("senior_citizens", 0)]
        }
        fig_age = px.bar(age_data, x="Age Group", y="Count", text="Count", color="Age Group")
        st.plotly_chart(fig_age, use_container_width=True)

# =============================================================
# 2. POPULATION & DEMOGRAPHICS
# =============================================================
elif menu == "👥 Population & Demographics":
    st.title("👥 Detailed Population & Demographics")

    pop_data = fetch_api(API_BASE_URL, "sarpanch/analytics/population")
    if pop_data:
        c1, col2, col3 = st.columns(3)
        c1.metric("Literacy Rate", f"{pop_data.get('literacy_rate', 0)}%")
        col2.metric("Employment Rate", f"{pop_data.get('employment_rate', 0)}%")
        col3.metric("BPL Households", pop_data.get("bpl_households", 0))

        st.markdown("### Socioeconomic Classification (Ration Cards)")
        socio_data = {
            "Category": ["APL (Above Poverty Line)", "BPL (Below Poverty Line)", "Antodaya (Extremely Poor)"],
            "Count": [pop_data.get("apl_households", 0), pop_data.get("bpl_households", 0), pop_data.get("antodaya_households", 0)]
        }
        fig_socio = px.pie(socio_data, names="Category", values="Count", hole=0.4, color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig_socio, use_container_width=True)

# =============================================================
# 3. WARD ANALYTICS
# =============================================================
elif menu == "🏘️ Ward Analytics":
    st.title("🏘️ Ward-wise Development Indicators")

    wards = fetch_api(API_BASE_URL, "sarpanch/analytics/wards")
    if wards:
        ward_df = pd.DataFrame(wards)
        st.dataframe(ward_df, use_container_width=True)

        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Population by Ward")
            fig_wpop = px.bar(ward_df, x="ward_name", y="population", color="population", color_continuous_scale="Blues")
            st.plotly_chart(fig_wpop, use_container_width=True)

        with c2:
            st.subheader("Issues by Ward")
            fig_wiss = px.bar(ward_df, x="ward_name", y="issues_count", color="high_priority_issues",
                              title="Issues Count (Color indicates High Priority)")
            st.plotly_chart(fig_wiss, use_container_width=True)

# =============================================================
# 4. REPORTED VILLAGE ISSUES
# =============================================================
elif menu == "📝 Reported Village Issues":
    st.title("📝 Village Complaints & Issues")

    issues = fetch_api(API_BASE_URL, "sarpanch/issues/all")
    if issues:
        issues_df = pd.DataFrame(issues)
        st.dataframe(issues_df, use_container_width=True)
    else:
        st.info("No issues recorded in the system yet.")

# =============================================================
# 5. AI DECISION SUPPORT & MULTI-AGENT
# =============================================================
elif menu == "🤖 AI Decision Support":
    st.title("🤖 Multi-Agent AI Decision Support System")

    st.markdown("""
    The Multi-Agent AI system uses specialized domain agents (**Population, Water, Health, Education, Infrastructure**)
    coordinated by an orchestrator to analyze village problems and provide explainable recommendations.
    """)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🚀 Run Multi-Agent Village Analysis", type="primary", use_container_width=True):
            with st.spinner("Executing domain agents across Population, Water, Health, Infrastructure..."):
                res = post_api(API_BASE_URL, "sarpanch/ai/analyze", {})
                if res:
                    st.session_state['agent_analysis'] = res
                    st.success("Analysis complete!")

    with col2:
        if st.button("💡 Generate AI Recommendations for Issues", use_container_width=True):
            with st.spinner("Matching issues with RAG Government schemes..."):
                res = post_api(API_BASE_URL, "sarpanch/ai/recommendations/generate", {})
                if res:
                    st.success(res.get("message", "Recommendations Generated!"))

    # Display Agent Analysis
    if 'agent_analysis' in st.session_state:
        analysis = st.session_state['agent_analysis']
        st.subheader("📋 Multi-Agent Analysis Report")
        st.info(analysis.get("summary", ""))

        st.markdown("### Domain Agent Findings")
        for agent in analysis.get("agent_results", []):
            severity_colors = {"low": "🟢", "medium": "🟡", "high": "🔴", "critical": "🚨"}
            sev_icon = severity_colors.get(agent.get("severity", "low"), "⚪")

            with st.expander(f"{sev_icon} **{agent.get('agent_name')}** - Severity: {agent.get('severity', '').upper()}"):
                st.write(f"**Domain:** {agent.get('domain')}")
                st.write(f"**Affected Count:** {agent.get('affected_count')}")

                issues_found = agent.get("issues_found", [])
                if issues_found:
                    st.markdown("**Issues Identified:**")
                    for iss in issues_found:
                        st.markdown(f"- **{iss.get('issue')}**: {iss.get('description')} *(Impact: {iss.get('impact')})*")

                recs = agent.get("recommendations", [])
                if recs:
                    st.markdown("**Recommendations:**")
                    for rec in recs:
                        st.markdown(f"- {rec}")

                st.markdown("**Evidence / Raw Demographics:**")
                st.json(agent.get("evidence", {}))

    # Display Generated Recommendations
    st.markdown("---")
    st.subheader("📑 Priority Recommendations List")
    recs_data = fetch_api(API_BASE_URL, "sarpanch/ai/recommendations")
    if recs_data:
        recs_list = recs_data.get("recommendations", [])
        if recs_list:
            for rec in recs_list:
                prio_score = rec.get("priority_score", 0)
                badge_color = "red" if prio_score >= 80 else ("orange" if prio_score >= 60 else "green")

                st.markdown(f"""
                <div style="padding:15px; border-radius:8px; border:1px solid #ddd; margin-bottom:15px; background-color:#f9f9f9;">
                    <h4>🎯 {rec.get('recommendation_id')} | Priority Score: <span style="color:{badge_color}; font-weight:bold;">{prio_score}/100</span></h4>
                    <p><b>Action:</b> {rec.get('recommendation_text')}</p>
                    <p><b>Status:</b> {rec.get('status')} | <b>Created:</b> {rec.get('created_at')}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No recommendations generated yet. Click 'Generate AI Recommendations' above.")

# =============================================================
# 6. GOVERNMENT SCHEMES KNOWLEDGE BASE
# =============================================================
elif menu == "📚 Government Schemes (RAG)":
    st.title("📚 Government Schemes Knowledge Base (RAG)")

    search_query = st.text_input("🔍 Semantic search schemes (e.g. 'water pipeline', 'school lab', 'farmer loan', 'housing')")

    if search_query:
        search_res = fetch_api(API_BASE_URL, f"schemes/search?query={search_query}")
        if search_res:
            matched = search_res.get("matched_schemes", [])
            st.markdown(f"**Found {len(matched)} relevant schemes:**")
            for scheme in matched:
                with st.expander(f"📌 **{scheme.get('name')}** ({scheme.get('level')} Govt - {scheme.get('category')})"):
                    st.markdown(f"**Description:** {scheme.get('description')}")
                    st.markdown(f"**Eligibility:** {scheme.get('eligibility_criteria')}")
                    st.markdown(f"**Benefits:** {scheme.get('benefits')}")
    else:
        schemes = fetch_api(API_BASE_URL, "schemes/")
        if schemes:
            for scheme in schemes:
                with st.expander(f"📌 **{scheme.get('name')}** ({scheme.get('level')} - {scheme.get('category')})"):
                    st.markdown(f"**Description:** {scheme.get('description')}")
                    st.markdown(f"**Eligibility:** {scheme.get('eligibility_criteria')}")
                    st.markdown(f"**Benefits:** {scheme.get('benefits')}")

# =============================================================
# 7. PANCHAYAT MEETING REPORTS
# =============================================================
elif menu == "📄 Panchayat Meeting Reports":
    st.title("📄 Panchayat Meeting Report Generator")

    report = fetch_api(API_BASE_URL, "sarpanch/reports/summary")
    if report:
        st.success(f"Report Generated for: **{report.get('village')}** on {report.get('generated_on')}")
        st.markdown(f"### Executive Summary\n{report.get('executive_summary')}")

        st.markdown("### Download Official Panchayat Meeting Brief")
        st.download_button(
            label="📥 Download Summary JSON",
            data=json.dumps(report, indent=2),
            file_name="panchayat_meeting_report.json",
            mime="application/json"
        )

# =============================================================
# 8. SECURITY & PRIVACY AUDIT TRAIL
# =============================================================
elif menu == "🛡️ Security & Privacy Audit Trail":
    st.title("🛡️ System Security & Privacy Audit Trail")

    st.markdown("""
    All access to sensitive Personally Identifiable Information (PII) like Aadhaar numbers,
    contact information, and logins are logged in compliance with data privacy regulations.
    """)

    if is_authenticated() and user_role in ["Sarpanch", "Panchayat Admin", "System Admin"]:
        logs = fetch_api(API_BASE_URL, "auth/audit-logs")
        if logs:
            log_df = pd.DataFrame(logs)
            st.dataframe(log_df, use_container_width=True)
        else:
            st.info("No audit entries found.")
    else:
        st.warning("🔒 Administrative access required to view the full security audit log.")
        st.info("Please sign in as `sarpanch` or `admin` in the sidebar.")
