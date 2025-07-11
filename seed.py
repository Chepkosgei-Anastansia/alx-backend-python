import csv
import mysql.connector
import uuid
import os

from dotenv import load_dotenv
load_dotenv('secret.env')

def connect_to_mysql():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        port=int(os.getenv('DB_PORT'))
    )

def connect_to_prodev():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME'),
        port=int(os.getenv('DB_PORT'))
    )

def create_database():
    conn = connect_to_mysql()
    cursor = conn.cursor()
    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
    finally:
        cursor.close()
        conn.close()

def create_table(connection):
    cursor = connection.cursor()
    try:
        cursor.execute("DROP TABLE IF EXISTS user_data")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                user_id VARCHAR(36) PRIMARY KEY,
                name VARCHAR(100),
                email VARCHAR(100) UNIQUE,
                age INT
            )
        """)
    finally:
        cursor.close()

def insert_data(connection, data):
    cursor = connection.cursor()
    query = """
        INSERT INTO user_data (user_id, name, email, age)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
        name = VALUES(name), email = VALUES(email), age = VALUES(age)
    """
    for row in data:
        uid = str(uuid.uuid4())
        cursor.execute(query, (uid, row['name'], row['email'], row['age']))
    connection.commit()
    cursor.close()

def read_csv(file_path):
    with open(file_path, newline='') as csvfile:
        return list(csv.DictReader(csvfile))

def stream_users(connection):
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")
    for row in cursor:
        yield row
    cursor.close()

