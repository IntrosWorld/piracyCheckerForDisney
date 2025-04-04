import os
import streamlit as st
import google.generativeai as genai
import requests
from bs4 import BeautifulSoup

# Load API key (from secrets if deployed, else from .env)
api_key = st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY"))

if not api_key:
    st.error("❌ GEMINI_API_KEY not found in secrets or environment.")
    raise ValueError("GEMINI_API_KEY is required")

# Configure Gemini
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.0-flash")

# ✅ Test Gemini API (optional for Streamlit debug)
def test_gemini_api():
    try:
        response = model.generate_content("Reply only: {\"status\": \"Gemini is working!\"}")
        return response.text
    except Exception as e:
        return f'{{"error": "Gemini failed: {e}"}}'

# ✅ Check if content is Disney related
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
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f'{{"error": "Gemini API call failed: {e}"}}'

# ✅ Analyze a webpage for pirated Disney content
def analyze_webpage_with_gemini(url):
    try:
        page = requests.get(url, timeout=10)
        soup = BeautifulSoup(page.text, "html.parser")
        text = soup.get_text()[:5000]  # Gemini input limit
    except Exception as e:
        return f'{{"error": "Failed to fetch page: {e}"}}'

    prompt = f"""
You are a piracy detection AI.

Analyze the following webpage text and determine if it links to pirated Disney content:

Text:
{text}

Respond ONLY in JSON:
{{
  "is_pirated": true/false,
  "confidence": 0-100,
  "reason": "Short reason"
}}
"""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f'{{"error": "Gemini analysis failed: {e}"}}'
