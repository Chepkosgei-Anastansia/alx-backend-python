
from itertools import islice
from seed import connect_to_prodev



def stream_users_in_batches(batch_size):
    connection = connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")
    while True:
        batch = cursor.fetchmany(batch_size)
        if not batch:
            break
        yield batch
    cursor.close()
    connection.close()

def batch_processing(batch_size=10):
    for batch in stream_users_in_batches(batch_size):
        filtered = [user for user in batch if user['age'] > 25]
        print(f"Users over 25 in this batch: {filtered}")

if __name__ == "__main__":
    print("Streaming users in batches and filtering users over age 25:")
    batch_processing(batch_size= 5)

    