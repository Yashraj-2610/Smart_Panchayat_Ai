import json
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from ..models.scheme import Scheme, SchemeCategory, SchemeLevel

class RAGService:
    """
    RAG (Retrieval-Augmented Generation) Service for Government Schemes
    Matches identified problems with relevant central and state schemes
    """

    GOVERNMENT_SCHEMES_DATA = [
        {
            "scheme_id": "JJM-001",
            "name": "Jal Jeevan Mission (JJM)",
            "name_hindi": "जल जीवन मिशन",
            "name_marathi": "जल जीवन मिशन",
            "category": "Water & Sanitation",
            "level": "Central",
            "description": "Aims to provide safe and adequate drinking water through individual household tap connections by 2024 to all rural households.",
            "eligibility_criteria": "All rural households without functional tap water connection.",
            "benefits": "Functional household tap connection providing 55 liters per capita per day.",
            "keywords": ["water", "drinking water", "tap", "pipeline", "scarcity", "potable water", "जल", "पाणी"]
        },
        {
            "scheme_id": "SBM-G-002",
            "name": "Swachh Bharat Mission (Grameen) Phase II",
            "name_hindi": "स्वच्छ भारत मिशन (ग्रामीण)",
            "name_marathi": "स्वच्छ भारत अभियान (ग्रामीण)",
            "category": "Water & Sanitation",
            "level": "Central",
            "description": "Focuses on sustaining the Open Defecation Free (ODF) status and management of solid and liquid waste (SLWM).",
            "eligibility_criteria": "Rural households without individual household latrines (IHHL).",
            "benefits": "Financial incentive of Rs 12,000 for construction of toilet; community sanitary complexes.",
            "keywords": ["sanitation", "toilet", "waste", "drainage", "garbage", "cleanliness", "शौचालय", "स्वच्छता"]
        },
        {
            "scheme_id": "AB-PMJAY-003",
            "name": "Ayushman Bharat - PMJAY",
            "name_hindi": "आयुष्मान भारत - प्रधानमंत्री जन आरोग्य योजना",
            "name_marathi": "आयुष्मान भारत - प्रधानमंत्री जन आरोग्य योजना",
            "category": "Health",
            "level": "Central",
            "description": "Provides health insurance cover of up to Rs 5 lakh per family per year for secondary and tertiary care hospitalization.",
            "eligibility_criteria": "Families listed in SECC database / BPL cardholders / identified deprived categories.",
            "benefits": "Cashless access to healthcare services at empaneled hospitals up to Rs 5 Lakhs.",
            "keywords": ["health", "hospital", "illness", "treatment", "disease", "medical", "doctor", "दवा", "आरोग्य", "दवाखाना"]
        },
        {
            "scheme_id": "PM-KISAN-004",
            "name": "PM Kisan Samman Nidhi",
            "name_hindi": "प्रधानमंत्री किसान सम्मान निधि",
            "name_marathi": "प्रधानमंत्री किसान सन्मान निधी",
            "category": "Agriculture",
            "level": "Central",
            "description": "Provides income support of Rs 6,000 per year to all landholding farmer families.",
            "eligibility_criteria": "All landholding farmer families with cultivable land.",
            "benefits": "Rs 6,000 per year in three equal installments of Rs 2,000 directly into bank accounts.",
            "keywords": ["farmer", "agriculture", "crop", "farming", "subsidy", "seeds", "fertilizer", "किसान", "शेतकरी", "पीक"]
        },
        {
            "scheme_id": "PMAY-G-005",
            "name": "Pradhan Mantri Awaas Yojana - Gramin",
            "name_hindi": "प्रधानमंत्री आवास योजना - ग्रामीण",
            "name_marathi": "प्रधानमंत्री आवास योजना - ग्रामीण",
            "category": "Housing",
            "level": "Central",
            "description": "Provides financial assistance for construction of pucca house with basic amenities to houseless and kutcha house dwellers.",
            "eligibility_criteria": "Houseless or living in 0, 1, 2 room kutcha houses according to SECC data.",
            "benefits": "Financial assistance of Rs 1.20 lakh in plain areas and Rs 1.30 lakh in hilly areas plus MGNREGS wages.",
            "keywords": ["house", "housing", "pucca house", "roof", "shelter", "kutcha", "घर", "आवास"]
        },
        {
            "scheme_id": "PMGSY-006",
            "name": "Pradhan Mantri Gram Sadak Yojana",
            "name_hindi": "प्रधानमंत्री ग्राम सड़क योजना",
            "name_marathi": "प्रधानमंत्री ग्राम सडक योजना",
            "category": "Infrastructure",
            "level": "Central",
            "description": "Provides all-weather road connectivity to unconnected eligible habitations in rural areas.",
            "eligibility_criteria": "Habitations with population 500+ (plain areas) or 250+ (hilly/tribal areas).",
            "benefits": "Construction of all-weather bituminous road connecting the village to main road network.",
            "keywords": ["road", "pothole", "connectivity", "transport", "bridge", "street", "सड़क", "रस्ता", "मार्ग"]
        },
        {
            "scheme_id": "SSA-007",
            "name": "Samagra Shiksha Abhiyan",
            "name_hindi": "समग्र शिक्षा अभियान",
            "name_marathi": "समग्र शिक्षा अभियान",
            "category": "Education",
            "level": "Central",
            "description": "Overarching program for school education sector extending from pre-school to class 12.",
            "eligibility_criteria": "Government and government-aided schools in rural and urban areas.",
            "benefits": "Free textbooks, uniforms, transport allowance, school infrastructure development.",
            "keywords": ["school", "education", "books", "uniform", "dropout", "teacher", "student", "शाळा", "शिक्षण", "विद्यार्थी"]
        },
        {
            "scheme_id": "MH-MAGS-008",
            "name": "Maharashtra Mukhyamantri Saur Krushi Vahini Yojana",
            "name_hindi": "मुख्यमंत्री सौर कृषि वाहिनी योजना",
            "name_marathi": "मुख्यमंत्री सौर कृषी वाहिनी योजना",
            "category": "Agriculture",
            "level": "State",
            "description": "Solar power feeder program to provide daytime reliable electricity supply to farmers in Maharashtra.",
            "eligibility_criteria": "Agricultural pumps and farmer groups in Maharashtra.",
            "benefits": "Daytime 8-hour solar power supply for irrigation pumps.",
            "keywords": ["electricity", "solar", "irrigation", "power", "pump", "farmer", "वीज", "सौर ऊर्जा"]
        }
    ]

    @staticmethod
    def seed_schemes(db: Session):
        """Seed the database with standard government schemes if not already present"""
        for scheme_data in RAGService.GOVERNMENT_SCHEMES_DATA:
            existing = db.query(Scheme).filter(Scheme.scheme_id == scheme_data["scheme_id"]).first()
            if not existing:
                category_enum = getattr(SchemeCategory, scheme_data["category"].upper().replace(" & ", "_").replace(" ", "_"), SchemeCategory.SOCIAL_WELFARE)
                level_enum = SchemeLevel.CENTRAL if scheme_data["level"] == "Central" else SchemeLevel.STATE

                scheme = Scheme(
                    scheme_id=scheme_data["scheme_id"],
                    name=scheme_data["name"],
                    name_hindi=scheme_data.get("name_hindi"),
                    name_marathi=scheme_data.get("name_marathi"),
                    category=category_enum,
                    level=level_enum,
                    description=scheme_data["description"],
                    eligibility_criteria=scheme_data["eligibility_criteria"],
                    benefits=scheme_data["benefits"]
                )
                db.add(scheme)
        db.commit()

    @staticmethod
    def retrieve_relevant_schemes(query: str, domain: str = None, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Semantic/keyword retrieval matching problem description with government schemes
        """
        query_lower = query.lower()
        scored_schemes = []

        for s in RAGService.GOVERNMENT_SCHEMES_DATA:
            score = 0
            # Domain match
            if domain and domain.lower() in s["category"].lower():
                score += 5

            # Keyword matching
            for kw in s.get("keywords", []):
                if kw.lower() in query_lower:
                    score += 3

            # Description words matching
            desc_words = set(s["description"].lower().split())
            query_words = set(query_lower.split())
            common_words = desc_words.intersection(query_words)
            score += len(common_words)

            if score > 0:
                scored_schemes.append((score, s))

        # Sort by match score descending
        scored_schemes.sort(key=lambda x: x[0], reverse=True)

        return [item[1] for item in scored_schemes[:top_k]]
