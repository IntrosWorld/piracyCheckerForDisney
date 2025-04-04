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
you know there  are muitpler card. the prpnelm is only happening for cad wihc ocntains tabs. show try to fi xthsat brsauder other csrc dont hsvre thid prbolem
st.markdown("""
<style>
/* Import Poppins Font */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');

/* Global Font + Background */
html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}
[data-testid="stApp"] {
    background: linear-gradient(-45deg, #1e3c72, #2a5298, #0f2027, #2c5364);
    background-size: 400% 400%;
    animation: gradientBG 15s ease infinite;
}
@keyframes gradientBG {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}

/* Fix Tabs for Mobile */
.stTabs [role="tablist"] {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-evenly;
    background: rgba(255,255,255,0.05);
    border-radius: 12px;
    padding: 10px;
    overflow-x: auto;
    scrollbar-width: none;
}
.stTabs [role="tablist"]::-webkit-scrollbar {
    display: none;
}
.stTabs [role="tab"] {
    color: white !important;
    font-weight: 600;
    padding: 10px 18px;
    margin: 5px;
    border-radius: 12px;
    background: rgba(255, 255, 255, 0.08);
    transition: background 0.3s ease;
    white-space: nowrap;
    flex-shrink: 0;
}
.stTabs [role="tab"]:hover {
    background: rgba(255,255,255,0.15);
}
.stTabs [role="tab"][aria-selected="true"] {
    background: #00aaff;
    color: white !important;
    box-shadow: 0 2px 10px rgba(0,170,255,0.3);
    border-bottom: none !important;
}

/* Optional: Center tabs */
@media screen and (max-width: 768px) {
    .stTabs [role="tablist"] {
        justify-content: flex-start;
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
