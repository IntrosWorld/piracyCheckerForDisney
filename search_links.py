import requests
import streamlit as st

def search_piracy_links(query, num_results=10):
    """
    Searches DuckDuckGo for piracy-related links using their unofficial Instant Answer API.
    This version replaces the need for Google CSE.
    """
    results = []
    try:
        url = "https://api.duckduckgo.com/"
        params = {
            "q": query,
            "format": "json",
            "no_redirect": 1,
            "no_html": 1,
            "skip_disambig": 1
        }

        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Use RelatedTopics as fallback
        related = data.get("RelatedTopics", [])[:num_results]

        for item in related:
            if isinstance(item, dict) and "Text" in item and "FirstURL" in item:
                results.append({
                    "title": item.get("Text"),
                    "link": item.get("FirstURL"),
                    "snippet": item.get("Text")
                })

    except Exception as e:
        st.error(f"❌ Error fetching results for `{query}` from DuckDuckGo: {e}")

    return results
