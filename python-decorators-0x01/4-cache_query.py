import time
import sqlite3
import functools

query_cache = {}

# Decorator to cache query results based on the SQL query string
def cache_query(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get("query")
        if query in query_cache:
            print("Returning cached result.")
            return query_cache[query]
        print("Executing query and caching result.")
        result = func(*args, **kwargs)
        query_cache[query] = result
        return result
    return wrapper

# Decorator to automatically pass a database connection to the function
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db") 
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

# Function that executes a query, using both decorators
@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# Usage Example
if __name__ == "__main__":
    # Create a table and insert data (for demonstration purposes)
    with sqlite3.connect("users.db") as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)")
        conn.execute("INSERT INTO users (name) VALUES ('Alice')")
        conn.execute("INSERT INTO users (name) VALUES ('Bob')")
        conn.commit()

    # First call: runs query and caches result
    users = fetch_users_with_cache(query="SELECT * FROM users")
    print(users)

    # Second call: uses cache
    users_again = fetch_users_with_cache(query="SELECT * FROM users")
    print(users_again)