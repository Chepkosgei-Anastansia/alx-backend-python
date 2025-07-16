import sqlite3
import functools

# Decorator to log SQL queries
def log_queries():
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            query = kwargs.get("query", args[0] if args else "UNKNOWN")
            print(f"[LOG] Executing SQL Query: {query}")
            return func(*args, **kwargs)
        return wrapper
    return decorator

@log_queries()
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# Usage example — create table and insert dummy data for demo
if __name__ == "__main__":
    with sqlite3.connect('users.db') as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)")
        conn.execute("INSERT INTO users (name) VALUES ('Alice')")
        conn.execute("INSERT INTO users (name) VALUES ('Bob')")
        conn.commit()

    # Fetch users while logging the query
    users = fetch_all_users(query="SELECT * FROM users")
    print(users)
