## tell wrong art
* tell_art_and_artist{"artist": "Claude Monet"}
    - slot{"artist": "Claude Monet"}
    - slot{"artist": "Claude Monet"}
    - action_fetch_artist
    - slot{"artist": "None"}
* goodbye
    - utter_goodbye
* tell_art_and_artist
    - utter_wrong_art   <!-- predicted: utter_unknown -->


