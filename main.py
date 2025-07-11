from seed import connect_to_prodev, create_database, create_table, insert_data, read_csv, stream_users



if __name__ == "__main__":
    create_database()
    prodev_conn = connect_to_prodev()
    create_table(prodev_conn)

    user_data = read_csv("user_data.csv")
    insert_data(prodev_conn, user_data)

    print("Streaming users from database:")
    for user in stream_users(prodev_conn):
        print(user)

    prodev_conn.close()