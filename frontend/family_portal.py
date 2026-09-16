import streamlit as st
import os
from utils import (
    fetch_api,
    post_api,
    is_authenticated,
    render_auth_sidebar,
    render_privacy_badge,
    display_success,
    display_warning,
    display_info
)

# Configuration - Support environment variables for deployment
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000/api/v1")

st.set_page_config(
    page_title="Smart Panchayat - Family Portal",
    page_icon="🏡",
    layout="wide"
)

# Multilingual labels
LABELS = {
    "en": {
        "title": "Family Head Portal - Smart Panchayat",
        "subtitle": "Alandi Gram Panchayat, Pune, Maharashtra",
        "household_reg": "Register New Household",
        "head_name": "Head of Family Name",
        "head_age": "Age",
        "head_gender": "Gender",
        "head_occupation": "Occupation",
        "contact": "Contact Number (Phone)",
        "address": "Residential Address",
        "ward": "Ward Number",
        "household_type": "Household Category (APL / BPL / Antodaya)",
        "annual_income": "Annual Income (₹)",
        "ration_card": "Ration Card Number",
        "submit": "Submit Registration",
        "add_member": "Add Family Member",
        "member_name": "Member Full Name",
        "member_age": "Member Age",
        "aadhar": "12-digit Aadhaar Number (Encrypted)",
        "relation": "Relation to Head of Family",
        "education": "Education Level",
        "submit_issue": "Report Village / Public Issue",
        "issue_category": "Issue Category",
        "issue_title": "Issue Title / Summary",
        "issue_description": "Detailed Description",
        "affected_count": "Number of Affected Households in Ward",
        "view_family": "My Family & Schemes",
        "auth_tab": "Account & Login"
    },
    "hi": {
        "title": "परिवार मुखिया पोर्टल - स्मार्ट पंचायत",
        "subtitle": "आलंदी ग्राम पंचायत, पुणे, महाराष्ट्र",
        "household_reg": "नया परिवार पंजीकृत करें",
        "head_name": "परिवार मुखिया का नाम",
        "head_age": "आयु",
        "head_gender": "लिंग",
        "head_occupation": "व्यवसाय",
        "contact": "संपर्क नंबर",
        "address": "आवासीय पता",
        "ward": "वार्ड संख्या",
        "household_type": "राशन श्रेणी (APL / BPL / अंत्योदय)",
        "annual_income": "वार्षिक आय (₹)",
        "ration_card": "राशन कार्ड संख्या",
        "submit": "जमा करें",
        "add_member": "परिवार सदस्य जोड़ें",
        "member_name": "सदस्य का पूरा नाम",
        "member_age": "सदस्य की आयु",
        "aadhar": "12 अंकों का आधार नंबर (एन्क्रिप्टेड)",
        "relation": "मुखिया से संबंध",
        "education": "शिक्षा स्तर",
        "submit_issue": "गाँव की समस्या दर्ज करें",
        "issue_category": "समस्या श्रेणी",
        "issue_title": "समस्या शीर्षक",
        "issue_description": "विस्तृत विवरण",
        "affected_count": "प्रभावित परिवारों की संख्या",
        "view_family": "मेरा परिवार और योजनाएं",
        "auth_tab": "खाता और लॉगिन"
    },
    "mr": {
        "title": "कुटुंब प्रमुख पोर्टल - स्मार्ट पंचायत",
        "subtitle": "आळंदी ग्रामपंचायत, पुणे, महाराष्ट्र",
        "household_reg": "नवीन घर नोंदणी",
        "head_name": "कुटुंब प्रमुखाचे नाव",
        "head_age": "वय",
        "head_gender": "लिंग",
        "head_occupation": "व्यवसाय",
        "contact": "संपर्क क्रमांक (फोन)",
        "address": "रहिवासी पत्ता",
        "ward": "प्रभाग / वॉर्ड क्रमांक",
        "household_type": "शिधापत्रिका प्रकार (APL / BPL / अंत्योदय)",
        "annual_income": "वार्षिक उत्पन्न (₹)",
        "ration_card": "रेशन कार्ड क्रमांक",
        "submit": "नोंदणी पूर्ण करा",
        "add_member": "कुटुंब सदस्य जोडा",
        "member_name": "सदस्याचे पूर्ण नाव",
        "member_age": "सदस्याचे वय",
        "aadhar": "१२ अंकी आधार क्रमांक (सुरक्षित/एन्क्रिप्टेड)",
        "relation": "प्रमुखाशी नाते",
        "education": "शिक्षण स्तर",
        "submit_issue": "गावातील तक्रार / समस्या नोंदवा",
        "issue_category": "समस्या प्रवर्ग",
        "issue_title": "समस्येचे शीर्षक",
        "issue_description": "तपशीलवार वर्णन",
        "affected_count": "बाधित कुटुंबांची संख्या",
        "view_family": "माझे कुटुंब व सरकारी योजना",
        "auth_tab": "खाते आणि लॉगिन"
    }
}

# Sidebar
st.sidebar.title("🏡 Smart Panchayat")
st.sidebar.markdown("**Alandi Gram Panchayat**, Pune")

lang = st.sidebar.selectbox(
    "🌐 Language / भाषा / भाषा निवडा",
    ["en", "hi", "mr"],
    format_func=lambda x: {"en": "English", "hi": "हिंदी (Hindi)", "mr": "मराठी (Marathi)"}[x]
)

# Render Authentication Box in sidebar
render_auth_sidebar(API_BASE_URL)

def get_label(key: str, l: str = "en") -> str:
    return LABELS.get(l, LABELS["en"]).get(key, key)

# Main Title Header
st.title(f"🏡 {get_label('title', lang)}")
st.caption(f"📍 {get_label('subtitle', lang)}")

# Privacy Notice
render_privacy_badge()

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    f"📝 {get_label('household_reg', lang)}",
    f"👥 {get_label('add_member', lang)}",
    f"📢 {get_label('submit_issue', lang)}",
    f"🔍 {get_label('view_family', lang)}",
    f"🔑 {get_label('auth_tab', lang)}"
])

# -------------------------------------------------------------
# TAB 1: Household Registration
# -------------------------------------------------------------
with tab1:
    st.subheader(f"🏠 {get_label('household_reg', lang)}")

    with st.form("household_registration_form"):
        col1, col2 = st.columns(2)

        with col1:
            head_name = st.text_input(get_label("head_name", lang), placeholder="e.g. Ramesh Patil")
            head_age = st.number_input(get_label("head_age", lang), min_value=18, max_value=120, value=35)
            gender = st.selectbox(get_label("head_gender", lang), ["Male", "Female", "Other"])
            occupation = st.text_input(get_label("head_occupation", lang), placeholder="e.g. Farmer / Teacher")
            contact = st.text_input(get_label("contact", lang), placeholder="e.g. +919876543210")

        with col2:
            address = st.text_area(get_label("address", lang), placeholder="e.g. House No. 42, Near Temple")
            ward_num = st.selectbox(get_label("ward", lang), [1, 2, 3, 4, 5, 6])
            hh_type = st.selectbox(get_label("household_type", lang), ["APL", "BPL", "Antodaya"])
            income = st.number_input(get_label("annual_income", lang), min_value=0, value=50000, step=5000)
            ration = st.text_input(get_label("ration_card", lang), placeholder="e.g. RC-MH-123456")

        submitted = st.form_submit_button(f"✅ {get_label('submit', lang)}", use_container_width=True)

        if submitted:
            if not head_name or not contact or not address:
                st.error("⚠️ Please fill in all required fields (Name, Contact, Address).")
            else:
                payload = {
                    "head_name": head_name,
                    "head_age": head_age,
                    "head_gender": gender,
                    "head_occupation": occupation,
                    "contact_number": contact,
                    "address": address,
                    "ward_id": ward_num,
                    "household_type": hh_type,
                    "annual_income": income,
                    "ration_card_number": ration
                }

                res = post_api(API_BASE_URL, "household/register", payload)
                if res and "id" in res:
                    st.session_state['household_id'] = res['id']
                    st.session_state['household_code'] = res['household_id']
                    st.success(f"🎉 Household Registered Successfully!")
                    st.info(f"🆔 **Your Household ID**: `{res['household_id']}` (Save this for reference)")
                    st.balloons()

# -------------------------------------------------------------
# TAB 2: Add Family Member
# -------------------------------------------------------------
with tab2:
    st.subheader(f"👥 {get_label('add_member', lang)}")

    default_hh_id = st.session_state.get('household_id', 1)
    hh_id_input = st.number_input("Household Database ID (from registration)", min_value=1, value=default_hh_id)

    with st.form("add_member_form"):
        col1, col2 = st.columns(2)

        with col1:
            member_name = st.text_input(get_label("member_name", lang), placeholder="e.g. Sunita Patil")
            member_age = st.number_input(get_label("member_age", lang), min_value=0, max_value=120, value=30)
            m_gender = st.selectbox(get_label("head_gender", lang), ["Male", "Female", "Other"], key="m_gender")
            relation = st.selectbox(
                get_label("relation", lang),
                ["Spouse", "Son", "Daughter", "Father", "Mother", "Brother", "Sister", "Grandparent", "Other"]
            )

        with col2:
            education = st.selectbox(
                get_label("education", lang),
                ["Illiterate", "Primary", "Secondary", "Higher Secondary", "Graduate", "Postgraduate"]
            )
            m_occupation = st.text_input("Occupation", placeholder="e.g. Homemaker / Student")
            aadhar_num = st.text_input(f"🔒 {get_label('aadhar', lang)}", max_chars=12, placeholder="12 digits e.g. 123456789012")
            is_student = st.checkbox("Currently a Student")
            is_employed = st.checkbox("Currently Employed")

        submitted_member = st.form_submit_button(f"➕ {get_label('add_member', lang)}", use_container_width=True)

        if submitted_member:
            if not member_name:
                st.error("⚠️ Member name is required.")
            else:
                payload = {
                    "full_name": member_name,
                    "age": member_age,
                    "gender": m_gender,
                    "relation_to_head": relation,
                    "education_level": education,
                    "occupation": m_occupation,
                    "is_student": is_student,
                    "is_employed": is_employed,
                    "has_health_issues": False
                }
                if aadhar_num and len(aadhar_num.strip()) == 12:
                    payload["aadhar_number"] = aadhar_num.strip()

                res = post_api(API_BASE_URL, f"household/{hh_id_input}/members", payload)
                if res and "id" in res:
                    st.success(f"✅ Family member **{member_name}** added successfully!")

# -------------------------------------------------------------
# TAB 3: Report Village Issue
# -------------------------------------------------------------
with tab3:
    st.subheader(f"📢 {get_label('submit_issue', lang)}")

    hh_id_issue = st.number_input("Household Database ID", min_value=1, value=st.session_state.get('household_id', 1), key="issue_hh")

    with st.form("issue_report_form"):
        category = st.selectbox(
            get_label("issue_category", lang),
            ["Water", "Sanitation", "Road & Infrastructure", "Health", "Education", "Agriculture", "Electricity", "Other"]
        )
        title = st.text_input(get_label("issue_title", lang), placeholder="e.g. Broken water pipeline on main road")
        description = st.text_area(get_label("issue_description", lang), placeholder="Describe the issue, location, and severity in detail...")
        affected = st.number_input(get_label("affected_count", lang), min_value=1, value=5)

        submitted_issue = st.form_submit_button(f"🚀 {get_label('submit', lang)}", use_container_width=True)

        if submitted_issue:
            if not title or not description:
                st.error("⚠️ Issue title and description are required.")
            else:
                payload = {
                    "category": category,
                    "title": title,
                    "description": description,
                    "affected_count": affected,
                    "language": lang
                }

                res = post_api(API_BASE_URL, f"household/{hh_id_issue}/issues", payload)
                if res and "issue_id" in res:
                    st.success(f"✅ Issue Reported Successfully! Tracking ID: **{res['issue_id']}**")
                    st.info("The AI Decision Support System will evaluate priority and recommend government schemes to the Sarpanch.")

# -------------------------------------------------------------
# TAB 4: Search & View Household Records
# -------------------------------------------------------------
with tab4:
    st.subheader("🔍 Search Household & Matched Schemes")

    col_s1, col_s2 = st.columns([3, 1])
    with col_s1:
        search_code = st.text_input("Enter Household ID Code (e.g. HH-W1-1001)", placeholder="HH-W1-1001")
    with col_s2:
        search_btn = st.button("Search Records", use_container_width=True)

    if search_btn and search_code:
        hh_data = fetch_api(API_BASE_URL, f"household/code/{search_code.strip()}")
        if hh_data:
            st.success(f"Household Found: **{hh_data.get('head_name')}**")
            c1, c2, c3 = st.columns(3)
            c1.metric("Total Members", hh_data.get("total_members", 1))
            c2.metric("Category", hh_data.get("household_type", "APL"))
            c3.metric("Ward", f"Ward {hh_data.get('ward_id', 1)}")

            # Fetch members
            members = fetch_api(API_BASE_URL, f"household/{hh_data['id']}/members")
            if members:
                st.markdown("#### 👥 Registered Family Members")
                st.table(members)
        else:
            st.warning("No household found with that ID code.")

# -------------------------------------------------------------
# TAB 5: Account & Registration
# -------------------------------------------------------------
with tab5:
    st.subheader("🔐 Resident / User Account")

    if is_authenticated():
        user = st.session_state["current_user"]
        st.success(f"Logged in as: **{user.get('full_name')}** ({user.get('email')})")
        st.info(f"Role: `{user.get('role')}` | Username: `{user.get('username')}`")
        if st.button("Log Out"):
            st.session_state["auth_token"] = None
            st.session_state["current_user"] = None
            st.rerun()
    else:
        col_login, col_register = st.columns(2)

        with col_login:
            st.markdown("### 🔑 Sign In")
            with st.form("main_login_form"):
                u_name = st.text_input("Username or Email")
                u_pwd = st.text_input("Password", type="password")
                btn_login = st.form_submit_button("Sign In", use_container_width=True)

                if btn_login and u_name and u_pwd:
                    res = post_api(API_BASE_URL, "auth/login", {
                        "username_or_email": u_name,
                        "password": u_pwd
                    })
                    if res and "access_token" in res:
                        st.session_state["auth_token"] = res["access_token"]
                        st.session_state["current_user"] = res["user"]
                        st.success(f"Welcome back, {res['user']['full_name']}!")
                        st.rerun()

        with col_register:
            st.markdown("### 📝 Create New Account")
            with st.form("main_register_form"):
                reg_name = st.text_input("Full Name", placeholder="e.g. Santosh Shinde")
                reg_uname = st.text_input("Username", placeholder="e.g. santosh_s")
                reg_email = st.text_input("Email", placeholder="e.g. santosh@example.com")
                reg_phone = st.text_input("Mobile Number", placeholder="+919876543210")
                reg_pwd = st.text_input("Password (min 6 chars)", type="password")
                reg_role = st.selectbox("Role", ["Family Head", "Sarpanch", "Panchayat Admin"])
                btn_reg = st.form_submit_button("Create Account", use_container_width=True)

                if btn_reg:
                    if not reg_name or not reg_uname or not reg_email or not reg_pwd:
                        st.error("Please fill all required registration fields.")
                    else:
                        payload = {
                            "full_name": reg_name,
                            "username": reg_uname,
                            "email": reg_email,
                            "password": reg_pwd,
                            "phone_number": reg_phone,
                            "role": reg_role,
                            "preferred_language": lang
                        }
                        res = post_api(API_BASE_URL, "auth/register", payload)
                        if res and "access_token" in res:
                            st.session_state["auth_token"] = res["access_token"]
                            st.session_state["current_user"] = res["user"]
                            st.success("Account created successfully!")
                            st.rerun()
