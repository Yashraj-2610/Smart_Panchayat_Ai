from typing import Dict, Any

class MultilingualService:
    """
    Multilingual support for English, Hindi, and Marathi
    Uses translation dictionaries for UI labels and messages
    For AI-generated content, translation would integrate with translation APIs
    """

    TRANSLATIONS = {
        "en": {
            "welcome": "Welcome to Smart Panchayat System",
            "household_registration": "Household Registration",
            "family_members": "Family Members",
            "submit_issue": "Submit Issue",
            "view_issues": "View Issues",
            "dashboard": "Dashboard",
            "total_population": "Total Population",
            "total_households": "Total Households",
            "male": "Male",
            "female": "Female",
            "children": "Children",
            "adults": "Adults",
            "senior_citizens": "Senior Citizens",
            "literacy_rate": "Literacy Rate",
            "employment_rate": "Employment Rate",
            "water": "Water",
            "sanitation": "Sanitation",
            "health": "Health",
            "education": "Education",
            "agriculture": "Agriculture",
            "infrastructure": "Infrastructure",
            "issue_submitted": "Issue submitted successfully",
            "household_registered": "Household registered successfully",
            "member_added": "Family member added successfully"
        },
        "hi": {
            "welcome": "स्मार्ट पंचायत प्रणाली में आपका स्वागत है",
            "household_registration": "घर का पंजीकरण",
            "family_members": "परिवार के सदस्य",
            "submit_issue": "समस्या दर्ज करें",
            "view_issues": "समस्याएं देखें",
            "dashboard": "डैशबोर्ड",
            "total_population": "कुल जनसंख्या",
            "total_households": "कुल घर",
            "male": "पुरुष",
            "female": "महिला",
            "children": "बच्चे",
            "adults": "वयस्क",
            "senior_citizens": "वरिष्ठ नागरिक",
            "literacy_rate": "साक्षरता दर",
            "employment_rate": "रोजगार दर",
            "water": "पानी",
            "sanitation": "स्वच्छता",
            "health": "स्वास्थ्य",
            "education": "शिक्षा",
            "agriculture": "कृषि",
            "infrastructure": "बुनियादी ढांचा",
            "issue_submitted": "समस्या सफलतापूर्वक दर्ज की गई",
            "household_registered": "घर सफलतापूर्वक पंजीकृत हुआ",
            "member_added": "परिवार के सदस्य सफलतापूर्वक जोड़े गए"
        },
        "mr": {
            "welcome": "स्मार्ट पंचायत प्रणालीमध्ये आपले स्वागत आहे",
            "household_registration": "घर नोंदणी",
            "family_members": "कुटुंब सदस्य",
            "submit_issue": "समस्या नोंदवा",
            "view_issues": "समस्या पहा",
            "dashboard": "डॅशबोर्ड",
            "total_population": "एकूण लोकसंख्या",
            "total_households": "एकूण घरे",
            "male": "पुरुष",
            "female": "स्त्री",
            "children": "मुले",
            "adults": "प्रौढ",
            "senior_citizens": "ज्येष्ठ नागरिक",
            "literacy_rate": "साक्षरता दर",
            "employment_rate": "रोजगार दर",
            "water": "पाणी",
            "sanitation": "स्वच्छता",
            "health": "आरोग्य",
            "education": "शिक्षण",
            "agriculture": "कृषी",
            "infrastructure": "पायाभूत सुविधा",
            "issue_submitted": "समस्या यशस्वीरित्या नोंदविली",
            "household_registered": "घर यशस्वीरित्या नोंदणीकृत झाले",
            "member_added": "कुटुंब सदस्य यशस्वीरित्या जोडले"
        }
    }

    @staticmethod
    def get_text(key: str, language: str = "en") -> str:
        """Get translated text for a given key and language"""
        lang_dict = MultilingualService.TRANSLATIONS.get(language, MultilingualService.TRANSLATIONS["en"])
        return lang_dict.get(key, key)

    @staticmethod
    def translate_dict(data: Dict[str, Any], language: str = "en") -> Dict[str, Any]:
        """Translate dictionary keys using the translation map"""
        if language == "en":
            return data

        translated = {}
        for key, value in data.items():
            translated_key = MultilingualService.get_text(key, language)
            translated[translated_key] = value
        return translated

    @staticmethod
    def get_supported_languages():
        """Return list of supported language codes"""
        return list(MultilingualService.TRANSLATIONS.keys())
