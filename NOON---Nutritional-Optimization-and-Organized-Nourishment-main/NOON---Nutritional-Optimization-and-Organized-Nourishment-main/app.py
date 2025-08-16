import tkinter as tk
from ui_components import App
from db_setup import init_db

# Initialize the SQLite database
init_db()

# Create the main window and run the application
root = tk.Tk()
root.title("Stellars")
root.geometry("600x600")
# Create the main App class to handle multiple pages
app = App(root)
app.show_page("LoginPage")  # Start on the Login page

root.mainloop()
