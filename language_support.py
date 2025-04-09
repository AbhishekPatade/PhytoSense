"""
Language support module for PhytoSense application.
Provides multi-language support for the application.
"""

import streamlit as st
import json
import os

# Available languages
AVAILABLE_LANGUAGES = {
    "en": "English",
    "hi": "हिंदी (Hindi)",
    "mr": "मराठी (Marathi)",
    "gu": "ગુજરાતી (Gujarati)",
    "bn": "বাংলা (Bengali)"
}

# Default translations path
TRANSLATIONS_PATH = "translations"

def initialize_language():
    """
    Initialize language support
    """
    # Create translations directory if it doesn't exist
    if not os.path.exists(TRANSLATIONS_PATH):
        os.makedirs(TRANSLATIONS_PATH, exist_ok=True)
    
    # For each language, create an empty translation file if it doesn't exist
    for lang_code in AVAILABLE_LANGUAGES:
        lang_file = os.path.join(TRANSLATIONS_PATH, f"{lang_code}.json")
        if not os.path.exists(lang_file):
            with open(lang_file, 'w') as f:
                json.dump({}, f)

def load_translations(lang_code):
    """
    Load translations for a specific language
    
    Args:
        lang_code: Language code
        
    Returns:
        dict: Translations dictionary
    """
    # Default to English if language code is not valid
    if lang_code not in AVAILABLE_LANGUAGES:
        lang_code = "en"
    
    # Try to load translations from file
    translations_file = os.path.join(TRANSLATIONS_PATH, f"{lang_code}.json")
    
    try:
        if os.path.exists(translations_file):
            with open(translations_file, 'r', encoding='utf-8') as f:
                return json.load(f)
    except (json.JSONDecodeError, IOError):
        pass
    
    # Return empty dictionary if translations couldn't be loaded
    return {}

def t(text, lang_code=None):
    """
    Translate text
    
    Args:
        text: Text to translate
        lang_code: Optional language code (defaults to session state language)
        
    Returns:
        string: Translated text
    """
    # Get language code from session state if not provided
    if lang_code is None:
        lang_code = st.session_state.get("language", "en")
    
    # Return original text if using English
    if lang_code == "en":
        return text
    
    # Load translations
    translations = load_translations(lang_code)
    
    # Return translation if available, otherwise return original text
    return translations.get(text, text)

def show_language_selector():
    """
    Display language selector in sidebar
    """
    # Show language selector
    st.sidebar.markdown("### 🌐 Language / भाषा")
    
    # Get current language from session state
    current_lang = st.session_state.get("language", "en")
    
    # Display language selector
    selected_lang = st.sidebar.selectbox(
        "Select Language",
        options=list(AVAILABLE_LANGUAGES.keys()),
        format_func=lambda x: AVAILABLE_LANGUAGES[x],
        index=list(AVAILABLE_LANGUAGES.keys()).index(current_lang)
    )
    
    # Update session state if language changed
    if selected_lang != current_lang:
        st.session_state.language = selected_lang
        st.rerun()
    
    # Display language information
    if selected_lang != "en":
        st.sidebar.info(f"Some content may still appear in English if translations are not available.")

def get_available_languages():
    """
    Get list of available languages
    
    Returns:
        dict: Available languages dictionary
    """
    return AVAILABLE_LANGUAGES

def add_translation(text, translation, lang_code):
    """
    Add a translation to the language file
    
    Args:
        text: Original text
        translation: Translated text
        lang_code: Language code
        
    Returns:
        bool: Success status
    """
    # Ignore English (source language)
    if lang_code == "en":
        return True
    
    # Load existing translations
    translations = load_translations(lang_code)
    
    # Add new translation
    translations[text] = translation
    
    # Save translations
    translations_file = os.path.join(TRANSLATIONS_PATH, f"{lang_code}.json")
    
    try:
        with open(translations_file, 'w', encoding='utf-8') as f:
            json.dump(translations, f, ensure_ascii=False, indent=2)
        return True
    except IOError:
        return False

# Populate translations for common UI elements
def populate_default_translations():
    """
    Populate default translations for common UI elements
    """
    # Hindi translations
    hindi_translations = {
        "Login to PhytoSense": "फाइटोसेंस में लॉगिन करें",
        "Username": "उपयोगकर्ता नाम",
        "Password": "पासवर्ड",
        "Login": "लॉगिन करें",
        "Create Account": "अकाउंट बनाएं",
        "Welcome to PhytoSense": "फाइटोसेंस में आपका स्वागत है",
        "Plant Health Analysis": "पौधे का स्वास्थ्य विश्लेषण",
        "Soil Analysis": "मिट्टी का विश्लेषण",
        "Weather Alerts": "मौसम चेतावनी",
        "Resources": "संसाधन",
        "History": "इतिहास",
        "Dashboard": "डैशबोर्ड",
        "Logout": "लॉगआउट करें"
    }
    
    # Marathi translations
    marathi_translations = {
        "Login to PhytoSense": "फायटोसेन्समध्ये लॉगिन करा",
        "Username": "वापरकर्ता नाव",
        "Password": "पासवर्ड",
        "Login": "लॉगिन करा",
        "Create Account": "खाते तयार करा",
        "Welcome to PhytoSense": "फायटोसेन्समध्ये आपले स्वागत आहे",
        "Plant Health Analysis": "वनस्पती आरोग्य विश्लेषण",
        "Soil Analysis": "माती विश्लेषण",
        "Weather Alerts": "हवामान सूचना",
        "Resources": "संसाधने",
        "History": "इतिहास",
        "Dashboard": "डॅशबोर्ड",
        "Logout": "लॉगआउट करा"
    }
    
    # Save translations
    for lang_code, translations in [("hi", hindi_translations), ("mr", marathi_translations)]:
        for text, translation in translations.items():
            add_translation(text, translation, lang_code)
