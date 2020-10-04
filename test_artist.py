import unittest
import artist_db
import sqlite3


class TestCase(unittest.TestCase):
    # Check if artist is inserted in @artist table or not
    def test_insert_artist(self):
        artist_db.database_setup()  # setting up a new database, deleting previous and creating new
        artist1 = artist_db.Artist("Ulrich nelson", "ulrich@gmail.com")
        artist2 = artist_db.Artist("Katherina", "katherina@gmail.com")
        # Adding new artist in database
        artist_db.insert_artist(artist1)
        artist_db.insert_artist(artist2)
        # Connecting to database
        connection = sqlite3.connect(artist_db.DATABASE_FILENAME)
        connection.row_factory = sqlite3.Row  # row_factory allows to access columns through columns names.
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM artist")  # selecting all artists from artist table

        artists = cursor.fetchall()
        connection.close()
        # Checking if added artists are present in database ot not
        self.assertTrue("Ulrich nelson" and "ulrich@gmail.com" in artists[0])
        self.assertTrue("Katherina" and "katherina@gmail.com" in artists[1])

    # Making sure that duplicate artist can't be inserted into @artist table
    def test_adding_duplicate_artist(self):
        artist_db.database_setup()
        artist1 = artist_db.Artist("Ulrich nelson", "ulrich@gmail.com")
        artist2 = artist_db.Artist("Katherina", "katherina@gmail.com")
        artist3 = artist_db.Artist("Ulrich nelson", "ulrich@gmail.com")

        artist_db.insert_artist(artist1)
        artist_db.insert_artist(artist2)
        artist_db.insert_artist(artist3)  # Adding a duplicate name

        connection = sqlite3.connect(artist_db.DATABASE_FILENAME)
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        # Selecting all names from artist table
        cursor.execute("SELECT name FROM artist")

        artists = cursor.fetchall()
        connection.close()
        # if duplicate name is not added then length will be previous length i.e len(artists) = 2
        self.assertEqual(len(artists), 2)  # Length is not increased

    # Check if artwork is inserted in @artwork table or not
    def test_add_artwork(self):
        artist_db.database_setup()
        artist1 = artist_db.Artist("Ulrich nelson", "ulrich@gmail.com")
        artist2 = artist_db.Artist("Katherina", "katherina@gmail.com")

        artwork1 = artist_db.Artwork("Dark", 78, artist1.name)
        artwork2 = artist_db.Artwork("Glass", 25, artist2.name)

        artist_db.insert_artist(artist1)  # adding artists
        artist_db.insert_artist(artist2)
        artist_db.add_artwork(artwork1)   # adding artworks
        artist_db.add_artwork(artwork2)

        connection = sqlite3.connect(artist_db.DATABASE_FILENAME)
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM artwork")  # selecting all artworks from artwork table
        artworks = cursor.fetchall()
        connection.close()
        # Checking if artworks are added or not
        self.assertTrue("Dark" and 78 and "available" in artworks[0])
        self.assertTrue("Glass" and 25 and "available" in artworks[1])

    # making sure that duplicate artworks can't be added in @artwork table
    def test_adding_duplicate_artwork(self):
        artist_db.database_setup()
        artist1 = artist_db.Artist("Ulrich nelson", "ulrich@gmail.com")
        artist2 = artist_db.Artist("Katherina", "katherina@gmail.com")

        artwork1 = artist_db.Artwork("Dark", 78, artist1.name)
        artwork2 = artist_db.Artwork("Glass", 25, artist2.name)
        artwork3 = artist_db.Artwork("Glass", 25, artist1.name)

        artist_db.insert_artist(artist1)
        artist_db.insert_artist(artist2)
        artist_db.add_artwork(artwork1)
        artist_db.add_artwork(artwork2)
        artist_db.add_artwork(artwork3)  # Adding a duplicate artwork

        connection = sqlite3.connect(artist_db.DATABASE_FILENAME)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM artwork")  # selecting all artworks
        # if no duplicate artwork is added the length will not increase.
        # We added only three artworks but third one is duplicate that means length has to be 2
        self.assertEqual(len(cursor.fetchall()), 2)
        connection.close()

    #  checking if adding a artwork with no artist
    def test_adding_artwork_without_artist(self):
        artist_db.database_setup()
        artist1 = artist_db.Artist("Ulrich nelson", "ulrich@gmail.com")
        artist2 = artist_db.Artist("Katherina", "katherina@gmail.com")

        artwork1 = artist_db.Artwork("Dark", 78, artist1.name)
        artwork2 = artist_db.Artwork("Glass", 25, "Ben")  # Adding a artwork with no artist

        artist_db.insert_artist(artist1)
        artist_db.insert_artist(artist2)
        artist_db.add_artwork(artwork1)
        artist_db.add_artwork(artwork2)

        connection = sqlite3.connect(artist_db.DATABASE_FILENAME)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM artwork")
        # artwork can't be added without artist. we are adding a artwork for "Ben" which is not in artist table
        # We added 2 artwork, but second artwork can't be added due to constraints
        # that means length of artwork table has to be 1
        self.assertTrue(len(cursor.fetchall()) == 1)
        connection.close()

    # Searching all artworks by an artist name
    def test_search_all_artworks(self):
        artist_db.database_setup()
        artist1 = artist_db.Artist("Ulrich nelson", "ulrich@gmail.com")
        artist2 = artist_db.Artist("Katherina", "katherina@gmail.com")

        artwork1 = artist_db.Artwork("Dark", 78, artist1.name)
        artwork2 = artist_db.Artwork("Glass", 25, artist2.name)

        artist_db.insert_artist(artist1)
        artist_db.insert_artist(artist2)
        artist_db.add_artwork(artwork1)
        artist_db.add_artwork(artwork2)

        # searching artworks with name
        artwork_details1 = artist_db.search_artwork(artist1.name)
        artwork_details2 = artist_db.search_artwork(artist2.name)

        # Checking if artwork is present or not for an artist name
        self.assertTrue(any("Dark" in row for row in artwork_details1))
        self.assertTrue(any("Glass" in row for row in artwork_details2))

        self.assertEqual(len(artwork_details1), 1)  # Checking the length of fetched artworks by an artist name
        self.assertEqual(len(artwork_details2), 1)

    # searching only available artwork by an artist name
    def test_only_available_artworks(self):
        artist_db.database_setup()
        artist1 = artist_db.Artist("Hannah", "hannah@gmail.com")

        artist_db.insert_artist(artist1)
        artwork1 = artist_db.Artwork("Dark", 78, artist1.name)
        artwork2 = artist_db.Artwork("Glass", 25, artist1.name)
        artwork3 = artist_db.Artwork("Mountains", 168, artist1.name)

        artist_db.add_artwork(artwork1)
        artist_db.add_artwork(artwork2)
        artist_db.add_artwork(artwork3)

        artist_db.change_availability(artwork2.artwork)  # Changing availability of an artwork, from available to sold
        available_artwork = artist_db.search_artwork(artist1.name, "available")

        connection = sqlite3.connect(artist_db.DATABASE_FILENAME)
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        # searching available artwork by an artist name
        cursor.execute("SELECT artistID FROM artist WHERE name = ?", (artist1.name,))
        artist = cursor.fetchall()
        cursor.execute("SELECT * FROM artwork WHERE availability = 'available' AND artistID = ?", (artist[0]["artistID"],))
        available_artwork_table = cursor.fetchall()

        # checking if available artworks fetched from database by queries
        # is equal to available artworks returned by @artist_db module or not
        self.assertEqual(available_artwork_table[0]["availability"], available_artwork[0]["availability"])
        self.assertTrue(available_artwork_table[1]["availability"], available_artwork[1]["availability"])

        # checking if length of only available artworks fetched from database by queries
        # is equal to available artwork returned by @artist_db module or not
        self.assertEqual(len(available_artwork), len(available_artwork_table))
        connection.close()

    # For checking artwork belongs to correct artist or not (Checking table correctness)
    def test_artwork_to_artist_relation(self):
        artist_db.database_setup()
        artist1 = artist_db.Artist("Hannah", "hannah@gmail.com")

        artist_db.insert_artist(artist1)  # adding artists
        artwork1 = artist_db.Artwork("Dark", 78, artist1.name)
        artist_db.add_artwork(artwork1)   # adding artwork
        connection = sqlite3.connect(artist_db.DATABASE_FILENAME)
        cursor = connection.cursor()
        # Selecting name of artist by an artwork
        cursor.execute("SELECT name FROM artist WHERE artistID = (SELECT artistID FROM artwork WHERE name = 'Dark')")
        name = cursor.fetchone()
        self.assertEqual(name[0], "Hannah")  # checking if fetched name is equal to "Hannah" or not
        connection.close()

    # Checking if artwork is deleted or not
    def test_delete_artwork(self):
        artist_db.database_setup()
        artist1 = artist_db.Artist("Ulrich nelson", "ulrich@gmail.com")
        artist2 = artist_db.Artist("Katherina", "katherina@gmail.com")

        artwork1 = artist_db.Artwork("Dark", 78, artist1.name)
        artwork2 = artist_db.Artwork("Glass", 25, artist2.name)

        artist_db.insert_artist(artist1)  # adding artists
        artist_db.insert_artist(artist2)
        artist_db.add_artwork(artwork1)  # adding artwork
        artist_db.add_artwork(artwork2)

        artist_db.delete_an_artwork(artwork1.artwork)  # deleting a artwork by artwork name

        connection = sqlite3.connect(artist_db.DATABASE_FILENAME)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM artwork WHERE name = ?", (artwork1.artwork,))  # Selecting artwork by artwork name

        artwork_details = cursor.fetchall()
        connection.close()
        # we deleted the artwork, means the artwork does not exists in our database if we search it we will get zero row
        self.assertEqual(len(artwork_details), 0)

    # Checking if availability of an artwork is changed or not
    def test_change_availability(self):
        artist_db.database_setup()
        artist1 = artist_db.Artist("Ulrich nelson", "ulrich@gmail.com")
        artist2 = artist_db.Artist("Katherina", "katherina@gmail.com")

        artwork1 = artist_db.Artwork("Dark", 78, artist1.name)
        artwork2 = artist_db.Artwork("Glass", 25, artist2.name)

        artist_db.insert_artist(artist1)  # adding artist
        artist_db.insert_artist(artist2)
        artist_db.add_artwork(artwork1)   # adding artwork
        artist_db.add_artwork(artwork2)

        artist_db.change_availability(artwork1.artwork)  # changing availability of an artwork by an artwork name

        connection = sqlite3.connect(artist_db.DATABASE_FILENAME)
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        # Fetching artworks from artwork table by an artwork name
        cursor.execute("SELECT * FROM artwork WHERE name = ?", (artwork1.artwork,))
        details = cursor.fetchone()
        self.assertEqual(details["availability"], "sold")  # Checking if its availability is changed to "sold" or not

        # Repeating above process again
        artist_db.change_availability(artwork1.artwork)
        cursor.execute("SELECT * FROM artwork WHERE name = ?", (artwork1.artwork,))
        details = cursor.fetchone()
        self.assertEqual(details["availability"], "available")
        connection.close()


if __name__ == '__main__':
    unittest.main()
