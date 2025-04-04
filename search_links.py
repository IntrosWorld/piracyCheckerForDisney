import streamlit as st
from duckduckgo_search import ddg  # ✅ Correct for duckduckgo-search v0.9+

def search_piracy_links(query, num_results=10):
    """Search DuckDuckGo for piracy-related links."""
    results = []

    try:
        raw_results = ddg(query, max_results=num_results)
        for r in raw_results:
            results.append({
                "title": r.get("title", "No Title"),
                "link": r.get("href", "No Link"),
                "snippet": r.get("body", "")
            })
    except Exception as e:
        st.error(f"❌ DuckDuckGo search failed: {e}")
        return []

    return results
