# Python Generators in Practice

## What is a Generator?

A **generator** is a special type of Python function or expression that **produces values one at a time** using the `yield` keyword or a generator expression. It **pauses** execution between values, making it memory-efficient and great for large datasets.

---

## Why Use Generators?

| Feature            | Benefit                                      |
|-------------------|----------------------------------------------|
| **Memory-Efficient** | Does not store all data in memory             |
| **Lazy Evaluation**  | Generates values only when needed             |
| **Simple Syntax**    | Clean, readable alternative to loops/lists    |

---

## Generator Functions

These use `yield` to return values one by one:

```python
def count_up_to(n):
    count = 1
    while count <= n:
        yield count
        count += 1

for number in count_up_to(3):
    print(number)
# Output: 1, 2, 3
```

---

## Example: Streaming Database Rows

Instead of:

```python
cursor.execute("SELECT * FROM user_data")
rows = cursor.fetchall()  # Loads all into memory 
```

Use a generator function:

```python
def stream_users(connection):
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")
    for row in cursor:
        yield row  # One row at a time 
    cursor.close()
```

### Usage:

```python
for user in stream_users(connection):
    print(user)
```

---

## Generator Expressions

A **generator expression** is like a list comprehension, but it uses **()` instead of []**, and **returns an iterator** instead of a full list.

### Syntax:

```python
(expression for item in iterable if condition)
```

### Example: Extracting User Emails from Stream

```python
emails = (user['email'] for user in stream_users(connection))
for email in emails:
    print(email)
```

Advantage: Emails are fetched **one by one**, without building a full list in memory.

---

## When to Use Generators

- Large datasets (e.g., databases, log files)
- Processing streams (e.g., network data, file I/O)
- Infinite or long sequences
- Efficient filtering and transformation

---

## Summary

| Type                   | Description                                |
|------------------------|--------------------------------------------|
| **Generator Function** | Uses `yield` to produce values lazily      |
| **Generator Expression** | Compact inline generator, uses `()` syntax  |

Generators are ideal for **memory-safe**, **scalable**, and **clean** data processing—especially when dealing with large databases or real-time data streams.
