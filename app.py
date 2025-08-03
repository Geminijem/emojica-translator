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

# Speech-to-text input injection
st.markdown("🎙️ Tap mic to speak (mobile only):")
st.components.v1.html("""
    <input type="text" id="speechInput" style="display:none;" />
    <button onclick="startDictation()">🎤 Speak</button>
    <script>
    function startDictation() {
        var recognition = new webkitSpeechRecognition();
        recognition.lang = "en-US";
        recognition.onresult = function(event) {
            var text = event.results[0][0].transcript;
            const inputBox = window.parent.document.querySelector('input[data-testid="stTextInput"]');
            if (inputBox) {
                inputBox.value = text;
                inputBox.dispatchEvent(new Event('input', { bubbles: true }));
            }
        };
        recognition.start();
    }
    </script>
""", height=100)

# Manual or speech-based input
user_input = st.text_input("💬 Or type your English sentence:")

if user_input:
    result = english_to_emojica(user_input)
    st.markdown("### ➡️ Emojica:")
    st.markdown(f"**{result}**")
