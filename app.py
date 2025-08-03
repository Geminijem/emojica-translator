import streamlit as st
import random

# ✅ Emojica Dictionary
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

# ✅ Translate function
def english_to_emojica(sentence):
    words = sentence.lower().split()
    translated = []
    for word in words:
        if word in filler_words:
            continue
        emoji = english_to_emoji.get(word, f"[{word}]")
        translated.append(emoji)
    return " ".join(translated)

# ✅ App UI
st.title("📘 Emojica Translator")

# 🔤 Text Input Translator
st.header("📝 English ➡️ Emojica")
text_input = st.text_input("💬 Type your English sentence:")
if st.button("Translate"):
    if text_input:
        result = english_to_emojica(text_input)
        st.success(f"➡️ **{result}**")
    else:
        st.warning("Please enter a sentence.")

# 🎯 Game Section
st.header("🎯 Emoji of the Day - Guess the Meaning")

# 🧠 State to keep the same emoji
if "emoji_question" not in st.session_state:
    st.session_state.emoji_question = random.choice(list(emoji_to_english.keys()))
if "score" not in st.session_state:
    st.session_state.score = 0

st.subheader(f"🧐 What does this emoji mean? → {st.session_state.emoji_question}")
user_guess = st.text_input("Your guess (one word, lowercase):", key="quiz_guess")

if st.button("Submit Guess"):
    correct = emoji_to_english[st.session_state.emoji_question]
    if user_guess.strip().lower() == correct:
        st.success("✅ Correct!")
        st.session_state.score += 1
        st.session_state.emoji_question = random.choice(list(emoji_to_english.keys()))
    else:
        st.error(f"❌ Wrong. It means **{correct}**.")
        st.session_state.emoji_question = random.choice(list(emoji_to_english.keys()))

st.info(f"🏆 Your score: {st.session_state.score}")
