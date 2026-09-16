import streamlit as st
import requests
import json
import os

# Configuration - Support environment variables for deployment
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000/api/v1")


# Multilingual labels
LABELS = {
    "en": {
        "title": "Family Head Portal - Household Registration",
        "household_reg": "Household Registration",
        "head_name": "Head of Family Name",
        "head_age": "Age",
        "head_gender": "Gender",
        "head_occupation": "Occupation",
        "contact": "Contact Number",
        "address": "Address",
        "ward": "Ward Number",
        "household_type": "Household Type",
        "annual_income": "Annual Income (₹)",
        "ration_card": "Ration Card Number",
        "submit": "Register Household",
        "add_member": "Add Family Member",
        "member_name": "Full Name",
        "member_age": "Age",
        "relation": "Relation to Head",
        "education": "Education Level",
        "submit_issue": "Report Village Issue",
        "issue_category": "Issue Category",
        "issue_title": "Issue Title",
        "issue_description": "Description",
        "affected_count": "Number of Affected Households"
    },
    "hi": {
        "title": "परिवार मुखिया पोर्टल - घर पंजीकरण",
        "household_reg": "घर का पंजीकरण",
        "head_name": "परिवार मुखिया का नाम",
        "head_age": "आयु",
        "head_gender": "लिंग",
        "head_occupation": "व्यवसाय",
        "contact": "संपर्क नंबर",
        "address": "पता",
        "ward": "वार्ड संख्या",
        "household_type": "घर का प्रकार",
        "annual_income": "वार्षिक आय (₹)",
        "ration_card": "राशन कार्ड संख्या",
        "submit": "घर पंजीकृत करें",
        "add_member": "परिवार सदस्य जोड़ें",
        "member_name": "पूरा नाम",
        "member_age": "आयु",
        "relation": "मुखिया से संबंध",
        "education": "शिक्षा स्तर",
        "submit_issue": "गाँव की समस्या दर्ज करें",
        "issue_category": "समस्या श्रेणी",
        "issue_title": "समस्या शीर्षक",
        "issue_description": "विवरण",
        "affected_count": "प्रभावित घरों की संख्या"
    },
    "mr": {
        "title": "कुटुंब मुख्य पोर्टल - घर नोंदणी",
        "household_reg": "घर नोंदणी",
        "head_name": "कुटुंब प्रमुखाचे नाव",
        "head_age": "वय",
        "head_gender": "लिंग",
        "head_occupation": "व्यवसाय",
        "contact": "संपर्क क्रमांक",
        "address": "पत्ता",
        "ward": "प्रभाग क्रमांक",
        "household_type": "घराचा प्रकार",
        "annual_income": "वार्षिक उत्पन्न (₹)",
        "ration_card": "रेशन कार्ड क्रमांक",
        "submit": "घर नोंदवा",
        "add_member": "कुटुंब सदस्य जोडा",
        "member_name": "पूर्ण नाव",
        "member_age": "वय",
        "relation": "प्रमुखाशी संबंध",
        "education": "शिक्षण स्तर",
        "submit_issue": "गावातील समस्या नोंदवा",
        "issue_category": "समस्या श्रेणी",
        "issue_title": "समस्या शीर्षक",
        "issue_description": "तपशील",
        "affected_count": "प्रभावित घरांची संख्या"
    }
}

def get_label(key, lang):
    return LABELS.get(lang, LABELS["en"]).get(key, key)

st.set_page_config(page_title="Smart Panchayat - Family Portal", page_icon="🏠", layout="wide")

# Language selector in sidebar
lang = st.sidebar.selectbox("Language / भाषा / भाषा", ["en", "hi", "mr"], format_func=lambda x: {"en": "English", "hi": "हिंदी", "mr": "मराठी"}[x])

st.title(get_label("title", lang))

# Tabs for different functions
tab1, tab2, tab3 = st.tabs([
    get_label("household_reg", lang),
    get_label("add_member", lang),
    get_label("submit_issue", lang)
])

# Tab 1: Household Registration
with tab1:
    st.header(get_label("household_reg", lang))

    with st.form("household_form"):
        col1, col2 = st.columns(2)

        with col1:
            head_name = st.text_input(get_label("head_name", lang))
            head_age = st.number_input(get_label("head_age", lang), min_value=18, max_value=120, value=35)
            head_gender = st.selectbox(get_label("head_gender", lang), ["Male", "Female", "Other"])
            head_occupation = st.text_input(get_label("head_occupation", lang))

        with col2:
            contact = st.text_input(get_label("contact", lang), placeholder="+91XXXXXXXXXX")
            ward = st.selectbox(get_label("ward", lang), list(range(1, 7)))
            household_type = st.selectbox(get_label("household_type", lang), ["APL", "BPL", "Antodaya"])
            annual_income = st.number_input(get_label("annual_income", lang), min_value=0, value=50000)

        address = st.text_area(get_label("address", lang))
        ration_card = st.text_input(get_label("ration_card", lang))

        submitted = st.form_submit_button(get_label("submit", lang))

        if submitted:
            payload = {
                "head_name": head_name,
                "head_age": head_age,
                "head_gender": head_gender,
                "head_occupation": head_occupation,
                "contact_number": contact,
                "address": address,
                "ward_id": ward,
                "household_type": household_type,
                "annual_income": annual_income,
                "ration_card_number": ration_card
            }

            try:
                response = requests.post(f"{API_BASE_URL}/household/register", json=payload)
                if response.status_code == 201:
                    data = response.json()
                    st.success(f"✅ Household registered successfully! Your Household ID: **{data['household_id']}**")
                    st.session_state['household_id'] = data['id']
                else:
                    st.error(f"Error: {response.text}")
            except Exception as e:
                st.error(f"Connection error: {e}")

# Tab 2: Add Family Member
with tab2:
    st.header(get_label("add_member", lang))

    household_id = st.number_input("Household ID (Database ID)", min_value=1, value=st.session_state.get('household_id', 1))

    with st.form("member_form"):
        col1, col2 = st.columns(2)

        with col1:
            member_name = st.text_input(get_label("member_name", lang))
            member_age = st.number_input(get_label("member_age", lang), min_value=0, max_value=120, value=10)
            gender = st.selectbox(get_label("head_gender", lang), ["Male", "Female", "Other"])
            relation = st.text_input(get_label("relation", lang), placeholder="Son, Daughter, Spouse, etc.")

        with col2:
            education = st.selectbox(get_label("education", lang),
                                    ["Illiterate", "Primary", "Secondary", "Higher Secondary", "Graduate", "Postgraduate"])
            occupation = st.text_input(get_label("head_occupation", lang))
            is_student = st.checkbox("Is Student?")
            is_employed = st.checkbox("Is Employed?")

        submitted_member = st.form_submit_button(get_label("submit", lang))

        if submitted_member:
            payload = {
                "full_name": member_name,
                "age": member_age,
                "gender": gender,
                "relation_to_head": relation,
                "education_level": education,
                "occupation": occupation,
                "is_student": is_student,
                "is_employed": is_employed,
                "has_health_issues": False
            }

            try:
                response = requests.post(f"{API_BASE_URL}/household/{household_id}/members", json=payload)
                if response.status_code == 201:
                    st.success("✅ Family member added successfully!")
                else:
                    st.error(f"Error: {response.text}")
            except Exception as e:
                st.error(f"Connection error: {e}")

# Tab 3: Report Issue
with tab3:
    st.header(get_label("submit_issue", lang))

    household_id_issue = st.number_input("Household ID", min_value=1, value=st.session_state.get('household_id', 1), key="issue_hh")

    with st.form("issue_form"):
        category = st.selectbox(get_label("issue_category", lang),
                               ["Water", "Sanitation", "Road & Infrastructure", "Health", "Education", "Agriculture", "Electricity", "Other"])
        title = st.text_input(get_label("issue_title", lang))
        description = st.text_area(get_label("issue_description", lang))
        affected = st.number_input(get_label("affected_count", lang), min_value=1, value=1)

        submitted_issue = st.form_submit_button(get_label("submit", lang))

        if submitted_issue:
            payload = {
                "category": category,
                "title": title,
                "description": description,
                "affected_count": affected,
                "language": lang
            }

            try:
                response = requests.post(f"{API_BASE_URL}/household/{household_id_issue}/issues", json=payload)
                if response.status_code == 201:
                    data = response.json()
                    st.success(f"✅ Issue reported successfully! Issue ID: **{data['issue_id']}**")
                else:
                    st.error(f"Error: {response.text}")
            except Exception as e:
                st.error(f"Connection error: {e}")
