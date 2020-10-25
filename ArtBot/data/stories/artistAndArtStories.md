## tell artist and art
* tell_art_and_artist{"artist": "Claude Monet", "art": "Mona Lisa"}
  - slot{"artist": "Claude Monet"}
  - slot{"art": "Mona Lisa"}
  - action_fetch_art_with_artist
  - slot{"artist": "None"}
  - slot{"art": "None"}
  
## tell wrong art and artist 
* tell_art_and_artist
  - utter_unknown
  
## tell artist and art twice
* tell_art_and_artist{"artist": "Claude Monet", "art": "Mona Lisa"}
  - slot{"artist": "Claude Monet"}
  - slot{"art": "Mona Lisa"}
  - action_fetch_art_with_artist
  - slot{"artist": "None"}
  - slot{"art": "None"}
* tell_art_and_artist{"artist": "Claude Monet", "art": "Mona Lisa"}
  - slot{"artist": "Claude Monet"}
  - slot{"art": "Mona Lisa"}
  - action_fetch_art_with_artist
  - slot{"artist": "None"}
  - slot{"art": "None"}