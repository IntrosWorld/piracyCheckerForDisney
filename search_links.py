import streamlit as st
from duckduckgo_search import ddg

def search_piracy_links(query, num_results=10):
    """Search DuckDuckGo for piracy-related links."""
    results = []

    try:
        raw_results = ddg(query, max_results=num_results)
        if not raw_results:
            st.warning(f"⚠️ No results returned for: `{query}`")
            return []

        for r in raw_results:
            # Ensure expected fields are present
            title = r.get("title", "No Title")
            link = r.get("href", "No Link")
            snippet = r.get("body", "")

            results.append({
                "title": title,
                "link": link,
                "snippet": snippet
            })

    except Exception as e:
        st.error(f"❌ DuckDuckGo search failed: {e}")
        return []

    return results
