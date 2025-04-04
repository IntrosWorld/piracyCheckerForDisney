import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai
import requests
from bs4 import BeautifulSoup

# ✅ Load API Key (use secrets for deployment)
api_key = st.secrets["GEMINI_API_KEY"] if "GEMINI_API_KEY" in st.secrets else os.getenv("GEMINI_API_KEY")

# ✅ Check if key is present
if not api_key:
    st.error("❌ GEMINI_API_KEY not found in Streamlit secrets or .env file.")
    raise ValueError("API key missing")

# ✅ Configure Gemini client
genai.configure(api_key=api_key)

# ✅ Initialize model
model = genai.GenerativeModel("gemini-pro")


# ✅ Function to check Disney IP violation from title + description
def is_disney_content(title, description):
    prompt = f"""
You are a copyright checker AI. Check if the following content is related to Disney:

Title: {title}
Description: {description}

Respond ONLY in JSON:
{{
  "is_disney": true/false,
  "reason": "Explain briefly why"
}}
"""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"❌ Gemini API call failed: {e}")
        return '{"error": "Gemini API call failed"}'


# ✅ Function to analyze any webpage for pirated Disney content
def analyze_webpage_with_gemini(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text()[:5000]  # Gemini input limit
    except Exception as e:
        return f'{{"error": "Failed to fetch page: {e}"}}'

    prompt = f"""
You are a piracy detection expert AI.

Analyze the following webpage and detect if it contains references or links to pirated Disney content.

Text:
{text}

Respond in JSON format:
{{
  "is_pirated": true/false,
  "confidence": 0-100,
  "reason": "Brief explanation"
}}
"""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f'{{"error": "Gemini analysis failed: {e}"}}'

