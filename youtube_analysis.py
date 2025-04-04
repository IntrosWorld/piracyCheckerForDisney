import os
import requests
from urllib.parse import urlparse, parse_qs
import google.generativeai as genai  # ✅ Correct import
import streamlit as st

# ✅ Load API keys
api_key = st.secrets["GEMINI_API_KEY"]
YOUTUBE_API_KEY = st.secrets["YOUTUBE_API_KEY"]

# ✅ Configure Gemini
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.0-flash")

# 🎥 Extract YouTube video ID
def extract_video_id(url):
    try:
        parsed = urlparse(url)
        if parsed.hostname == "youtu.be":
            return parsed.path[1:]
        if parsed.hostname in ["www.youtube.com", "youtube.com"]:
            query = parse_qs(parsed.query)
            return query.get("v", [None])[0]
    except:
        return None

# 📊 Fetch video + channel info
def fetch_video_details(video_id):
    url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics&id={video_id}&key={YOUTUBE_API_KEY}"
    video_response = requests.get(url).json()

    if "items" not in video_response or not video_response["items"]:
        return "", "", "", False, "0", "0", "0"

    item = video_response["items"][0]
    snippet = item["snippet"]
    statistics = item["statistics"]
    channel_id = snippet.get("channelId", "")
    channel_title = snippet.get("channelTitle", "")

    # 👤 Fetch channel stats
    channel_url = f"https://www.googleapis.com/youtube/v3/channels?part=statistics&id={channel_id}&key={YOUTUBE_API_KEY}"
    channel_response = requests.get(channel_url).json()

    subscriber_count = "0"
    if "items" in channel_response and channel_response["items"]:
        stats = channel_response["items"][0].get("statistics", {})
        subscriber_count = stats.get("subscriberCount", "0")

    try:
        is_verified = int(subscriber_count) >= 100000
    except:
        is_verified = False

    view_count = statistics.get("viewCount", "0")
    like_count = statistics.get("likeCount", "0")

    return snippet.get("title", ""), snippet.get("description", ""), channel_title, is_verified, subscriber_count, view_count, like_count

# 💬 Get top comments
def fetch_top_comments(video_id, max_results=5):
    url = f"https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&videoId={video_id}&key={YOUTUBE_API_KEY}&maxResults={max_results}&textFormat=plainText"
    response = requests.get(url).json()
    comments = []
    for item in response.get("items", []):
        comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
        comments.append(comment)
    return "\n".join(comments)

# 🤖 Analyze with Gemini
def analyze_with_gemini(title, description, comments, channel_title, is_verified):
    prompt = f"""
You are a piracy detection AI.

Analyze the following YouTube video and estimate the chance of it being pirated Disney content.

📺 Title: {title}
🧑‍💻 Channel: {channel_title}
✔️ Channel Verified: {"Yes" if is_verified else "No"}

📄 Description:
{description}

💬 Top Comments:
{comments}

Reply in JSON:
{{
  "is_pirated": true/false,
  "confidence": 0-100,
  "reason": "Short explanation",
  "is_channel_verified": true/false
}}
"""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f'{{"error": "Gemini call failed: {e}"}}'
