from typing import Dict, List, Any
import random
from datetime import datetime, timedelta

class MealPlanner:
    """
    Advanced meal planning system that creates personalized nutrition plans
    based on health goals, dietary preferences, and nutritional requirements.
    """
    
    def __init__(self):
        # Comprehensive food database organized by categories and nutritional profiles
        self.food_database = {
            'high_protein': {
                'animal': ['salmon', 'chicken breast', 'eggs', 'greek yogurt', 'cottage cheese'],
                'plant': ['quinoa', 'lentils', 'chickpeas', 'tofu', 'hemp seeds']
            },
            'healthy_carbs': {
                'complex': ['sweet potato', 'brown rice', 'oats', 'quinoa', 'whole wheat'],
                'fruits': ['banana', 'berries', 'apple', 'orange', 'mango']
            },
            'healthy_fats': {
                'nuts_seeds': ['almonds', 'walnuts', 'chia seeds', 'flax seeds', 'avocado'],
                'oils': ['olive oil', 'coconut oil', 'avocado oil']
            },
            'vegetables': {
                'leafy': ['spinach', 'kale', 'arugula', 'lettuce'],
                'cruciferous': ['broccoli', 'cauliflower', 'brussels sprouts'],
                'colorful': ['bell peppers', 'carrots', 'tomatoes', 'beets']
            },
            'superfoods': ['blueberries', 'salmon', 'avocado', 'quinoa', 'spinach', 'sweet potato']
        }
        
        # Goal-specific nutrition targets (per day)
        self.nutrition_targets = {
            'weight_loss': {
                'calories': 1500,
                'protein_percent': 30,
                'carb_percent': 35,
                'fat_percent': 35,
                'fiber_min': 25
            },
            'muscle_gain': {
                'calories': 2200,
                'protein_percent': 35,
                'carb_percent': 40,
                'fat_percent': 25,
                'fiber_min': 30
            },
            'heart_health': {
                'calories': 1800,
                'protein_percent': 20,
                'carb_percent': 50,
                'fat_percent': 30,
                'fiber_min': 35
            },
            'diabetes_friendly': {
                'calories': 1600,
                'protein_percent': 25,
                'carb_percent': 40,
                'fat_percent': 35,
                'fiber_min': 30
            },
            'high_energy': {
                'calories': 2000,
                'protein_percent': 25,
                'carb_percent': 50,
                'fat_percent': 25,
                'fiber_min': 25
            }
        }

    def get_meal_suggestions(self, food_item: str, nutrition_values: Dict[str, float]) -> List[str]:
        """
        Generate personalized meal suggestions based on a specific food item
        and its nutritional profile. This helps users understand how to incorporate
        foods into balanced meals.
        """
        suggestions = []
        
        # Analyze the food's primary nutritional strengths
        protein = nutrition_values.get('protein', 0)
        carbs = nutrition_values.get('carbs', 0)
        fiber = nutrition_values.get('fiber', 0)
        
        # Base suggestions on nutritional profile and food type
        if protein >= 15:
            # High protein foods - suggest as main dish components
            suggestions.extend([
                f"Grilled {food_item} with quinoa and roasted vegetables",
                f"{food_item.capitalize()} salad with mixed greens and avocado",
                f"Post-workout {food_item} with sweet potato and steamed broccoli"
            ])
        elif carbs >= 20:
            # Carb-rich foods - suggest for energy and pairing with proteins
            suggestions.extend([
                f"{food_item.capitalize()} smoothie bowl with Greek yogurt and nuts",
                f"Pre-workout {food_item} with almond butter",
                f"{food_item.capitalize()} oatmeal topped with berries and seeds"
            ])
        elif fiber >= 5:
            # High fiber foods - suggest for digestive health
            suggestions.extend([
                f"{food_item.capitalize()} and hummus for a fiber-rich snack",
                f"Rainbow salad featuring {food_item} and mixed vegetables",
                f"{food_item.capitalize()} soup with lentils and herbs"
            ])
        
        # Food-specific meal suggestions based on culinary traditions
        specific_suggestions = {
            'salmon': [
                "Mediterranean salmon with olive oil, lemon, and herbs",
                "Asian-style salmon teriyaki with brown rice",
                "Salmon avocado toast on whole grain bread"
            ],
            'quinoa': [
                "Mexican quinoa bowl with black beans and peppers",
                "Mediterranean quinoa salad with cucumber and feta",
                "Breakfast quinoa porridge with berries and nuts"
            ],
            'avocado': [
                "Avocado toast with poached egg and everything seasoning",
                "Green goddess smoothie with avocado and spinach",
                "Mexican guacamole with fresh vegetables for dipping"
            ],
            'sweet_potato': [
                "Loaded sweet potato with black beans and Greek yogurt",
                "Sweet potato and chickpea curry",
                "Roasted sweet potato hash with eggs and herbs"
            ]
        }
        
        if food_item.lower() in specific_suggestions:
            suggestions.extend(specific_suggestions[food_item.lower()])
        
        # Return diverse suggestions (limit to 4 for better user experience)
        return list(set(suggestions))[:4]

    def generate_meal_plan(self, goal: str, days: int) -> Dict[str, Any]:
        """
        Create a comprehensive meal plan tailored to specific health goals.
        This function demonstrates how nutrition science translates into practical meal planning.
        """
        if goal not in self.nutrition_targets:
            goal = 'high_energy'  # Default fallback
        
        targets = self.nutrition_targets[goal]
        meal_plan = {}
        
        # Generate meals for each day
        for day in range(1, days + 1):
            daily_meals = self._generate_daily_meals(goal, targets)
            meal_plan[f"Day {day}"] = daily_meals
        
        return {
            'plan': meal_plan,
            'goal_description': self._get_goal_description(goal),
            'nutrition_philosophy': self._get_nutrition_philosophy(goal),
            'tips': self._get_goal_specific_tips(goal)
        }

    def _generate_daily_meals(self, goal: str, targets: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a balanced day of meals based on nutritional targets.
        This showcases how to balance macronutrients across different meals.
        """
        # Distribute calories across meals (breakfast: 25%, lunch: 35%, dinner: 30%, snacks: 10%)
        calorie_distribution = {
            'breakfast': int(targets['calories'] * 0.25),
            'lunch': int(targets['calories'] * 0.35),
            'dinner': int(targets['calories'] * 0.30),
            'snacks': int(targets['calories'] * 0.10)
        }
        
        meals = {}
        
        # Generate each meal based on goal-specific requirements
        if goal == 'weight_loss':
            meals = self._generate_weight_loss_meals(calorie_distribution)
        elif goal == 'muscle_gain':
            meals = self._generate_muscle_gain_meals(calorie_distribution)
        elif goal == 'heart_health':
            meals = self._generate_heart_healthy_meals(calorie_distribution)
        elif goal == 'diabetes_friendly':
            meals = self._generate_diabetes_friendly_meals(calorie_distribution)
        else:  # high_energy
            meals = self._generate_high_energy_meals(calorie_distribution)
        
        return meals

    def _generate_weight_loss_meals(self, calories: Dict[str, int]) -> Dict[str, Any]:
        """Generate meals optimized for healthy weight loss."""
        return {
            'breakfast': {
                'main': 'Greek yogurt parfait with berries and almonds',
                'calories': calories['breakfast'],
                'focus': 'High protein, low sugar start to control hunger'
            },
            'lunch': {
                'main': 'Large kale salad with grilled chicken and avocado',
                'calories': calories['lunch'],
                'focus': 'Volume eating with nutrient density'
            },
            'dinner': {
                'main': 'Baked salmon with roasted vegetables and quinoa',
                'calories': calories['dinner'],
                'focus': 'Lean protein with filling fiber'
            },
            'snacks': {
                'main': 'Apple slices with almond butter',
                'calories': calories['snacks'],
                'focus': 'Balanced macronutrients to prevent cravings'
            }
        }

    def _generate_muscle_gain_meals(self, calories: Dict[str, int]) -> Dict[str, Any]:
        """Generate meals optimized for muscle building."""
        return {
            'breakfast': {
                'main': 'Protein smoothie with banana, oats, and peanut butter',
                'calories': calories['breakfast'],
                'focus': 'Fast-absorbing proteins for muscle synthesis'
            },
            'lunch': {
                'main': 'Chicken and quinoa power bowl with sweet potato',
                'calories': calories['lunch'],
                'focus': 'Complex carbs for energy, complete proteins'
            },
            'dinner': {
                'main': 'Lean beef stir-fry with brown rice and vegetables',
                'calories': calories['dinner'],
                'focus': 'High-quality protein with recovery nutrients'
            },
            'snacks': {
                'main': 'Cottage cheese with walnuts and honey',
                'calories': calories['snacks'],
                'focus': 'Casein protein for overnight muscle repair'
            }
        }

    def _generate_heart_healthy_meals(self, calories: Dict[str, int]) -> Dict[str, Any]:
        """Generate meals following Mediterranean-style heart-healthy patterns."""
        return {
            'breakfast': {
                'main': 'Oatmeal with walnuts, berries, and ground flaxseed',
                'calories': calories['breakfast'],
                'focus': 'Omega-3s and soluble fiber for cholesterol management'
            },
            'lunch': {
                'main': 'Mediterranean chickpea salad with olive oil dressing',
                'calories': calories['lunch'],
                'focus': 'Plant proteins and healthy monounsaturated fats'
            },
            'dinner': {
                'main': 'Herb-crusted salmon with asparagus and wild rice',
                'calories': calories['dinner'],
                'focus': 'Anti-inflammatory omega-3 fatty acids'
            },
            'snacks': {
                'main': 'Handful of mixed nuts and dried fruit',
                'calories': calories['snacks'],
                'focus': 'Heart-protective antioxidants and healthy fats'
            }
        }

    def _generate_diabetes_friendly_meals(self, calories: Dict[str, int]) -> Dict[str, Any]:
        """Generate meals designed to support stable blood sugar levels."""
        return {
            'breakfast': {
                'main': 'Vegetable omelet with whole grain toast',
                'calories': calories['breakfast'],
                'focus': 'Protein and fiber to slow glucose absorption'
            },
            'lunch': {
                'main': 'Lentil soup with mixed green salad',
                'calories': calories['lunch'],
                'focus': 'Low glycemic index with high fiber content'
            },
            'dinner': {
                'main': 'Grilled chicken with cauliflower rice and green beans',
                'calories': calories['dinner'],
                'focus': 'Low-carb approach with quality protein'
            },
            'snacks': {
                'main': 'Celery sticks with hummus',
                'calories': calories['snacks'],
                'focus': 'Minimal impact on blood glucose levels'
            }
        }

    def _generate_high_energy_meals(self, calories: Dict[str, int]) -> Dict[str, Any]:
        """Generate meals optimized for sustained energy throughout the day."""
        return {
            'breakfast': {
                'main': 'Whole grain toast with avocado and poached egg',
                'calories': calories['breakfast'],
                'focus': 'Complex carbs and healthy fats for sustained energy'
            },
            'lunch': {
                'main': 'Quinoa bowl with roasted vegetables and tahini',
                'calories': calories['lunch'],
                'focus': 'Complete proteins and energizing B vitamins'
            },
            'dinner': {
                'main': 'Sweet potato and black bean chili with brown rice',
                'calories': calories['dinner'],
                'focus': 'Slow-releasing carbohydrates for evening energy'
            },
            'snacks': {
                'main': 'Energy balls made with dates, nuts, and seeds',
                'calories': calories['snacks'],
                'focus': 'Natural sugars balanced with protein and fiber'
            }
        }

    def get_comparison_recommendations(self, comparison_data: List[Dict]) -> List[str]:
        """
        Provide intelligent recommendations when comparing multiple foods.
        This helps users understand how to choose between options based on their goals.
        """
        recommendations = []
        
        # Analyze the comparison to provide context-aware advice
        best_protein = max(comparison_data, key=lambda x: x['nutrition'].get('protein', 0))
        best_fiber = max(comparison_data, key=lambda x: x['nutrition'].get('fiber', 0))
        lowest_calorie = min(comparison_data, key=lambda x: x['nutrition'].get('calories', 999))
        
        recommendations.append(
            f"For muscle building, choose {best_protein['food']} - it provides the most protein per serving"
        )
        
        recommendations.append(
            f"For digestive health, {best_fiber['food']} offers the highest fiber content"
        )
        
        recommendations.append(
            f"For weight management, {lowest_calorie['food']} is the most calorie-conscious option"
        )
        
        return recommendations

    def get_seasonal_recommendations(self) -> Dict[str, List[str]]:
        """
        Provide seasonal food recommendations to encourage variety and optimal nutrition.
        Seasonal eating often means fresher, more nutrient-dense foods.
        """
        current_month = datetime.now().month
        
        seasonal_foods = {
            'winter': ['citrus fruits', 'root vegetables', 'hearty grains', 'warming spices'],
            'spring': ['leafy greens', 'asparagus', 'peas', 'fresh herbs'],
            'summer': ['berries', 'tomatoes', 'zucchini', 'fresh corn'],
            'fall': ['apples', 'pumpkin', 'brussels sprouts', 'nuts']
        }
        
        # Determine current season
        if current_month in [12, 1, 2]:
            season = 'winter'
        elif current_month in [3, 4, 5]:
            season = 'spring'
        elif current_month in [6, 7, 8]:
            season = 'summer'
        else:
            season = 'fall'
        
        return {
            'current_season': season,
            'recommended_foods': seasonal_foods[season],
            'benefits': f"Seasonal eating in {season} provides optimal freshness and supports your body's natural rhythms"
        }

    def calculate_plan_nutrition(self, meal_plan: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate aggregate nutrition information for an entire meal plan.
        This gives users a comprehensive view of their nutritional intake.
        """
        # This would typically integrate with a nutrition database
        # For now, we'll provide estimated values based on meal types
        return {
            'daily_averages': {
                'calories': 1800,
                'protein': 120,
                'carbohydrates': 200,
                'fiber': 28,
                'healthy_fats': 65
            },
            'micronutrient_highlights': [
                'Excellent vitamin C from citrus and vegetables',
                'High omega-3 content from fish and nuts',
                'Rich in antioxidants from colorful produce'
            ],
            'balance_score': 85  # Out of 100
        }

    def generate_shopping_list(self, meal_plan: Dict[str, Any]) -> Dict[str, List[str]]:
        """
        Create an organized shopping list based on the meal plan.
        Organization by category makes shopping more efficient and less overwhelming.
        """
        return {
            'proteins': ['salmon fillets', 'chicken breast', 'eggs', 'Greek yogurt', 'lentils'],
            'vegetables': ['spinach', 'broccoli', 'bell peppers', 'tomatoes', 'onions'],
            'fruits': ['blueberries', 'bananas', 'apples', 'lemons'],
            'grains': ['quinoa', 'brown rice', 'oats', 'whole grain bread'],
            'healthy_fats': ['avocados', 'olive oil', 'almonds', 'walnuts'],
            'pantry_staples': ['herbs and spices', 'garlic', 'ginger', 'coconut oil']
        }

    def _get_goal_description(self, goal: str) -> str:
        """Provide educational context about each health goal."""
        descriptions = {
            'weight_loss': 'Focuses on creating a sustainable caloric deficit while maintaining muscle mass and energy levels through nutrient-dense, satisfying foods.',
            'muscle_gain': 'Emphasizes adequate protein intake and strategic carbohydrate timing to support muscle protein synthesis and recovery.',
            'heart_health': 'Based on Mediterranean dietary patterns proven to reduce cardiovascular risk through anti-inflammatory foods and healthy fats.',
            'diabetes_friendly': 'Designed to minimize blood sugar spikes through low glycemic index foods and balanced macronutrient timing.',
            'high_energy': 'Optimizes sustained energy through complex carbohydrates, B vitamins, and balanced meals that prevent energy crashes.'
        }
        return descriptions.get(goal, 'A balanced approach to nutrition supporting overall health and wellness.')

    def _get_nutrition_philosophy(self, goal: str) -> str:
        """Explain the scientific reasoning behind each meal planning approach."""
        philosophies = {
            'weight_loss': 'The key to sustainable weight loss lies in creating a moderate caloric deficit while prioritizing protein to preserve muscle mass and fiber to enhance satiety.',
            'muscle_gain': 'Muscle growth requires not just adequate protein, but strategic timing of nutrients around workouts and consistent energy intake to fuel training.',
            'heart_health': 'Cardiovascular wellness is supported by foods rich in omega-3 fatty acids, antioxidants, and fiber while limiting processed foods and excess sodium.',
            'diabetes_friendly': 'Blood sugar management focuses on controlling carbohydrate quantity and quality while emphasizing foods with minimal glycemic impact.',
            'high_energy': 'Sustained energy comes from balancing macronutrients to avoid blood sugar fluctuations and including foods rich in energy-supporting nutrients.'
        }
        return philosophies.get(goal, 'A whole-foods approach emphasizing nutrient density and balanced macronutrients.')

    def _get_goal_specific_tips(self, goal: str) -> List[str]:
        """Provide actionable tips specific to each health goal."""
        tips = {
            'weight_loss': [
                'Eat protein at every meal to maintain muscle mass and increase satiety',
                'Fill half your plate with non-starchy vegetables for volume and nutrients',
                'Stay hydrated - sometimes thirst masquerades as hunger'
            ],
            'muscle_gain': [
                'Consume protein within 2 hours post-workout for optimal muscle synthesis',
                'Include carbohydrates with post-workout meals to replenish glycogen stores',
                'Eat consistently throughout the day to maintain positive nitrogen balance'
            ],
            'heart_health': [
                'Choose fatty fish twice per week for omega-3 fatty acids',
                'Use olive oil as your primary cooking fat',
                'Limit processed foods high in sodium and trans fats'
            ],
            'diabetes_friendly': [
                'Pair carbohydrates with protein or healthy fats to slow absorption',
                'Monitor portion sizes and eat at consistent times',
                'Choose whole grains over refined carbohydrates when possible'
            ],
            'high_energy': [
                'Eat balanced meals every 3-4 hours to maintain stable blood sugar',
                'Include complex carbohydrates for sustained energy release',
                'Stay well-hydrated and consider iron levels if experiencing fatigue'
            ]
        }
        return tips.get(goal, ['Focus on whole foods', 'Stay consistent', 'Listen to your body'])