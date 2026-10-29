from db import get_db_connection

connection = get_db_connection()
cursor = connection.cursor()

cursor.execute("SHOW TABLES")
tables = [row[0] for row in cursor.fetchall()]

print("\nEXISTING DATABASE TABLES")

for table in tables:
    print(f"\n--- {table} ---")

    cursor.execute(f"SHOW COLUMNS FROM `{table}`")
    for column in cursor.fetchall():
        print(f"{column[0]} : {column[1]}")

    cursor.execute(f"SELECT COUNT(*) FROM `{table}`")
    print("Current records:", cursor.fetchone()[0])

cursor.close()
connection.close()
