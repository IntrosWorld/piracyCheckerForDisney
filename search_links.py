import streamlit as st
from duckduckgo_search import DDGS  # Make sure it's in requirements.txt

def search_piracy_links(query, num_results=10):
    """Searches DuckDuckGo for piracy-related links."""
    try:
        with DDGS() as ddgs:
            results = ddgs.text(query, region='wt-wt', safesearch='Moderate', max_results=num_results)
            return [
                {
                    "title": r.get("title", ""),
                    "link": r.get("href", ""),
                    "snippet": r.get("body", "")
                }
                for r in results
            ]
    except Exception as e:
        st.error(f"❌ DuckDuckGo search failed for `{query}`: {e}")
        return []
