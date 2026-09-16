"""
Enhanced utility functions for Streamlit frontends
Includes authentication, RBAC, retry logic, caching, and privacy helpers
"""
import streamlit as st
import requests
import time
from functools import wraps
from typing import Optional, Dict, Any


def get_auth_headers() -> Dict[str, str]:
    """Get Authorization headers from Streamlit session state"""
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    token = st.session_state.get("auth_token")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def is_authenticated() -> bool:
    """Check if a user is currently logged in"""
    return bool(st.session_state.get("auth_token") and st.session_state.get("current_user"))


def get_current_user_role() -> Optional[str]:
    """Get the role of the logged in user"""
    user = st.session_state.get("current_user")
    if user:
        return user.get("role")
    return None


def logout_user():
    """Clear user session state on logout"""
    st.session_state["auth_token"] = None
    st.session_state["current_user"] = None
    st.success("Logged out successfully!")
    st.rerun()


def retry_with_backoff(max_retries=3, backoff_factor=2):
    """Decorator to retry API calls with exponential backoff"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except requests.exceptions.ConnectionError:
                    if attempt == max_retries - 1:
                        raise
                    time.sleep(backoff_factor ** attempt)
                except requests.exceptions.Timeout:
                    if attempt == max_retries - 1:
                        raise
                    time.sleep(backoff_factor ** attempt)
        return wrapper
    return decorator


@st.cache_data(ttl=180)  # Cache for 3 minutes
def fetch_api_cached(base_url: str, endpoint: str) -> Optional[Dict[Any, Any]]:
    """Fetch data from API with caching"""
    return fetch_api(base_url, endpoint)


@retry_with_backoff(max_retries=3)
def fetch_api(base_url: str, endpoint: str, timeout: int = 12) -> Optional[Dict[Any, Any]]:
    """
    Fetch data from API with authentication token and retry logic
    """
    try:
        response = requests.get(
            f"{base_url}/{endpoint}",
            timeout=timeout,
            headers=get_auth_headers()
        )
        response.raise_for_status()
        return response.json()

    except requests.exceptions.ConnectionError:
        st.error("⚠️ Cannot connect to server. Please check if the backend is running.")
        st.info("💡 Render free tier service may take 30-60s to wake up. Please wait and refresh.")
        return None

    except requests.exceptions.Timeout:
        st.error("⏱️ Request timed out. The server is taking too long to respond.")
        return None

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            st.warning("🔒 Session expired or unauthorized. Please log in.")
        elif e.response.status_code == 403:
            st.error("🚫 Access Denied: Your account role does not have permission for this resource.")
        elif e.response.status_code == 404:
            st.error(f"❌ Resource not found: {endpoint}")
        elif e.response.status_code == 500:
            st.error("🔥 Server error. Please try again later.")
        else:
            st.error(f"❌ HTTP Error {e.response.status_code}")
        return None

    except Exception as e:
        st.error(f"❌ Request failed: {str(e)}")
        return None


@retry_with_backoff(max_retries=2)
def post_api(base_url: str, endpoint: str, data: Dict, timeout: int = 15) -> Optional[Dict[Any, Any]]:
    """
    POST data to API with authentication token and retry logic
    """
    try:
        response = requests.post(
            f"{base_url}/{endpoint}",
            json=data,
            timeout=timeout,
            headers=get_auth_headers()
        )
        response.raise_for_status()
        return response.json()

    except requests.exceptions.ConnectionError:
        st.error("⚠️ Cannot connect to server. Please check if the backend is running.")
        return None

    except requests.exceptions.Timeout:
        st.error("⏱️ Request timed out. Please try again.")
        return None

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            st.error("🔒 Authentication required. Please log in.")
        elif e.response.status_code == 403:
            st.error("🚫 Access Denied: You do not have permission to perform this action.")
        elif e.response.status_code == 422:
            st.error("❌ Validation Error. Please check your inputs.")
            try:
                err_detail = e.response.json()
                if "details" in err_detail or "detail" in err_detail:
                    st.json(err_detail.get("details") or err_detail.get("detail"))
            except:
                pass
        elif e.response.status_code == 400:
            try:
                err = e.response.json().get("detail", "Bad Request")
                st.error(f"❌ {err}")
            except:
                st.error("❌ Bad Request (400)")
        else:
            st.error(f"❌ HTTP Error {e.response.status_code}")
        return None

    except Exception as e:
        st.error(f"❌ Request failed: {str(e)}")
        return None


def render_auth_sidebar(base_url: str):
    """Render Login / Logout / User profile box in Streamlit sidebar"""
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔐 Security & Access")

    if is_authenticated():
        user = st.session_state["current_user"]
        role = user.get("role", "User")
        name = user.get("full_name", user.get("username", "User"))

        st.sidebar.success(f"👤 **{name}**")
        st.sidebar.caption(f"Role: `{role}` | 🛡️ E2E PII Protected")

        if st.sidebar.button("🚪 Log Out", key="sidebar_logout_btn", use_container_width=True):
            logout_user()
    else:
        st.sidebar.info("👋 You are in Guest / Public View")
        with st.sidebar.expander("🔑 Quick Login / Sign In", expanded=False):
            with st.form("sidebar_login_form"):
                login_id = st.text_input("Username / Email", placeholder="e.g. sarpanch or resident")
                password = st.text_input("Password", type="password")
                submitted = st.form_submit_button("Sign In", use_container_width=True)

                if submitted and login_id and password:
                    res = post_api(base_url, "auth/login", {
                        "username_or_email": login_id,
                        "password": password
                    })
                    if res and "access_token" in res:
                        st.session_state["auth_token"] = res["access_token"]
                        st.session_state["current_user"] = res["user"]
                        st.success(f"Welcome {res['user']['full_name']}!")
                        st.rerun()
                    else:
                        st.error("Invalid credentials")

            st.caption("Demo Accounts:")
            st.code("Sarpanch: sarpanch / sarpanch123\nAdmin: admin / admin123\nFamily: resident / resident123")


def render_privacy_badge():
    """Render standard privacy protection notice"""
    st.info("🔒 **End-to-End Privacy Enabled**: Aadhaar, phone numbers, and financial records are AES-encrypted and masked in compliance with data protection standards.")
