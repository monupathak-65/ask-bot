import streamlit as st
from transformers import pipeline
from langdetect import detect

# Load emotion model
emotion_classifier = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base")

# Emotion-based responses
RESPONSES = {
    "Angry": {
        "en": "I'm really sorry you're facing this. Let me fix it immediately.",
        "hi": "माफ़ कीजिए कि आपको समस्या हुई। मैं तुरंत इसका समाधान करता हूँ।"
    },
    "Sad": {
        "en": "I understand this is disappointing. I'm here to help you.",
        "hi": "मैं समझ सकता हूँ कि यह निराशाजनक है। मैं आपकी मदद के लिए यहाँ हूँ।"
    },
    "Confused": {
        "en": "Let me simplify this for you. Here's what you can do...",
        "hi": "चलिए मैं इसे आसान बनाता हूँ। आप ऐसा कर सकते हैं..."
    },
    "Happy": {
        "en": "That's great to hear! Let’s keep it going!",
        "hi": "यह सुनकर अच्छा लगा! आइए इसे जारी रखें!"
    }
}

# Detect language
def detect_language(text):
    try:
        if "chal nikal" in text.lower():
            return "hi"
        lang = detect(text)
        return "hi" if lang == "hi" else "en"
    except:
        return "en"

# Detect emotion
def detect_emotion(text):
    label = emotion_classifier(text)[0]['label'].lower()
    if label in ['anger', 'angry']:
        return 'Angry'
    elif label in ['sadness', 'sad']:
        return 'Sad'
    elif label in ['confusion', 'disgust', 'fear']:
        return 'Confused'
    else:
        return 'Happy'

# Detect intent
def classify_query(message):
    message = message.lower()
    if "refund" in message or "money back" in message:
        return "Refund"
    elif "complaint" in message or "issue" in message or "problem" in message:
        return "Complaint"
    elif "order" in message or "status" in message or "delivery" in message:
        return "Order"
    elif "cancel" in message:
        return "Cancel"
    else:
        return "General"

# Generate chatbot reply
def generate_response(name, message, email, order_id, lang_mode):
    if lang_mode == "Auto Detect":
        lang = detect_language(message)
    elif lang_mode == "Hindi":
        lang = "hi"
    else:
        lang = "en"

    lang_label = "Hindi 🇮🇳" if lang == "hi" else "English 🇬🇧"
    emotion = detect_emotion(message)
    intent = classify_query(message)
    reply = RESPONSES.get(emotion, {}).get(lang, "Sorry, I couldn’t understand.")

    return f"""
**Hi {name}!** 👋  
🌐 **Language Selected:** {lang_label}  
❤️ **Emotion Detected:** {emotion}  
🧠 **Intent Identified:** {intent}  

🤖 **ASK-BOT says:**  
{reply}

📩 We will send the details regarding your *{intent.lower()}* to your email: **{email}**, for Order ID: **{order_id}**.
"""

# Streamlit UI
st.set_page_config(page_title="ASK-BOT 🤖", page_icon="🤖")
st.title("ASK-BOT – Emotion Smart Order Assistant")
st.markdown("Handles Refunds, Complaints, Cancellations & More with Emotion & Language Awareness")

# Language selection
lang_mode = st.selectbox("🌐 Choose Language:", ["Auto Detect", "English", "Hindi"])

# Input form
with st.form("chat_form"):
    name = st.text_input("👤 Enter your name:")
    query = st.text_area("💬 What is your query about the order?")
    email = st.text_input("📧 Your email address:")
    order_id = st.text_input("🧾 Your Order ID:")
    submitted = st.form_submit_button("Submit to ASK-BOT")

# Display chatbot response
if submitted:
    if name and query and email and order_id:
        reply = generate_response(name, query, email, order_id, lang_mode)
        st.markdown(reply)
    else:
        st.warning("⚠️ Please fill in all fields before submitting.")
