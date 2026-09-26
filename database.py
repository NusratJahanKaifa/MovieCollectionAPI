import sqlite3

def get_connection():
    connection = sqlite3.connect("movies.db")
    connection.row_factory = sqlite3.Row
    return connection
def create_table():
    connection = get_connection()
    connection.execute("""
        CREATE TABLE IF NOT EXISTS movies (
            movie_id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            director TEXT NOT NULL,
            genre TEXT NOT NULL,
            duration INTEGER NOT NULL,
            rating REAL NOT NULL
        )
    """)
    connection.commit()
    connection.close()