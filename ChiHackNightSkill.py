"""
ChiHackNightSkill.py
"""

import urllib2
import json

devo_application_id = "amzn1.echo-sdk-ams.app.987e0809-da10-4883-bb3c-a77bc1c61679"
valid_application_ids = (devo_application_id)

def lambda_handler(event, context):
    """ Prevent someone else from configuring a skill that sends requests to this function. """
    application_id = event['session']['application']['applicationId']
    print("event.session.application.applicationId=" + application_id)
    if (application_id not in valid_application_ids):
        raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])


def on_session_started(session_started_request, session):
    """ Called when the session starts """
    log("on_session_started", session_started_request, session)


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they want """
    log("on_launch", launch_request, session)

    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """
    log("on_intent", intent_request, session)

    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "WelcomeIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")

def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.
    Is not called when the skill returns should_end_session=true """
    log("on_session_ended", session_ended_request, session)
    # add cleanup logic here

def log(func_name, request, session):
    print(func_name + " requestId=" + request['requestId'] + ", sessionId=" + session['sessionId'])

# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():

    session_attributes = {}
    card_title = "Welcome"
    # TODO: Chai Hack Night!
    speech_output = "Tonight at Chai Hack Night, we will learn how to create an Alexa Skill. " \
                    "Then we will brainstorm ideas for a skill to build together."
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please try again by saying, tell me about tonight's breakout group."
    should_end_session = True
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))



def handle_session_end_request():
    card_title = "Session Ended"
    # TODO: Chai Hack Night!
    speech_output = "Thank you for trying the Chai Hack Night Skill. " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))



# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session, image=""):
    card = {}
    if image == "":
        card['type'] = 'Simple'
        card['content'] = title
    else:
        card['type'] = 'Standard'
        card['image'] = {'smallImageUrl': image, 'largeImageUrl': image}
        card['text'] = title
    card['title'] = title

    return {
        'outputSpeech': {
            'type': 'PlainText',  #'SSML', # Indicates that the output speech is text marked up with SSML.
            'text': output
        },
        'card': card,
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }
