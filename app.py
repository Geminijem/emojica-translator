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

def english_to_emojica(sentence):
    words = sentence.lower().split()
    translated = []
    for word in words:
        if word in filler_words:
            continue
        emoji = english_to_emoji.get(word, f"[{word}]")
        translated.append(emoji)
    return " ".join(translated)

# 🧠 Random Emoji of the Day
today_emoji = random.choice(list(emoji_to_english.keys()))

# 🧠 Check user guess
def check_guess(user_input, actual_answer):
    return user_input.strip().lower() == actual_answer.lower()

# ✅ Streamlit UI
st.set_page_config(page_title="Emojica Translator", page_icon="📘")
st.title("📘 Emojica Translator")

# 🎙️ Voice input (Mobile Only - not working on Streamlit Cloud)
st.markdown("🎙️ Tap mic to speak (mobile only):")
st.components.v1.html("""
<button onclick="startDictation()">🎤 Speak</button>
<input id="result" style="width:100%; font-size:18px; margin-top:10px;" placeholder="Your speech will appear here...">

<script>
function startDictation() {
    var recognition = new webkitSpeechRecognition();
    recognition.lang = "en-US";
    recognition.onresult = function(event) {
        document.getElementById('result').value = event.results[0][0].transcript;
        document.dispatchEvent(new Event("input"));
    }
    recognition.start();
}
</script>
""", height=130)

# ✍️ Text Input for Translation
user_input = st.text_input("💬 Or type your English sentence:", key="speech_input")
if st.button("Translate to Emojica"):
    if user_input:
        result = english_to_emojica(user_input)
        st.markdown("### ➡️ Emojica:")
        st.markdown(f"**{result}**")
    else:
        st.warning("Please enter or speak a sentence.")

st.markdown("---")

# 🎯 Emoji Guessing Game
st.header("🧠 Guess the Emoji Meaning!")
st.markdown(f"**Emoji of the Day:** {today_emoji}")
user_guess = st.text_input("What does this emoji mean?")

if user_guess:
    correct_answer = emoji_to_english[today_emoji]
    if check_guess(user_guess, correct_answer):
        st.success("🎉 Correct! Great job!")
    else:
        st.error(f"❌ Oops! The correct answer is **{correct_answer}**.")
