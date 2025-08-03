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

# ✅ UI Title
st.title("📘 Emojica Translator")

# ✅ Input placeholder (speech result will be injected here)
user_input = st.text_input("💬 Type or speak your English sentence:", key="speech_input")

# ✅ JavaScript: Speech Recognition to input field (works on mobile)
st.components.v1.html("""
    <script>
    const loadMic = () => {
        const btn = document.getElementById("micButton");
        const input = window.parent.document.querySelector('input[data-testid="stTextInput"]');
        btn.onclick = () => {
            const recognition = new webkitSpeechRecognition();
            recognition.lang = "en-US";
            recognition.onresult = function(event) {
                const transcript = event.results[0][0].transcript;
                input.value = transcript;
                input.dispatchEvent(new Event("input", { bubbles: true }));
            };
            recognition.onerror = function(event) {
                alert("Mic error: " + event.error);
            };
            recognition.start();
        };
    };
    window.addEventListener("DOMContentLoaded", loadMic);
    </script>
    <button id="micButton" style="font-size:18px; padding:8px; margin-top:10px;">🎤 Tap to Speak</button>
""", height=100)

# ✅ Translate and Display Result
if user_input:
    result = english_to_emojica(user_input)
    st.markdown("### ➡️ Emojica:")
    st.markdown(f"**{result}**")
