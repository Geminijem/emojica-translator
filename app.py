# ✍️ Let user guess the meaning
user_guess = st.text_input("What does this emoji mean?")

# ✅ Check answer
if user_guess:
    correct_answer = emoji_to_english[today_emoji]
    if user_guess.strip().lower() == correct_answer:
        st.success("🎉 Correct! Great job!")
    else:
        st.error(f"❌ Oops! The correct answer is **{correct_answer}**.")
