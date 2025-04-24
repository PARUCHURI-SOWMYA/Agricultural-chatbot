import streamlit as st
import os
import random
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

# Set page config
st.set_page_config(page_title="Agri Chatbot", layout="centered")

# API Keys
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

# YouTube search function
def fetch_youtube_videos(query):
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
    request = youtube.search().list(part="snippet", maxResults=3, q=query)
    response = request.execute()
    return response.get("items", [])

# Language dictionary
language_options = {
    "English": {
        "select_language": "Select Language",
        "mode": "Choose Mode",
        "chat_mode": "Agriculture Chat",
        "predict_mode": "Plant Disease Prediction",
        "input_prompt": "Enter your question about agriculture:",
        "submit": "Submit",
        "result": "Chatbot Response:",
        "select_crop": "Select Crop",
        "select_disease": "Select Disease",
        "symptoms": "Symptoms",
        "cause": "Cause",
        "prevention": "Prevention",
        "pesticides": "Pesticides",
        "natural_pesticides": "Natural Pesticides",
        "chemical_pesticides": "Chemical Pesticides",
        "environmental_factors": "Environmental Factors",
        "precautions": "Precautions",
        "care_instructions": "Care Instructions",
        "encouragement": "Encouragement",
        "youtube_videos": "YouTube Videos"
    },
    "Telugu": {
        "select_language": "భాషను ఎంచుకోండి",
        "mode": "మోడ్‌ను ఎంచుకోండి",
        "chat_mode": "వ్యవసాయం చాట్",
        "predict_mode": "మొక్కల వ్యాధి అంచనా",
        "input_prompt": "వ్యవసాయంపై మీ ప్రశ్నను నమోదు చేయండి:",
        "submit": "సబ్మిట్ చేయండి",
        "result": "బోటు సమాధానం:",
        "select_crop": "పంటను ఎంచుకోండి",
        "select_disease": "రోగాన్ని ఎంచుకోండి",
        "symptoms": "లక్షణాలు",
        "cause": "కారణం",
        "prevention": "నిరోధక చర్యలు",
        "pesticides": "పెస్టిసైడ్లు",
        "natural_pesticides": "సాధారణ పెస్టిసైడ్లు",
        "chemical_pesticides": "రసాయన పెస్టిసైడ్లు",
        "environmental_factors": "పర్యావరణ పరిస్థితులు",
        "precautions": "జాగ్రత్తలు",
        "care_instructions": "శ్రద్ధ సూచనలు",
        "encouragement": "ధైర్యం చెప్పు",
        "youtube_videos": "యూట్యూబ్ వీడియోలు"
    },
    "Hindi": {
        "select_language": "भाषा चुनें",
        "mode": "मोड चुनें",
        "chat_mode": "कृषि चैट",
        "predict_mode": "फसल रोग भविष्यवाणी",
        "input_prompt": "कृषि से संबंधित अपना प्रश्न दर्ज करें:",
        "submit": "सबमिट करें",
        "result": "चैटबॉट उत्तर:",
        "select_crop": "फसल चुनें",
        "select_disease": "रोग चुनें",
        "symptoms": "लक्षण",
        "cause": "कारण",
        "prevention": "रोकथाम",
        "pesticides": "कीटनाशक",
        "natural_pesticides": "प्राकृतिक कीटनाशक",
        "chemical_pesticides": "रासायनिक कीटनाशक",
        "environmental_factors": "पर्यावरणीय कारक",
        "precautions": "सावधानियाँ",
        "care_instructions": "देखभाल निर्देश",
        "encouragement": "प्रोत्साहन",
        "youtube_videos": "यूट्यूब वीडियो"
    }
}

# Mock disease suggestion function
def get_suggestions(crop, disease):
    return {
        "symptoms": f"{disease} symptoms in {crop} include wilting, spots, and yellowing.",
        "cause": f"{disease} is commonly caused by fungal or bacterial infections.",
        "prevention": "Regular monitoring and proper spacing help prevent disease spread.",
        "natural_pesticides": "Neem oil and garlic spray are effective natural pesticides.",
        "chemical_pesticides": "Use Mancozeb or Carbendazim as recommended.",
        "environmental_factors": "High humidity and poor drainage favor disease development.",
        "precautions": "Wear gloves and avoid waterlogging.",
        "care_instructions": "Improve soil drainage and avoid overhead irrigation.",
        "encouragement": "Timely care and treatment can save your crop!"
    }

# Gemini AI chat mock function
def gemini_ai_chat(prompt):
    return f"AI response to: {prompt}"

# UI
st.title("🌾 AI-based Agriculture Helper Chatbot")

language = st.selectbox("🌐 Select Language", options=list(language_options.keys()))
labels = language_options[language]

mode = st.radio(f"🔍 {labels['mode']}", [labels["chat_mode"], labels["predict_mode"]])

if mode == labels["chat_mode"]:
    query = st.text_input(labels["input_prompt"])
    if st.button(labels["submit"]):
        response = gemini_ai_chat(query)
        st.markdown(f"**{labels['result']}** {response}")

elif mode == labels["predict_mode"]:
    crop = st.selectbox(f"🌱 {labels['select_crop']}", ["Tomato", "Potato", "Rice", "Wheat"])
    disease = st.selectbox(f"🦠 {labels['select_disease']}", ["Leaf Blight", "Root Rot", "Powdery Mildew"])

    if st.button(labels["submit"]):
        suggestions = get_suggestions(crop, disease)

        st.markdown(f"**{labels['symptoms']}**")
        st.write(suggestions["symptoms"])

        st.markdown(f"**{labels['cause']}**")
        st.write(suggestions["cause"])

        st.markdown(f"**{labels['prevention']}**")
        st.write(suggestions["prevention"])

        st.markdown(f"**{labels['pesticides']}**")
        st.markdown(f"**{labels['natural_pesticides']}**")
        st.write(suggestions["natural_pesticides"])
        st.markdown(f"**{labels['chemical_pesticides']}**")
        st.write(suggestions["chemical_pesticides"])

        st.markdown(f"**{labels['environmental_factors']}**")
        st.write(suggestions["environmental_factors"])

        st.markdown(f"**{labels['precautions']}**")
        st.write(suggestions["precautions"])

        st.markdown(f"**{labels['care_instructions']}**")
        st.write(suggestions["care_instructions"])

        st.markdown(f"**{labels['encouragement']}**")
        st.write(suggestions["encouragement"])

        # YouTube Videos
        st.markdown(f"**{labels['youtube_videos']}**")
        videos = fetch_youtube_videos(f"{crop} {disease} treatment")
        for video in videos:
            video_id = video["id"].get("videoId")
            title = video["snippet"]["title"]
            if video_id:
                video_url = f"https://www.youtube.com/watch?v={video_id}"
                st.markdown(f"[{title}]({video_url})")
