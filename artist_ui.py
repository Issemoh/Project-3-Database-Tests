import artist_db


def choice_1():
    name = input("Enter name: ").title()
    email = input("Enter email: ").lower()
    # creating instance of Artist for inserting name and email in @artist table
    artist = artist_db.Artist(name, email)
    print(artist_db.insert_artist(artist))


def choice_2():
    name = input("Enter artist's name: ").title()
    artwork_details = artist_db.search_artwork(name)

    # if length of @artwork_details is zero that means no artwork for selected artist
    if len(artwork_details) == 0 and type(artwork_details) == list:
        print("No artworks found.")
    elif len(artwork_details) > 0 and type(artwork_details) == list:
        for row in artwork_details:
            print("Artwork name: {} with price: {}$ is {}.".format(row[1], row[2], row[3]))
    else:
        print(artwork_details)


def choice_3():
    name = input("Enter artist's name: ").title()
    artwork_details = artist_db.search_artwork(name, "available")

    if len(artwork_details) == 0 and type(artwork_details) == list:
        print("No available artworks.")
    elif len(artwork_details) > 0 and type(artwork_details) == list:
        for row in artwork_details:
            print("Artwork name: {} with price: {}$.".format(row[1], row[2]))
    else:
        print(artwork_details)


def choice_4():
    artwork = input("Enter name of artwork: ").title()
    price = int(input("Enter price of artwork: "))
    print("Enter name for which artwork belong to: ")
    name = input("Name: ").title()
    # creating instance of Artwork for inserting a new artwork in @artwork table
    new_artwork = artist_db.Artwork(artwork, price, name)
    print(artist_db.add_artwork(new_artwork))


def choice_5():
    artwork = input("Enter the name of artwork which you want to be deleted: ").title()
    print(artist_db.delete_an_artwork(artwork))


def choice_6():
    artwork = input("Enter the artwork name to change its availability status: ").title()
    print(artist_db.change_availability(artwork))


def main():
    artist_db.database_setup()
    while True:
        choice = input("""
        Enter
        1 for new artist: 
        2 to search for all the artwork by an artist (everything - available and sold)
        3 to display for all the available artwork by an artist
        4 for adding new artwork: 
        5 for deleting an artwork: 
        6 for changing availability status: 
        7 for checking all artists: 
        8 for checking all artworks: 
        exit for exiting.
        """)
        if choice == "1":
            choice_1()

        elif choice == "2":
            choice_2()

        elif choice == "3":
            choice_3()

        elif choice == "4":
            choice_4()

        elif choice == "5":
            choice_5()

        elif choice == "6":
            choice_6()

        elif choice == "7":
            artist_db.show_table("artist")

        elif choice == "8":
            artist_db.show_table("artwork")

        elif choice.lower() == "exit":
            print("Thanks, Bye")
            break
        else:
            print("Wrong choice. Try again")


if __name__ == '__main__':
    main()