import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
from bmi_calculator import calculate_bmi
from food_search import search_food
import csv

# SQLite connection for user authentication
def connect_db():
    return sqlite3.connect('users.db')

class App:
    def __init__(self, root):
        self.root = root
        self.frames = {}
        self.bmi = None
        self.calorie_needs = None
        self.protein_needs = None
        self.carbs_needs = None
        self.fats_needs = None

        # Initialize all pages
        for Page in (LoginPage, RegisterPage, BMIPage, NutritionPage):
            page_name = Page.__name__
            frame = Page(parent=root, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

    def show_page(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

    def login_user(self, username):
        '''Set the current user after successful login'''
        self.current_user = username

class LoginPage(tk.Frame):
    '''Page where users can log in'''

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        tk.Label(self, text="Login", font=("NewAmsterdam", 18)).pack(pady=20)

        tk.Label(self, text="Username:").pack(pady=5)
        self.username_entry = ttk.Entry(self)
        self.username_entry.pack(pady=5)

        tk.Label(self, text="Password:").pack(pady=5)
        self.password_entry = ttk.Entry(self, show='*')
        self.password_entry.pack(pady=5)

        ttk.Button(self, text="Login", command=self.login).pack(pady=20)
        ttk.Button(self, text="Register", command=lambda: controller.show_page("RegisterPage")).pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        conn = connect_db()
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = c.fetchone()
        conn.close()

        if user:
            self.controller.login_user(username)
            self.controller.show_page("BMIPage")  # Redirect to BMI page after successful login
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

class RegisterPage(tk.Frame):
    '''Page where users can register a new account'''

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        tk.Label(self, text="Register", font=("NewAmsterdam", 18)).pack(pady=20)

        tk.Label(self, text="Username:").pack(pady=5)
        self.username_entry = ttk.Entry(self)
        self.username_entry.pack(pady=5)

        tk.Label(self, text="Password:").pack(pady=5)
        self.password_entry = ttk.Entry(self, show='*')
        self.password_entry.pack(pady=5)

        ttk.Button(self, text="Register", command=self.register).pack(pady=20)
        ttk.Button(self, text="Back to Login", command=lambda: controller.show_page("LoginPage")).pack()

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Both fields are required")
            return

        conn = connect_db()
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            messagebox.showinfo("Success", "Account created! Please log in.")
            self.controller.show_page("LoginPage")
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists")
        finally:
            conn.close()

class BMIPage(tk.Frame):
    '''BMI calculation page for logged-in users'''



    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # BMI input fields
        tk.Label(self, text="BMI Calculator", font=("NewAmsterdam", 18)).pack(pady=20)

        tk.Label(self, text="Weight (kg):").pack(pady=5)
        self.weight_entry = ttk.Entry(self)
        self.weight_entry.pack(pady=5)

        tk.Label(self, text="Height (cm):").pack(pady=5)
        self.height_entry = ttk.Entry(self)
        self.height_entry.pack(pady=5)

        tk.Label(self, text="Age:").pack(pady=5)
        self.age_entry = ttk.Entry(self)
        self.age_entry.pack(pady=5)

        tk.Label(self, text="Gender:").pack(pady=5)
        self.gender_var = tk.StringVar()
        gender_dropdown = ttk.Combobox(self, textvariable=self.gender_var, values=["Male", "Female"], state="readonly")
        gender_dropdown.pack(pady=5)

        tk.Label(self, text="Activity Level:").pack(pady=5)
        self.activity_var = tk.StringVar()
        activity_dropdown = ttk.Combobox(self, textvariable=self.activity_var, values=["Sedentary", "Lightly active", "Moderately active", "Very active", "Extra active"], state="readonly")
        activity_dropdown.pack(pady=5)

        # Button to calculate BMI and go to the Nutrition page
        ttk.Button(self, text="Calculate BMI", command=self.calculate_bmi).pack(pady=20)

    def calculate_bmi(self):
        try:
            # Get user input for BMI
            weight_kg = float(self.weight_entry.get())
            height_cm = float(self.height_entry.get())
            age = int(self.age_entry.get())
            gender = self.gender_var.get()
            activity_level = self.activity_var.get()

            # Validate inputs
            if weight_kg <= 0 or height_cm <= 0 or age <= 0:
                raise ValueError

            # Calculate BMI and daily calorie needs
            bmi, calorie_needs = calculate_bmi(weight_kg, height_cm, age, gender, activity_level)

            # Suggested macronutrient distribution (40% carbs, 30% protein, 30% fat)
            protein_needs = 0.3 * calorie_needs / 4  # 1g protein = 4 calories
            carbs_needs = 0.4 * calorie_needs / 4    # 1g carbs = 4 calories
            fats_needs = 0.3 * calorie_needs / 9     # 1g fat = 9 calories

            # Pass the calculated data to the controller
            self.controller.bmi = bmi
            self.controller.calorie_needs = calorie_needs
            self.controller.protein_needs = protein_needs
            self.controller.carbs_needs = carbs_needs
            self.controller.fats_needs = fats_needs

            # Transition to the NutritionPage
            self.controller.show_page("NutritionPage")

        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid positive numbers for all fields.")

class NutritionPage(tk.Frame):
    '''Nutrition calculation and food search page'''

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        tk.Label(self, text="Your BMI and Nutritional Needs", font=("NewAmsterdam", 18)).pack(pady=20)

        self.bmi_label = tk.Label(self, text="")
        self.bmi_label.pack(pady=5)

        self.calorie_needs_label = tk.Label(self, text="")
        self.calorie_needs_label.pack(pady=5)

        self.protein_needs_label = tk.Label(self, text="")
        self.protein_needs_label.pack(pady=5)

        self.carbs_needs_label = tk.Label(self, text="")
        self.carbs_needs_label.pack(pady=5)

        self.fats_needs_label = tk.Label(self, text="")
        self.fats_needs_label.pack(pady=5)

        # Food search section
        tk.Label(self, text="Search for Food Items", font=("NewAmsterdam", 14)).pack(pady=10)
        self.search_entry = ttk.Entry(self)
        self.search_entry.pack(pady=5)
        self.search_button = ttk.Button(self, text="Search", command=self.search_food)
        self.search_button.pack(pady=10)

        # Loading label to display during API call
        self.loading_label = tk.Label(self, text="", font=("NewAmsterdam", 12))
        self.loading_label.pack(pady=5)

        # Listbox to display search results
        self.food_results_listbox = tk.Listbox(self, height=10, width=50)
        self.food_results_listbox.pack(pady=10)

        # Button to add food to the grocery list
        ttk.Button(self, text="Add to Grocery List", command=self.add_to_grocery_list).pack(pady=10)

        # Grocery list section
        tk.Label(self, text="Your Grocery List", font=("NewAmsterdam", 14)).pack(pady=10)
        self.grocery_listbox = tk.Listbox(self, height=10, width=50)
        self.grocery_listbox.pack(pady=10)

        # Buttons to remove, save, and load the grocery list
        ttk.Button(self, text="Remove Selected Item", command=self.remove_from_grocery_list).pack(pady=5)
        ttk.Button(self, text="Save Grocery List", command=self.save_grocery_list).pack(pady=5)
        ttk.Button(self, text="Load Grocery List", command=self.load_grocery_list).pack(pady=5)

        self.grocery_list = []  # Store the grocery list items

    def tkraise(self, *args, **kwargs):
        '''Update the labels with the calculated values when this page is raised'''
        super().tkraise(*args, **kwargs)
        bmi = self.controller.bmi
        calorie_needs = self.controller.calorie_needs
        protein_needs = self.controller.protein_needs
        carbs_needs = self.controller.carbs_needs
        fats_needs = self.controller.fats_needs

        self.bmi_label.config(text=f"Your BMI: {bmi:.2f}")
        self.calorie_needs_label.config(text=f"Suggested Daily Calories: {calorie_needs:.0f} kcal")
        self.protein_needs_label.config(text=f"Protein: {protein_needs:.0f}g")
        self.carbs_needs_label.config(text=f"Carbs: {carbs_needs:.0f}g")
        self.fats_needs_label.config(text=f"Fats: {fats_needs:.0f}g")

    def search_food(self):
        '''Search for food items using the OpenFoodFacts API'''
        search_term = self.search_entry.get()
        
        # Show loading message
        self.loading_label.config(text="Searching... Please wait.")
        self.food_results_listbox.delete(0, tk.END)
        self.search_button.config(state=tk.DISABLED)

        # Perform the search
        self.after(100, self.perform_search, search_term)  # Delay to allow UI to update

    def perform_search(self, search_term):
        '''Perform the actual search after a short delay for UI responsiveness'''
        products = search_food(search_term)
        
        # Clear the loading message
        self.loading_label.config(text="")
        self.search_button.config(state=tk.NORMAL)

        if products:
            for product in products:
                food_info = f"{product['name']} - Calories: {product['calories']}, Proteins: {product['proteins']}, Carbs: {product['carbs']}, Fats: {product['fats']}"
                self.food_results_listbox.insert(tk.END, food_info)
        else:
            self.food_results_listbox.insert(tk.END, "No results found. Please try a different search.")

    def add_to_grocery_list(self):
        '''Add the selected food item to the grocery list'''
        selected_item = self.food_results_listbox.get(tk.ACTIVE)
        if selected_item:
            self.grocery_list.append(selected_item)
            self.grocery_listbox.insert(tk.END, selected_item)
            messagebox.showinfo("Added to Grocery List", f"Added:\n{selected_item}")

    def remove_from_grocery_list(self):
        '''Remove the selected item from the grocery list'''
        selected_item = self.grocery_listbox.get(tk.ACTIVE)
        if selected_item in self.grocery_list:
            self.grocery_list.remove(selected_item)
            self.grocery_listbox.delete(tk.ACTIVE)

    def save_grocery_list(self):
        '''Save the grocery list to a CSV file'''
        if not self.grocery_list:
            messagebox.showinfo("No Items", "There are no items in the grocery list to save.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if file_path:
            try:
                with open(file_path, mode='w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(["Item"])
                    for item in self.grocery_list:
                        writer.writerow([item])
                messagebox.showinfo("Success", f"Grocery list saved to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {str(e)}")

    def load_grocery_list(self):
        '''Load a grocery list from a CSV file'''
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            try:
                with open(file_path, mode='r') as file:
                    reader = csv.reader(file)
                    next(reader)  # Skip header
                    loaded_items = [row[0] for row in reader]
                    self.grocery_list.clear()
                    self.grocery_listbox.delete(0, tk.END)
                    self.grocery_list.extend(loaded_items)
                    for item in loaded_items:
                        self.grocery_listbox.insert(tk.END, item)
                messagebox.showinfo("Success", f"Grocery list loaded from {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {str(e)}")
