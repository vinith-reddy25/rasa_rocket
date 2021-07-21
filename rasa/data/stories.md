## happy path
* greet
  - utter_greet


## sad path 1
* greet
  - utter_greet
* mood_unhappy
  - utter_cheer_up
  - utter_did_that_help
* affirm
  - utter_happy

## sad path 2
* greet
  - utter_greet
* mood_unhappy
  - utter_cheer_up
  - utter_did_that_help
* deny
  - utter_goodbye

## say goodbye
* goodbye
  - utter_goodbye

## bot challenge
* bot_challenge
  - utter_iamabot

## check mail
* greet
  - utter_greet
* mailing
  - action_hello_world


## survey api
* greet
  - utter_greet
* apicall
  - action_get_user

## survey specificuser
* greet
  - utter_greet
* specificuser
  - action_get_specific_user

## survey details
* greet
  - utter_greet
* affirm
  - details_form
  - form{"name":"details_form"}
  - form{"name":"null"}
  - utter_slots_values
* affirm
  - utter_goodbye
  