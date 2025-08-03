%%writefile app.py
import streamlit as st

emoji_to_english = {
    "🙋": "i", "👉": "you", "👥": "we", "👨": "he", "👩": "she",
    "🤖": "ai", "👨‍⚕️": "doctor", "🧑‍🎓": "student", "👨‍🏫": "teacher", "👮": "police", "👶": "baby",
    "📚": "study", "🏃": "go", "😴": "sleep", "🗣️": "speak", "🤔": "think", "❤️": "love",
    "✅": "yes", "❌": "no", "👀": "see", "🔊": "listen", "✍️": "write", "📖": "read", "👂": "hear", "🧠": "understand",
    "⬅️": "past", "🔄": "present", "⏳": "future", "🌇": "yesterday", "🌅": "tomorrow",
    "🕒": "today", "🕘": "morning", "🌃": "night",
    "🔥": "lot", "❓": "question", "😂": "laugh", "😢": "sad", "😡": "angry", "😄": "happy", "😐": "neutral",
    "🏥": "hospital", "🏫": "school", "🏠": "home", "🚗": "car", "📱": "phone",
    "💻": "computer", "📧": "email", "📦": "package"
}
english_to_emoji = {v: k for k, v in emoji_to_english.items()}
filler_words = {"a", "an", "the", "to", "is", "are", "was", "were", "am", "be"}

def english_to_emojica(sentence):
    words = sentence.lower().split()
    translated = []
    for word in words:
        if word in filler_words:
            continue
        emoji = english_to_emoji.get(word, f"[{word}]")
        translated.append(emoji)
    return " ".join(translated)

# Streamlit UI
st.title("📘 Emojica Translator")
user_input = st.text_input("💬 Type your English sentence:")
if st.button("Translate to Emojica"):
    if user_input:
        result = english_to_emojica(user_input)
        st.markdown("### ➡️ Emojica:")
        st.markdown(f"**{result}**")
    else:
        st.warning("Please enter a sentence.")
