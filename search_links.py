import streamlit as st
from duckduckgo_search.ddgs import DDGS  # ✅ Correct import for latest version

def search_piracy_links(query, num_results=10):
    """Searches DuckDuckGo for piracy-related links."""
    results = []

    try:
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=num_results):
                results.append({
                    "title": r.get("title", "No Title"),
                    "link": r.get("href", "No Link"),
                    "snippet": r.get("body", "")
                })
    except Exception as e:
        st.error(f"❌ DuckDuckGo search failed: {e}")
        return []

    return results
