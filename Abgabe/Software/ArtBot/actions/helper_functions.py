import database_api as api


# global variable for the path of the images
img_path = "./static/art/"


def check_user_input_equals_db_value(user_input, db_value, is_artist, dispatcher):
    """
    Checks if the given user_input is equal to the db_value and outputs an appropriate message.
    Differs between a given artist and art value.

    Parameters:
    user_input (string): Input from the user, either artist or art
    db_value (string): Appropriate value from the database, either artist or art
    is_artist (bool): True if the given value from the user is an artist
    dispatcher (object): Instance from Rasa to let the chatbot print messages

    Returns:
    bool: True if the user_input and the db_value is the same, else False
    """
    # compare values
    if user_input.lower() == db_value.lower():
        return True
    else:
        # output for artist
        if is_artist:
            dispatcher.utter_message("Für die Eingabe " + str(user_input) + " habe ich den Künstler " +
                                     str(db_value) + " gefunden.")
        # output for art
        else:
            dispatcher.utter_message("Für die Eingabe " + str(user_input) + " habe ich das Bild " +
                                     str(db_value) + " gefunden.")

    return False


def get_all_artists_as_string():
    """
    Return all artists from the database parsed as string.

    Returns:
    string: All artists in the database
    """
    # fetch all artists
    all_artists = api.get_all_artists()
    ret = ""
    # all artists as one string
    for artist in all_artists:
        ret += str(artist) + ", "
    # remove the last comma
    return ret[:-2]


def get_all_image_names_as_list(all_images):
    """
    Fetches the title from the given images and return them as a list.

    Parameters:
    all_images (list): Multiple images from the database as records

    Returns:
    list: Multiple images as strings
    """
    ret = []
    # only create the list when there are more then one
    if len(all_images) <= 1:
        return ret
    else:
        # create the list
        for image in all_images:
            ret.append(image[1])
    return ret


def check_artist_exists(user_artist):
    """
    Checks if the given artist exists in the database.

    Parameters:
    user_artist (string): Input for the artist from the user

    Returns:
    bool: Existence of the artist
    """
    # fetch artists
    artist_from_db = api.get_artist(user_artist)
    # check
    if len(artist_from_db) == 0:
        return False
    else:
        return True


def check_art_exists(user_art):
    """
    Checks if the given art exists in the database.

    Parameters:
    user_art (string): Input for the art from the user

    Returns:
    bool: Existence of the art
    """
    # fetch art
    art_from_db = api.get_pictures_by_title(user_art)
    # check
    if len(art_from_db) == 0:
        return False
    else:
        return True


def check_art_list_from_multiple_artists(user_art):
    """
    Checks if the given art stands for multiple images from multiple artists.

    Parameters:
    user_art (string):  Input for the art from the user

    Returns:
    bool: Existence of multiple artists
    """
    # fetch image
    images = api.get_pictures_by_title(user_art)
    # only check if there are more then one
    if len(images) <= 1:
        return False

    # artist is at index 5
    artist = images[0][4]
    for image in images:
        # if they are not the same return True
        if artist != image[4]:
            return True
        # check next artist
        else:
            artist = image[4]

    return False
