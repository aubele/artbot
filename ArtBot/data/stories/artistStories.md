## tell artist + tell art
* tell_art_and_artist{"artist": "Claude Monet"}
  - slot{"artist": "Claude Monet"}
  - action_fetch_artist
  - slot{"artist": "None"}
* tell_art_and_artist{"art": "Mona Lisa"}
  - slot{"art": "Mona Lisa"}
  - action_fetch_art
  - slot{"art": "None"}

## tell artist + tell art + tell art
* tell_art_and_artist{"artist": "Claude Monet"}
  - slot{"artist": "Claude Monet"}
  - action_fetch_artist
  - slot{"artist": "None"}
* tell_art_and_artist{"art": "Mona Lisa"}
  - slot{"art": "Mona Lisa"}
  - action_fetch_art
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
* tell_art_and_artist{"artist": "Claude Monet"}
  - slot{"artist": "Claude Monet"}
  - action_fetch_artist
  - slot{"artist": "None"}
* tell_art_and_artist{"artist": "Claude Monet"}
  - slot{"artist": "Claude Monet"}
  - action_fetch_artist
  - slot{"artist": "None"}
* tell_art_and_artist
  - utter_wrong_art

## tell artist twice + art
* tell_art_and_artist{"artist": "Claude Monet"}
  - slot{"artist": "Claude Monet"}
  - action_fetch_artist
  - slot{"artist": "None"}
* tell_art_and_artist{"artist": "Claude Monet"}
  - slot{"artist": "Claude Monet"}
  - action_fetch_artist
  - slot{"artist": "None"}
* tell_art_and_artist{"art": "Mona Lisa"}
  - slot{"art": "Mona Lisa"}
  - action_fetch_art
  - slot{"art": "None"}