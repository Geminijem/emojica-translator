import streamlit as st
import random
import json
from fpdf import FPDF
import base64
import pyttsx3
import speech_recognition as sr
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
    "📱": "phone", "💻": "computer", "📧": "email", "📦": "package"
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
    return " ".join([emoji_to_english.get(e, f"[{e}]") for e in symbols])

def speak_text(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def record_voice():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎙️ Listening...")
        audio = r.listen(source, phrase_time_limit=5)
    try:
        text = r.recognize_google(audio)
        return text
    except:
        st.error("❌ Could not recognize voice. Try again.")
        return ""

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

if st.button("🎤 Voice Input"):
    text_input = record_voice()
    st.write(f"You said: {text_input}")

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

# 📄 Export to PDF
if st.button("📤 Export History as PDF"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Emojica Game History", ln=1, align='C')
    for entry in st.session_state.history:
        line = f"{entry['emoji']} → You: {entry['your_answer']} | Correct: {entry['correct_answer']} | {entry['status']}"
        pdf.cell(200, 10, txt=line, ln=1)
    pdf.output("history.pdf")
    with open("history.pdf", "rb") as file:
        b64 = base64.b64encode(file.read()).decode()
        href = f'<a href="data:application/octet-stream;base64,{b64}" download="emojica_history.pdf">📥 Download History PDF</a>'
        st.markdown(href, unsafe_allow_html=True)

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
