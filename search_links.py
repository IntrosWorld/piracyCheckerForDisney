import os
import requests
from dotenv import load_dotenv
import streamlit as st

# Load .env variables locally (only works locally, not in Streamlit Cloud)
load_dotenv()

# Load secrets (these must be added in Streamlit Cloud secrets too)
API_KEY = st.secrets.get("GOOGLE_API_KEY", os.getenv("GOOGLE_API_KEY"))
CSE_ID = st.secrets.get("CSE_ID", os.getenv("CSE_ID"))

def search_piracy_links(query, num_results=10):
    """Searches Google Custom Search Engine (CSE) for piracy-related links."""
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": API_KEY,
        "cx": CSE_ID,
        "q": query,
        "num": num_results
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()  # Raise exception for HTTP errors
        data = response.json()
    except Exception as e:
        st.error(f"❌ Error fetching results for `{query}`: {e}")
        return []

    results = []
    for item in data.get("items", []):
        results.append({
            "title": item.get("title"),
            "link": item.get("link"),
            "snippet": item.get("snippet", "")
        })

    return results
