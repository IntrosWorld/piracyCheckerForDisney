import streamlit as st
from duckduckgo_search import DDGS

def search_piracy_links(query, num_results=5):
    results = []

    try:
        with DDGS() as ddgs:
            raw_results = ddgs.text(
                query,
                max_results=num_results,
                safesearch="off"  # 👈 turn off safe search
            )
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
