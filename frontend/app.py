"""Unified Smart Panchayat Streamlit — One Login, Role Tabs"""
import streamlit as st
from shared_login import show_login_interface

st.set_page_config(page_title="Smart Panchayat AI", page_icon="🏛️", layout="wide")

with st.sidebar:
    st.title("Smart Panchayat")
    show_login_interface()

if st.session_state.get("auth_token"):
    role = st.session_state.get("user_role", "Family Head")
    tab = st.sidebar.radio("Select Portal", ["🏡 Family Portal", "📊 Sarpanch Dashboard"])
    st.sidebar.caption(f"Signed in as {st.session_state.get('current_user', 'User')} — {role}")
    if "Family" in tab:
        st.title("Family Head Portal")
        st.info("Household & issue reporting — shared session active.")
    else:
        st.title("Sarpanch Dashboard")
        st.info("Analytics, ward maps, AI recommendations — shared session.")
else:
    st.info("👋 Sign in via sidebar to access your portal.")
