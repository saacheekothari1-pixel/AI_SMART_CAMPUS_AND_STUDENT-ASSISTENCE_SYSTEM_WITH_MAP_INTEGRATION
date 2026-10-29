from db import get_db_connection

try:
    connection = get_db_connection()

    if connection.is_connected():
        print("SUCCESS: Python is connected to MySQL!")
        print("Database: smart_campus")

    connection.close()

except Exception as e:
    print("ERROR:", e)