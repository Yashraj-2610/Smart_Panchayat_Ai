"""
Shared Login Component for Smart Panchayat AI
Provides unified authentication interface for both dashboards.
Uses session keys compatible with frontend/utils.py (auth_token / current_user).
"""
import streamlit as st
from frontend.utils import API_BASE_URL, post_api, is_authenticated, logout_user


def show_login_interface():
    """Unified login interface used by Family Portal + Sarpanch Dashboard."""
    # Use same auth keys as utils.py
    token_key = "auth_token"
    user_key = "current_user"

    if not is_authenticated():
        st.title("🔐 Sign In — Smart Panchayat")
        st.markdown("Welcome to the AI-powered Panchayat Decision Support System.")
        st.caption("Log in once to access your portal based on role.")

        # Unified form
        with st.form("unified_login", clear_on_submit=False):
            st.subheader("Account Login")
            identifier = st.text_input("Username or Email",
                                       placeholder="e.g. sarpanch / admin / resident",
                                       key="unified_login_id")
            password = st.text_input("Password", type="password",
                                    placeholder="Enter your password",
                                    key="unified_login_pw")
            submitted = st.form_submit_button("Sign In", type="primary", use_container_width=True)

        if submitted:
            res = post_api(API_BASE_URL, "auth/login",
                           {"username_or_email": identifier, "password": password})
            if res and "access_token" in res:
                st.session_state[token_key] = res["access_token"]
                # Store full user dict so get_current_user_role works
                st.session_state[user_key] = res.get("user", res)
                # Also keep role accessible
                st.session_state["user_role"] = res["user"].get("role", "User")
                st.success(f"✓ Welcome, {res['user'].get('full_name', identifier)}!")
                st.rerun()
            else:
                st.error("❌ Login failed — check username/email or password.")

        # Demo credentials helper
        st.divider()
        with st.expander("📋 Demo Accounts (for testing)"):
            st.code("Sarpanch:  sarpanch / sarpanch123\n"
                    "Admin:    admin / admin123\n"
                    "Resident: resident / resident123")

    else:
        user = st.session_state.get(user_key)
        role = (user.get("role") if isinstance(user, dict) else
                st.session_state.get("user_role", "Unknown"))
        name = (user.get("full_name") if isinstance(user, dict) else
                user.get("username") if isinstance(user, dict) else str(user))

        st.success(f"✓ Signed in as **{name}**")
        st.info(f"Role: `{role}` | End-to-End Encryption Active")

        # Quick nav hint
        if role in ["Sarpanch", "Panchayat Admin", "System Admin"]:
            st.caption("🔓 Full administrative access — Sarpanch Dashboard available.")
        else:
            st.caption("🏡 Family Head access — Household & Issue reporting available.")

        if st.button("🚪 Log Out", type="secondary", use_container_width=True):
            logout_user()
