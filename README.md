# MasterChef AI 🍽️

## AI-Powered Smart Cooking Recommendation and Nutrition Assistant

MasterChef AI is an AI-powered Smart Cooking Recommendation and Nutrition Assistant built using Python, Streamlit, and Gemini AI. It helps users discover personalized meal recommendations, healthy cooking alternatives, recipe guidance, and expert nutrition suggestions based on their food preferences and health considerations.

This project combines Recommendation Systems, Generative AI, RAG concepts, and Human-in-the-Loop (HITL) escalation to create a safer and smarter cooking assistant experience.

---

## Features

* Personalized Dish Recommendation System
* Recipe Viewer with Ingredients and Cooking Steps
* Nutrition Information and Healthy Cooking Tips
* AI-Powered Cooking Assistant using Gemini API
* Human-in-the-Loop (HITL) escalation for medical-sensitive dietary queries
* Health condition detection for diabetes, PCOS, thyroid, pregnancy, kidney issues, BP, cholesterol, and more
* Dynamic fallback responses when Gemini API is unavailable
* Premium multi-theme UI (Dark, Light, Warm Food Theme, Healthy Green Theme)
* Attractive food cards with images and modern responsive layout

---

## Tech Stack

* Python
* Streamlit
* Pandas
* Gemini AI (Google Generative AI)
* HTML + CSS Styling
* Recommendation Logic
* RAG Concepts
* HITL (Human-in-the-Loop)

---

## Project Workflow

### Normal Query Flow

**User asks:**

How can I make Brinjal Bhaji healthier for weight loss?

→ Gemini AI provides a detailed cooking and nutrition response

---

### Sensitive Medical Query Flow

**User asks:**

I have diabetes, can I eat Dal Rice every day?

→ HITL triggers
→ Escalated to Nutrition Expert 👨‍⚕️
→ Safe dietary guidance is shown instead of risky AI advice

---

## Project Structure

MasterChef-AI/

├── app.py
├── dishes.csv
├── requirements.txt
├── .env
├── .gitignore
├── README.md

└── images/
  ├── dal_chawal.png
  ├── paneer_bhaji.png
  ├── brinjal_bhaji_chapati.png
  └── ...

---

## Installation

### Clone Repository

git clone https://github.com/your-username/MasterChef-AI.git

cd MasterChef-AI

---

### Install Dependencies

pip install -r requirements.txt

---

### Setup Environment Variable

Create a `.env` file:

GOOGLE_API_KEY=your_actual_gemini_api_key_here

---

### Run Application

streamlit run app.py

---

## Future Improvements

* Advanced RAG-based recipe retrieval
* User login and saved meal plans
* Weekly meal planner
* Calorie tracker
* Voice-enabled cooking assistant
* Smart grocery list generation
* Personalized diet plans using ML

---

## Author

**Lavanya**
BSc Data Science Student
AI | Data Science | Recommendation Systems | GenAI | HITL | RAG

---
