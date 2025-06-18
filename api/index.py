from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import re
import openai
from dotenv import load_dotenv
import logging
from datetime import datetime
from typing import Dict, List

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add these debug lines right here:
# print("=== DEBUG: Environment Variable Loading ===")
# print(f"Current working directory: {os.getcwd()}")
# print(f"OPENAI_API_KEY found: {bool(os.getenv('OPENAI_API_KEY'))}")
if os.getenv('OPENAI_API_KEY'):
    api_key_preview = os.getenv('OPENAI_API_KEY')
    # print(f"API key preview: {api_key_preview[:10]}...{api_key_preview[-4:]}")
# else:
    # print("No API key detected in environment")
# print("==========================================")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if OPENAI_API_KEY:
    client = openai.OpenAI(api_key=OPENAI_API_KEY)
else:
    client = None

app = FastAPI(title="AI Nutrition Analyzer API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class EnhancedNutritionDatabase:
    """A comprehensive nutrition database with realistic food profiles"""
    
    def __init__(self):
        # Realistic nutrition profiles for different food categories
        self.food_profiles = {
            'banana': {
                'calories': 89, 'protein': 1.1, 'fat': 0.3, 'carbs': 23, 
                'fiber': 2.6, 'sugar': 12, 'potassium': 358, 'vitamin_c': 8.7,
                'category': 'fruit', 'glycemic_index': 'medium'
            },
            'avocado': {
                'calories': 160, 'protein': 2.0, 'fat': 15, 'carbs': 9, 
                'fiber': 7, 'sugar': 0.7, 'potassium': 485, 'vitamin_k': 21,
                'category': 'fruit', 'glycemic_index': 'low'
            },
            'salmon': {
                'calories': 208, 'protein': 22, 'fat': 12, 'carbs': 0, 
                'fiber': 0, 'sugar': 0, 'omega3': 1.8, 'vitamin_d': 360,
                'category': 'protein', 'glycemic_index': 'none'
            },
            'quinoa': {
                'calories': 222, 'protein': 8, 'fat': 4, 'carbs': 39, 
                'fiber': 5, 'sugar': 1.6, 'iron': 2.8, 'magnesium': 118,
                'category': 'grain', 'glycemic_index': 'medium'
            },
            'spinach': {
                'calories': 23, 'protein': 2.9, 'fat': 0.4, 'carbs': 3.6, 
                'fiber': 2.2, 'sugar': 0.4, 'iron': 2.7, 'vitamin_k': 483,
                'category': 'vegetable', 'glycemic_index': 'low'
            },
            'blueberries': {
                'calories': 84, 'protein': 1.1, 'fat': 0.3, 'carbs': 21, 
                'fiber': 3.6, 'sugar': 15, 'vitamin_c': 9.7, 'antioxidants': 'high',
                'category': 'fruit', 'glycemic_index': 'low'
            },
            'almonds': {
                'calories': 161, 'protein': 6, 'fat': 14, 'carbs': 6, 
                'fiber': 3.5, 'sugar': 1.2, 'vitamin_e': 7.3, 'magnesium': 76,
                'category': 'nut', 'glycemic_index': 'low'
            },
            'sweet_potato': {
                'calories': 86, 'protein': 1.6, 'fat': 0.1, 'carbs': 20, 
                'fiber': 3, 'sugar': 4.2, 'vitamin_a': 709, 'potassium': 337,
                'category': 'vegetable', 'glycemic_index': 'medium'
            }
        }
        
    def get_nutrition_profile(self, food_item: str) -> Dict:
        """Get realistic nutrition profile for a food item"""
        food_key = food_item.lower().strip()
        
        # Direct match
        if food_key in self.food_profiles:
            return self.food_profiles[food_key].copy()
        
        # Partial match for variations
        for key, profile in self.food_profiles.items():
            if key in food_key or food_key in key:
                return profile.copy()
        
        # Generate reasonable estimates for unknown foods
        return self._generate_estimated_profile(food_item)
    
    def _generate_estimated_profile(self, food_item: str) -> Dict:
        """Use OpenAI to get real nutrition data for unknown foods"""
        print(f"Calling OpenAI for unknown food: {food_item}")
        
        # Call the global OpenAI function that's defined in this file
        openai_result = get_nutrition_info(food_item)
        
        # Convert the OpenAI result to match our expected format
        return {
            'calories': openai_result.get('calories', 100),
            'protein': openai_result.get('protein', 2),
            'fat': openai_result.get('fat', 1),
            'carbs': openai_result.get('carbs', 20),
            'fiber': openai_result.get('fiber', 2),
            'sugar': openai_result.get('sugar', 5),
            'category': 'unknown',
            'glycemic_index': 'medium'
        }

    def calculate_health_score(self, nutrition_profile: Dict) -> int:
        """Calculate a realistic health score based on nutrition profile"""
        score = 0
        
        # Protein scoring (more nuanced)
        protein = nutrition_profile.get('protein', 0)
        if protein >= 20: score += 25
        elif protein >= 15: score += 22
        elif protein >= 10: score += 18
        elif protein >= 5: score += 12
        elif protein >= 2: score += 8
        elif protein >= 1: score += 4
        
        # Fiber scoring (very important for health)
        fiber = nutrition_profile.get('fiber', 0)
        if fiber >= 10: score += 25
        elif fiber >= 7: score += 22
        elif fiber >= 5: score += 18
        elif fiber >= 3: score += 12
        elif fiber >= 2: score += 8
        
        # Fat content (context matters)
        fat = nutrition_profile.get('fat', 0)
        calories = nutrition_profile.get('calories', 100)
        fat_percentage = (fat * 9) / calories * 100 if calories > 0 else 0
        
        if fat_percentage <= 20: score += 20  # Very low fat
        elif fat_percentage <= 30: score += 15  # Moderate fat (healthy range)
        elif fat_percentage <= 40: score += 10  # Higher fat (could be healthy fats)
        elif fat_percentage <= 50: score += 5   # High fat
        
        # Sugar penalty (more sophisticated)
        sugar = nutrition_profile.get('sugar', 0)
        if sugar <= 2: score += 15
        elif sugar <= 5: score += 12
        elif sugar <= 10: score += 8
        elif sugar <= 15: score += 4
        elif sugar <= 25: score += 1
        
        # Calorie density consideration
        if calories <= 50: score += 10  # Very low calorie
        elif calories <= 100: score += 8   # Low calorie
        elif calories <= 200: score += 5   # Moderate calorie
        
        return min(score, 100)

# Initialize our enhanced nutrition system
nutrition_db = EnhancedNutritionDatabase()

def get_nutrition_info(food_item: str) -> Dict:
    """Get nutrition info - first check our database, then ask OpenAI"""
    
    # First, check if we have verified data for this food
    food_key = food_item.lower().strip()
    
    # Our small but accurate database
    verified_foods = {
        'banana': {'calories': 89, 'protein': 1.1, 'fat': 0.3, 'carbs': 23, 'fiber': 2.6, 'sugar': 12},
        'salmon': {'calories': 208, 'protein': 22, 'fat': 12, 'carbs': 0, 'fiber': 0, 'sugar': 0},
        'avocado': {'calories': 160, 'protein': 2.0, 'fat': 15, 'carbs': 9, 'fiber': 7, 'sugar': 0.7},
        'quinoa': {'calories': 222, 'protein': 8, 'fat': 4, 'carbs': 39, 'fiber': 5, 'sugar': 1.6},
        'spinach': {'calories': 23, 'protein': 2.9, 'fat': 0.4, 'carbs': 3.6, 'fiber': 2.2, 'sugar': 0.4},
        'blueberries': {'calories': 84, 'protein': 1.1, 'fat': 0.3, 'carbs': 21, 'fiber': 3.6, 'sugar': 15},
        'almonds': {'calories': 161, 'protein': 6, 'fat': 14, 'carbs': 6, 'fiber': 3.5, 'sugar': 1.2},
        'sweet_potato': {'calories': 86, 'protein': 1.6, 'fat': 0.1, 'carbs': 20, 'fiber': 3, 'sugar': 4.2}
    }
    
    # If we have verified data, use it
    if food_key in verified_foods:
        print(f"Using verified data for {food_item}")
        return verified_foods[food_key]
    
    # If we don't have it, and we have OpenAI, ask the AI
    if client:
        print(f"Asking OpenAI about {food_item}")
        return ask_openai_for_nutrition(food_item)
    
    # If no OpenAI, return a basic estimate
    print(f"No API available, using estimate for {food_item}")
    return {'calories': 100, 'protein': 2, 'fat': 1, 'carbs': 20, 'fiber': 2, 'sugar': 5}

def ask_openai_for_nutrition(food_item: str) -> Dict:
    """Ask OpenAI for nutrition facts and convert to our format"""
    try:
        prompt = f"""
        Give me the nutrition facts for {food_item} per standard serving.
        
        Respond with ONLY these numbers in this exact format:
        Calories: [number]
        Protein: [number]g
        Fat: [number]g
        Carbohydrates: [number]g
        Fiber: [number]g
        Sugar: [number]g
        
        Example format:
        Calories: 52
        Protein: 0.3g
        Fat: 0.2g
        Carbohydrates: 14g
        Fiber: 2.4g
        Sugar: 10g
        """
        
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a nutrition expert. Always respond with the exact format requested."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,
            max_tokens=200
        )
        
        # Get the response text
        nutrition_text = response.choices[0].message.content
        
        # Convert the text response to numbers our system can use
        return parse_openai_nutrition_response(nutrition_text)
        
    except Exception as e:
        print(f"OpenAI error for {food_item}: {e}")
        # If OpenAI fails, return a reasonable estimate
        return {'calories': 100, 'protein': 2, 'fat': 1, 'carbs': 20, 'fiber': 2, 'sugar': 5}

def parse_openai_nutrition_response(nutrition_text: str) -> Dict:
    """Convert OpenAI's text response into numbers we can use"""
    nutrition_values = {'calories': 0, 'protein': 0, 'fat': 0, 'carbs': 0, 'fiber': 0, 'sugar': 0}
    
    # Look for patterns like "Calories: 52" and extract the number
    patterns = {
        'calories': r'Calories:\s*(\d+\.?\d*)',
        'protein': r'Protein:\s*(\d+\.?\d*)',
        'fat': r'Fat:\s*(\d+\.?\d*)',
        'carbs': r'Carbohydrates:\s*(\d+\.?\d*)',
        'fiber': r'Fiber:\s*(\d+\.?\d*)',
        'sugar': r'Sugar:\s*(\d+\.?\d*)'
    }
    
    for nutrient, pattern in patterns.items():
        match = re.search(pattern, nutrition_text)
        if match:
            try:
                nutrition_values[nutrient] = float(match.group(1))
            except:
                pass  # If conversion fails, keep the default 0
    
    return nutrition_values


@app.get("/")
async def root():
    return {
        "message": "🚀 Enhanced AI Nutrition Analyzer API",
        "version": "2.0.0",
        "status": "healthy",
        "features": ["realistic_nutrition_data", "varied_health_scores", "comprehensive_analysis"]
    }

@app.get("/api/analyze/{food_item}")
async def analyze_food(food_item: str):
    try:
        if not food_item or len(food_item.strip()) < 2:
            raise HTTPException(status_code=400, detail="Please enter a valid food item")
        
        # Get realistic nutrition profile
        nutrition_profile = nutrition_db.get_nutrition_profile(food_item)
        
        # Calculate realistic health score
        health_score = nutrition_db.calculate_health_score(nutrition_profile)
        
        # Generate food-specific benefits
        benefits = []
        if nutrition_profile.get('protein', 0) >= 5:
            benefits.append("Excellent source of protein for muscle building")
        if nutrition_profile.get('fiber', 0) >= 3:
            benefits.append("High fiber content supports digestive health")
        if nutrition_profile.get('calories', 0) <= 100:
            benefits.append("Low calorie option for weight management")
        if 'omega3' in nutrition_profile:
            benefits.append("Rich in omega-3 fatty acids for brain health")
        if 'antioxidants' in nutrition_profile:
            benefits.append("High in antioxidants for cellular protection")
        
        # Ensure we have at least 2 benefits
        if len(benefits) < 2:
            benefits.extend([
                "Provides essential nutrients for overall health",
                "Can be part of a balanced, nutritious diet"
            ])
        
        # Generate meal suggestions
        meal_suggestions = [
            f"Include {food_item} in a balanced breakfast",
            f"Add {food_item} to your favorite salad",
            f"Combine {food_item} with whole grains",
            f"Use {food_item} as a healthy snack option"
        ]
        
        # Create dietary tags
        dietary_tags = []
        if nutrition_profile.get('protein', 0) >= 10:
            dietary_tags.append("High Protein")
        if nutrition_profile.get('fiber', 0) >= 5:
            dietary_tags.append("High Fiber")
        if nutrition_profile.get('calories', 0) <= 50:
            dietary_tags.append("Low Calorie")
        if nutrition_profile.get('fat', 0) <= 1:
            dietary_tags.append("Low Fat")
            
        response_data = {
            "food": food_item.lower(),
            "nutrition_info": f"Realistic nutrition data for {food_item}",
            "detailed_breakdown": {
                "calories": nutrition_profile.get('calories', 0),
                "protein": nutrition_profile.get('protein', 0),
                "fat": nutrition_profile.get('fat', 0),
                "carbs": nutrition_profile.get('carbs', 0),
                "fiber": nutrition_profile.get('fiber', 0),
                "sugar": nutrition_profile.get('sugar', 0)
            },
            "health_benefits": benefits[:4],
            "meal_suggestions": meal_suggestions,
            "health_score": health_score,
            "dietary_tags": dietary_tags,
            "calories_per_serving": nutrition_profile.get('calories', 0),
            "serving_size": "1 standard serving"
        }

        return JSONResponse(content=response_data, status_code=200)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Analysis failed for {food_item}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "database_loaded": len(nutrition_db.food_profiles),
        "openai_configured": OPENAI_API_KEY is not None
    }