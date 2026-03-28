import csv
from connect import get_connection

def create_table():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            phone VARCHAR(20)
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

def insert_from_csv(file_path):
    conn = get_connection()
    cur = conn.cursor()
    with open(file_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cur.execute(
                "INSERT INTO phonebook (name, phone) VALUES (%s, %s)",
                (row['name'], row['phone'])
            )
    conn.commit()
    cur.close()
    conn.close()

def insert_from_console():
    name = input("Enter name: ")
    phone = input("Enter phone: ")

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO phonebook (name, phone) VALUES (%s, %s)",
        (name, phone)
    )
    conn.commit()
    cur.close()
    conn.close()

def update_contact(old_name, new_name=None, new_phone=None):
    conn = get_connection()
    cur = conn.cursor()

    if new_name:
        cur.execute("UPDATE phonebook SET name = %s WHERE name = %s", (new_name, old_name))
    if new_phone:
        cur.execute("UPDATE phonebook SET phone = %s WHERE name = %s", (new_phone, old_name))

    conn.commit()
    cur.close()
    conn.close()

def query_contacts(name=None, phone_prefix=None):
    conn = get_connection()
    cur = conn.cursor()

    if name:
        cur.execute("SELECT * FROM phonebook WHERE name ILIKE %s", ('%' + name + '%',))
    elif phone_prefix:
        cur.execute("SELECT * FROM phonebook WHERE phone LIKE %s", (phone_prefix + '%',))
    else:
        cur.execute("SELECT * FROM phonebook")

    rows = cur.fetchall()
    for row in rows:
        print(row)

    cur.close()
    conn.close()

def delete_contact(name=None, phone=None):
    conn = get_connection()
    cur = conn.cursor()

    if name:
        cur.execute("DELETE FROM phonebook WHERE name = %s", (name,))
    elif phone:
        cur.execute("DELETE FROM phonebook WHERE phone = %s", (phone,))

    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    create_table()
    print("PhoneBook ready!")
