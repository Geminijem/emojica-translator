import streamlit as st

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

# ✅ Streamlit UI
st.title("📘 Emojica Translator")

st.markdown("🎙️ Tap below to speak (mobile only):")
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

user_input = st.text_input("💬 Or type your English sentence:", key="speech_input")
if st.button("Translate to Emojica"):
    if user_input:
        result = english_to_emojica(user_input)
        st.markdown("### ➡️ Emojica:")
        st.markdown(f"**{result}**")
    else:
        st.warning("Please enter or speak a sentence.")
