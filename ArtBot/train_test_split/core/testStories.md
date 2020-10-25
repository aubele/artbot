## say hello
* tell_art_and_artist{"art": "Mona Lisa"}
  - slot{"art": "Mona Lisa"}
  - action_fetch_art
  - slot{"art": "None"}
* greet
  - action_greet
* goodbye
  - utter_goodbye

## say goodbye
* goodbye
  - utter_goodbye
* tell_art_and_artist{"artist": "Claude Monet", "art": "Mona Lisa"}
  - slot{"artist": "Claude Monet"}
  - slot{"art": "Mona Lisa"}
  - action_fetch_art_with_artist
  - slot{"artist": "None"}
  - slot{"art": "None"}
* bot_challenge
  - utter_iamabot
  
## tell artist and art twice
* tell_art_and_artist{"artist": "Claude Monet", "art": "Mona Lisa"}
  - slot{"artist": "Claude Monet"}
  - slot{"art": "Mona Lisa"}
  - action_fetch_art_with_artist
  - slot{"artist": "None"}
  - slot{"art": "None"}
* want_art
  - utter_ask_art_and_artist
* tell_art_and_artist{"artist": "Claude Monet", "art": "Mona Lisa"}
  - slot{"artist": "Claude Monet"}
  - slot{"art": "Mona Lisa"}
  - action_fetch_art_with_artist
  - slot{"artist": "None"}
  - slot{"art": "None"}
* tell_art_and_artist
  - utter_unknown
  
  
## tell artist + tell art
* tell_art_and_artist{"artist": "Claude Monet"}
  - slot{"artist": "Claude Monet"}
  - action_fetch_artist
  - slot{"artist": "None"}
* greet
  - action_greet
* tell_art_and_artist{"artist": "Claude Monet", "art": "Mona Lisa"}
  - slot{"artist": "Claude Monet"}
  - slot{"art": "Mona Lisa"}
  - action_fetch_art_with_artist
  - slot{"artist": "None"}
  - slot{"art": "None"}

## tell artist + tell art + tell art
* tell_art_and_artist{"artist": "Claude Monet"}
  - slot{"artist": "Claude Monet"}
  - action_fetch_artist
  - slot{"artist": "None"}
* tell_art_and_artist{"artist": "Claude Monet", "art": "Mona Lisa"}
  - slot{"artist": "Claude Monet"}
  - slot{"art": "Mona Lisa"}
  - action_fetch_art_with_artist
  - slot{"artist": "None"}
  - slot{"art": "None"}
* tell_art_and_artist{"art": "Mona Lisa"}
  - slot{"art": "Mona Lisa"}
  - action_fetch_art
  - slot{"art": "None"}

## tell wrong art
* tell_art_and_artist{"artist": "Claude Monet"}
  - slot{"artist": "Claude Monet"}
  - action_fetch_artist
  - slot{"artist": "None"}
* goodbye
  - utter_goodbye
* tell_art_and_artist
  - utter_wrong_art

## tell wrong art and then correct art
* tell_art_and_artist{"artist": "Claude Monet"}
  - slot{"artist": "Claude Monet"}
  - action_fetch_artist
  - slot{"artist": "None"}
* tell_art_and_artist
  - utter_wrong_art
* tell_art_and_artist{"art": "Mona Lisa"}
  - slot{"art": "Mona Lisa"}
  - action_fetch_art
  - slot{"art": "None"}

## tell artist twice + wrong art
* tell_art_and_artist{"artist": "Claude Monet", "art": "Mona Lisa"}
  - slot{"artist": "Claude Monet"}
  - slot{"art": "Mona Lisa"}
  - action_fetch_art_with_artist
  - slot{"artist": "None"}
  - slot{"art": "None"}
* want_art
  - utter_ask_art_and_artist
* greet
  - action_greet
* tell_art_and_artist{"artist": "Claude Monet"}
  - slot{"artist": "Claude Monet"}
  - action_fetch_artist
  - slot{"artist": "None"}

## tell artist twice + art
* tell_art_and_artist{"artist": "Claude Monet"}
  - slot{"artist": "Claude Monet"}
  - action_fetch_artist
  - slot{"artist": "None"}
* tell_art_and_artist
  - utter_wrong_art
* tell_art_and_artist{"art": "Mona Lisa"}
  - slot{"art": "Mona Lisa"}
  - action_fetch_art
  - slot{"art": "None"}