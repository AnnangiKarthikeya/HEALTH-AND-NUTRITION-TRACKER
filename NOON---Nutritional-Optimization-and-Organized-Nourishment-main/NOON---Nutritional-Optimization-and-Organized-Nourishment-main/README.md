# Nutrition and BMI Tracker App (NOON - Nutritional Optimization and Organized Nourishment)

## Project Overview

**NOON** is a Python-based desktop application that helps users calculate their BMI, determine their daily nutritional needs (calories, proteins, fats, and carbs), and manage a grocery list. 
It integrates with the **OpenFoodFacts API** to allow users to search for food items and track their nutritional intake.

## Features

- **BMI Calculation**: Users can input their weight, height, age, gender, and activity level to calculate their BMI.
- **Nutritional Needs Calculation**: Based on the calculated BMI, the app determines the user's recommended daily intake of calories, proteins, carbs, and fats.
- **Food Search**: Users can search for food items through the **OpenFoodFacts API** and view the nutritional information for each item.
- **Grocery List Management**: Users can add food items to a grocery list, remove items, and save/load the list to/from a CSV file.
- **User Authentication**: Secure user registration and login functionality using **SQLite** to store user credentials.
- **Error Handling**: Includes error handling for network issues when searching for food items via the API.

## Tech Stack

### Language:
- **Python**

### Libraries/Frameworks:
- **Tkinter**: Used for creating the graphical user interface (GUI).
- **Requests**: Used to interact with the **OpenFoodFacts API**.
- **SQLite3**: Used for user authentication and database management.
- **CSV**: Used to handle the saving and loading of grocery lists.

## How It Works

1. **User Registration/Login**:
   - Users can register a new account, which is securely stored in the local **SQLite** database.
   - Once registered, users can log in and access the BMI and nutrition tracker features.

2. **BMI and Nutrition Calculation**:
   - After logging in, users can input their details (weight, height, age, gender, and activity level) to calculate their BMI and daily nutritional needs.
   - The app calculates daily calorie intake and breaks it down into proteins, carbs, and fats based on standard nutritional guidelines.

3. **Food Search and Grocery List**:
   - Users can search for food items using the **OpenFoodFacts API**.
   - Nutritional information (calories, proteins, carbs, and fats) for each food item is displayed, and users can add items to a grocery list.
   - The grocery list can be saved to a CSV file or loaded from a previously saved file.
