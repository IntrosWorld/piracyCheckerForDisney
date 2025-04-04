# gemini_utils.py
import os
import requests
from bs4 import BeautifulSoup
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# Load .env variables locally (for local dev)
load_dotenv()

# API Key from secrets or .env
api_key = st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY"))

if not api_key:
    st.error("❌ GEMINI_API_KEY not found.")
    raise ValueError("API key missing")

# Configure Gemini
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.0-flash")


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


def analyze_webpage_with_gemini(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text()[:5000]
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
        gemini_response = model.generate_content(prompt)
        return gemini_response.text
    except Exception as e:
        return f'{{"error": "Gemini analysis failed: {e}"}}'
