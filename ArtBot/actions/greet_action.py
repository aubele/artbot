from typing import Any, Text, Dict

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from actions import helper_functions as helper


class ActionGreet(Action):

    def name(self):
        return "action_greet"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]):
        # greet the user
        dispatcher.utter_message(template="utter_greet")
        # fetch all artists
        dispatcher.utter_message(helper.get_all_artists_as_string())

        return []
