import streamlit as st
import google.generativeai as genai
from PIL import Image

# Set up Google API Key
GOOGLE_API_KEY = "AIzaSyDbuGQIiDaVb90HpXCCgQmpie0x4ffVytk"  # Replace with your actual API key
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize the Gemini model
model = genai.GenerativeModel('gemini-1.5-flash-002')

# Language-specific labels and options
language_options = {
    "English": {
        "title": "🌱 Smart Agriculture Chatbot",
        "choose_language": "Choose Language",
        "choose_mode": "Choose Mode",
        "modes": ["Agriculture Chat", "Disease Prediction"],
        "choose_topic": "Choose an Option",
        "sub_topics": {
            "Harvesting": ["Best Time to Harvest", "Harvesting Techniques", "Post-Harvest Handling"],
            "Planting": ["Seed Selection", "Planting Techniques", "Crop Rotation"],
            "Irrigation": ["Drip Irrigation", "Sprinkler Systems", "Water Management"],
            "Pest Control": ["Organic Pest Control", "Chemical Pest Control", "Integrated Pest Management"],
            "Soil Health": ["Soil Testing", "Fertilizer Application", "Soil Conservation"]
        },
        "input_label": "Ask me anything about {}:",
        "submit_button": "Submit",
        "response_label": "Chatbot Response:",
        "disease_prediction": "Plant Disease Prediction",
        "upload_image": "Upload an image of your crop/plant",
        "predict_button": "Predict Disease",
        "crop_identification": "Plant Identification:",
        "disease_details": "Disease Details:",
        "symptoms": "Symptoms:",
        "cause": "Cause of the Disease:",
        "prevention": "Prevention Measures:",
        "pesticides": "Pesticide/Fungicide Recommendations:",
        "natural_pesticides": "Natural Pesticides:",
        "chemical_pesticides": "Chemical Pesticides:",
        "environmental_factors": "Suitable Environmental Factors:",
        "precautions": "Precautions to Take:",
        "care_instructions": "Care Instructions:",
        "encouragement": "Encouragement and Follow-up:"
    },
    "Telugu": {
        "title": "🌱 స్మార్ట్ వ్యవసాయ చాట్‌బాట్",
        "choose_language": "భాషను ఎంచుకోండి",
        "choose_mode": "మోడ్‌ను ఎంచుకోండి",
        "modes": ["వ్యవసాయ చాట్", "రోగ నిర్ధారణ"],
        "choose_topic": "ఎంపికను ఎంచుకోండి",
        "sub_topics": {
            "పంట కోత": ["పంట కోతకు ఉత్తమ సమయం", "పంట కోత పద్ధతులు", "పంట కోత తర్వాత నిర్వహణ"],
            "నాటడం": ["విత్తనాల ఎంపిక", "నాటడం పద్ధతులు", "పంట మార్పిడి"],
            "నీటిపారుదల": ["డ్రిప్ ఇరిగేషన్", "స్ప్రింక్లర్ వ్యవస్థలు", "నీటి నిర్వహణ"],
            "కీటక నియంత్రణ": ["సేంద్రీయ కీటక నియంత్రణ", "రసాయన కీటక నియంత్రణ", "సమగ్ర కీటక నియంత్రణ"],
            "నేల ఆరోగ్యం": ["నేల పరీక్ష", "ఎరువు వినియోగం", "నేల సంరక్షణ"]
        },
        "input_label": "{} గురించి ఏదైనా అడగండి:",
        "submit_button": "సమర్పించండి",
        "response_label": "చాట్‌బాట్ ప్రతిస్పందన:",
        "disease_prediction": "పంట రోగ నిర్ధారణ",
        "upload_image": "మీ పంట/మొక్క యొక్క చిత్రాన్ని అప్‌లోడ్ చేయండి",
        "predict_button": "రోగాన్ని నిర్ధారించండి",
        "crop_identification": "పంట గుర్తింపు:",
        "disease_details": "రోగ వివరాలు:",
        "symptoms": "లక్షణాలు:",
        "cause": "రోగ కారణాలు:",
        "prevention": "నివారణ చర్యలు:",
        "pesticides": "పురుగుమందులు/ఫంగిసైడ్ సిఫార్సులు:",
        "natural_pesticides": "సహజ పురుగుమందులు:",
        "chemical_pesticides": "రసాయన పురుగుమందులు:",
        "environmental_factors": "సరైన పర్యావరణ కారకాలు:",
        "precautions": "జాగ్రత్తలు:",
        "care_instructions": "సంరక్షణ సూచనలు:",
        "encouragement": "ప్రోత్సాహం మరియు ఫాలో-అప్:"
    },
    "Hindi": {
        "title": "🌱 स्मार्ट कृषि चैटबॉट",
        "choose_language": "भाषा चुनें",
        "choose_mode": "मोड चुनें",
        "modes": ["कृषि चैट", "रोग पूर्वानुमान"],
        "choose_topic": "एक विकल्प चुनें",
        "sub_topics": {
            "फसल कटाई": ["फसल कटाई का सही समय", "फसल कटाई के तरीके", "फसल कटाई के बाद प्रबंधन"],
            "बुवाई": ["बीज चयन", "बुवाई के तरीके", "फसल चक्र"],
            "सिंचाई": ["ड्रिप सिंचाई", "स्प्रिंकलर सिस्टम", "जल प्रबंधन"],
            "कीट नियंत्रण": ["जैविक कीट नियंत्रण", "रासायनिक कीट नियंत्रण", "समन्वित कीट प्रबंधन"],
            "मृदा स्वास्थ्य": ["मृदा परीक्षण", "उर्वरक अनुप्रयोग", "मृदा संरक्षण"]
        },
        "input_label": "{} के बारे में कुछ भी पूछें:",
        "submit_button": "जमा करें",
        "response_label": "चैटबॉट प्रतिक्रिया:",
        "disease_prediction": "पौध रोग पूर्वानुमान",
        "upload_image": "अपनी फसल/पौधे की तस्वीर अपलोड करें",
        "predict_button": "रोग की पहचान करें",
        "crop_identification": "फसल पहचान:",
        "disease_details": "रोग विवरण:",
        "symptoms": "लक्षण:",
        "cause": "रोग का कारण:",
        "prevention": "रोकथाम उपाय:",
        "pesticides": "कीटनाशक/फंगीसाइड सिफारिशें:",
        "natural_pesticides": "प्राकृतिक कीटनाशक:",
        "chemical_pesticides": "रासायनिक कीटनाशक:",
        "environmental_factors": "उपयुक्त पर्यावरणीय कारक:",
        "precautions": "सावधानियां:",
        "care_instructions": "देखभाल निर्देश:",
        "encouragement": "प्रोत्साहन और फॉलो-अप:"
    }
}

# Function to get response from Gemini AI
def get_gemini_response(question, language):
    prompt = f"Respond in {language}: {question}"
    response = model.generate_content(prompt)
    return response.text

# Mock function for crop identification and disease prediction
def predict_disease(image):
    return "Tomato Plant", "Early Blight"

# Enhanced function for suggestions
def get_suggestions(crop, disease):
    suggestions = {
        "Tomato Plant": {
            "Early Blight": {
                "symptoms": "1. Brown spots on leaves.\n2. Yellowing of leaves.\n3. Wilting and defoliation.",
                "cause": "1. Fungal infection caused by Alternaria solani.\n2. High humidity and warm temperatures.\n3. Poor air circulation.",
                "prevention": "1. Rotate crops every 2-3 years.\n2. Avoid overhead watering.\n3. Use disease-resistant varieties.",
                "natural_pesticides": "1. Neem oil – Effective against pests and fungal infections.\n2. Garlic spray – Acts as a natural insect repellent.\n3. Baking soda spray – Prevents fungal growth.",
                "chemical_pesticides": "1. Chlorothalonil – Apply every 7-10 days.\n2. Mancozeb – Apply as a preventive measure.",
                "environmental_factors": "1. Ideal temperature: 20-25°C.\n2. Maintain soil pH between 6.0 and 7.0.\n3. Ensure proper spacing for air circulation.",
                "precautions": "1. Avoid overwatering.\n2. Remove infected leaves and debris.\n3. Ensure proper drainage.",
                "care_instructions": "1. Water deeply once a week.\n2. Apply balanced fertilizers.\n3. Monitor for early signs of disease.",
                "encouragement": "Your plant can recover with proper care! Stay consistent with the treatment."
            }
        }
    }
    return suggestions.get(crop, {}).get(disease, {
        "symptoms": "No specific symptoms available.",
        "cause": "No specific cause available.",
        "prevention": "No specific prevention measures available.",
        "natural_pesticides": "No specific natural pesticides recommended.",
        "chemical_pesticides": "No specific chemical pesticides recommended.",
        "environmental_factors": "No specific environmental factors available.",
        "precautions": "No specific precautions available.",
        "care_instructions": "No specific care instructions available.",
        "encouragement": "No specific encouragement message available."
    })

# Sidebar for language selection
st.sidebar.title(language_options["English"]["choose_language"])
language = st.sidebar.selectbox(
    "Select Language",
    ["English", "Telugu", "Hindi"],
    label_visibility="collapsed"
)

# Update labels based on selected language
labels = language_options[language]

# Streamlit app title
st.title(labels["title"])

# Sidebar for mode selection
st.sidebar.title(labels["choose_mode"])
mode = st.sidebar.selectbox(
    "Select Mode",
    labels["modes"],
    label_visibility="collapsed"
)

# Agriculture Chat Mode
if mode == labels["modes"][0]:  # Agriculture Chat
    st.sidebar.title(labels["choose_topic"])
    main_option = st.sidebar.selectbox(
        "Select Main Topic",
        list(labels["sub_topics"].keys()),
        label_visibility="collapsed"
    )

    # Sub-options based on the main option
    sub_option = st.sidebar.selectbox(
        "Select Sub Topic",
        labels["sub_topics"][main_option],
        label_visibility="collapsed"
    )

    # Main chat interface
    st.write(f"**మీరు ఎంచుకున్నది:** {main_option} - {sub_option}" if language == "Telugu" else f"**आपने चुना:** {main_option} - {sub_option}" if language == "Hindi" else f"**You selected:** {main_option} - {sub_option}")

    # User input (text only)
    user_input = st.text_input(labels["input_label"].format(sub_option), "")

    # Submit button
    if st.button(labels["submit_button"]):
        if user_input:
            question = f"{main_option} - {sub_option}: {user_input}"
            st.write(f"**మీరు అడిగిన ప్రశ్న:** {user_input}" if language == "Telugu" else f"**आपका प्रश्न:** {user_input}" if language == "Hindi" else f"**You asked:** {user_input}")
            
            # Get response from Gemini AI
            try:
                response = get_gemini_response(question, language)
                st.write(f"**{labels['response_label']}**")
                st.write(response)
                    
            except Exception as e:
                st.error(f"An error occurred: {e}")
        else:
            st.warning("Please enter a question before submitting.")

# Disease Prediction Mode
elif mode == labels["modes"][1]:  # Disease Prediction
    st.sidebar.title(labels["disease_prediction"])
    uploaded_image = st.sidebar.file_uploader(labels["upload_image"], type=["jpg", "jpeg", "png"])

    # Display disease prediction results
    if uploaded_image is not None:
        image = Image.open(uploaded_image)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        if st.sidebar.button(labels["predict_button"]):
            # Predict crop and disease
            crop, disease = predict_disease(image)
            st.write(f"**{labels['crop_identification']}** {crop}")
            st.write(f"**{labels['disease_details']}** {disease}")

            # Get suggestions
            suggestions = get_suggestions(crop, disease)
            st.write(f"**{labels['symptoms']}**\n{suggestions['symptoms']}")
            st.write(f"**{labels['cause']}**\n{suggestions['cause']}")
            st.write(f"**{labels['prevention']}**\n{suggestions['prevention']}")
            st.write(f"**{labels['natural_pesticides']}**\n{suggestions['natural_pesticides']}")
            st.write(f"**{labels['chemical_pesticides']}**\n{suggestions['chemical_pesticides']}")
            st.write(f"**{labels['environmental_factors']}**\n{suggestions['environmental_factors']}")
            st.write(f"**{labels['precautions']}**\n{suggestions['precautions']}")
            st.write(f"**{labels['care_instructions']}**\n{suggestions['care_instructions']}")
            st.write(f"**{labels['encouragement']}**\n{suggestions['encouragement']}")
