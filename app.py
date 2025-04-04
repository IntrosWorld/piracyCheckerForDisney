import streamlit as st
import re
import json

from gemini_utils import is_disney_content, analyze_webpage_with_gemini
from youtube_analysis import (
    extract_video_id,
    fetch_video_details,
    fetch_top_comments,
    analyze_with_gemini,
)
from search_links import search_piracy_links

st.set_page_config(page_title="🎬 Safeguarding Stories", layout="wide")

# 🌈 Inject Gradient Background
st.markdown("""
    <style>
    body {
        background: linear-gradient(-45deg, #1e3c72, #2a5298, #1e3c72, #2a5298);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
        color: white;
    }

    @keyframes gradient {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }

    .stMarkdown, .stButton>button, .stSelectbox {
        background-color: rgba(0, 0, 0, 0.15);
        border-radius: 12px;
        padding: 10px;
    }

    h1, h2, h3, h4, .stTextInput>label {
        color: white;
    }

    .stAlert {
        background-color: rgba(0, 0, 0, 0.3) !important;
        border-radius: 10px;
    }

    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 10px 16px;
        border-radius: 10px;
        font-weight: bold;
        transition: 0.3s;
    }

    .stButton>button:hover {
        background-color: #66bb6a;
    }

    .stTabs [role="tablist"] {
        background-color: #111;
        border-radius: 10px;
    }

    .stTabs [role="tab"] {
        color: white;
    }

    </style>
""", unsafe_allow_html=True)

from gemini_utils import is_disney_content, analyze_webpage_with_gemini, test_gemini_api

if st.button("🚀 Test Gemini API"):
    st.code(test_gemini_api(), language="json")





st.title("🛡️ Safeguarding Stories – Disney IP Protection System")

# ───────────────────────────────────────────────────── #
# 🎛️ Tabbed Interface for YouTube & Web
tab1, tab2 = st.tabs(["▶️ YouTube Piracy Scanner", "🌍 Web Piracy Scanner"])

# ───────────────────────────────────────────────────── #
# ▶️ YOUTUBE TAB
with tab1:
    st.subheader("🔎 YouTube Search Settings")
    num_yt = st.selectbox(
        "How many results per YouTube query?",
        options=[1, 3, 5, 10],
        index=2
    )

    if st.button("🔍 Scan YouTube for Pirated Videos"):
        st.success("Scanning YouTube and analyzing content using Gemini...")

        youtube_queries = [
            "site:youtube.com watch disney frozen full movie",
            "frozen full movie youtube"
        ]

        for query in youtube_queries:
            st.subheader(f"🔎 `{query}`")
            results = search_piracy_links(query, num_results=num_yt)

            if not results:
                st.warning("❌ No results found.")
                continue

            for result in results:
                link = result["link"]
                title = result["title"]
                snippet = result["snippet"]

                st.markdown(f"📺 **[{title}]({link})**")
                st.write(f"📝 {snippet}")

                video_id = extract_video_id(link)
                if not video_id:
                    st.warning("⚠️ Could not extract video ID.")
                    continue

                yt_title, description, channel_name, is_verified, views, likes, subscribers = fetch_video_details(video_id)
                comments = fetch_top_comments(video_id)

                gemini_result = analyze_with_gemini(yt_title, description, comments, channel_name, is_verified)

                st.markdown("#### 🤖 Gemini Analysis")

                try:
                    cleaned = gemini_result.strip().replace("```json", "").replace("```", "").replace('\\"', '"')
                    parsed = json.loads(cleaned)

                    is_pirated = parsed.get("is_pirated", False)
                    confidence = parsed.get("confidence", 0)
                    reason = parsed.get("reason", "N/A")
                    verified = parsed.get("is_channel_verified", False)

                    st.markdown("**📋 Extracted Gemini Analysis:**")
                    st.markdown(f"""
- 🔍 **Is Pirated:** `{is_pirated}`
- 📊 **Confidence:** `{confidence}%`
- 💬 **Reason:** _{reason}_
- 🛡️ **Channel Verified:** `{verified}`
- 👥 **Subscribers:** `{subscribers}`
- 👁️ **Views:** `{views}`
- 👍 **Likes:** `{likes}`
""")

                    if is_pirated:
                        st.error("🚫 Piracy Likely Detected!")
                    else:
                        st.success("✅ Looks Clean (Not Pirated)")

                except Exception as e:
                    st.warning("⚠️ Could not parse Gemini's response.")
                    st.code(gemini_result, language="json")

                st.video(f"https://www.youtube.com/watch?v={video_id}")
                st.markdown("---")

# ───────────────────────────────────────────────────── #
# 🌍 WEB TAB
# 🌍 WEB TAB
with tab2:
    st.subheader("🌐 Web Search Settings")
    num_web = st.selectbox(
        "How many results per Web query?",
        options=[1, 2, 5, 10],
        index=2  # Default to 10 results
    )

    if st.button("🌍 Scan General Web for Pirated Links"):
        st.success("Scanning the general web for suspicious content...")

        duckduck_queries = [
            "frozen movie 480p mkv file download",
            "disney frozen full movie mp4 google drive",
            "frozen full movie index of mkv",
            "watch frozen movie free streaming site",
            "disney frozen 1080p DDL download link"
        ]

        for query in duckduck_queries:
            st.subheader(f"🔎 `{query}`")
            results = search_piracy_links(query, num_results=num_web)  # Use num_web to control results count
            results = [r for r in results if "reddit.com" not in r["link"]]  # Filter out Reddit links

            if not results:
                st.warning("❌ No non-reddit results found.")
                continue

            # Limit the results to the selected number (num_web)
            results_to_show = results[:num_web]

            for result in results_to_show:
                title = result["title"]
                link = result["link"]
                snippet = result["snippet"]

                st.markdown(f"🔗 **[{title}]({link})**")
                st.write(f"📝 {snippet}")

                with st.spinner("🤖 Analyzing with Gemini..."):
                    gemini_result = analyze_webpage_with_gemini(link)

                st.markdown("#### 🤖 Gemini Webpage Analysis")

                try:
                    cleaned = gemini_result.strip().replace("```json", "").replace("```", "").replace('\\"', '"')
                    parsed = json.loads(cleaned)

                    is_pirated = parsed.get("is_pirated", False)
                    confidence = parsed.get("confidence", 0)
                    reason = parsed.get("reason", "N/A")

                    st.markdown("**📋 Extracted Gemini Analysis:**")
                    st.markdown(f"""
- 🔍 **Is Pirated:** `{is_pirated}`
- 📊 **Confidence:** `{confidence}%`
- 💬 **Reason:** _{reason}_
""")

                    if is_pirated:
                        st.error("🚫 Piracy Likely Detected!")
                    else:
                        st.success("✅ Looks Clean (Not Pirated)")

                except Exception:
                    st.warning("⚠️ Could not parse Gemini's response.")
                    st.code(gemini_result, language="json")

            st.markdown("---")


