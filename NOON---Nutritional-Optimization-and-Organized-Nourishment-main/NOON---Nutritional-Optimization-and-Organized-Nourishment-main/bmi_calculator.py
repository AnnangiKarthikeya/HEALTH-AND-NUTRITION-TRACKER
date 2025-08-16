def calculate_bmi(weight_kg, height_cm, age, gender, activity_level):
    # Convert height to meters
    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)

    # Calculate BMR using Mifflin-St Jeor Equation
    if gender == "Male":
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    else:
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161

    # Adjust BMR based on activity level
    activity_factors = {
        "Sedentary": 1.2,
        "Lightly active": 1.375,
        "Moderately active": 1.55,
        "Very active": 1.725,
        "Extra active": 1.9
    }
    calorie_needs = bmr * activity_factors.get(activity_level, 1.2)

    return bmi, calorie_needs