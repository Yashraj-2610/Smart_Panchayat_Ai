from fastapi import APIRouter, Query
from ...services.multilingual_service import MultilingualService

router = APIRouter()

@router.get("/languages")
def get_supported_languages():
    """Get list of supported language codes"""
    return {
        "supported_languages": MultilingualService.get_supported_languages(),
        "default": "mr"
    }

@router.get("/translate/{key}")
def translate_key(key: str, lang: str = Query("en", regex="^(en|hi|mr)$")):
    """Translate a UI label key to the specified language"""
    return {
        "key": key,
        "language": lang,
        "translated_text": MultilingualService.get_text(key, lang)
    }

@router.post("/translate-dict")
def translate_dictionary(data: dict, lang: str = Query("en", regex="^(en|hi|mr)$")):
    """Translate dictionary keys to specified language"""
    return {
        "language": lang,
        "translated_data": MultilingualService.translate_dict(data, lang)
    }
