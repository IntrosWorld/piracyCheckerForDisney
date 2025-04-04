import streamlit as st
from duckduckgo_search import ddg

def search_piracy_links(query, num_results=10):
    """Safe DuckDuckGo search for piracy-related links."""
    try:
        # Run DuckDuckGo search
        raw_results = ddg(query, max_results=num_results)

        if not raw_results or len(raw_results) == 0:
            st.warning(f"⚠️ DuckDuckGo returned no results for: `{query}`")
            return []

        results = []
        for item in raw_results:
            if not isinstance(item, dict):
                continue  # skip if malformed result

            results.append({
                "title": item.get("title", "No Title"),
                "link": item.get("href", "No Link"),
                "snippet": item.get("body", "No description")
            })

        return results

    except Exception as e:
        st.error(f"❌ DuckDuckGo search failed for `{query}`: {e}")
        return []
