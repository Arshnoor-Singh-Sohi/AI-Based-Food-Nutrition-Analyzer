from fastapi import FastAPI
from fastapi.responses import JSONResponse
from src.ai_model import get_nutrition_info
from src.ai_model import query_nutrition_knowledge


app = FastAPI()

@app.get("/")
async def root():
    return {"message": "AI-Based Food Nutrition Analyzer is running!"}

@app.get("/analyze/{food_item}")
async def analyze_food(food_item: str):
    """
    Get structured nutrition info for a food item.
    """
    result = get_nutrition_info(food_item)

    # Formatting output properly for better JSON readability
    structured_response = {
        "food": food_item,
        "nutrition_info": result.replace("\n", " ")  # Remove \n for cleaner JSON
    }

    return JSONResponse(content=structured_response, status_code=200)

@app.get("/ask/{question}")
async def ask_nutrition_question(question: str):
    """
    Ask a free-form nutrition question based on uploaded docs.
    """
    result = query_nutrition_knowledge(question)
    return {"question": question, "answer": result}
