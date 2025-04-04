import os
import requests
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

API_KEY = st.secrets("GOOGLE_API_KEY")
CSE_ID = st.secrets("CSE_ID")

def search_piracy_links(query, num_results=10):
    url = f"https://www.googleapis.com/customsearch/v1"
    params = {
        "key": API_KEY,
        "cx": CSE_ID,
        "q": query,
        "num": num_results
    }
    response = requests.get(url, params=params)
    data = response.json()

    results = []
    for item in data.get("items", []):
        results.append({
            "title": item.get("title"),
            "link": item.get("link"),
            "snippet": item.get("snippet")
        })
    return results
