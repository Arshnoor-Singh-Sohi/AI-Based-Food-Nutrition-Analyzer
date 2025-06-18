from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Dict, Optional
import re
import json
from src.ai_model import get_nutrition_info, get_enhanced_nutrition_analysis
from src.nutrition_calculator import NutritionCalculator
from src.meal_planner import MealPlanner

app = FastAPI(
    title="AI Nutrition Analyzer API",
    description="Advanced nutrition analysis with AI-powered insights",
    version="2.0.0"
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize our enhanced components
nutrition_calc = NutritionCalculator()
meal_planner = MealPlanner()

class NutritionResponse(BaseModel):
    food: str
    nutrition_info: str
    detailed_breakdown: Dict[str, float]
    health_benefits: List[str]
    meal_suggestions: List[str]
    health_score: int
    dietary_tags: List[str]
    calories_per_serving: int
    serving_size: str

class FoodComparisonRequest(BaseModel):
    foods: List[str]

@app.get("/")
async def root():
    return {
        "message": "🚀 AI Nutrition Analyzer 2.0 - Your Personal Nutrition Assistant",
        "version": "2.0.0",
        "features": [
            "Advanced nutrition analysis",
            "Health scoring algorithm",
            "Meal planning suggestions",
            "Food comparison tools",
            "Dietary restriction support"
        ]
    }

@app.get("/analyze/{food_item}", response_model=NutritionResponse)
async def analyze_food(food_item: str):
    """
    Get comprehensive nutrition analysis for a food item with AI-powered insights.
    """
    try:
        # Get raw nutrition info from AI
        raw_nutrition = get_nutrition_info(food_item)
        
        if not raw_nutrition:
            raise HTTPException(status_code=500, detail="Failed to get nutrition information")

        # Enhanced analysis with structured data
        enhanced_data = get_enhanced_nutrition_analysis(food_item, raw_nutrition)
        
        # Parse nutrition values using regex
        nutrition_values = nutrition_calc.parse_nutrition_text(raw_nutrition)
        
        # Calculate health score
        health_score = nutrition_calc.calculate_health_score(nutrition_values)
        
        # Get health benefits based on nutrition profile
        health_benefits = nutrition_calc.get_health_benefits(food_item, nutrition_values)
        
        # Get meal suggestions
        meal_suggestions = meal_planner.get_meal_suggestions(food_item, nutrition_values)
        
        # Get dietary tags
        dietary_tags = nutrition_calc.get_dietary_tags(food_item, nutrition_values)
        
        # Structure the response
        response_data = {
            "food": food_item.lower(),
            "nutrition_info": raw_nutrition,
            "detailed_breakdown": nutrition_values,
            "health_benefits": health_benefits,
            "meal_suggestions": meal_suggestions,
            "health_score": health_score,
            "dietary_tags": dietary_tags,
            "calories_per_serving": int(nutrition_values.get('calories', 0)),
            "serving_size": enhanced_data.get('serving_size', '1 medium')
        }

        return JSONResponse(content=response_data, status_code=200)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.post("/compare")
async def compare_foods(request: FoodComparisonRequest):
    """
    Compare nutrition profiles of multiple foods side by side.
    """
    try:
        if len(request.foods) < 2 or len(request.foods) > 4:
            raise HTTPException(status_code=400, detail="Please provide 2-4 foods for comparison")
        
        comparison_data = []
        
        for food in request.foods:
            # Get nutrition data for each food
            raw_nutrition = get_nutrition_info(food)
            nutrition_values = nutrition_calc.parse_nutrition_text(raw_nutrition)
            health_score = nutrition_calc.calculate_health_score(nutrition_values)
            
            comparison_data.append({
                "food": food,
                "nutrition": nutrition_values,
                "health_score": health_score
            })
        
        # Determine the "winner" in each category
        analysis = nutrition_calc.compare_foods_analysis(comparison_data)
        
        return {
            "foods": comparison_data,
            "analysis": analysis,
            "recommendations": meal_planner.get_comparison_recommendations(comparison_data)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Comparison failed: {str(e)}")

@app.get("/ask/{question}")
async def ask_nutrition_question(question: str):
    """
    Ask a free-form nutrition question with AI-powered responses.
    """
    try:
        from src.ai_model import query_nutrition_knowledge
        result = query_nutrition_knowledge(question)
        
        # Enhanced response with structured suggestions
        enhanced_response = {
            "question": question,
            "answer": result,
            "related_topics": nutrition_calc.get_related_topics(question),
            "suggested_foods": nutrition_calc.suggest_foods_for_question(question)
        }
        
        return enhanced_response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Question processing failed: {str(e)}")

@app.get("/meal-plan/{goal}")
async def generate_meal_plan(goal: str, days: int = 7):
    """
    Generate a personalized meal plan based on health goals.
    Goals: weight_loss, muscle_gain, heart_health, diabetes_friendly, high_energy
    """
    try:
        if days < 1 or days > 14:
            raise HTTPException(status_code=400, detail="Days must be between 1 and 14")
        
        meal_plan = meal_planner.generate_meal_plan(goal, days)
        
        return {
            "goal": goal,
            "duration_days": days,
            "meal_plan": meal_plan,
            "nutrition_summary": meal_planner.calculate_plan_nutrition(meal_plan),
            "shopping_list": meal_planner.generate_shopping_list(meal_plan)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Meal plan generation failed: {str(e)}")

@app.get("/health-score/{food_item}")
async def get_health_score(food_item: str):
    """
    Get just the health score and breakdown for a food item.
    """
    try:
        raw_nutrition = get_nutrition_info(food_item)
        nutrition_values = nutrition_calc.parse_nutrition_text(raw_nutrition)
        
        score_breakdown = nutrition_calc.get_detailed_score_breakdown(nutrition_values)
        
        return {
            "food": food_item,
            "overall_score": nutrition_calc.calculate_health_score(nutrition_values),
            "score_breakdown": score_breakdown,
            "improvement_suggestions": nutrition_calc.get_improvement_suggestions(nutrition_values)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Health score calculation failed: {str(e)}")

@app.get("/trending")
async def get_trending_foods():
    """
    Get trending healthy foods and superfoods.
    """
    try:
        trending_data = {
            "superfoods": [
                {"name": "Quinoa", "benefits": "Complete protein, gluten-free"},
                {"name": "Blueberries", "benefits": "High antioxidants, brain health"},
                {"name": "Salmon", "benefits": "Omega-3 fatty acids, heart health"},
                {"name": "Avocado", "benefits": "Healthy fats, fiber"},
                {"name": "Sweet Potato", "benefits": "Beta-carotene, complex carbs"}
            ],
            "seasonal_recommendations": meal_planner.get_seasonal_recommendations(),
            "diet_trends": [
                {"name": "Mediterranean", "description": "Heart-healthy, anti-inflammatory"},
                {"name": "Plant-Based", "description": "Environmentally friendly, nutrient-dense"},
                {"name": "Intermittent Fasting", "description": "Metabolic benefits, weight management"}
            ]
        }
        
        return trending_data
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Trending data fetch failed: {str(e)}")

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": "2024-01-20T10:00:00Z"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)