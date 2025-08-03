import streamlit as st
import datetime

# 🎯 Emojica Dictionary
emoji_to_english = {
    "🙋": "i", "👉": "you", "👥": "we", "🤖": "ai",
    "📚": "study", "🏃": "go", "😴": "sleep", "❤️": "love",
    "✅": "yes", "❌": "no", "👀": "see", "🔥": "lot"
}

# 🗓️ Select today's emoji
emojis = list(emoji_to_english.keys())
index = datetime.datetime.now().day % len(emojis)
today_emoji = emojis[index]

# 🧩 UI
st.title("📅 Daily Emojica Challenge")
st.markdown("Guess the meaning of today’s emoji:")

st.markdown(f"## {today_emoji}")
