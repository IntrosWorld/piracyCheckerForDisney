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
# 💫 Full Gradient Background & Modern Glassmorphism UI
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }

    /* 🌈 Animated Gradient Background */
    [data-testid="stApp"] {
        background: linear-gradient(-45deg, #1e3c72, #2a5298, #0f2027, #2c5364);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
        height: 100%;
    }

    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* 🎯 Fix TAB container specifically */
    [data-testid="stHorizontalBlock"] > div:first-child {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border-radius: 16px;
        box-shadow: none !important;
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        padding: 1rem;
        margin-bottom: 1rem;
        overflow: visible !important;
    }

    /* 🧼 Tab list fix */
    .stTabs [role="tablist"] {
        overflow-x: auto;
        background-color: transparent !important;
        scrollbar-width: none;
    }

    .stTabs [role="tablist"]::-webkit-scrollbar {
        display: none;
    }

    /* Tab items */
    .stTabs [role="tab"] {
        color: #fff;
        padding: 8px 16px;
        border-radius: 8px;
        font-weight: 500;
        white-space: nowrap;
        background: rgba(255, 255, 255, 0.08);
    }

    .stTabs [aria-selected="true"] {
        background: rgba(255, 255, 255, 0.15);
        border-bottom: 2px solid #fff !important;
        color: #fff !important;
    }

    /* 🟦 Button hover */
    .stButton>button {
        color: #fff;
        font-weight: 500;
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        border: none;
        background: linear-gradient(to right, #00c6ff, #0072ff);
        transition: all 0.3s ease-in-out;
    }

    .stButton>button:hover {
        background: linear-gradient(to right, #0072ff, #00c6ff);
        color: #fff;
        transform: scale(1.03);
    }

    /* ✨ Inputs and Dropdowns */
    .stSelectbox, .stTextInput>div, .stMarkdown {
        background-color: rgba(255, 255, 255, 0.06) !important;
        border-radius: 12px;
        color: white !important;
        backdrop-filter: blur(6px);
        padding: 1rem;
    }

    .stSelectbox label, .stSelectbox div, .stTextInput input {
        color: #fff !important;
    }
 @media only screen and (max-width: 768px) {
    .stTabs [role="tablist"] {
        display: flex !important;
        flex-direction: column !important;
        gap: 12px;
        background: none !important;
        padding: 0 !important;
        box-shadow: none !important;
        border-radius: 0 !important;
    }

    .stTabs [role="tab"] {
        background: linear-gradient(to right, #00c6ff, #0072ff);
        border: none !important;
        border-radius: 12px !important;
        padding: 14px 0 !important;
        width: 100% !important;
        text-align: center;
        font-weight: 600;
        font-size: 16px;
        color: white !important;
        box-shadow: 0 3px 6px rgba(0, 0, 0, 0.15);
        transition: all 0.3s ease;
    }

    .stTabs [role="tab"]:hover {
        transform: scale(1.03);
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(to right, #0072ff, #00c6ff) !important;
        color: white !important;
    }
}

</style>
""", unsafe_allow_html=True)







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
with tab2:
    st.subheader("🌐 Web Search Settings")
    num_web = st.selectbox(
        "How many results per Web query?",
        options=[1, 2, 5, 10],
        index=2
    )

    if st.button("🌍 Scan General Web for Pirated Links"):
        st.success("Scanning the general web for suspicious content...")

        general_queries = [
            "disney free movie download",
            "watch disney movies online free",
            "frozen movie 480p download",
            "frozen full movie watch online"
        ]

        for query in general_queries:
            st.subheader(f"🔎 `{query}`")
            results = search_piracy_links(query, num_results=num_web)
            results = [r for r in results if "reddit.com" not in r["link"]]

            if not results:
                st.warning("❌ No non-reddit results found.")
                continue

            for result in results:
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
