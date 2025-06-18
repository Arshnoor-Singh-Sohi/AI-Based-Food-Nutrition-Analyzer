import React, { useState } from 'react';
import { Search, Sparkles, Heart, Zap, Shield, ChefHat, BarChart3, Utensils, Loader2, AlertCircle } from 'lucide-react';

const NutritionAnalyzer = () => {
    // State management - these are like the app's memory
    const [foodItem, setFoodItem] = useState(''); // What food the user typed
    const [loading, setLoading] = useState(false); // Is the AI thinking?
    const [nutritionData, setNutritionData] = useState(null); // The analysis results
    const [error, setError] = useState(''); // Any error messages
    const [darkMode, setDarkMode] = useState(false); // Light or dark theme

    // Function to analyze food using our AI backend
    const analyzeFood = async () => {
        // Basic validation - make sure user entered something
        if (!foodItem.trim()) {
            setError('Please enter a food item');
            return;
        }

        setLoading(true); // Show loading spinner
        setError(''); // Clear any previous errors

        try {
            // Call our backend API to analyze the food
            const response = await fetch(`/api/analyze/${encodeURIComponent(foodItem.trim())}`);

            // Check if the request was successful
            if (!response.ok) {
                throw new Error(`Failed to analyze ${foodItem}. Please try again.`);
            }

            // Get the JSON data from the response
            const data = await response.json();

            // Validate that we got the expected data structure
            if (!data || !data.detailed_breakdown) {
                throw new Error('Invalid response from server');
            }

            // Store the results in our state
            setNutritionData(data);

        } catch (err) {
            console.error('Analysis error:', err);
            setError(err.message || 'Failed to analyze food. Please try again.');
        } finally {
            setLoading(false); // Hide loading spinner
        }
    };

    // Helper functions for displaying health scores with colors
    const getScoreColor = (score) => {
        if (score >= 80) return 'text-green-500';
        if (score >= 60) return 'text-yellow-500';
        if (score >= 40) return 'text-orange-500';
        return 'text-red-500';
    };

    const getScoreEmoji = (score) => {
        if (score >= 80) return '🟢';
        if (score >= 60) return '🟡';
        if (score >= 40) return '🟠';
        return '🔴';
    };

    const getScoreDescription = (score) => {
        if (score >= 80) return 'Excellent Choice';
        if (score >= 60) return 'Good Option';
        if (score >= 40) return 'Fair Choice';
        return 'Consider Alternatives';
    };

    // Quick food suggestions for users to try
    const quickSuggestions = [
        'Banana', 'Avocado', 'Quinoa', 'Salmon',
        'Spinach', 'Blueberries', 'Almonds', 'Sweet Potato'
    ];

    const handleQuickAnalysis = async (food) => {
        // Clear any previous errors first
        setError('');

        // Set the food item in the input field so users can see what was selected
        setFoodItem(food.toLowerCase());

        // Immediately trigger the analysis without waiting
        // This creates a smooth, immediate response
        setLoading(true);

        try {
            // Call our backend API to analyze the selected food
            const response = await fetch(`http://localhost:8000/api/analyze/${encodeURIComponent(food.trim())}`);

            if (!response.ok) {
                throw new Error(`Failed to analyze ${food}. Please try again.`);
            }

            const data = await response.json();

            if (!data || !data.detailed_breakdown) {
                throw new Error('Invalid response from server');
            }

            setNutritionData(data);

        } catch (err) {
            console.error('Analysis error:', err);
            setError(err.message || 'Failed to analyze food. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className={`min-h-screen transition-all duration-500 ${darkMode
            ? 'bg-gradient-to-br from-gray-900 via-purple-900 to-violet-900'
            : 'bg-gradient-to-br from-blue-50 via-indigo-100 to-purple-100'
            }`}>
            {/* Animated Background Elements - these create the floating blob effect */}
            <div className="fixed inset-0 overflow-hidden pointer-events-none">
                <div className={`absolute -top-4 -right-4 w-72 h-72 ${darkMode ? 'bg-purple-500' : 'bg-blue-300'} rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob`}></div>
                <div className={`absolute -bottom-8 -left-4 w-72 h-72 ${darkMode ? 'bg-yellow-500' : 'bg-purple-300'} rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob animation-delay-2000`}></div>
                <div className={`absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-72 h-72 ${darkMode ? 'bg-pink-500' : 'bg-yellow-300'} rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob animation-delay-4000`}></div>
            </div>

            {/* Main Content Container */}
            <div className="relative z-10 container mx-auto px-4 py-8">
                {/* Header Section */}
                {/* Enhanced Header Section with Better Mobile Support */}
                <div className="text-center mb-8 md:mb-12 px-4">
                    <div className="flex flex-col sm:flex-row justify-center items-center gap-2 sm:gap-3 mb-4">
                        <div className="p-2 sm:p-3 bg-gradient-to-r from-green-400 to-blue-500 rounded-full">
                            <Sparkles className="w-6 h-6 sm:w-8 sm:h-8 text-white" />
                        </div>
                        <h1 className={`text-2xl sm:text-4xl md:text-5xl lg:text-6xl font-bold bg-gradient-to-r from-green-400 via-blue-500 to-purple-600 bg-clip-text text-transparent text-center`}>
                            AI Nutrition Analyzer
                        </h1>
                    </div>
                    <p className={`text-base sm:text-lg md:text-xl ${darkMode ? 'text-gray-300' : 'text-gray-600'} max-w-2xl mx-auto mb-4 px-4`}>
                        Discover the nutritional power of your food with AI-driven insights and personalized recommendations
                    </p>

                    {/* Dark Mode Toggle Button - Better Mobile Positioning */}
                    <button
                        onClick={() => setDarkMode(!darkMode)}
                        className={`mt-3 sm:mt-4 px-3 sm:px-4 py-2 rounded-full text-sm sm:text-base ${darkMode ? 'bg-yellow-500 text-gray-900' : 'bg-gray-800 text-white'
                            } transition-all duration-300 hover:scale-105 active:scale-95`}
                    >
                        {darkMode ? '☀️ Light Mode' : '🌙 Dark Mode'}
                    </button>
                </div>

                {/* Search Section - where users enter food items */}
                {/* Enhanced Search Section with Better Mobile Layout */}
                <div className={`max-w-2xl mx-auto mb-8 md:mb-12 backdrop-blur-sm ${darkMode ? 'bg-white/10' : 'bg-white/70'
                    } rounded-2xl sm:rounded-3xl p-4 sm:p-6 md:p-8 shadow-2xl border ${darkMode ? 'border-white/20' : 'border-white/50'} mx-4`}>
                    <div className="flex flex-col gap-3 sm:gap-4">
                        <div className="relative">
                            <input
                                type="text"
                                value={foodItem}
                                onChange={(e) => setFoodItem(e.target.value)}
                                placeholder="Enter any food item..."
                                className={`w-full px-4 sm:px-6 py-3 sm:py-4 rounded-xl sm:rounded-2xl text-base sm:text-lg ${darkMode
                                        ? 'bg-gray-800/50 text-white placeholder-gray-400'
                                        : 'bg-white/80 text-gray-900 placeholder-gray-500'
                                    } border-2 border-transparent focus:border-blue-500 focus:outline-none transition-all duration-300`}
                                onKeyPress={(e) => e.key === 'Enter' && !loading && analyzeFood()}
                                disabled={loading}
                            />
                            <Search className={`absolute right-3 sm:right-4 top-1/2 transform -translate-y-1/2 w-5 h-5 sm:w-6 sm:h-6 ${darkMode ? 'text-gray-400' : 'text-gray-500'
                                }`} />
                        </div>
                        <button
                            onClick={analyzeFood}
                            disabled={loading}
                            className="w-full px-6 sm:px-8 py-3 sm:py-4 bg-gradient-to-r from-green-500 to-blue-600 text-white rounded-xl sm:rounded-2xl font-semibold text-base sm:text-lg hover:from-green-600 hover:to-blue-700 focus:outline-none focus:ring-4 focus:ring-blue-300 transition-all duration-300 transform hover:scale-105 active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
                        >
                            {loading ? (
                                <div className="flex items-center justify-center gap-2">
                                    <Loader2 className="w-5 h-5 animate-spin" />
                                    <span className="hidden sm:inline">Analyzing...</span>
                                    <span className="sm:hidden">Loading...</span>
                                </div>
                            ) : (
                                <div className="flex items-center justify-center gap-2">
                                    <Zap className="w-5 h-5" />
                                    Analyze
                                </div>
                            )}
                        </button>
                    </div>

                    {/* Error Message Display */}
                    {error && (
                        <div className="mt-4 p-4 bg-red-500/20 border border-red-500/30 rounded-xl text-red-400 flex items-center gap-2">
                            <AlertCircle className="w-5 h-5 flex-shrink-0" />
                            {error}
                        </div>
                    )}
                </div>

                {/* Results Section - shows when we have nutrition data */}
                {nutritionData && (
                    <div className="max-w-7xl mx-auto space-y-8">
                        {/* Health Score Display */}
                        <div className={`backdrop-blur-sm ${darkMode ? 'bg-white/10' : 'bg-white/70'
                            } rounded-3xl p-8 shadow-2xl border ${darkMode ? 'border-white/20' : 'border-white/50'}`}>
                            <div className="text-center">
                                <h3 className={`text-2xl font-bold mb-4 ${darkMode ? 'text-white' : 'text-gray-800'}`}>
                                    Health Score for {nutritionData.food.charAt(0).toUpperCase() + nutritionData.food.slice(1)}
                                </h3>
                                <div className="flex justify-center items-center gap-4 mb-6">
                                    <div className={`text-6xl font-bold ${getScoreColor(nutritionData.health_score)}`}>
                                        {nutritionData.health_score}
                                    </div>
                                    <div className="text-4xl">
                                        {getScoreEmoji(nutritionData.health_score)}
                                    </div>
                                </div>
                                <div className={`text-xl font-semibold mb-4 ${getScoreColor(nutritionData.health_score)}`}>
                                    {getScoreDescription(nutritionData.health_score)}
                                </div>
                                <div className="w-full bg-gray-200 rounded-full h-4 mb-4">
                                    <div
                                        className={`h-4 rounded-full transition-all duration-1000 ${nutritionData.health_score >= 80 ? 'bg-green-500' :
                                            nutritionData.health_score >= 60 ? 'bg-yellow-500' :
                                                nutritionData.health_score >= 40 ? 'bg-orange-500' : 'bg-red-500'
                                            }`}
                                        style={{ width: `${nutritionData.health_score}%` }}
                                    ></div>
                                </div>
                            </div>
                        </div>

                        {/* Nutrition Breakdown Table */}
                        <div className={`backdrop-blur-sm ${darkMode ? 'bg-white/10' : 'bg-white/70'
                            } rounded-3xl p-8 shadow-2xl border ${darkMode ? 'border-white/20' : 'border-white/50'}`}>
                            <h3 className={`text-2xl font-bold mb-6 flex items-center gap-2 ${darkMode ? 'text-white' : 'text-gray-800'}`}>
                                <BarChart3 className="w-6 h-6" />
                                Nutritional Breakdown
                            </h3>
                            <div className="overflow-x-auto">
                                <table className="w-full">
                                    <thead>
                                        <tr className={`${darkMode ? 'border-gray-600' : 'border-gray-300'} border-b-2`}>
                                            <th className={`text-left py-4 px-4 font-semibold ${darkMode ? 'text-gray-200' : 'text-gray-700'}`}>Nutrient</th>
                                            <th className={`text-left py-4 px-4 font-semibold ${darkMode ? 'text-gray-200' : 'text-gray-700'}`}>Amount</th>
                                            <th className={`text-left py-4 px-4 font-semibold ${darkMode ? 'text-gray-200' : 'text-gray-700'}`}>Status</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {[
                                            { name: 'Calories', value: nutritionData.detailed_breakdown.calories, unit: 'kcal' },
                                            { name: 'Protein', value: nutritionData.detailed_breakdown.protein, unit: 'g' },
                                            { name: 'Carbohydrates', value: nutritionData.detailed_breakdown.carbs, unit: 'g' },
                                            { name: 'Fiber', value: nutritionData.detailed_breakdown.fiber, unit: 'g' },
                                            { name: 'Fat', value: nutritionData.detailed_breakdown.fat, unit: 'g' },
                                            { name: 'Sugar', value: nutritionData.detailed_breakdown.sugar, unit: 'g' }
                                        ].map((nutrient, index) => (
                                            <tr key={index} className={`${darkMode ? 'border-gray-700 hover:bg-white/5' : 'border-gray-200 hover:bg-gray-50'} border-b transition-colors`}>
                                                <td className={`py-4 px-4 font-medium ${darkMode ? 'text-gray-300' : 'text-gray-700'}`}>{nutrient.name}</td>
                                                <td className={`py-4 px-4 ${darkMode ? 'text-gray-300' : 'text-gray-700'}`}>{nutrient.value}{nutrient.unit}</td>
                                                <td className="py-4 px-4">
                                                    <span className={`px-3 py-1 rounded-full text-sm font-medium ${nutrient.value > 10 ? 'bg-green-100 text-green-800' :
                                                        nutrient.value > 5 ? 'bg-yellow-100 text-yellow-800' :
                                                            'bg-blue-100 text-blue-800'
                                                        }`}>
                                                        {nutrient.value > 10 ? 'High' : nutrient.value > 5 ? 'Good' : 'Low'}
                                                    </span>
                                                </td>
                                            </tr>
                                        ))}
                                    </tbody>
                                </table>
                            </div>
                        </div>

                        {/* Health Benefits Section */}
                        <div className={`backdrop-blur-sm ${darkMode ? 'bg-white/10' : 'bg-white/70'
                            } rounded-3xl p-8 shadow-2xl border ${darkMode ? 'border-white/20' : 'border-white/50'}`}>
                            <h3 className={`text-2xl font-bold mb-6 flex items-center gap-2 ${darkMode ? 'text-white' : 'text-gray-800'}`}>
                                <Heart className="w-6 h-6 text-red-500" />
                                Health Benefits
                            </h3>
                            <div className="grid md:grid-cols-2 gap-4">
                                {nutritionData.health_benefits?.map((benefit, index) => (
                                    <div key={index} className={`p-4 rounded-xl ${darkMode ? 'bg-green-500/20 border border-green-500/30' : 'bg-green-50 border border-green-200'
                                        } flex items-center gap-3`}>
                                        <Shield className="w-5 h-5 text-green-500 flex-shrink-0" />
                                        <span className={`${darkMode ? 'text-green-300' : 'text-green-700'} font-medium`}>{benefit}</span>
                                    </div>
                                ))}
                            </div>
                        </div>

                        {/* Meal Suggestions Section */}
                        <div className={`backdrop-blur-sm ${darkMode ? 'bg-white/10' : 'bg-white/70'
                            } rounded-3xl p-8 shadow-2xl border ${darkMode ? 'border-white/20' : 'border-white/50'}`}>
                            <h3 className={`text-2xl font-bold mb-6 flex items-center gap-2 ${darkMode ? 'text-white' : 'text-gray-800'}`}>
                                <ChefHat className="w-6 h-6 text-orange-500" />
                                Meal Ideas & Pairings
                            </h3>
                            <div className="grid md:grid-cols-2 gap-4">
                                {nutritionData.meal_suggestions?.map((suggestion, index) => (
                                    <div key={index} className={`p-4 rounded-xl ${darkMode ? 'bg-orange-500/20 border border-orange-500/30' : 'bg-orange-50 border border-orange-200'
                                        } flex items-center gap-3 hover:scale-105 transition-transform cursor-pointer`}>
                                        <Utensils className="w-5 h-5 text-orange-500 flex-shrink-0" />
                                        <span className={`${darkMode ? 'text-orange-300' : 'text-orange-700'} font-medium`}>{suggestion}</span>
                                    </div>
                                ))}
                            </div>
                        </div>
                    </div>
                )}

                {/* Quick Suggestions - shows when no results are displayed */}
                {!nutritionData && (
                    <div className={`max-w-4xl mx-auto backdrop-blur-sm ${darkMode ? 'bg-white/10' : 'bg-white/70'
                        } rounded-3xl p-8 shadow-2xl border ${darkMode ? 'border-white/20' : 'border-white/50'}`}>
                        <h3 className={`text-2xl font-bold mb-6 text-center ${darkMode ? 'text-white' : 'text-gray-800'}`}>
                            ✨ Try These Popular Foods
                        </h3>
                        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                            {quickSuggestions.map((food) => (
                                <button
                                    key={food}
                                    onClick={() => handleQuickAnalysis(food)}
                                    disabled={loading}
                                    className={`p-4 rounded-xl ${darkMode ? 'bg-gradient-to-r from-purple-500/20 to-pink-500/20 hover:from-purple-500/30 hover:to-pink-500/30' : 'bg-gradient-to-r from-blue-100 to-purple-100 hover:from-blue-200 hover:to-purple-200'
                                        } transition-all duration-300 hover:scale-105 border ${darkMode ? 'border-white/20' : 'border-white/50'} disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none`}
                                >
                                    <div className="text-2xl mb-2">
                                        {food === 'Banana' ? '🍌' :
                                            food === 'Avocado' ? '🥑' :
                                                food === 'Quinoa' ? '🌾' :
                                                    food === 'Salmon' ? '🐟' :
                                                        food === 'Spinach' ? '🥬' :
                                                            food === 'Blueberries' ? '🫐' :
                                                                food === 'Almonds' ? '🌰' : '🍠'}
                                    </div>
                                    <div className={`font-medium ${darkMode ? 'text-white' : 'text-gray-700'}`}>{food}</div>
                                </button>
                            ))}
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};

export default NutritionAnalyzer;