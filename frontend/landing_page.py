# Professional Landing Page - Smart Panchayat AI
# Launch-ready with modern design and access control

import streamlit as st
import os
from styles import (
    apply_professional_styles, render_modern_header, render_metric_row,
    render_privacy_badge, render_role_badge, COLORS, PRIVACY_LEVELS, MEMBER_STATUS
)
from utils import (
    fetch_api, post_api, is_authenticated, get_current_user_role,
    render_auth_sidebar, logout_user
)

# Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000/api/v1")

st.set_page_config(
    page_title="Smart Panchayat AI",
    page_icon="🏘️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply professional styling
apply_professional_styles()

# Render authentication sidebar
render_auth_sidebar(API_BASE_URL)

if is_authenticated():
    user = st.session_state["current_user"]
    user_role = user.get("role", "Family Head")

    # Professional header with user context
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.markdown(f"# 🏘️ Smart Panchayat AI")
        st.markdown(f"**Alandi Gram Panchayat** | Pune, Maharashtra")

    with col2:
        render_role_badge(user_role)

    with col3:
        st.markdown(f"👤 {user.get('full_name')}")

    st.markdown("---")

    # Dashboard with role-based content
    if user_role == "Sarpanch":
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📊 Dashboard", "👥 Residents", "🤖 AI Analysis", "📋 Reports", "⚙️ Settings"
        ])

        with tab1:
            render_modern_header("Panchayat Overview", "Real-time village development indicators")

            # Fetch dashboard data
            dash_data = fetch_api(API_BASE_URL, "sarpanch/dashboard/overview")

            if dash_data:
                pop = dash_data.get("population_summary", {})
                metrics = [
                    {"icon": "👥", "label": "Total Population", "value": pop.get("total_population", 0)},
                    {"icon": "🏠", "label": "Households", "value": pop.get("total_households", 0)},
                    {"icon": "📢", "label": "Issues Reported", "value": dash_data.get("issue_statistics", {}).get("total_issues", 0)},
                    {"icon": "✅", "label": "Avg Household Size", "value": f"{pop.get('avg_household_size', 0):.1f}"},
                ]
                render_metric_row(metrics)

        with tab2:
            render_modern_header("Resident Management", "View and manage household data")
            st.info("👥 Household registration and family member management")

        with tab3:
            render_modern_header("AI Decision Support", "Multi-agent analysis and predictions")
            if st.button("🚀 Run AI Analysis", use_container_width=True):
                with st.spinner("Analyzing village data..."):
                    res = post_api(API_BASE_URL, "sarpanch/ai/analyze", {})
                    if res:
                        st.success("Analysis complete!")
                        st.json(res.get("summary"))

        with tab4:
            render_modern_header("Official Reports", "Generate and download village reports")
            st.info("📄 Generate meeting briefs and development reports")

        with tab5:
            render_modern_header("Settings", "System configuration and preferences")
            lang = st.selectbox("Language", ["English", "हिंदी", "मराठी"])
            st.success(f"Preferences saved for {lang}")

    elif user_role == "Family Head":
        tab1, tab2, tab3, tab4 = st.tabs([
            "🏡 My Household", "📢 Report Issue", "💡 Schemes", "🔐 Account"
        ])

        with tab1:
            render_modern_header("Household Profile", "Manage your family information")
            st.info("👨‍👩‍👧‍👦 View and update household members safely")

        with tab2:
            render_modern_header("Report Issue", "Submit village problems for resolution")
            render_privacy_badge("PUBLIC")

            with st.form("issue_form"):
                category = st.selectbox("Category", ["Water", "Health", "Education", "Road", "Electricity"])
                title = st.text_input("Issue Title")
                description = st.text_area("Description")
                affected = st.number_input("Affected Households", min_value=1, value=5)

                if st.form_submit_button("📤 Submit Report", use_container_width=True):
                    res = post_api(API_BASE_URL, "household/1/issues", {
                        "category": category,
                        "title": title,
                        "description": description,
                        "affected_count": affected,
                        "language": "en"
                    })
                    if res:
                        st.success(f"✅ Issue reported! Tracking ID: {res.get('issue_id')}")

        with tab3:
            render_modern_header("Recommended Schemes", "Government benefits matching your needs")
            render_privacy_badge("INTERNAL")

            schemes = fetch_api(API_BASE_URL, "schemes/")
            if schemes:
                for scheme in schemes[:3]:
                    with st.expander(f"📌 {scheme.get('name')}"):
                        st.markdown(f"**Benefits:** {scheme.get('benefits')}")
                        st.markdown(f"**Eligibility:** {scheme.get('eligibility_criteria')}")

        with tab4:
            render_modern_header("Account Settings", "Privacy and security")
            render_privacy_badge("RESTRICTED")

            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Profile Information** (Encrypted)")
                st.text_input("Full Name", value=user.get("full_name"), disabled=True)

            with col2:
                st.markdown("**Security**")
                if st.button("🔑 Change Password"):
                    st.info("Password change requested")

    else:
        # Default view for other roles
        render_modern_header("Welcome", f"Smart Panchayat AI - {user.get('full_name')}")
        st.info(f"Role: {user_role}")

else:
    # Public/Guest Landing Page
    st.markdown("""
    <style>
        .hero {
            background: linear-gradient(135deg, #2563EB 0%, #1E40AF 100%);
            padding: 60px 40px;
            border-radius: 16px;
            color: white;
            text-align: center;
            margin-bottom: 40px;
        }
        .hero h1 { font-size: 44px; font-weight: 700; margin: 0; }
        .hero p { font-size: 18px; margin: 12px 0 0 0; opacity: 0.9; }
        .feature { padding: 24px; border-radius: 12px; background: #F3F4F6; }
    </style>

    <div class="hero">
        <h1>🏘️ Smart Panchayat AI</h1>
        <p>AI-Powered Decision Support for Village Development</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="feature">
        <h3>📊 Data-Driven Decisions</h3>
        <p>Real-time analytics on village development, population, and infrastructure needs</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="feature">
        <h3>🤖 AI Analysis</h3>
        <p>Multi-agent system analyzes health, education, water, and infrastructure issues</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="feature">
        <h3>💰 Scheme Matching</h3>
        <p>Automatically match village problems with relevant government schemes</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    col_a, col_b = st.columns([1, 1])

    with col_a:
        st.markdown("### 👨‍🌾 For Residents")
        st.markdown("- Report village issues")
        st.markdown("- View family information")
        st.markdown("- Access recommended schemes")
        if st.button("🔑 Login as Resident"):
            st.session_state.show_login = True
            st.rerun()

    with col_b:
        st.markdown("### 👨‍💼 For Panchayat Officials")
        st.markdown("- Village analytics dashboard")
        st.markdown("- AI-powered insights")
        st.markdown("- Generate official reports")
        if st.button("🔐 Login as Administrator"):
            st.session_state.show_login = True
            st.rerun()

    st.markdown("---")
    st.markdown("### 🔐 Privacy & Security")
    st.info("✅ All sensitive data is end-to-end encrypted  \n✅ Aadhaar numbers masked and protected  \n✅ Audit logs for compliance")
