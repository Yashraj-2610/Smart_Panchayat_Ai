# Phase 3: Voice Interface Component (Text-to-Speech / Speech-to-Text)
# Ready to integrate with gTTS / speech_recognition libraries

import streamlit as st

API_BASE_URL = st.secrets.get("API_BASE_URL", "http://localhost:8000/api/v1")

def render_voice_input():
    """Voice input for issue reporting (speech-to-text placeholder)"""
    st.subheader("🎙 Voice Report Issue")

    # Note: Full voice integration requires speech_recognition + gTTS
    # These are optional dependencies listed in requirements
    try:
        import speech_recognition as sr
        HAS_SPEECH = True
    except ImportError:
        HAS_SPEECH = False

    if HAS_SPEECH:
        st.info("Speech recognition available. Click below to record.")
        # Placeholder for actual recording logic
        if st.button("🔴 Start Voice Recording", type="primary"):
            st.success("Voice recorded (demo mode). In production, this passes audio to STT service.")
    else:
        st.warning("Speech recognition library not installed. Add `speech_recognition` to requirements.txt for full voice support.")
        # Provide manual input as fallback
        voice_text = st.text_area("Or type description:", placeholder="Describe the village issue...")
        if st.button("Submit Voice Description", help="Fallback when STT unavailable"):
            st.info(f"Submitted: {voice_text[:100]}...")

def render_voice_output():
    """Text-to-speech for AI recommendations"""
    st.subheader("🔊 Listen to AI Recommendations")

    try:
        import gtts
        HAS_TTS = True
    except ImportError:
        HAS_TTS = False

    recommendation_text = st.text_area("Recommendation text to read aloud:",
                                      value="Water pipeline repair needed in Ward 3. Apply for Jal Jeevan Mission.")

    if HAS_TTS:
        if st.button("🔊 Play Recommendation"):
            # In production: generate audio file with gTTS and serve via Streamlit
            # For now, show that TTS is ready
            st.info("Text-to-speech enabled (gTTS). Audio file generation available.")
    else:
        st.info("Text-to-speech library (gTTS) not installed. Add to requirements for voice output.")
