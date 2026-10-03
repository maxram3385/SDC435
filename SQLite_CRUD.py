# Name: Max Ramos
# Date: 10/03/2026
# Assignment: 5.6 Performance Assessment
# Purpose: Create an SQLite database, import review data from a JSON file,
# and allow the user to perform CRUD operations on the database.

import sqlite3
import json


DATABASE_NAME = "EN_ReviewData.db"
JSON_FILE = "dataset_en_dev.json"


# Create the database and tables
def create_database():

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Reviewers (
            reviewer_id TEXT PRIMARY KEY
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Categories (
            product_category TEXT PRIMARY KEY
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Products (
            product_id TEXT PRIMARY KEY,
            product_category TEXT,
            FOREIGN KEY (product_category)
            REFERENCES Categories(product_category)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Reviews (
            review_id TEXT PRIMARY KEY,
            product_id TEXT,
            reviewer_id TEXT,
            stars INTEGER,
            review_body TEXT,
            review_title TEXT,
            FOREIGN KEY (product_id)
            REFERENCES Products(product_id),
            FOREIGN KEY (reviewer_id)
            REFERENCES Reviewers(reviewer_id)
        )
    """)

    conn.commit()
    conn.close()


# Import data from the JSON file
def import_json():

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    with open(JSON_FILE, "r", encoding="utf-8") as file:

        for line in file:

            record = json.loads(line)

            review_id = record["review_id"]
            product_id = record["product_id"]
            reviewer_id = record["reviewer_id"]
            stars = record["stars"]
            review_body = record["review_body"]
            review_title = record["review_title"]
            product_category = record["product_category"]

            cursor.execute("""
                INSERT OR IGNORE INTO Reviewers
                VALUES (?)
            """, (reviewer_id,))

            cursor.execute("""
                INSERT OR IGNORE INTO Categories
                VALUES (?)
            """, (product_category,))

            cursor.execute("""
                INSERT OR IGNORE INTO Products
                VALUES (?, ?)
            """, (
                product_id,
                product_category
            ))

            cursor.execute("""
                INSERT OR IGNORE INTO Reviews
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                review_id,
                product_id,
                reviewer_id,
                stars,
                review_body,
                review_title
            ))

    conn.commit()
    conn.close()

    print("Data imported successfully.")


# Insert a new record
def insert_record():

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    print()
    print("Choose a table:")
    print("1. Reviewers")
    print("2. Categories")
    print("3. Products")
    print("4. Reviews")

    choice = input("Enter table number: ")

    if choice == "1":

        reviewer_id = input("Enter reviewer ID: ")

        cursor.execute("""
            INSERT INTO Reviewers
            VALUES (?)
        """, (reviewer_id,))

    elif choice == "2":

        category = input("Enter product category: ")

        cursor.execute("""
            INSERT INTO Categories
            VALUES (?)
        """, (category,))

    elif choice == "3":

        product_id = input("Enter product ID: ")
        category = input("Enter product category: ")

        cursor.execute("""
            INSERT INTO Products
            VALUES (?, ?)
        """, (
            product_id,
            category
        ))

    elif choice == "4":

        review_id = input("Enter review ID: ")
        product_id = input("Enter product ID: ")
        reviewer_id = input("Enter reviewer ID: ")
        stars = input("Enter number of stars: ")
        body = input("Enter review body: ")
        title = input("Enter review title: ")

        cursor.execute("""
            INSERT INTO Reviews
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            review_id,
            product_id,
            reviewer_id,
            stars,
            body,
            title
        ))

    else:

        print("Invalid selection.")
        conn.close()
        return

    conn.commit()
    conn.close()

    print("Record inserted successfully.")


# Display categories with a minimum number of products
def display_categories():

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    minimum = int(input(
        "\nWhat is the minimum product count?\n"
    ))

    cursor.execute("""
        SELECT product_category, COUNT(product_id)
        FROM Products
        GROUP BY product_category
        HAVING COUNT(product_id) >= ?
        ORDER BY product_category
    """, (minimum,))

    results = cursor.fetchall()

    print()
    print(
        "Displaying Categories with "
        + str(minimum)
        + "+ products:"
    )

    for row in results:
        print(row)

    conn.close()


# Allow the user to enter a SELECT statement
def enter_query():

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    query = input(
        "\nEnter a SELECT statement:\n"
    )

    try:

        cursor.execute(query)

        results = cursor.fetchall()

        for row in results:
            print(row)

    except sqlite3.Error as error:

        print("Error:", error)

    conn.close()


# Update a review
def update_review():

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    review_id = input(
        "\nEnter the review ID to update: "
    )

    stars = input(
        "Enter the new star rating: "
    )

    cursor.execute("""
        UPDATE Reviews
        SET stars = ?
        WHERE review_id = ?
    """, (
        stars,
        review_id
    ))

    conn.commit()
    conn.close()

    print("Review updated.")


# Delete reviews from a selected product category
def delete_reviews():

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    category = input(
        "\nEnter the product category: "
    )

    cursor.execute("""
        DELETE FROM Reviews
        WHERE product_id IN (
            SELECT product_id
            FROM Products
            WHERE product_category = ?
        )
    """, (category,))

    conn.commit()
    conn.close()

    print(
        "Reviews deleted from category:",
        category
    )


# Delete all tables
def delete_tables():

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        DROP TABLE IF EXISTS Reviews
    """)

    cursor.execute("""
        DROP TABLE IF EXISTS Products
    """)

    cursor.execute("""
        DROP TABLE IF EXISTS Categories
    """)

    cursor.execute("""
        DROP TABLE IF EXISTS Reviewers
    """)

    conn.commit()
    conn.close()

    print("All tables deleted.")


# Main menu
def menu():

    while True:

        print()
        print(
            "Type in a number and press enter "
            "to execute the menu option."
        )
        print("1. Insert a new record")
        print("2. Display product count per category")
        print("3. Enter a query")
        print("4. Update a review")
        print("5. Delete reviews from a category")
        print("6. Delete all tables")
        print("7. Exit the program")

        choice = input("\nEnter option: ")

        if choice == "1":

            insert_record()

        elif choice == "2":

            display_categories()

        elif choice == "3":

            enter_query()

        elif choice == "4":

            update_review()

        elif choice == "5":

            delete_reviews()

        elif choice == "6":

            delete_tables()

        elif choice == "7":

            print("Program ended.")
            break

        else:

            print("Invalid option.")


# Run the program
create_database()
import_json()
menu()