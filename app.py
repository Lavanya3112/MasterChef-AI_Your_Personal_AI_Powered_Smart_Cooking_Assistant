import streamlit as st
import pandas as pd
import google.generativeai as genai
import os
from dotenv import load_dotenv

# ======================================================
# ENV + GEMINI SETUP
# ======================================================
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.0-flash")

# ======================================================
# PAGE CONFIG
# ======================================================
st.set_page_config(
    page_title="MasterChef AI",
    page_icon="🍽️",
    layout="centered"
)

# ======================================================
# THEME SELECTOR
# ======================================================

theme = st.selectbox(
    "Choose Theme",
    ["Dark Mode", "Light Mode", "Warm Food Theme", "Healthy Green Theme"]
)

# ======================================================
# THEME COLORS
# ======================================================

if theme == "Dark Mode":
    bg_color = "#121826"
    card_color = "#1E293B"
    text_color = "#F8FAFC"
    button_gradient = "linear-gradient(90deg, #E85D04, #F4A300)"
    accent_color = "#F4A300"

elif theme == "Light Mode":
    bg_color = "#FEF4F5"
    card_color ="#2A2D3E"
    text_color = "#1F2937"
    button_gradient = "linear-gradient(90deg, #E85D04, #F4A300)"
    accent_color = "#F59E0B"

elif theme == "Warm Food Theme":
    bg_color = "#2B1B17"
    card_color = "#4A2E1F"
    text_color = "#FFF8E7"
    button_gradient = "linear-gradient(90deg, #E85D04, #F48C06, #F4A300)"
    accent_color = "#F4A300"

elif theme == "Healthy Green Theme":
    bg_color = "#102A1F"
    card_color = "#183D2D"
    text_color = "#ECFDF5"
    button_gradient = "linear-gradient(90deg, #F4A300, #FEE907, #22C55E)"
    accent_color = "#FEE907"

# ======================================================
# APPLY CSS
# ======================================================

st.markdown(f"""
<style>

/* Full App Background */
.stApp {{
    background-color: {bg_color};
}}

/* Main Container */
.main {{
    background-color: {bg_color};
}}

/* Block Container */
section[data-testid="stSidebar"],
div[data-testid="stAppViewContainer"],
div[data-testid="stHeader"] {{
    background-color: {bg_color};
}}

/* Subtitles */
p {{
    font-size: 16px;
}}

/* Premium Cards */
.card {{
    background-color: {card_color};
    border: 1px solid rgba(255,255,255,0.08);
    padding: 22px;
    border-radius: 18px;
    margin-bottom: 18px;
    backdrop-filter: blur(12px);
    box-shadow: 0 10px 30px rgba(0,0,0,0.18);
}}

/* Form Labels */
label, .stSelectbox label, .stTextInput label {{
    color: {text_color} !important;;
    font-weight: 600;
}}

/* Buttons */
.stButton > button {{
    width: 100%;
    background: {button_gradient};
    color: white;
    border: none;
    border-radius: 14px;
    height: 3.2em;
    font-size: 16px;
    font-weight: 700;
    box-shadow: 0 8px 20px rgba(0,0,0,0.18);
}}

/* Food Images */
img {{
    border-radius: 18px !important;
    object-fit: cover;
}}

.stButton > button:hover {{
    transform: translateY(-2px);
}}

/* Input Boxes */
.stTextInput > div > div > input,
.stSelectbox > div > div {{
    border-radius: 12px !important;
}}

/* Expander */
.streamlit-expanderHeader {{
    font-size: 17px;
    font-weight: 600;
}}

/* Success + Warning */
.stSuccess,
.stWarning {{
    border-radius: 14px;
}}

</style>
""", unsafe_allow_html=True)

# ======================================================
# LOAD DATA
# ======================================================
df = pd.read_csv("dishes.csv")

# ======================================================
# HITL ESCALATION KEYWORDS
# ======================================================

ESCALATION_KEYWORDS = [
    "diabetes",
    "thyroid",
    "pcos",
    "pcod",
    "pregnancy",
    "kidney",
    "blood pressure",
    "bp",
    "cholesterol",
    "heart problem",
    "heart disease",
    "fatty liver",
    "liver issue",
    "cancer",
    "allergy",
    "gluten allergy",
    "lactose intolerance",
    "ulcer",
    "gastric",
    "ibs",
    "weight loss medicine",
    "surgery recovery",
    "fever diet",
    "doctor advised"
]

# ======================================================
# RECOMMENDATION FUNCTION
# ======================================================
def recommend_dishes(yesterday, meal_type, quick_meal, healthy_meal):
    recommendations = df.copy()

    # avoid repeating yesterday's dish
    if yesterday:
        recommendations = recommendations[
            recommendations["Dish_Name"].str.lower() != yesterday.lower()
        ]

    # meal type match
    recommendations = recommendations[
        recommendations["Meal_Type"] == meal_type
    ]

    # quick meal filter
    if quick_meal == "Yes":
        recommendations = recommendations[
            recommendations["Cook_Time"] <= 30
        ]

    # healthy meal filter
    if healthy_meal == "Yes":
        healthy_keywords = [
            "Khichdi", "Dal", "Bhaji", "Chole", "Rajma"
        ]
        recommendations = recommendations[
            recommendations["Dish_Name"].str.contains(
                "|".join(healthy_keywords),
                case=False,
                na=False
            )
        ]

    return recommendations.head(5)

# ======================================================
# TITLE
# ======================================================

st.markdown("""
<div style="
    background:
        linear-gradient(rgba(0,0,0,0.45), rgba(0,0,0,0.60)),
        url('https://images.unsplash.com/photo-1504674900247-0877df9cc836');
    background-size: cover;
    background-position: center;
    padding: 80px 40px;
    border-radius: 24px;
    margin-bottom: 30px;
">

<div style="
    color: white !important;
    font-size: 56px;
    font-weight: 800;
    margin-bottom: 14px;
    text-shadow: 2px 2px 10px rgba(0,0,0,0.30);
">
MasterChef AI
</div>

<div style="
    color: white !important;
    font-size: 32px;
    font-weight: 600;
    margin-bottom: 14px;
">
Your Personal AI-Powered Smart Cooking Assistant
</div>

<div style="
    color: #F8FAFC !important;
    font-size: 18px;
    line-height: 1.7;
    max-width: 800px;
">
Get personalized meal recommendations, healthy alternatives,
and expert cooking suggestions powered by Gemini AI.
</div>

</div>
""", unsafe_allow_html=True)

# ======================================================
# USER INPUTS
# ======================================================
col1, col2 = st.columns(2)

with col1:
    yesterday = st.selectbox(
        "What was cooked yesterday?",
        [""] + sorted(df["Dish_Name"].dropna().unique().tolist())
    )

    meal_type = st.selectbox(
        "Meal Type",
        ["Lunch", "Dinner"]
    )

with col2:
    quick_meal = st.selectbox(
        "Quick meal needed?",
        ["Yes", "No"]
    )

    healthy_meal = st.selectbox(
        "Healthy / Light meal?",
        ["Yes", "No"]
    )

# ======================================================
# MAIN BUTTON
# ======================================================

if "show_result" not in st.session_state:
    st.session_state.show_result = False

if st.button("Recommend Dish"):
    st.session_state.show_result = True

if st.session_state.show_result:

    result = recommend_dishes(
        yesterday,
        meal_type,
        quick_meal,
        healthy_meal
    )

    st.markdown("---")
    st.subheader("Recommended Dishes")

    if not result.empty:

        cols = st.columns(2)

        for index, (_, row) in enumerate(result.iterrows()):
            with cols[index % 2]:

                st.image(
                    row["Image"],
                    width=350
                )

                st.markdown(f"""
                <div class="card">
                    <h3>🍽️ {row['Dish_Name']}</h3>
                    <p><b>Main Ingredient:</b> {row['Main_Ingredient']}</p>
                    <p><b>Cook Time:</b> {row['Cook_Time']} mins</p>
                    <p><b>Nutrition:</b> {row['Nutrition']}</p>
                    <p><b>Healthy Tip:</b> {row['Healthy_Tips']}</p>
                </div>
                """, unsafe_allow_html=True)

                # =============================================
                # RECIPE VIEWER
                # =============================================
                with st.expander(f"Show Recipe - {row['Dish_Name']}"):

                    st.success(f"Recipe for {row['Dish_Name']}")

                    st.write("### Ingredients")
                    st.write(row["Ingredients"])

                    st.write("### Cooking Steps")
                    st.write(row["Steps"])

                    st.write("### Nutrition")
                    st.write(row["Nutrition"])

                    st.write("### Healthy Tips")
                    st.write(row["Healthy_Tips"])

                    # =========================================
                    # GEMINI + RAG + HITL
                    # =========================================

                    st.write("### Ask AI About This Dish 👨‍🍳")

                    user_question = st.text_input(
                        f"Ask something about {row['Dish_Name']}",
                        key=f"question_{row['Dish_Name']}"
                    )

                    if st.button(
                        f"Ask AI ✨",
                        key=f"ask_button_{row['Dish_Name']}"
                    ):

                        if not user_question:
                            st.warning("Please enter a question first.")

                        else:
                            query_lower = user_question.lower()

                        # =========================================
                        # HITL for Sensitive Medical Questions
                        # =========================================

                            if any(word in query_lower for word in ESCALATION_KEYWORDS):

                                def get_nutrition_expert_response(user_query):
                                    query = user_query.lower()

                                    if "diabetes" in query:
                                        return (
                                            "Since diabetes requires careful carbohydrate control, "
                                            "portion size and cooking method matter a lot. "
                                            "We recommend consulting a certified dietician before making this dish a regular part of your meal plan."
                                        )

                                    elif "pregnancy" in query:
                                        return (
                                            "During pregnancy, nutritional balance and food safety are very important. "
                                            "Please consult your doctor or nutrition expert before including this dish regularly in your diet."
                                        )

                                    elif "pcos" in query or "pcod" in query:
                                        return (
                                            "For PCOS management, low-oil cooking, balanced carbs, and high-protein meals are recommended. "
                                            "A dietician can help personalize this dish according to your health goals."
                                        )

                                    elif "kidney" in query:
                                        return (
                                            "Kidney-related diets often require sodium, potassium, and protein monitoring. "
                                            "Please consult a healthcare professional before consuming this dish frequently."
                                        )

                                    elif "thyroid" in query:
                                        return (
                                            "For thyroid conditions, ingredient balance and meal timing may matter depending on your treatment plan. "
                                            "Professional dietary guidance is recommended before regular consumption."
                                        )

                                    elif "blood pressure" in query or "bp" in query:
                                        return (
                                            "For blood pressure management, sodium and oil intake should be monitored carefully. "
                                            "Please consult a doctor or dietician before adding this dish regularly to your routine."
                                        )

                                    elif "cholesterol" in query or "heart" in query:
                                        return (
                                            "For cholesterol or heart-related conditions, cooking oil, fats, and portion control are important. "
                                            "A certified nutrition expert can guide you better based on your medical history."
                                        )

                                    else:
                                        return (
                                            "This health-related question requires expert dietary guidance. "
                                            "Please consult a certified dietician or doctor for personalized advice."
                                        )

                                expert_response = get_nutrition_expert_response(user_question)

                                st.warning(
                                    "👨‍⚕️ This question requires expert dietary guidance.\n\n"
                                    "Escalated to Nutrition Expert."
                                )

                                st.info(expert_response)

                            # =========================================
                            # GEMINI RESPONSE for Normal Questions
                            # =========================================

                            else:

                                prompt = f"""
                                You are MasterChef AI, an expert cooking and nutrition assistant.

                                Dish Name: {row["Dish_Name"]}
                                Ingredients: {row["Ingredients"]}
                                Cooking Steps: {row["Steps"]}
                                Nutrition: {row["Nutrition"]}
                                Healthy Tips: {row["Healthy_Tips"]}

                                User Question:
                                {user_question}

                                Instructions:
                                - Give detailed and useful answers
                                - Explain clearly in 4–6 lines
                                - Suggest healthier alternatives if needed
                                - Recommend ingredient substitutions if helpful
                                - Keep the answer practical and beginner-friendly
                                - Sound professional but friendly
                                - Avoid one-line answers
                                - Keep the response specific to this dish
                                """

                                try:
                                    response = model.generate_content(prompt)

                                    st.success("AI Suggestion")
                                    st.write(response.text)

                                except Exception as e:
                                    st.warning("Gemini is currently busy. Showing smart fallback response instead.")

                                    st.success("AI Suggestion")

                                    if "weight loss" in user_question.lower():
                                        st.write(
                                            f"To make {row['Dish_Name']} healthier for weight loss, use less oil and ghee, "
                                            f"add more vegetables like spinach, carrots, beans, or seasonal vegetables for extra fiber, "
                                            f"and keep portion sizes balanced. You can also use healthier cooking methods like steaming, "
                                            f"grilling, or light sautéing instead of deep frying wherever possible."
                                        )

                                    elif "healthy" in user_question.lower():
                                        st.write(
                                            f"To make {row['Dish_Name']} healthier, use less oil, avoid excess ghee, "
                                            f"include fresh vegetables, and prefer homemade ingredients over packaged items. "
                                            f"Balanced portions and simple cooking methods make the dish healthier and easier to digest."
                                        )

                                    elif "side dish" in user_question.lower():
                                        st.write(
                                            f"The best side dishes for {row['Dish_Name']} include curd, fresh salad, "
                                            f"light soup, roasted vegetables, or buttermilk. These improve digestion and balance the meal."
                                        )

                                    elif "replace" in user_question.lower():
                                        st.write(
                                            f"You can make {row['Dish_Name']} healthier by replacing refined ingredients with better options "
                                            f"like brown rice instead of white rice, less oil instead of heavy frying, "
                                            f"and fresh homemade spices instead of processed masalas."
                                        )

                                    else:
                                        st.write(
                                            f"{row['Dish_Name']} can be made healthier by reducing oil, adding vegetables, "
                                            f"and keeping portion sizes balanced. Fresh homemade preparation is always better for nutrition and digestion."
                                        )

    else:
        st.warning("No suitable dishes found.")
