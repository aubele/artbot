import random

import database_api as api
from actions import helper_functions as helper


def show_art_with_artist(user_art, user_artist, dispatcher, one_utterance):
    """
    Decides which output to print, based on the fetched image titles.
    There are different cases for no image, one image and multiple images.

    Parameters:
    user_art (string): Input for the art from the user
    user_artist (string): Input for the artist from the user
    dispatcher (object): Instance from Rasa to let the chatbot print messages
    one_utterance (bool): Signalises if artist and art got mentioned in one utterance from the user

    Returns:
    None
    """
    # get the image
    all_images = api.get_picture_by_title_and_artist(user_art, user_artist)

    # no image
    if len(all_images) == 0:
        dispatcher.utter_message(template="utter_wrong_art_from_artist")
    # one image
    elif len(all_images) == 1:
        # create output for the user
        create_output_for_artist_and_art(user_art, user_artist, all_images, one_utterance, True, dispatcher)
        # show image
        dispatcher.utter_message(image=helper.img_path + all_images[0][0])
        dispatcher.utter_message(template="utter_ask_more_art")
    # more images
    else:
        if one_utterance:
            # check if there are multiple artists
            all_artists = api.get_artist(user_artist)
            # no artist but can't happen since we checked this with the first API call
            if len(all_artists) == 0:
                dispatcher.utter_message(template="utter_unknown")
                return
            # multiple artists
            elif len(all_artists) > 1:
                dispatcher.utter_message(template="utter_more_artists")
                output = ""
                for artist in all_artists:
                    output += "- " + str(artist) + "\n"
                dispatcher.utter_message(output)
                return

        # just one artists
        # check if an exact image title exists
        exact_image = api.get_picture_by_exact_title_and_artist(user_art, user_artist)
        if len(exact_image) == 1:
            # create output for the user
            create_output_for_artist_and_art(user_art, user_artist, exact_image, one_utterance, False, dispatcher)
            # show image
            dispatcher.utter_message(image=helper.img_path + exact_image[0][0])
            dispatcher.utter_message(template="utter_ask_more_art")
        else:
            # check if artist got mentioned correctly from the user
            if one_utterance:
                helper.check_user_input_equals_db_value(user_artist, all_images[0][4], True, dispatcher)
            dispatcher.utter_message("Leider ist der angegebene Titel " + str(user_art) + " zu ungenau, da es mehrere "
                                     "Bilder von " + str(all_images[0][4]) + " gibt, die so heißen.\nFolgende Bilder "
                                     "stehen zur Auswahl:")
            # fetch all images as list with just the names in it
            output_alter = ""
            for alternative in helper.get_all_image_names_as_list(all_images):
                output_alter += "- " + str(alternative) + "\n"
            dispatcher.utter_message(output_alter)

    return


def create_output_for_artist_and_art(user_art, user_artist, image, compare_artist, compare_art, dispatcher):
    """
    Checks if the user input is equal to the real value and creates an output for the user.
    The given boolean values signalise what comparisons are needed

    Parameters:
    user_art (string): Input for the art from the user
    user_artist (string): Input for the artist from the user
    image (list): The row from the database, which contains all necessary information (always only one image)
    compare_artist (bool): Signalises if artist needs to be compared to the db value
    compare_art (bool): Signalises if artist needs to be compared to the db value
    dispatcher (object): Instance from Rasa to let the Chatbot print messages

    Returns:
    None
    """
    # check if artist got mentioned correctly from the user, based on one_utterance
    if compare_artist:
        helper.check_user_input_equals_db_value(user_artist, image[0][4], True, dispatcher)
        if compare_art:
            helper.check_user_input_equals_db_value(user_art, image[0][1], False, dispatcher)
    elif compare_art:
        helper.check_user_input_equals_db_value(user_art, image[0][1], False, dispatcher)

    # output message
    messages = ["Hier das gewünschte Bild " + str(image[0][1]) + " von " + str(image[0][4]) + ".",
                "Du solltest jetzt das Bild " + str(image[0][1]) + " von " + str(image[0][4]) + " betrachten können.",
                "Ich hoffe dir gefällt das gewüschte Kunstwerk " + str(image[0][1]) + " von " + str(image[0][4]) + "."]
    dispatcher.utter_message(messages[random.randrange(2)])

    return
