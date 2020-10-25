from typing import Any, Text, Dict

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

import random

import database_api as api
from actions import helper_functions as helper
from actions import artist_and_art_output as output


class ActionFetchArt(Action):

    def name(self):
        """
        Name from the action used for the assignment from Rasa stories.

        Returns:
        string: Name from the action
        """
        return "action_fetch_art"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]):
        """
        Action to determine the correct output for the given value/entity: art.
        Also handles the case when an artist is already set.

        Parameters:
        dispatcher (object): Instance from Rasa to let the Chatbot print messages
        tracker (object): Maintain the state of a dialogue between the assistant and the user
        domain (dict): The custom domain of the Chatbot

        Returns:
        list: Multiple SlotSets, which set the given slot on the given value
        """
        # get slots
        user_art = tracker.get_slot('art')
        user_artist = tracker.get_slot('artist')

        # check art
        if user_art is None:
            dispatcher.utter_message(template="utter_unknown")
            # set art back to None since its irrelevant for later usage
            return [SlotSet("art", None)]

        # check artist
        if user_artist is None:
            # no artist is set -> show art without artist
            self.show_art_without_artist(user_art, dispatcher)
            # set art back to None since its irrelevant for later usage
            return [SlotSet("art", None)]
        # when an artist is already set, that also means the artist exists in the database -> show art with artist
        else:
            output.show_art_with_artist(user_art, user_artist, dispatcher, False)
            # set art back to None since its irrelevant for later usage
            return [SlotSet("art", None)]

    def show_art_without_artist(self, user_art, dispatcher):
        """
        Parses the output for the case that the user only gives the art without the artist.

        Parameters:
        user_art (string): Input for the art from the user
        dispatcher (object): Instance from Rasa to let the chatbot print messages

        Returns:
        None
        """
        # fetch images
        all_images = api.get_pictures_by_title(user_art)
        # no images
        if len(all_images) == 0:
            dispatcher.utter_message(template="utter_wrong_art")
        # one image
        elif len(all_images) == 1:
            # creates output for the user
            self.create_output_for_art(user_art, all_images, True, dispatcher)
            # show image
            dispatcher.utter_message(image=helper.img_path + all_images[0][0])
            dispatcher.utter_message(template="utter_ask_more_art")
        # more images
        else:
            # check if an exact image title exists
            exact_image = api.get_picture_by_exact_title(user_art)
            if len(exact_image) == 1:
                # creates output for the user
                self.create_output_for_art(user_art, exact_image, False, dispatcher)
                # show image
                dispatcher.utter_message(image=helper.img_path + exact_image[0][0])
                dispatcher.utter_message(template="utter_ask_more_art")
            # multiple images with same title
            else:
                dispatcher.utter_message(template="utter_vague")
                # fetch all images as list with just the names in it
                output_art = ""
                for alternative in helper.get_all_image_names_as_list(all_images):
                    output_art += "- " + str(alternative) + "\n"
                dispatcher.utter_message(output_art)

        return

    @staticmethod
    def create_output_for_art(user_art, image, compare_art, dispatcher):
        """
        Parses the output for the case that the artist and art is given and both values are unique.

        Parameters:
        user_art (string): Input for the art from the user
        image (list): The row from the database, which contains all necessary information (always only one image)
        compare_art (bool): Signalises if artist needs to be compared to the db value
        dispatcher (object): Instance from Rasa to let the chatbot print messages

        Returns:
        None
        """
        # compare art
        if compare_art:
            helper.check_user_input_equals_db_value(user_art, image[0][1], False, dispatcher)

        # pick one message random
        messages = ["Hier das gewünschte Bild " + str(image[0][1]) + ".",
                    "Du solltest jetzt das Bild " + str(image[0][1]) + " betrachten können.",
                    "Ich hoffe dir gefällt das gewünschte Kunstwerk " + str(image[0][1]) + "."]
        dispatcher.utter_message(messages[random.randrange(2)])
        return
