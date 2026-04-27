import pandas as pd


def load_data():
    """Load dishes dataset"""
    return pd.read_csv("dishes.csv")


def recommend_dishes(yesterday, meal_type, quick_meal, healthy_meal):
    """AI-Powered Smart Cooking Assistant"""

    df = load_data()
    recommendations = df.copy()

    # Avoid exact same dish from yesterday
    if yesterday:
        recommendations = recommendations[
            recommendations["Dish_Name"].str.lower() != yesterday.lower()
        ]

    # Match meal type if column exists
    if "Meal_Type" in recommendations.columns:
        recommendations = recommendations[
            recommendations["Meal_Type"].str.lower() == meal_type.lower()
        ]

    # Quick meal filter
    if quick_meal.lower() == "yes":
        recommendations = recommendations[
            recommendations["Cook_Time"] <= 30
        ]

    # Healthy / light meal filter
    if healthy_meal.lower() == "yes":
        healthy_keywords = [
            "Khichdi",
            "Dal",
            "Bhaji",
            "Chole",
            "Rajma"
        ]

        recommendations = recommendations[
            recommendations["Dish_Name"].str.contains(
                "|".join(healthy_keywords),
                case=False,
                na=False
            )
        ]

    return recommendations.head(5)


if __name__ == "__main__":
    print("\n🍽️ MasterChef AI - Smart Food Recommendation System\n")

    yesterday = input("What was cooked yesterday? : ")
    meal_type = input("Meal Type (Lunch/Dinner): ")
    quick_meal = input("Do you want a quick meal? (Yes/No): ")
    healthy_meal = input("Do you want a healthy/light meal? (Yes/No): ")

    result = recommend_dishes(
        yesterday,
        meal_type,
        quick_meal,
        healthy_meal
    )

    print("\nRecommended Dishes:\n")

    if not result.empty:
        for _, row in result.iterrows():
            print(
                f"🍽️ {row['Dish_Name']} | "
                f"{row['Main_Ingredient']} | "
                f"{row['Cook_Time']} mins"
            )
    else:
        print("No suitable dishes found.")