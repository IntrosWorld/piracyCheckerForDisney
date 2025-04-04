import streamlit as st
from duckduckgo_search import ddg

def search_piracy_links(query, num_results=10):
    """Search DuckDuckGo for piracy-related links. Safe from index errors."""
    try:
        raw_results = ddg(query, max_results=num_results)

        # Check if list is valid and has dicts
        if not raw_results or not isinstance(raw_results, list):
            raise ValueError("Empty or invalid result")

        results = []
        for item in raw_results:
            if not isinstance(item, dict):
                continue  # Skip malformed

            results.append({
                "title": item.get("title", "No Title"),
                "link": item.get("href", "No Link"),
                "snippet": item.get("body", "No Description")
            })

        return results

    except Exception as e:
        st.error(f"❌ DuckDuckGo search failed for `{query}`: {e}")
        return []
