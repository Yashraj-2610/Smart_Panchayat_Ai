# Professional UI Design System for Smart Panchayat AI
# Clean, modern, accessible - Launch Ready

import streamlit as st
from typing import Optional, Dict, Any

# Professional Color Palette (matches modern SaaS apps)
COLORS = {
    "primary": "#2563EB",      # Trustworthy blue
    "primary_dark": "#1E40AF", # Darker blue for hover
    "success": "#059669",      # Green for positive actions
    "warning": "#D97706",      # Orange for warnings
    "error": "#DC2626",        # Red for errors
    "neutral_100": "#F3F4F6",  # Light background
    "neutral_200": "#E5E7EB",  # Borders
    "neutral_700": "#374151",  # Secondary text
    "neutral_900": "#111827",  # Primary text
}

# Privacy Levels Configuration
PRIVACY_LEVELS = {
    "PUBLIC": {
        "level": 1,
        "icon": "🌐",
        "label": "Public Data",
        "description": "Viewable by all village residents",
        "color": "#10B981"
    },
    "INTERNAL": {
        "level": 2,
        "icon": "🏘️",
        "label": "Internal Use",
        "description": "Panchayat staff and officials only",
        "color": "#F59E0B"
    },
    "CONFIDENTIAL": {
        "level": 3,
        "icon": "🔒",
        "label": "Confidential",
        "description": "Sarpanch and Admin only",
        "color": "#EF4444"
    },
    "RESTRICTED": {
        "level": 4,
        "icon": "🔐",
        "label": "Restricted",
        "description": "Encrypted PII - Audit logged",
        "color": "#7C3AED"
    }
}

# Member Status Configuration
MEMBER_STATUS = {
    "VERIFIED_RESIDENT": {
        "can_view": ["PUBLIC", "INTERNAL"],
        "can_edit_own": True,
        "can_report_issues": True,
        "label": "Verified Resident",
        "badge_color": "#10B981"
    },
    "FAMILY_HEAD": {
        "can_view": ["PUBLIC", "INTERNAL"],
        "can_edit_own": True,
        "can_report_issues": True,
        "can_register_members": True,
        "label": "Family Head",
        "badge_color": "#3B82F6"
    },
    "PANCHAYAT_STAFF": {
        "can_view": ["PUBLIC", "INTERNAL", "CONFIDENTIAL"],
        "can_edit_own": True,
        "can_report_issues": True,
        "can_view_all_issues": True,
        "label": "Panchayat Staff",
        "badge_color": "#8B5CF6"
    },
    "SARPANCH": {
        "can_view": ["PUBLIC", "INTERNAL", "CONFIDENTIAL", "RESTRICTED"],
        "can_edit_own": True,
        "can_edit_all": True,
        "can_view_audit_logs": True,
        "can_generate_reports": True,
        "label": "Sarpanch",
        "badge_color": "#F59E0B"
    },
    "SYSTEM_ADMIN": {
        "can_view": ["PUBLIC", "INTERNAL", "CONFIDENTIAL", "RESTRICTED"],
        "can_edit_all": True,
        "can_manage_users": True,
        "can_view_audit_logs": True,
        "full_access": True,
        "label": "System Administrator",
        "badge_color": "#EF4444"
    }
}


def apply_professional_styles():
    """Apply custom CSS for professional, aesthetic UI"""
    st.markdown("""
    <style>
        /* Remove Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        /* Clean typography */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }

        /* Modern card styling */
        .stMetric {
            background-color: """ + COLORS["neutral_100"] + """;
            padding: 20px;
            border-radius: 12px;
            border: 1px solid """ + COLORS["neutral_200"] + """;
        }

        .stMetric > label {
            font-size: 14px;
            font-weight: 500;
            color: """ + COLORS["neutral_700"] + """;
        }

        .stMetric > div {
            font-size: 32px;
            font-weight: 700;
            color: """ + COLORS["neutral_900"] + """;
        }

        /* Professional buttons */
        .stButton > button {
            border-radius: 8px;
            font-weight: 500;
            transition: all 0.2s;
        }

        .stButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }

        /* Clean input fields */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea {
            border-radius: 8px;
        }

        /* Professional tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }

        .stTabs [data-baseweb="tab"] {
            border-radius: 8px 8px 0 0;
            padding: 12px 24px;
            font-weight: 500;
        }

        /* Clean sidebar */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #F9FAFB 0%, #F3F4F6 100%);
        }

        /* Privacy badge styling */
        .privacy-badge {
            display: inline-flex;
            align-items: center;
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
            gap: 6px;
        }

        /* Role badge */
        .role-badge {
            display: inline-flex;
            align-items: center;
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        /* Modern cards */
        .modern-card {
            background: white;
            border-radius: 16px;
            padding: 24px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            border: 1px solid """ + COLORS["neutral_200"] + """;
            margin-bottom: 16px;
        }

        /* Loading states */
        .loading-skeleton {
            background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
            background-size: 200% 100%;
            animation: loading 1.5s infinite;
        }

        @keyframes loading {
            0% { background-position: 200% 0; }
            100% { background-position: -200% 0; }
        }
    </style>
    """, unsafe_allow_html=True)


def render_privacy_badge(privacy_level: str):
    """Render privacy level badge with professional styling"""
    config = PRIVACY_LEVELS.get(privacy_level, PRIVACY_LEVELS["PUBLIC"])

    badge_html = f"""
    <div class="privacy-badge" style="background-color: {config['color']}20; color: {config['color']};">
        <span>{config['icon']}</span>
        <span>{config['label']}</span>
    </div>
    """
    st.markdown(badge_html, unsafe_allow_html=True)


def render_role_badge(role: str):
    """Render role badge with professional styling"""
    status_config = MEMBER_STATUS.get(role, MEMBER_STATUS["VERIFIED_RESIDENT"])

    badge_html = f"""
    <div class="role-badge" style="background-color: {status_config['badge_color']}20; color: {status_config['badge_color']};">
        {status_config['label']}
    </div>
    """
    st.markdown(badge_html, unsafe_allow_html=True)


def render_access_control_notice(user_role: str, resource_privacy: str):
    """Show access control notice if user lacks permission"""
    status_config = MEMBER_STATUS.get(user_role, MEMBER_STATUS["VERIFIED_RESIDENT"])

    if resource_privacy not in status_config.get("can_view", []):
        st.warning(f"⚠️ **Access Restricted**: This resource requires {resource_privacy} level access.")
        st.info(f"Your current role: **{status_config['label']}**")
        return False
    return True


def render_modern_header(title: str, subtitle: str = "", icon: str = "🏘️"):
    """Render professional page header"""
    header_html = f"""
    <div class="modern-card" style="margin-bottom: 24px;">
        <h1 style="font-size: 28px; font-weight: 700; color: {COLORS['neutral_900']}; margin-bottom: 8px;">
            {icon} {title}
        </h1>
        {f'<p style="color: {COLORS["neutral_700"]}; font-size: 14px;">{subtitle}</p>' if subtitle else ''}
    </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)


def render_metric_row(metrics: list):
    """Render a row of professional metrics"""
    cols = st.columns(len(metrics))

    for idx, metric in enumerate(metrics):
        with cols[idx]:
            st.markdown(f"""
            <div class="modern-card">
                <p style="font-size: 12px; color: {COLORS['neutral_700']}; margin-bottom: 4px;">
                    {metric.get('icon', '📊')} {metric['label']}
                </p>
                <p style="font-size: 24px; font-weight: 700; color: {COLORS['neutral_900']}; margin: 0;">
                    {metric['value']}
                </p>
                {f'<p style="font-size: 11px; color: {COLORS["success"] if metric.get("trend", "").startswith("+") else COLORS["error"]};">{metric.get("trend", "")}</p>' if metric.get('trend') else ''}
            </div>
            """, unsafe_allow_html=True)


def render_action_button(label: str, icon: str = "→", variant: str = "primary", key: str = None):
    """Render professional action button with variants"""
    button_type = "primary" if variant == "primary" else "secondary"

    return st.button(
        f"{icon} {label}",
        type=button_type,
        key=key,
        use_container_width=True
    )


def check_permission(user_role: str, permission: str) -> bool:
    """Check if user role has specific permission"""
    status_config = MEMBER_STATUS.get(user_role, MEMBER_STATUS["VERIFIED_RESIDENT"])
    return status_config.get(permission, False)


def can_view_privacy_level(user_role: str, privacy_level: str) -> bool:
    """Check if user can view data at specific privacy level"""
    status_config = MEMBER_STATUS.get(user_role, MEMBER_STATUS["VERIFIED_RESIDENT"])
    return privacy_level in status_config.get("can_view", [])