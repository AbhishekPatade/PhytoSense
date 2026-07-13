"""
Language support module for PhytoSense application.
Provides multi-language support for the application using deep-translator.
"""

import streamlit as st
from deep_translator import GoogleTranslator
import json
import os

# cache file to store translations
CACHE_FILE = "translations_cache.json"
if os.path.exists(CACHE_FILE):
    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            translations_cache = json.load(f)
    except Exception:
        translations_cache = {}
else:
    translations_cache = {}

def save_cache():
    try:
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(translations_cache, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

def translate_text(text: str, dest: str) -> str:
    """Translate a single string with caching (deep-translator)."""
    if not text:
        return ""
    key = f"{dest}|{text}"
    if key in translations_cache:
        return translations_cache[key]
    try:
        result = GoogleTranslator(source="auto", target=dest).translate(text)
    except Exception:
        result = text  # fallback
    translations_cache[key] = result
    save_cache()
    return result

def initialize_language():
    """Setup language selector in sidebar"""
    lang = st.sidebar.selectbox(
        "🌐 Select Language",
        ["en", "hi", "mr"],  # English, Hindi, Marathi
        index=0
    )
    return lang

def t(text: str, lang: str) -> str:
    """Helper to wrap translatable strings"""
    if lang == "en":
        return text
    return translate_text(text, lang)

# Optional: helper to translate DataFrames
import pandas as pd
def translate_dataframe(df: pd.DataFrame, lang: str) -> pd.DataFrame:
    """Translate all text columns in a dataframe"""
    if lang == "en":
        return df
    df = df.copy()
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].apply(lambda x: translate_text(str(x), lang))
    return df
