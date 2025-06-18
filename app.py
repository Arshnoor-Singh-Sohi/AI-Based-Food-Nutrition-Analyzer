import streamlit as st
import requests
import re

st.set_page_config(page_title="Food Nutrition Dashboard", layout="centered")
st.title("🥗 AI-Based Food Nutrition Analyzer")

# --- Input ---
food_item = st.text_input("Enter a food item (e.g., banana, oats, eggs):")

if st.button("Analyze"):
    if not food_item.strip():
        st.warning("Please enter a food item.")
    else:
        try:
            # Backend FastAPI call
            url = f"http://127.0.0.1:8000/analyze/{food_item}"
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                nutrition_text = data["nutrition_info"]

                # --- Display Raw Info ---
                st.subheader(f"Nutrition info for: {food_item.capitalize()}")
                st.write(nutrition_text)

                # --- Extract Macros ---
                def extract_macro(pattern, text):
                    match = re.search(pattern, text, re.IGNORECASE)
                    return float(match.group(1)) if match else 0

                protein = extract_macro(r"Protein: (\d+\.?\d*)\s?g", nutrition_text)
                fat = extract_macro(r"Fat: (\d+\.?\d*)\s?g", nutrition_text)
                carbs = extract_macro(r"Carbohydrates: (\d+\.?\d*)\s?g", nutrition_text)
                fiber = extract_macro(r"Fiber: (\d+\.?\d*)\s?g", nutrition_text)

                # --- Bar Chart ---
                st.markdown("### 🧩 Macronutrient Breakdown")
                st.bar_chart({
                    "Grams": {
                        "Protein": protein,
                        "Fat": fat,
                        "Carbs": carbs,
                        "Fiber": fiber
                    }
                })

                # --- Health Score ---
                score = 0
                if fiber >= 3: score += 1
                if protein >= 3: score += 1
                if fat <= 3: score += 1
                if carbs <= 30: score += 1

                health_status = {
                    4: "Excellent 🟢",
                    3: "Good 🟡",
                    2: "Fair 🟠",
                    1: "Poor 🔴",
                    0: "Very Poor 🔴"
                }

                st.markdown(f"### 🩺 Health Score: {score}/4 — **{health_status[score]}**")

                # --- Meal Suggestion ---
                st.markdown("### 🍽 Suggested Pairing:")
                suggestions = {
                    "banana": "Pair banana with Greek yogurt and oats for a complete breakfast.",
                    "oats": "Top your oats with berries and nuts for extra fiber and healthy fats.",
                    "eggs": "Pair boiled eggs with whole grain toast and avocado for a protein-rich meal.",
                }
                default_suggestion = "Try combining this food with greens, healthy fats, and lean protein."

                st.info(suggestions.get(food_item.lower(), default_suggestion))

            else:
                st.error("API error. Please try again.")
        except Exception as e:
            st.error(f"Error: {str(e)}")
