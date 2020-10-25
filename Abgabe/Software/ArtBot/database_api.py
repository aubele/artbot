import sqlite3
from sqlite3 import Error


def open_db(db_file="./art.db"):
    """
    Open, or create the database if it is not exsisting and returns the connection.

    Parameters:
    db_file(String): Path to the database file

    Returns:
    connection(sqlite3.Connection): The connection to the database
    """
    connnection = None
    try:
        connection = sqlite3.connect(db_file)
        connection.execute("PRAGMA foreign_keys = 1")
        return connection
    except Error as e:
        print(e)
    return connection


def close_db(connection):
    """
    Closes the connection to the database.

    Parameters:
    connection(sqlite3.Connection): The connection to the database, that should get closed

    Returns:
    None
    """
    try:
        connection.close()
    except Error as e:
        print(e)


def set_up_db():
    """
    Initialize the database with the two tables pictures and artists and their values.

    Parameters:
    None

    Returns:
    None
    """

    connection = open_db()
    cursor = connection.cursor()

    cursor.execute("DROP TABLE IF EXISTS pictures;")
    cursor.execute("DROP TABLE IF EXISTS artists;")

    setup_artists = """
        CREATE TABLE artists(
        name VARCHAR(50) NOT NULL PRIMARY KEY,
        birth DATE NOT NULL);
    """
    cursor.execute(setup_artists)

    setup_pictures = """
        CREATE TABLE pictures(
        filename VARCHAR(50) PRIMARY KEY,
        title VARCHAR(100),
        epoch VARCHAR(50),
        genre VARCHAR(50),
        artist VARCHAR(50),
        FOREIGN KEY (artist) REFERENCES artists(name));
    """
    cursor.execute(setup_pictures)

    connection.commit()
    close_db(connection)


def insert_artist(artist, birth):
    """
    Inserts an artist into the artist table.

    Parameters:
    artist(string): the name of the artist
    birth(string): the birth of the artist

    Returns:
    None
    """
    connection = open_db()
    cursor = connection.cursor()
    insert_artist = "INSERT INTO artists (name, birth) VALUES (?,?)"
    data_tuple = (artist, birth)
    cursor.execute(insert_artist, data_tuple)
    connection.commit()
    close_db(connection)


def insert_picture(filename, title, artist, epoch, genre):
    """
    Inserts a picture into the picture table in the database.

    Parameters:
    filename(string): the filename of the picture
    title(string): the title of the picture
    artist(string): the name of the artist
    epoch(string): the epoch of the picture
    genre(string): the genre of the picture

    Returns:
    None
    """
    connection = open_db()
    cursor = connection.cursor()
    insert_picture = "INSERT INTO pictures (filename, title, epoch, genre, artist) VALUES (?,?,?,?,?)"
    data_tuple = (filename, title, epoch, genre, artist)
    cursor.execute(insert_picture, data_tuple)
    connection.commit()
    close_db(connection)


def delete_artist(artist):
    """
    Deletes the artist with the given name.

    Parameters:
    artist(string): the name of the artist

    Returns:
    None
    """
    connection = open_db()
    cursor = connection.cursor()
    delete_command = "DELETE FROM artists WHERE name= ?;"
    cursor.execute(delete_command, artist)
    connection.commit()
    close_db(connection)


def delete_picture(filename):
    """
    Deletes the picture with the given filename in the picture table.

    Parameters:
    filename(string): the name of the file of the picture

    Returns:
    None
    """
    connection = open_db()
    cursor = connection.cursor()
    delete_command = "DELETE FROM pictures WHERE filename= ?;"
    cursor.execute(delete_command, filename)
    connection.commit()
    close_db(connection)


def get_artist(name):
    """
    Returns the artists with the given name.

    Parameters:
    name(string): a partstring or a full name of an artist

    Returns:
    artists(list): a list of all artists with the given string in their name
    """
    connection = open_db()
    cursor = connection.cursor()
    get_command = "SELECT * FROM artists WHERE instr(LOWER(name), ?) >= 1;"
    cursor.execute(get_command, (name.lower(),))
    record = cursor.fetchall()
    close_db(connection)
    artists = []
    for row in record:
        artists.append(row[0])
    return artists


def get_artists_birth(name):
    """
    Returns the birth of an artist, whose name is given. It must be the exact name.

    Parameters:
    name(string): the name of the artist

    Returns:
    birth(string): the birthday of the artist
    """
    connection = open_db()
    cursor = connection.cursor()
    get_command = "SELECT * FROM artists WHERE name = ?;"
    cursor.execute(get_command, (name,))
    record = cursor.fetchall()
    close_db(connection)
    return record[0][1]


def get_pictures_by_title(title):
    """
    Returns the pictures with the given title.

    Parameters:
    title(string): the title of the picture

    Returns:
    pictures(list): a list of tuples of all pictures with the given title, containing the filename, the title, the epoch,
    the genre and the artist
    """
    connection = open_db()
    cursor = connection.cursor()
    get_command = "SELECT * FROM pictures WHERE instr(LOWER(title), ?) >= 1;"
    cursor.execute(get_command, (title.lower(),))
    record = cursor.fetchall()
    close_db(connection)
    return record



def get_pictures_by_artist(artist):
    """
    Returns the pictures of a given artist

    Parameters:
    artist(string): the name of the artist

    Returns:
    pictures(list): a list of tuples of all pictures from the given artist, containing the filename, the title, the epoch,
    the genre and the artist
    """
    connection = open_db()
    cursor = connection.cursor()
    get_command = "SELECT * FROM pictures WHERE instr(LOWER(artist), ?) >= 1;"
    cursor.execute(get_command, (artist.lower(),))
    record = cursor.fetchall()
    close_db(connection)
    return record


def get_picture_by_title_and_artist(title, artist):
    """
    Returns the picture with the given title and artist, checks for containing strings.

    Parameters:
    title(string): the title of the picture
    artist(string): the name of the artist

    Returns:
    pictures(list): a list of tuples of all pictures with the given title and artist, containing the filename,
    the title, the epoch, the genre and the artist
    """
    connection = open_db()
    cursor = connection.cursor()
    get_command = "SELECT * FROM pictures WHERE (instr(LOWER(artist), ?) >= 1) AND (instr(LOWER(title), ?) >= 1);"
    data_tuple = (artist.lower(), title.lower())
    cursor.execute(get_command, data_tuple)
    record = cursor.fetchall()
    close_db(connection)
    return record


def get_picture_by_exact_title_and_artist(title, artist):
    """
    Returns the picture with the given title and artist. The given strings must be the exact title and artistname.

    Parameters:
    title(string): the exact title of the picture
    artist(string): the exact name of the artist

    Returns:
    pictures(list): a list of tuples of all pictures with the given title and artist, containing the filename,
    the title, the epoch, the genre and the artist
    """
    connection = open_db()
    cursor = connection.cursor()
    get_command = "SELECT * FROM pictures WHERE (instr(LOWER(artist), ?) >= 1)  AND (LOWER(title) =  ?);"
    data_tuple = (artist.lower(), title.lower())
    cursor.execute(get_command, data_tuple)
    record = cursor.fetchall()
    close_db(connection)
    return record


def get_picture_by_exact_title(title):
    """
    Returns the picture with the given title. The given string must be the exact title.

    Parameters:
    title(string): The exact title of the picture

    Returns:
    pictures(list): a list of tuples of all pictures with the given title, containing the filename, the title, the epoch,
    the genre and the artist
    """
    connection = open_db()
    cursor = connection.cursor()
    get_command = "SELECT * FROM pictures WHERE (LOWER(title) = ?);"
    cursor.execute(get_command, (title.lower(),))
    record = cursor.fetchall()
    close_db(connection)
    return record


def get_random_picture():
    """
    Returns a random picture.

    Parameters:
    None

    Returns:
    picture(tuple): a tuple containing the filename, the title, the epoch, the genre and the artist
    """
    connection = open_db()
    cursor = connection.cursor()
    get_command = "SELECT * FROM pictures ORDER BY RANDOM() LIMIT 1;"
    cursor.execute(get_command)
    record = cursor.fetchall()
    close_db(connection)
    return record


def get_random_picture_by_artist(artist):
    """
    Returns a random picture from the given artist.

    Parameters:
    artist(string): the name of the artist

    Returns:
    picture(tuple): a tuple containing the filename, the title, the epoch, the genre and the artist
    """
    connection = open_db()
    cursor = connection.cursor()
    get_command = "SELECT * FROM pictures WHERE instr(LOWER(artist), ?) >= 1 ORDER BY RANDOM() LIMIT 1;"
    cursor.execute(get_command, (artist.lower(),))
    record = cursor.fetchall()
    close_db(connection)
    return record


def get_all_pictures():
    """
    Returns all pictures in the database.

    Parameters:
    None
    Returns:
    pictures(list): a list of tuples of all pictures containing the filename, the title, the epoch,
    the genre and the artist
    """
    connection = open_db()
    cursor = connection.cursor()
    get_command = "SELECT * FROM pictures"
    cursor.execute(get_command)
    record = cursor.fetchall()
    close_db(connection)
    return record


def get_all_artists_with_births():
    """
    Returns all artists with their births.

    Parameters:
    None

    Returns:
    artists(dictionary): a dictionary with the artists as keys and the birth as value.
    """
    connection = open_db()
    cursor = connection.cursor()
    get_command = "SELECT * FROM artists"
    cursor.execute(get_command)
    record = cursor.fetchall()
    close_db(connection)
    artists = {}
    for row in record:
        artist = {row[0]: row[1]}
        artists.update(artist)
    return artists


def get_all_artists():
    """
    Returns all artists in the database.

    Parameters:
    None
    Returns:
    artists(list): a list with all artists
    """
    record = get_all_artists_with_births()
    artists = record.keys()
    return artists

if __name__ == '__main__':
    #open_db()
    re = get_all_artists()
    print(type(re))
    print(re)