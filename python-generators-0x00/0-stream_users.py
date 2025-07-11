from itertools import islice
from seed import connect_to_prodev, create_database, create_table, insert_data, read_csv;        

def stream_users(connection):
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")
    for row in cursor:
        yield row
    cursor.close()

    connection.close()


if __name__ == "__main__":
    conn = connect_to_prodev()
    for user in stream_users(conn):
        print(user)
# Fetching a limited number of users
    print("\nStreaming first 6 users:")
    conn2 = connect_to_prodev()
    for user in islice(stream_users(conn2), 6):
        print(user)

