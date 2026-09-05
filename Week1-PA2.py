# Name: Max Ramos
# Date: September 5, 2026
# Assignment: Week 1 PA2
# Purpose: Perform CRUD operations on sets in a Redis database.

import redis

# Connect to Redis
r = redis.Redis(host="localhost", port=6379)

# Display the menu until the user exits
while True:
    print("\nType in a number and press enter to execute the menu option.")
    print("1. Query for set members")
    print("2. Add a new set")
    print("3. Update members of a set")
    print("4. Delete a set")
    print("5. Delete all data from the database")
    print("6. Exit the program")

    choice = input()

    # Read members from a set
    if choice == "1":
        key = input("\nEnter the key of the set you wish to query:\n")
        members = r.smembers(key)

        print("\nSet members:")
        for member in members:
            print(member)

    # Create a new set
    elif choice == "2":
        key = input("\nEnter the key you wish to add:\n")
        amount = int(input("\nEnter how many members will this set have:\n"))

        for i in range(amount):
            member = input("\nEnter the next member value:\n")
            r.sadd(key, member)

    # Update members of a set
    elif choice == "3":
        key = input("\nEnter the key of the set you wish to update:\n")

        print("\nPlease type in a number and press enter to execute the menu option")
        print("1. Add new member")
        print("2. Remove member")
        print("3. Remove all members")
        print("4. Exit Update Menu")

        update_choice = input()

        # Add a member
        if update_choice == "1":
            member = input("\nEnter the member you wish to add:\n")
            r.sadd(key, member)

        # Remove one member
        elif update_choice == "2":
            member = input("\nEnter the member you wish to remove:\n")
            r.srem(key, member)

        # Remove all members
        elif update_choice == "3":
            members = r.smembers(key)

            print("\nRemoving all set members...")

            for member in members:
                print("Removing Member:", member, "...")
                r.srem(key, member)

            print("\nThe cardinality of the set is now:")
            print(r.scard(key))

        # Option 4 simply returns to the main menu
        elif update_choice == "4":
            pass

    # Delete a specific set
    elif choice == "4":
        key = input("\nEnter the key of the set you wish to delete:\n")
        r.delete(key)

    # Delete all data from Redis
    elif choice == "5":
        r.flushdb()

    # Exit the program
    elif choice == "6":
        break