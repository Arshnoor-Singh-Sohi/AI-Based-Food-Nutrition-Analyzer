import os
import openai
from dotenv import load_dotenv
from loguru import logger
from typing import Dict, Any, Optional
import json
import re

# Load environment variables - this is crucial for deployment
load_dotenv()

# Get API key from environment variables
api_key = os.getenv("OPENAI_API_KEY")

# Configure logging for production
logger.add("logs/app.log", rotation="10 MB", level="DEBUG")

def get_nutrition_info(food_item: str) -> str:
    """
    Enhanced nutrition information retrieval using OpenAI's GPT-4.
    Now includes more detailed prompting for better, more structured responses.
    """
    try:
        # Validate API key first
        if not api_key:
            logger.error("OpenAI API key not found in environment variables")
            return None
            
        client = openai.OpenAI(api_key=api_key)
        
        # Enhanced prompt for more detailed and structured nutrition information
        enhanced_prompt = f"""
        As a professional nutritionist and food scientist, provide comprehensive nutritional information for {food_item}.
        
        Please include the following details in your response:
        1. Macronutrients (protein, carbohydrates, fat, fiber) in grams per standard serving
        2. Micronutrients (vitamins and minerals) with amounts
        3. Calories per serving
        4. Key health benefits and bioactive compounds
        5. Any potential allergens or considerations
        
        Format your response to include specific numerical values where possible.
        Use standard serving sizes (e.g., 1 medium banana, 1 cup cooked quinoa, 3 oz salmon).
        
        Food item: {food_item}
        """
        
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system", 
                    "content": """You are a world-renowned nutritionist and food scientist with expertise in 
                    nutritional analysis, biochemistry, and public health nutrition. You provide precise, 
                    evidence-based nutritional information that helps people make informed dietary choices. 
                    Your responses are detailed yet accessible, always including specific numerical values 
                    and serving sizes."""
                },
                {
                    "role": "user", 
                    "content": enhanced_prompt
                }
            ],
            temperature=0.3,  # Lower temperature for more consistent, factual responses
            max_tokens=1000   # Increased token limit for comprehensive responses
        )
        
        nutrition_data = response.choices[0].message.content
        logger.info(f"Successfully retrieved enhanced nutritional information for {food_item}")
        return nutrition_data
        
    except openai.OpenAIError as e:
        logger.error(f"OpenAI API error for {food_item}: {str(e)}")
        return f"Error retrieving nutritional information: {str(e)}"
    except Exception as e:
        logger.error(f"Unexpected error retrieving nutritional information for {food_item}: {str(e)}")
        return None

def get_enhanced_nutrition_analysis(food_item: str, raw_nutrition: str) -> Dict[str, Any]:
    """
    Provide enhanced analysis including serving size estimation and additional insights.
    This function adds value beyond the basic OpenAI response.
    """
    try:
        client = openai.OpenAI(api_key=api_key)
        
        analysis_prompt = f"""
        Based on this nutritional information for {food_item}:
        {raw_nutrition}
        
        Please provide:
        1. Standard serving size (e.g., "1 medium fruit", "1 cup cooked", "3 oz")
        2. Glycemic index category (low/medium/high)
        3. Primary nutritional category (protein source/complex carb/healthy fat/superfood/etc.)
        4. Best meal timing (breakfast/lunch/dinner/snack/pre-workout/post-workout)
        5. Complementary foods that pair well nutritionally
        
        Respond in JSON format.
        """
        
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a nutrition analysis expert. Respond with valid JSON only."},
                {"role": "user", "content": analysis_prompt}
            ],
            temperature=0.2
        )
        
        # Parse the JSON response
        try:
            analysis_data = json.loads(response.choices[0].message.content)
            return analysis_data
        except json.JSONDecodeError:
            # Fallback if JSON parsing fails
            return {
                "serving_size": "1 serving",
                "glycemic_index": "medium",
                "category": "whole food",
                "meal_timing": "any time",
                "complementary_foods": ["balanced meal components"]
            }
            
    except Exception as e:
        logger.error(f"Error in enhanced analysis for {food_item}: {str(e)}")
        return {
            "serving_size": "1 serving",
            "glycemic_index": "unknown",
            "category": "whole food",
            "meal_timing": "any time",
            "complementary_foods": ["healthy foods"]
        }

def query_nutrition_knowledge(question: str) -> str:
    """
    Enhanced nutrition knowledge query system that can answer complex nutrition questions.
    This replaces the LlamaIndex implementation with a more robust OpenAI-based system.
    """
    try:
        if not api_key:
            return "OpenAI API key not configured. Please check your environment variables."
            
        client = openai.OpenAI(api_key=api_key)
        
        # Enhanced system prompt for nutrition expertise
        system_prompt = """
        You are Dr. Nutrition, a world-class nutritionist, dietitian, and food scientist with over 20 years of experience. 
        You have:
        - PhD in Nutritional Sciences
        - Board certification in clinical nutrition
        - Expertise in sports nutrition, clinical nutrition, and public health
        - Deep knowledge of biochemistry, metabolism, and nutrient interactions
        - Experience with diverse dietary patterns and cultural foods
        
        Your responses should be:
        - Evidence-based and scientifically accurate
        - Practical and actionable
        - Accessible to general audiences while maintaining scientific rigor
        - Inclusive of different dietary preferences and restrictions
        - Updated with current nutrition research and guidelines
        
        When uncertain about specific claims, acknowledge limitations and suggest consulting healthcare providers when appropriate.
        """
        
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Nutrition question: {question}"}
            ],
            temperature=0.4,
            max_tokens=800
        )
        
        answer = response.choices[0].message.content
        logger.info(f"Successfully answered nutrition question: {question[:50]}...")
        return answer
        
    except Exception as e:
        logger.error(f"Error answering nutrition question '{question}': {str(e)}")
        return f"I'm sorry, I encountered an error while processing your question. Please try rephrasing or ask a different nutrition question."

def get_food_safety_info(food_item: str) -> Dict[str, Any]:
    """
    New function to provide food safety and storage information.
    This adds practical value for users beyond just nutrition.
    """
    try:
        client = openai.OpenAI(api_key=api_key)
        
        safety_prompt = f"""
        Provide food safety and storage information for {food_item}:
        1. Proper storage methods (refrigerator, freezer, pantry)
        2. Shelf life and signs of spoilage
        3. Food safety considerations
        4. Preparation tips for maximum nutrition retention
        5. Any special handling requirements
        
        Be practical and specific.
        """
        
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a food safety expert providing practical storage and safety advice."},
                {"role": "user", "content": safety_prompt}
            ],
            temperature=0.3
        )
        
        return {
            "food": food_item,
            "safety_info": response.choices[0].message.content
        }
        
    except Exception as e:
        logger.error(f"Error getting food safety info for {food_item}: {str(e)}")
        return {
            "food": food_item,
            "safety_info": "Please follow general food safety guidelines for storage and preparation."
        }

def validate_food_input(food_item: str) -> bool:
    """
    Validate that the input appears to be a food item.
    This helps prevent API abuse and improves user experience.
    """
    if not food_item or len(food_item.strip()) < 2:
        return False
    
    # Check for obviously non-food inputs
    non_food_patterns = [
        r'\b(computer|phone|car|house|money)\b',
        r'[0-9]{5,}',  # Long numbers
        r'[!@#$%^&*()+={}[\]|\\:";\'<>?,./]{3,}',  # Multiple special characters
    ]
    
    for pattern in non_food_patterns:
        if re.search(pattern, food_item.lower()):
            return False
    
    return True

# Health check function for deployment
def health_check() -> Dict[str, str]:
    """
    Simple health check to verify the AI model service is working.
    Essential for production monitoring.
    """
    try:
        if not api_key:
            return {"status": "unhealthy", "reason": "OpenAI API key not configured"}
        
        # Test a simple API call
        client = openai.OpenAI(api_key=api_key)
        test_response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": "Say 'OK' if you're working"}],
            max_tokens=5
        )
        
        if test_response.choices[0].message.content:
            return {"status": "healthy", "timestamp": str(logger._core.now())}
        else:
            return {"status": "unhealthy", "reason": "API not responding correctly"}
            
    except Exception as e:
        return {"status": "unhealthy", "reason": f"Health check failed: {str(e)}"}

# For backward compatibility with existing code
def build_food_index(data_path: str = "data"):
    """
    Placeholder function for backward compatibility.
    In the enhanced version, we rely on OpenAI's knowledge instead of local indexing.
    """
    logger.info("Using OpenAI-based knowledge instead of local indexing")
    return True  # Always return success since we're using OpenAI