import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai
import requests
from bs4 import BeautifulSoup

# ✅ Load environment and secrets
load_dotenv()
api_key = st.secrets["GEMINI_API_KEY"] if "GEMINI_API_KEY" in st.secrets else os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("❌ GEMINI_API_KEY not found in secrets or .env")
    raise ValueError("Missing Gemini API Key")

# ✅ Configure Gemini and initialize model
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-pro")

# ✅ For testing inside your Streamlit app
def test_gemini_api():
    prompt = "Respond with a JSON: {\"status\": \"Gemini is working fine!\"}"
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f'{{"error": "Gemini test failed: {e}"}}'

# ✅ Check if content is Disney IP related
def is_disney_content(title, description):
    prompt = f"""
You are a copyright checker AI. Determine if the following is Disney-related content.

Title: {title}
Description: {description}

Respond ONLY in JSON:
{{
  "is_disney": true/false,
  "reason": "Short explanation"
}}
"""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f'{{"error": "Gemini Disney check failed: {e}"}}'

# ✅ Analyze webpage for Disney piracy risk
def analyze_webpage_with_gemini(url):
    try:
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        page_text = soup.get_text()[:5000]  # Limit to Gemini input size
    except Exception as e:
        return f'{{"error": "Failed to fetch page: {e}"}}'

    prompt = f"""
You are a piracy detection expert AI.

Analyze the webpage content and detect if it contains references or links to pirated Disney content.

Webpage Text:
{page_text}

Respond ONLY in JSON:
{{
  "is_pirated": true/false,
  "confidence": 0-100,
  "reason": "Short explanation"
}}
"""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f'{{"error": "Gemini analysis failed: {e}"}}'
