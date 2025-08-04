import streamlit as st
import datetime
import random
import json
import os
import tempfile
import base64
from fpdf import FPDF
from gtts import gTTS

# ---------- Emojica Dictionaries ----------
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
    "😀": "happy", "😃": "smile", "😁": "big smile", "😆": "laugh",
    "😅": "sweat", "🤣": "rolling on floor laughing", "😭": "crying", "😉": "wink",
    "😗": "kiss", "😙": "blow kiss", "😚": "sweet kiss", "😘": "kissing heart",
    "🥰": "in love", "😍": "heart eyes", "🤩": "star eyes", "🥳": "party",
    "🫠": "melting", "🙃": "upside down", "🙂": "smile", "🥲": "tearful smile",
    "🥹": "crying with smile", "😊": "blushing smile", "☺️": "smiling",
    "🧐": "serious", "🤗": "hug", "🤭": "shy", "🤫": "quiet", "🤐": "zipper mouth",
    "😱": "scream", "🤪": "crazy", "😜": "playful", "😝": "silly", "😛": "cheeky"
}
english_to_emoji = {v: k for k, v in emoji_to_english.items()}
filler_words = {"a", "an", "the", "to", "is", "are", "was", "were", "am", "be", "at", "in", "on", "with"}

# ---------- Translate Functions ----------
def english_to_emojica(sentence):
    words = sentence.lower().split()
    return " ".join([english_to_emoji.get(word, f"[{word}]") for word in words if word not in filler_words])

def emojica_to_english(emoji_sentence):
    symbols = emoji_sentence.strip().split()
    return " ".join([emoji_to_english.get(e, f"[{e}]") for e in symbols])

def speak_text(text):
    tts = gTTS(text=text, lang='en')
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        tts.save(tmp.name)
        audio_file = open(tmp.name, 'rb')
        st.audio(audio_file.read(), format='audio/mp3')

# ---------- Progress Functions ----------
def save_progress():
    progress = {"score": st.session_state.get("score", 0), "history": st.session_state.get("history", [])}
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

# ---------- Mood Tracker + Quote ----------
st.title("🧠 Emojica + Mood Tracker")
st.markdown("A hybrid translator, tracker, and learning game in one!")

emoji_list = list(set(list(emoji_to_english.keys())))
quotes = [
    "Keep going, you're doing great!", "Every day is a new beginning.",
    "You are stronger than you think.", "Focus on progress, not perfection.",
    "Believe in yourself!", "Even small steps lead to big change."
]
today = str(datetime.date.today())
random.seed(today)
quote_of_the_day = random.choice(quotes)
st.markdown(f"### 🌟 Quote of the Day:\n> *{quote_of_the_day}*")

st.subheader("How are you feeling today?")
mood = st.selectbox("Pick a mood emoji:", emoji_list)

if st.button("💾 Save Mood"):
    mood_data = {today: {"emoji": mood, "quote": quote_of_the_day}}
    with open("mood_data.json", "w") as f:
        json.dump(mood_data, f)
    st.success(f"Saved mood for {today}: {mood}")

if st.checkbox("📅 Show Mood History"):
    if os.path.exists("mood_data.json"):
        with open("mood_data.json", "r") as f:
            data = json.load(f)
        for date, info in data.items():
            st.write(f"**{date}** - Mood: {info['emoji']} | Quote: _{info['quote']}_")
    else:
        st.info("No mood history yet.")

# ---------- Translation Tools ----------
st.header("📝 English ➡️ Emojica")
text_input = st.text_area("💬 Type an English sentence:")
if st.button("Translate to Emojica"):
    if text_input:
        result = english_to_emojica(text_input)
        st.success(result)
        if st.button("🔊 Speak Output"):
            speak_text(result)

st.header("🔁 Emojica ➡️ English")
emoji_input = st.text_input("Paste Emojica symbols:")
if st.button("Translate to English"):
    if emoji_input:
        translated = emojica_to_english(emoji_input)
        st.success(translated)
        if st.button("🔊 Speak Output (English)"):
            speak_text(translated)

# ---------- Game Quiz ----------
st.header("🎯 Emoji of the Day - Guess the Meaning")
if "emoji_question" not in st.session_state:
    st.session_state.emoji_question = random.choice(list(emoji_to_english.keys()))
if "score" not in st.session_state:
    st.session_state.score = 0
if "history" not in st.session_state:
    st.session_state.history = []

st.subheader(f"🧐 What does this emoji mean? → {st.session_state.emoji_question}")
guess = st.text_input("Your guess:", key="quiz")
if st.button("Submit Guess"):
    correct = emoji_to_english[st.session_state.emoji_question]
    user_ans = guess.strip().lower()
    is_correct = (user_ans == correct)
    if is_correct:
        st.success("✅ Correct!")
        st.session_state.score += 1
    else:
        st.error(f"❌ Wrong! It means **{correct}**.")
    st.session_state.history.append({
        "emoji": st.session_state.emoji_question,
        "your_answer": user_ans,
        "correct_answer": correct,
        "status": "✅" if is_correct else "❌"
    })
    st.session_state.emoji_question = random.choice(list(emoji_to_english.keys()))

st.info(f"🏆 Score: {st.session_state.score}")

# ---------- Learning Levels ----------
st.header("🧠 Emojica Learning Levels")
levels = {
    "Beginner": ["🙋", "👉", "❤️", "📚", "😄"],
    "Intermediate": ["🧠", "✍️", "🗣️", "🕒", "🔄"],
    "Advanced": ["🧑‍🎓", "👨‍⚕️", "📧", "📦", "🌇"]
}
level_choice = st.selectbox("📊 Choose level:", list(levels.keys()))
learn_emoji = random.choice(levels[level_choice])
st.subheader(f"👁️ What does this mean → {learn_emoji}")
learn_guess = st.text_input("Your answer ('skip' to reveal):", key="learn")
if st.button("Check Answer"):
    meaning = emoji_to_english[learn_emoji]
    if learn_guess.strip().lower() == meaning:
        st.success("🎉 Correct!")
    elif learn_guess.strip().lower() == "skip":
        st.info(f"It means: **{meaning}**")
    else:
        st.error(f"Oops! It means: **{meaning}**")

# ---------- Save/Load + Export ----------
st.header("💾 Manage Progress")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("💾 Save Progress"):
        save_progress()
with col2:
    if st.button("📂 Load Progress"):
        load_progress()
with col3:
    if st.button("📤 Export History PDF"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Emojica Game History", ln=1, align='C')
        for entry in st.session_state.history:
            line = f"{entry['emoji']} → You: {entry['your_answer']} | Correct: {entry['correct_answer']} | {entry['status']}"
            pdf.cell(200, 10, txt=line, ln=1)
        pdf.output("history.pdf")
        with open("history.pdf", "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
            href = f'<a href="data:application/octet-stream;base64,{b64}" download="emojica_history.pdf">📥 Download PDF</a>'
            st.markdown(href, unsafe_allow_html=True)
