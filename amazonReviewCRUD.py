import pymongo

# Max Ramos
# 2.5 Performance Assessment: MongoDB CRUD Application
# Date: 9/14/2026
# Objective: Use Python to perform CRUD operations on the Amazon MongoDB database.


# Connect to the local Mongo database
print("Connecting to local Mongo database...")

myClient = pymongo.MongoClient("mongodb://localhost:27017/")

# Connect to the Amazon database
db = myClient["Amazon"]

# Connect to the ReviewData collection
myCollection = db["ReviewData"]

print("Database connected successfully!")


while True:

    # Display main menu
    print("\nType in a number and press enter to execute the menu option.")
    print("1. Query for documents")
    print("2. Add a new document")
    print("3. Update fields of a document")
    print("4. Delete a document")
    print("5. Delete all documents from the collection")
    print("6. Delete a collection")
    print("7. Exit the program")

    menuOption = input("\nEnter menu option: ")


    # *** READ SECTION ***
    if menuOption == "1":

        print("\nPlease type in a number and press enter to execute the menu option")
        print("1. Query by reviewID")
        print("2. Filter for a number of stars and greater")
        print("3. Filter for less than a number of stars")
        print("4. Filter for a word in the title")
        print("5. Filter for a word in the review body content")

        queryOption = input("\nEnter query option: ")


        # Retrieve one document using find_one()
        if queryOption == "1":

            reviewID = input("Enter the ReviewID to search for: ")

            query = {"review_id": reviewID}

            data = myCollection.find_one(query)

            print(data)


        # Filter for stars greater than or equal to entered value
        elif queryOption == "2":

            stars = input("Enter the minimum number of stars: ")

            query = {"stars": {"$gte": stars}}

            data = myCollection.find(query)

            for doc in data:
                print(doc)


        # Filter for stars less than entered value
        elif queryOption == "3":

            stars = input("Enter the number of stars: ")

            query = {"stars": {"$lt": stars}}

            data = myCollection.find(query)

            for doc in data:
                print(doc)


        # Filter for a word in review_title
        elif queryOption == "4":

            word = input("Search the title for: ")

            query = {"review_title": {"$regex": word, "$options": "i"}}

            data = myCollection.find(query)

            for doc in data:
                print(doc)


        # Filter for a word in review_body
        elif queryOption == "5":

            word = input("Search the review body for: ")

            query = {"review_body": {"$regex": word, "$options": "i"}}

            data = myCollection.find(query)

            for doc in data:
                print(doc)


    # *** CREATE SECTION ***
    elif menuOption == "2":

        print("\nAdd a new document")

        reviewID = input("Enter review ID: ")
        productID = input("Enter product ID: ")
        reviewerID = input("Enter reviewer ID: ")
        stars = input("Enter number of stars: ")
        reviewBody = input("Enter review body: ")
        reviewTitle = input("Enter review title: ")
        language = input("Enter language: ")
        productCategory = input("Enter product category: ")

        newData = {
            "review_id": reviewID,
            "product_id": productID,
            "reviewer_id": reviewerID,
            "stars": stars,
            "review_body": reviewBody,
            "review_title": reviewTitle,
            "language": language,
            "product_category": productCategory
        }

        myCollection.insert_one(newData)

        print("New document inserted!")


    # *** UPDATE SECTION ***
    elif menuOption == "3":

        reviewID = input("\nWhat is the ReviewID you wish to update? ")

        field = input("Which field would you like to update? ")

        newValue = input("What would you like to change the value to? ")

        query = {"review_id": reviewID}

        updateData = {
            "$set": {
                field: newValue
            }
        }

        myCollection.update_one(query, updateData)

        print("\nNew document has been updated to: ")
        print(myCollection.find_one({"review_id": reviewID}))


    # *** DELETE SECTION ***
    elif menuOption == "4":

        reviewID = input(
            "\nWhat is the ReviewID of the document you wish to delete? "
        )

        query = {"review_id": reviewID}

        myCollection.delete_one(query)

        print("Document deleted!")


    # Delete all documents from the collection
    elif menuOption == "5":

        print("\nRemoving all documents from the collection...")

        removeData = myCollection.delete_many({})

        print(
            "Number of documents deleted: "
            + str(removeData.deleted_count)
        )


    # Delete the ReviewData collection
    elif menuOption == "6":

        myCollection.drop()

        print("Collection removed!")


    # Exit program
    elif menuOption == "7":

        print("Program has ended!")

        break


    else:

        print("Invalid menu option.")