import sqlite3

def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    
    # Create the users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

# Initialize the database when this script is run
if __name__ == "__main__":
    init_db()
