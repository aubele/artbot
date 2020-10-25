from typing import Any, Text, Dict

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

import random

import database_api as api
from actions import helper_functions as helper


class ActionFetchArtist(Action):

    def name(self):
        """
        Name from the action used for the assignment from Rasa stories.

        Returns:
        string: Name from the action
        """
        return "action_fetch_artist"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]):
        """
        Action to determine the correct output for the given value/entity: artist.

        Parameters:
        dispatcher (object): Instance from Rasa to let the Chatbot print messages
        tracker (object): Maintain the state of a dialogue between the assistant and the user
        domain (dict): The custom domain of the Chatbot

        Returns:
        list: Multiple SlotSets, which set the given slot on the given value
        """
        # get and check slot
        user_artist = tracker.get_slot('artist')
        if user_artist is None:
            dispatcher.utter_message(template="utter_unknown")
            # set artist back to None since the artist is irrelevant
            return [SlotSet("artist", None)]

        # fetch the artists
        all_artists = api.get_artist(user_artist)
        # when there is no artist
        if len(all_artists) == 0:
            dispatcher.utter_message(template="utter_wrong_artist")
            # fetch all artists
            dispatcher.utter_message(helper.get_all_artists_as_string())
            # set artist back to None since the artist is irrelevant
            return [SlotSet("artist", None)]

        # when there is one artist
        elif len(all_artists) == 1:
            # check if artist got mentioned correctly from the user
            helper.check_user_input_equals_db_value(user_artist, all_artists[0], True, dispatcher)
            # random messages
            messages = ["Von dem Künstler " + str(all_artists[0]) + " haben wir folgende Bilder zur Auswahl:",
                        "Diese Bilder von dem Künstler " + str(all_artists[0]) + " kann ich dir zeigen:"]
            dispatcher.utter_message(messages[random.randrange(1)])

            # fetch the images
            all_images = api.get_pictures_by_artist(user_artist)
            output_art = ""
            for img in all_images:
                output_art += ("- " + str(img[1] + "\n"))
            dispatcher.utter_message(output_art)
            dispatcher.utter_message(template="utter_ask_art")

        # when there are multiple artists
        else:
            dispatcher.utter_message(template="utter_more_artists")
            output_artist = ""
            for artist in all_artists:
                output_artist += ("- " + str(artist + "\n"))
            dispatcher.utter_message(output_artist)

        return []
