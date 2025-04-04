import os
from dotenv import load_dotenv
import google.generativeai as genai  ✅  # CORRECT
import streamlit as st
import requests
from bs4 import BeautifulSoup

# ✅ Load .env locally, but use st.secrets in production
load_dotenv()
api_key = st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY"))

# ✅ Check if key exists
if not api_key:
    st.error("❌ GEMINI_API_KEY not found in secrets or .env file.")
    raise ValueError("API key missing")

# ✅ Initialize Gemini Client
try:
    client = genai.Client(api_key=api_key)
except Exception as e:
    st.error(f"❌ Failed to create Gemini client: {e}")
    raise

# ✅ Disney IP Check Function
def is_disney_content(title, description):
    prompt = f"""
    You are a copyright checker AI. Check if the following content is related to Disney:

    Title: {title}
    Description: {description}

    Respond ONLY in JSON:
    {{
        "is_disney": true/false,
        "reason": "Explain why"
    }}
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        cleaned = response.text.strip().strip("`").replace("json", "").strip()
        return cleaned

    except Exception as e:
        st.error(f"❌ Gemini API call failed: {e}")
        return '{"error": "Gemini API call failed"}'

# ✅ Webpage Piracy Checker
def analyze_webpage_with_gemini(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text()[:5000]
    except Exception as e:
        return f'{{"error": "Failed to fetch page: {e}"}}'

    prompt = f"""
You are a piracy detection expert.

Analyze the following webpage text and estimate if it contains links or references to pirated Disney movies.

Webpage Text:
{text}

Respond in JSON format like:
{{
  "is_pirated": true/false,
  "confidence": 0-100,
  "reason": "Short reason"
}}
"""

    try:
        gemini_response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        return gemini_response.text
    except Exception as e:
        return f'{{"error": "Gemini analysis failed: {e}"}}'
