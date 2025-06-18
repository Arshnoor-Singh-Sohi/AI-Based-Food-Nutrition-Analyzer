import re
from typing import Dict, List, Any
import json

class NutritionCalculator:
    """
    Advanced nutrition calculation and analysis engine.
    Handles parsing, scoring, and recommendations for food items.
    """
    
    def __init__(self):
        # Nutrition databases and scoring weights
        self.scoring_weights = {
            'protein': 0.25,
            'fiber': 0.25,
            'healthy_fats': 0.20,
            'vitamins': 0.15,
            'low_sugar': 0.10,
            'low_sodium': 0.05
        }
        
        # Food categories for better analysis
        self.food_categories = {
            'fruits': ['apple', 'banana', 'orange', 'berry', 'grape', 'mango', 'pineapple'],
            'vegetables': ['spinach', 'broccoli', 'carrot', 'tomato', 'pepper', 'cucumber'],
            'grains': ['rice', 'quinoa', 'oats', 'bread', 'pasta', 'barley'],
            'proteins': ['chicken', 'fish', 'beef', 'eggs', 'beans', 'tofu', 'salmon'],
            'dairy': ['milk', 'cheese', 'yogurt', 'butter'],
            'nuts_seeds': ['almond', 'walnut', 'seed', 'peanut', 'cashew']
        }

    def parse_nutrition_text(self, nutrition_text: str) -> Dict[str, float]:
        """
        Parse AI-generated nutrition text into structured data.
        Uses advanced regex patterns to extract nutritional values.
        """
        nutrition_values = {
            'protein': 0.0,
            'fat': 0.0,
            'carbs': 0.0,
            'fiber': 0.0,
            'sugar': 0.0,
            'calories': 0.0,
            'sodium': 0.0,
            'potassium': 0.0,
            'calcium': 0.0,
            'iron': 0.0,
            'vitamin_c': 0.0,
            'vitamin_a': 0.0
        }
        
        # Comprehensive regex patterns for nutrition extraction
        patterns = {
            'protein': r'protein:?\s*(\d+\.?\d*)\s*g',
            'fat': r'(?:total\s+)?fat:?\s*(\d+\.?\d*)\s*g',
            'carbs': r'carbohydrates?:?\s*(\d+\.?\d*)\s*g',
            'fiber': r'(?:dietary\s+)?fiber:?\s*(\d+\.?\d*)\s*g',
            'sugar': r'(?:total\s+)?sugars?:?\s*(\d+\.?\d*)\s*g',
            'calories': r'calories?:?\s*(\d+\.?\d*)',
            'sodium': r'sodium:?\s*(\d+\.?\d*)\s*(?:mg|g)',
            'potassium': r'potassium:?\s*(\d+\.?\d*)\s*(?:mg|g)',
            'calcium': r'calcium:?\s*(\d+\.?\d*)\s*(?:mg|g)',
            'iron': r'iron:?\s*(\d+\.?\d*)\s*(?:mg|g)',
            'vitamin_c': r'vitamin\s+c:?\s*(\d+\.?\d*)\s*(?:mg|g)',
            'vitamin_a': r'vitamin\s+a:?\s*(\d+\.?\d*)\s*(?:iu|mcg|mg)'
        }
        
        # Extract values using regex patterns
        for nutrient, pattern in patterns.items():
            match = re.search(pattern, nutrition_text.lower())
            if match:
                try:
                    nutrition_values[nutrient] = float(match.group(1))
                except (ValueError, IndexError):
                    continue
        
        return nutrition_values

    def calculate_health_score(self, nutrition_values: Dict[str, float]) -> int:
        """
        Calculate comprehensive health score (0-100) based on nutritional profile.
        Uses weighted scoring system considering multiple health factors.
        """
        score = 0
        max_score = 100
        
        # Protein scoring (0-25 points)
        protein = nutrition_values.get('protein', 0)
        if protein >= 20: score += 25
        elif protein >= 15: score += 20
        elif protein >= 10: score += 15
        elif protein >= 5: score += 10
        elif protein >= 1: score += 5
        
        # Fiber scoring (0-25 points)
        fiber = nutrition_values.get('fiber', 0)
        if fiber >= 10: score += 25
        elif fiber >= 7: score += 20
        elif fiber >= 5: score += 15
        elif fiber >= 3: score += 10
        elif fiber >= 1: score += 5
        
        # Fat quality scoring (0-20 points)
        fat = nutrition_values.get('fat', 0)
        if fat <= 2: score += 20  # Very low fat
        elif fat <= 5: score += 15  # Low fat
        elif fat <= 10: score += 10  # Moderate fat
        elif fat <= 15: score += 5   # Higher fat (could be healthy)
        
        # Vitamin content (0-15 points)
        vitamin_c = nutrition_values.get('vitamin_c', 0)
        vitamin_a = nutrition_values.get('vitamin_a', 0)
        if vitamin_c > 50 or vitamin_a > 500: score += 15
        elif vitamin_c > 20 or vitamin_a > 200: score += 10
        elif vitamin_c > 5 or vitamin_a > 50: score += 5
        
        # Sugar penalty (0-10 points)
        sugar = nutrition_values.get('sugar', 0)
        if sugar <= 5: score += 10
        elif sugar <= 10: score += 7
        elif sugar <= 15: score += 5
        elif sugar <= 25: score += 2
        
        # Sodium consideration (0-5 points)
        sodium = nutrition_values.get('sodium', 0)
        if sodium <= 100: score += 5
        elif sodium <= 300: score += 3
        elif sodium <= 600: score += 1
        
        return min(score, max_score)

    def get_health_benefits(self, food_item: str, nutrition_values: Dict[str, float]) -> List[str]:
        """
        Generate personalized health benefits based on nutritional profile.
        Uses food-specific knowledge and nutrient analysis.
        """
        benefits = []
        
        # Protein benefits
        if nutrition_values.get('protein', 0) >= 5:
            benefits.append("Excellent source of protein for muscle building and repair")
        
        # Fiber benefits
        if nutrition_values.get('fiber', 0) >= 3:
            benefits.append("High fiber content supports digestive health")
        
        # Vitamin C benefits
        if nutrition_values.get('vitamin_c', 0) >= 10:
            benefits.append("Rich in vitamin C for immune system support")
        
        # Potassium benefits
        if nutrition_values.get('potassium', 0) >= 200:
            benefits.append("Good source of potassium for heart health")
        
        # Low calorie benefits
        if nutrition_values.get('calories', 0) <= 100:
            benefits.append("Low calorie option for weight management")
        
        # Food-specific benefits
        food_benefits = {
            'banana': ["Natural energy boost from healthy carbohydrates", "Contains tryptophan for mood regulation"],
            'salmon': ["Rich in omega-3 fatty acids for brain health", "Anti-inflammatory properties"],
            'spinach': ["High in folate for cell division", "Contains lutein for eye health"],
            'blueberries': ["Packed with antioxidants for anti-aging", "May improve memory and cognitive function"],
            'avocado': ["Healthy monounsaturated fats for heart health", "Helps nutrient absorption"],
            'quinoa': ["Complete protein with all essential amino acids", "Gluten-free grain alternative"],
            'sweet_potato': ["Beta-carotene for eye and skin health", "Complex carbohydrates for sustained energy"]
        }
        
        if food_item.lower() in food_benefits:
            benefits.extend(food_benefits[food_item.lower()])
        
        return benefits[:4]  # Return top 4 benefits

    def get_dietary_tags(self, food_item: str, nutrition_values: Dict[str, float]) -> List[str]:
        """
        Generate dietary restriction and lifestyle tags for foods.
        """
        tags = []
        
        # Basic dietary tags
        if nutrition_values.get('protein', 0) >= 10:
            tags.append("High Protein")
        
        if nutrition_values.get('fiber', 0) >= 5:
            tags.append("High Fiber")
        
        if nutrition_values.get('calories', 0) <= 50:
            tags.append("Low Calorie")
        
        if nutrition_values.get('fat', 0) <= 1:
            tags.append("Low Fat")
        
        if nutrition_values.get('sugar', 0) <= 5:
            tags.append("Low Sugar")
        
        # Food-specific tags
        plant_foods = ['banana', 'apple', 'spinach', 'quinoa', 'avocado', 'blueberry', 'sweet_potato']
        if any(plant in food_item.lower() for plant in plant_foods):
            tags.extend(["Vegan", "Vegetarian", "Plant-Based"])
        
        gluten_free_foods = ['quinoa', 'rice', 'potato', 'banana', 'apple', 'salmon']
        if any(gf_food in food_item.lower() for gf_food in gluten_free_foods):
            tags.append("Gluten-Free")
        
        keto_friendly = ['avocado', 'salmon', 'eggs', 'nuts']
        if any(keto in food_item.lower() for keto in keto_friendly):
            tags.append("Keto-Friendly")
        
        return tags

    def get_detailed_score_breakdown(self, nutrition_values: Dict[str, float]) -> Dict[str, Any]:
        """
        Provide detailed breakdown of health score calculation.
        """
        breakdown = {
            'protein_score': min(25, max(0, nutrition_values.get('protein', 0) * 2.5)),
            'fiber_score': min(25, max(0, nutrition_values.get('fiber', 0) * 2.5)),
            'fat_score': self._calculate_fat_score(nutrition_values.get('fat', 0)),
            'vitamin_score': self._calculate_vitamin_score(nutrition_values),
            'sugar_penalty': self._calculate_sugar_penalty(nutrition_values.get('sugar', 0)),
            'sodium_score': self._calculate_sodium_score(nutrition_values.get('sodium', 0))
        }
        
        breakdown['total_score'] = sum(breakdown.values())
        return breakdown

    def _calculate_fat_score(self, fat: float) -> float:
        """Calculate fat score component."""
        if fat <= 2: return 20
        elif fat <= 5: return 15
        elif fat <= 10: return 10
        elif fat <= 15: return 5
        return 0

    def _calculate_vitamin_score(self, nutrition_values: Dict[str, float]) -> float:
        """Calculate vitamin score component."""
        vitamin_c = nutrition_values.get('vitamin_c', 0)
        vitamin_a = nutrition_values.get('vitamin_a', 0)
        
        if vitamin_c > 50 or vitamin_a > 500: return 15
        elif vitamin_c > 20 or vitamin_a > 200: return 10
        elif vitamin_c > 5 or vitamin_a > 50: return 5
        return 0

    def _calculate_sugar_penalty(self, sugar: float) -> float:
        """Calculate sugar penalty (negative scoring)."""
        if sugar <= 5: return 10
        elif sugar <= 10: return 7
        elif sugar <= 15: return 5
        elif sugar <= 25: return 2
        return 0

    def _calculate_sodium_score(self, sodium: float) -> float:
        """Calculate sodium score component."""
        if sodium <= 100: return 5
        elif sodium <= 300: return 3
        elif sodium <= 600: return 1
        return 0

    def compare_foods_analysis(self, comparison_data: List[Dict]) -> Dict[str, Any]:
        """
        Analyze multiple foods and determine winners in each category.
        """
        analysis = {
            'highest_protein': max(comparison_data, key=lambda x: x['nutrition'].get('protein', 0)),
            'highest_fiber': max(comparison_data, key=lambda x: x['nutrition'].get('fiber', 0)),
            'lowest_calories': min(comparison_data, key=lambda x: x['nutrition'].get('calories', 999)),
            'best_overall': max(comparison_data, key=lambda x: x['health_score']),
            'category_winners': {},
            'recommendations': []
        }
        
        # Add contextual recommendations
        if analysis['best_overall']['health_score'] >= 80:
            analysis['recommendations'].append(f"{analysis['best_overall']['food']} is an excellent choice overall")
        
        return analysis

    def get_related_topics(self, question: str) -> List[str]:
        """Generate related nutrition topics based on question."""
        topics = {
            'protein': ['muscle building', 'amino acids', 'complete proteins'],
            'weight': ['calorie deficit', 'metabolism', 'portion control'],
            'diabetes': ['glycemic index', 'blood sugar', 'carb counting'],
            'heart': ['omega-3', 'cholesterol', 'sodium intake'],
            'energy': ['complex carbs', 'B vitamins', 'iron levels']
        }
        
        related = []
        for keyword, topic_list in topics.items():
            if keyword in question.lower():
                related.extend(topic_list)
        
        return related[:3]

    def suggest_foods_for_question(self, question: str) -> List[str]:
        """Suggest relevant foods based on nutrition question."""
        suggestions = {
            'protein': ['salmon', 'quinoa', 'eggs', 'lentils'],
            'fiber': ['oats', 'apples', 'broccoli', 'chia seeds'],
            'energy': ['bananas', 'sweet potato', 'oats', 'dates'],
            'weight loss': ['spinach', 'cucumber', 'berries', 'lean protein'],
            'heart health': ['salmon', 'avocado', 'nuts', 'olive oil']
        }
        
        for keyword, foods in suggestions.items():
            if keyword in question.lower():
                return foods
        
        return ['salmon', 'quinoa', 'spinach', 'blueberries']  # Default suggestions

    def get_improvement_suggestions(self, nutrition_values: Dict[str, float]) -> List[str]:
        """Provide suggestions for improving nutritional profile."""
        suggestions = []
        
        if nutrition_values.get('fiber', 0) < 3:
            suggestions.append("Add more fiber-rich foods like beans, vegetables, or whole grains")
        
        if nutrition_values.get('protein', 0) < 5:
            suggestions.append("Include more protein sources like lean meats, fish, or legumes")
        
        if nutrition_values.get('sugar', 0) > 15:
            suggestions.append("Consider reducing sugar content or pairing with fiber-rich foods")
        
        if nutrition_values.get('sodium', 0) > 600:
            suggestions.append("Look for lower sodium alternatives to support heart health")
        
        return suggestions