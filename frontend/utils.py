"""
Enhanced utility functions for Streamlit frontends
Includes retry logic, better error handling, and caching
"""
import streamlit as st
import requests
import time
from functools import wraps
from typing import Optional, Dict, Any


def retry_with_backoff(max_retries=3, backoff_factor=2):
    """Decorator to retry API calls with exponential backoff"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except requests.exceptions.ConnectionError as e:
                    if attempt == max_retries - 1:
                        raise
                    wait_time = backoff_factor ** attempt
                    time.sleep(wait_time)
                except requests.exceptions.Timeout as e:
                    if attempt == max_retries - 1:
                        raise
                    wait_time = backoff_factor ** attempt
                    time.sleep(wait_time)
        return wrapper
    return decorator


@st.cache_data(ttl=300)  # Cache for 5 minutes
def fetch_api_cached(base_url: str, endpoint: str) -> Optional[Dict[Any, Any]]:
    """Fetch data from API with caching"""
    return fetch_api(base_url, endpoint)


@retry_with_backoff(max_retries=3)
def fetch_api(base_url: str, endpoint: str, timeout: int = 10) -> Optional[Dict[Any, Any]]:
    """
    Fetch data from API with retry logic and better error handling

    Args:
        base_url: Base API URL
        endpoint: API endpoint path
        timeout: Request timeout in seconds

    Returns:
        JSON response or None if failed
    """
    try:
        response = requests.get(
            f"{base_url}/{endpoint}",
            timeout=timeout,
            headers={"Accept": "application/json"}
        )
        response.raise_for_status()
        return response.json()

    except requests.exceptions.ConnectionError:
        st.error("⚠️ Cannot connect to server. Please check if the backend is running.")
        st.info("💡 The free tier service may need 30-60 seconds to wake up. Please wait and refresh.")
        return None

    except requests.exceptions.Timeout:
        st.error("⏱️ Request timed out. The server is taking too long to respond.")
        return None

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            st.error(f"❌ Endpoint not found: {endpoint}")
        elif e.response.status_code == 500:
            st.error("🔥 Server error. Please try again later.")
        else:
            st.error(f"❌ HTTP Error {e.response.status_code}: {e.response.reason}")
        return None

    except requests.exceptions.RequestException as e:
        st.error(f"❌ Request failed: {str(e)}")
        return None

    except ValueError:
        st.error("❌ Invalid response format from server")
        return None


@retry_with_backoff(max_retries=2)
def post_api(base_url: str, endpoint: str, data: Dict, timeout: int = 15) -> Optional[Dict[Any, Any]]:
    """
    POST data to API with retry logic and better error handling

    Args:
        base_url: Base API URL
        endpoint: API endpoint path
        data: Data to POST
        timeout: Request timeout in seconds

    Returns:
        JSON response or None if failed
    """
    try:
        response = requests.post(
            f"{base_url}/{endpoint}",
            json=data,
            timeout=timeout,
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json"
            }
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
        if e.response.status_code == 422:
            st.error("❌ Invalid data format. Please check your inputs.")
            try:
                error_detail = e.response.json()
                if "detail" in error_detail:
                    st.json(error_detail["detail"])
            except:
                pass
        elif e.response.status_code == 500:
            st.error("🔥 Server error. Please try again later.")
        else:
            st.error(f"❌ HTTP Error {e.response.status_code}")
        return None

    except requests.exceptions.RequestException as e:
        st.error(f"❌ Request failed: {str(e)}")
        return None


def show_loading_spinner(message: str = "Loading..."):
    """Context manager for showing loading spinner"""
    return st.spinner(message)


def display_success(message: str):
    """Display success message with icon"""
    st.success(f"✅ {message}")


def display_info(message: str):
    """Display info message with icon"""
    st.info(f"ℹ️ {message}")


def display_warning(message: str):
    """Display warning message with icon"""
    st.warning(f"⚠️ {message}")


def check_api_health(base_url: str) -> bool:
    """
    Check if API is healthy and reachable

    Returns:
        True if healthy, False otherwise
    """
    try:
        response = requests.get(f"{base_url.replace('/api/v1', '')}/health", timeout=5)
        return response.status_code == 200
    except:
        return False
