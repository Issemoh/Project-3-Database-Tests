import sqlite3


DATABASE_FILENAME = "artist_details"


def database_setup():
    connection = sqlite3.connect(DATABASE_FILENAME)
    cursor = connection.cursor()

    # deleting previous tables if exists
    cursor.execute("DROP TABLE IF EXISTS artist")
    cursor.execute("DROP TABLE IF EXISTS artwork")

    with connection:
        cursor.execute("CREATE TABLE artist(artistID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, "
                       "name TEXT UNIQUE NOT NULL, email TEXT UNIQUE NOT NULL)")

    with connection:
        cursor.execute("CREATE TABLE artwork(artworkID INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE NOT NULL, "
                       "price INTEGER NOT NULL, availability TEXT NOT NULL DEFAULT 'available',"
                       "artistID INTEGER  NOT NULL, "
                       "FOREIGN KEY(artistID) REFERENCES artist(artistID) ON DELETE CASCADE)")

    connection.close()  # closes the connection


class Artist:
    def __init__(self, name, email):
        self.name = name
        self.email = email


class Artwork:
    def __init__(self, artwork, price, name):
        self.artwork = artwork  # name of artwork
        self.price = price      # price of artwork
        self.name = name        # name of artist for which this artwork belong to


def insert_artist(artist):  # adding new artist
    connection = sqlite3.connect(DATABASE_FILENAME)
    cursor = connection.cursor()
    try:
        # trying to add a artist name and email
        with connection:
            cursor.execute("INSERT INTO artist(name, email) VALUES(?, ?)", (artist.name, artist.email))
        connection.close()
        return "Details captured."
    except sqlite3.IntegrityError:
        # if the entered email is already present in database, this block will be executed
        connection.close()
        return "Name: {} is already present in database. Try again with another name.".format(artist.name)


def show_table(table_name):  # printing artist or artwork table whichever is called.
    connection = sqlite3.connect(DATABASE_FILENAME)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM {}".format(table_name))  # selecting rows from @table_name
    table = cursor.fetchall()
    connection.close()
    if table_name == "artist":
        for row in table:
            print("Name: {}, Email: {}".format(row[1], row[2]))
        print("No artists found." if len(table) == 0 else "Total: {} records fetched.".format(len(table)))
    if table_name == "artwork":
        for row in table:
            print("Artwork name: {} with price: {}$ is {}.".format(row[1], row[2], row[3]))
        print("No artworks found." if len(table) == 0 else "Total: {} records fetched.".format(len(table)))


def add_artwork(new_artwork):
    connection = sqlite3.connect(DATABASE_FILENAME)
    cursor = connection.cursor()
    # searching for artistID
    cursor.execute("SELECT artistID FROM artist WHERE name = ?", (new_artwork.name,))
    artist_id = cursor.fetchall()
    # if no artist is present for which the artwork to correspond,
    # then length of @artist_id will be zero and then we return a failure message
    if len(artist_id) == 0:
        return "Specified name ({}) is not present in database." \
               " To add a artwork first add a artist.".format(new_artwork.name)
    else:
        try:
            # trying to add a artwork but if artwork name is already present in database except block will be executed.
            with connection:
                cursor.execute("INSERT INTO artwork(name, price, artistID) VALUES(?, ?, ?)",
                               (new_artwork.artwork, new_artwork.price, artist_id[0][0]))
            connection.close()
            return "Artwork added."
        except sqlite3.IntegrityError:
            return "The artwork name ({}) is already present in database. Please try again with " \
                   "different artwork name.".format(new_artwork.artwork)


def search_artwork(artist, filter_by=None):
    connection = sqlite3.connect(DATABASE_FILENAME)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM artist WHERE name = ?", (artist,))  # finding the artist
    artist_detail = cursor.fetchall()

    if len(artist_detail) == 0:  # if the name of artist is not in database then length of artist_detail will be zero
        return "No Data found for artist name: {}".format(artist)

    # All artworks (available and sold),
    # if filter_by is None then all available and sold artwork (everything will be selected)
    if filter_by is None:
        for art in artist_detail:
            print("\nArtworks of artist: {} with email: {} (everything - available and sold)".format(art["name"], art["email"]))
            # selecting artworks of artist
            cursor.execute("SELECT * FROM artwork WHERE artistID = ?", (art["artistID"],))
            artwork_details = cursor.fetchall()
            connection.close()
            return artwork_details

    # Only AVAILABLE artworks
    else:
        for art in artist_detail:
            print("\nArtworks of artist: {} with email: {} (only available)".format(art["name"], art["email"]))
            # selecting artworks of artist which are available
            cursor.execute("SELECT * FROM artwork WHERE artistID = ? AND availability = 'available'", (art["artistID"],))
            artwork_details = cursor.fetchall()
            connection.close()
            return artwork_details


def delete_an_artwork(artwork):
    connection = sqlite3.connect(DATABASE_FILENAME)
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM artwork WHERE name = ?", (artwork,))
    # If artwork name is not present in database
    if len(cursor.fetchall()) == 0:
        connection.close()
        return "Artwork doesn't exists."
    # Deleting artwork name
    with connection:
        cursor.execute("DELETE FROM artwork WHERE name = ?", (artwork,))
    connection.close()
    return "Artwork deleted successfully."


def change_availability(artwork):
    connection = sqlite3.connect(DATABASE_FILENAME)
    cursor = connection.cursor()
    cursor.execute("SELECT availability FROM artwork WHERE name = ?", (artwork,))
    status = cursor.fetchall()
    # If artwork is not in database
    if len(status) == 0:
        connection.close()
        return "Artwork doesn't exists."
    # Changing availability from available to sold
    if status[0][0] == "available":
        with connection:
            cursor.execute("UPDATE artwork SET availability = 'sold' WHERE name = ?", (artwork,))
        connection.close()
        return "Availability of artwork: [{}] is updated from [available] to [sold]".format(artwork)
    # changing availability from sold to available
    with connection:
        cursor.execute("UPDATE artwork SET availability = 'available' WHERE name = ?", (artwork,))
    connection.close()
    return "Availability of artwork: [{}] is updated from [sold] to [available]".format(artwork)

