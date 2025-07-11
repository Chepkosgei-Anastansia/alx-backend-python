from seed import connect_to_prodev

def paginate_users(page_size, offset):
    connection = connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM user_data LIMIT %s OFFSET %s", (page_size, offset)
    )
    users = cursor.fetchall()
    cursor.close()
    connection.close()
    return users

def lazy_paginate(page_size):
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size

if __name__ == "__main__":
    # print("First page of users:")
    # first_page = next(lazy_paginate(10))
    # print(first_page)
    
    print("Paginating users with lazy generator:")
    for page in lazy_paginate(10):
        print(page)