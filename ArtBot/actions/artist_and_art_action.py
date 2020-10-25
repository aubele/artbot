from typing import Any, Text, Dict

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

from actions import helper_functions as helper
from actions import artist_and_art_output as output


class ActionFetchArtWithArtist(Action):

    def name(self):
        """
        Name from the action used for the assignment from Rasa stories.

        Returns:
        string: Name from the action
        """
        return "action_fetch_art_with_artist"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]):
        """
        Action to determine the correct output for the given values/entities: artist and art.

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

        # check both
        if user_artist is None or user_art is None:
            dispatcher.utter_message(template="utter_unknown")
            # set artist and art back to None since they are irrelevant in this scenario
            return [SlotSet("artist", None), SlotSet("art", None)]

        # artist is unknown
        if not helper.check_artist_exists(user_artist):
            dispatcher.utter_message(template="utter_wrong_artist")
            # fetch all artists
            dispatcher.utter_message(helper.get_all_artists_as_string())
            # set artist and art back to None since they are irrelevant in this scenario
            return [SlotSet("artist", None), SlotSet("art", None)]

        # if art is unknown
        if not helper.check_art_exists(user_art):
            dispatcher.utter_message(template="utter_wrong_art")
            # set artist and art back to None since they are irrelevant in this scenario
            return [SlotSet("artist", None), SlotSet("art", None)]

        # function to determine the correct output for artist and art
        output.show_art_with_artist(user_art, user_artist, dispatcher, True)

        # set artist and art back to None since else a there is a conflict when the user just asks for art and the
        # artist is saved
        return [SlotSet("artist", None), SlotSet("art", None)]
