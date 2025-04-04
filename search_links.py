import streamlit as st
from duckduckgo_search import DDGS

def search_piracy_links(query, num_results=5):
    """Search DuckDuckGo for piracy-related links."""
    results = []
    
    try:
        with DDGS() as ddgs:
            raw_results = ddgs.text(query, max_results=num_results)
            for item in raw_results:
                results.append({
                    "title": item.get("title", ""),
                    "link": item.get("href", ""),
                    "snippet": item.get("body", "")
                })

    except Exception as e:
        st.error(f"❌ DuckDuckGo search failed for `{query}`: {e}")
        return []

    return results
