import streamlit as st
import random
import json
from gtts import gTTS
import tempfile
import os

# ✅ Emojica Dictionary
emoji_to_english = {
    "🙋": "i", "👉": "you", "👥": "we", "👨": "he", "👩": "she", "🤖": "ai",
    "👨‍⚕️": "doctor", "🧑‍🎓": "student", "👨‍🏫": "teacher", "👮": "police",
    "👶": "baby", "📚": "study", "🏃": "go", "😴": "sleep", "🗣️": "speak",
    "🤔": "think", "❤️": "love", "✅": "yes", "❌": "no", "👀": "see",
    "🔊": "listen", "✍️": "write", "📖": "read", "👂": "hear", "🧠": "understand",
    "⬅️": "past", "🔄": "present", "⏳": "future", "🌇": "yesterday",
    "🌅": "tomorrow", "🕒": "today", "🕘": "morning", "🌃": "night", "🔥": "lot",
    "❓": "question", "😂": "laugh", "😢": "sad", "😡": "angry", "😄": "happy",
    "😐": "neutral", "🏥": "hospital", "🏫": "school", "🏠": "home", "🚗": "car",
    "📱": "phone", "💻": "computer", "📧": "email", "📦": "package",
    "😀": "happy", "😃": "smile", "😁": "big smile", "😆": "laugh", "😅": "sweat",
    "🤣": "rolling on the floor laughing", "😭": "crying", "😉": "wink",
    "😗": "kiss", "😙": "blow kiss", "😚": "sweet kiss", "😘": "kissing heart",
    "🥰": "in love", "😍": "heart eyes", "🤩": "star eyes", "🥳": "party",
    "🫠": "melting", "🙃": "upside down", "🙂": "smile", "🥲": "tearful smile",
    "🥹": "crying with smile", "😊": "blushing smile", "☺️": "smiling",
    "🧐": "serious", "🤗": "hug", "🤭": "shy", "🤫": "quiet", "🤐": "zipper mouth",
    "😱": "scream", "🤪": "crazy", "😜": "playful", "😝": "silly", "😛": "cheeky"
}
english_to_emoji = {v: k for k, v in emoji_to_english.items()}
filler_words = {"a", "an", "the", "to", "is", "are", "was", "were", "am", "be", "at", "in", "on", "with"}

# ✅ Translate functions
def english_to_emojica(sentence):
    words = sentence.lower().split()
    translated = []
    for word in words:
        if word in filler_words:
            continue
        emoji = english_to_emoji.get(word, f"[{word}]")
        translated.append(emoji)
    return " ".join(translated)

def emojica_to_english(emoji_sentence):
    symbols = emoji_sentence.strip().split()
    return " ".join([emoji_to_english.get(e, f"[unknown:{e}]") for e in symbols])

def speak_text(text):
    tts = gTTS(text=text, lang='en')
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        tts.save(tmp.name)
        audio_file = open(tmp.name, 'rb')
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format='audio/mp3')

# ✅ Save/Load Progress
def save_progress():
    progress = {
        "score": st.session_state.get("score", 0),
        "history": st.session_state.get("history", [])
    }
    with open("progress.json", "w") as f:
        json.dump(progress, f)
    st.success("✅ Progress saved!")

def load_progress():
    if os.path.exists("progress.json"):
        with open("progress.json", "r") as f:
            progress = json.load(f)
        st.session_state.score = progress.get("score", 0)
        st.session_state.history = progress.get("history", [])
        st.success("🔄 Progress loaded!")
    else:
        st.warning("⚠️ No saved progress found.")

# ✅ App UI
st.title("📘 Emojica Translator")

# 🔤 Text Input Translator
st.header("📝 English ➡️ Emojica")
text_input = st.text_area("💬 Type a full English sentence (supports complex ones):")

if st.button("Translate to Emojica"):
    if text_input:
        result = english_to_emojica(text_input)
        st.success(f"➡️ {result}")
        if st.button("🔊 Speak Output"):
            speak_text(result)
    else:
        st.warning("Please enter a sentence.")

# 🔁 Reverse Translation
st.header("🔁 Emojica ➡️ English")
emoji_input = st.text_input("🔡 Paste your Emojica sentence:")
if st.button("Translate to English"):
    if emoji_input:
        translated = emojica_to_english(emoji_input)
        st.success(f"🔠 {translated}")
        if st.button("🔊 Speak Output (English)"):
            speak_text(translated)
    else:
        st.warning("Please enter Emojica symbols.")

# 💾 Save/Load Progress Buttons
st.header("💾 Progress Control")
col1, col2 = st.columns(2)
with col1:
    if st.button("💾 Save Progress"):
        save_progress()
with col2:
    if st.button("📂 Load Progress"):
        load_progress()

# 🎯 Game Section
st.header("🎯 Emoji of the Day - Guess the Meaning")
if "emoji_question" not in st.session_state:
    st.session_state.emoji_question = random.choice(list(emoji_to_english.keys()))
if "score" not in st.session_state:
    st.session_state.score = 0
if "history" not in st.session_state:
    st.session_state.history = []

st.subheader(f"🧐 What does this emoji mean? → {st.session_state.emoji_question}")
user_guess = st.text_input("Your guess (one word, lowercase):", key="quiz_guess")

if st.button("Submit Guess"):
    correct = emoji_to_english[st.session_state.emoji_question]
    user_answer = user_guess.strip().lower()
    is_correct = user_answer == correct

    if is_correct:
        st.success("✅ Correct!")
        st.session_state.score += 1
    else:
        st.error(f"❌ Wrong. It means **{correct}**.")

    st.session_state.history.append({
        "emoji": st.session_state.emoji_question,
        "your_answer": user_answer,
        "correct_answer": correct,
        "status": "✅" if is_correct else "❌"
    })
    st.session_state.emoji_question = random.choice(list(emoji_to_english.keys()))

st.info(f"🏆 Your score: {st.session_state.score}")

# 🧾 Show Game History
if st.session_state.history:
    st.header("📜 Game History")
    for entry in reversed(st.session_state.history):
        st.markdown(
            f"{entry['emoji']} → You: {entry['your_answer']} | "
            f"Correct: {entry['correct_answer']} | {entry['status']}"
        )

# 🎮 Emojica Learning Assistant with Levels
st.header("🧠 Emojica Learning Levels")
levels = {
    "Beginner": ["🙋", "👉", "❤️", "📚", "😄"],
    "Intermediate": ["🧠", "✍️", "🗣️", "🕒", "🔄"],
    "Advanced": ["🧑‍🎓", "👨‍⚕️", "📧", "📦", "🌇"]
}
level_choice = st.selectbox("📊 Choose your level:", list(levels.keys()))

random_emoji = random.choice(levels[level_choice])
st.subheader(f"👁️ What does this mean → {random_emoji}")
user_learn_guess = st.text_input("Your answer (type 'skip' to see the answer):", key="learn_guess")

if st.button("Check Answer"):
    correct_meaning = emoji_to_english[random_emoji]
    if user_learn_guess.strip().lower() == correct_meaning:
        st.success("🎉 Correct! Great job learning.")
    elif user_learn_guess.strip().lower() == "skip":
        st.info(f"ℹ️ It means {correct_meaning}.")
    else:
        st.error(f"😓 Not quite. It actually means {correct_meaning}.")
