"""
This Lambda function implements the backend behavior for the "training schedule" Alexa Skill.
built with the Amazon Alexa Skills Kit.
The Intent Schema and other artifacts can be found at https://github.com/kennyk65/alexa-skill-training-schedule
"""

from __future__ import print_function
import boto3
import json
import datetime



# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
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


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to the Exit Certified training schedule sample.  " \
                    "You can ask me things like 'what is event ID', and then give me a number.. "
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please ask me for an event ID."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying the the Exit Certified training schedule sample. " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def create_instructor_attributes(instructor):
    return {"instructor": instructor}


def set_instructor_in_session(intent, session):
    """ Sets the instructor in the session and prepares the speech to reply to the
    user.
    """

    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

    if 'InstructorName' in intent['slots']:
        instructor = intent['slots']['InstructorName']['value']
        session_attributes = create_instructor_attributes(instructor)
        reprompt_text = "You can now ask me things about your schedule such as 'what's next on my schedule?' or 'where am I supposed to go next week?'"
        speech_output = "Thanks, now I understand you are listed as " + instructor + " on the schedule." + \
                        reprompt_text
    else:
        speech_output = "I'm not sure which name you are under on the schedule, Please try again."
        reprompt_text = "I'm not sure which name you are listed on in the schedule. " \
                        "You can tell me your name by saying, " \
                        "call me Krueger or my name is Stapleton."
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def get_instructor_from_session(intent, session):
    session_attributes = {}
    reprompt_text = None
    should_end_session = False

    if session.get('attributes', {}) and "instructor" in session.get('attributes', {}):
        instructor = session['attributes']['instructor']
        speech_output = "I understand your name is " + instructor 
    else:
        speech_output = "I'm not sure what your name is on the schedule.  " \
                        "You can set your name by saying, 'call me Durst' or 'my name is Cory'."

    # Setting reprompt_text to None signifies that we do not want to reprompt
    # the user. If the user does not respond or says something that is not
    # understood, the session will end.
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))


# This function responds to questions like "What is event ID xxx".
# It responds with a verbal description of the event:
def get_event(intent, session):
    card_title = intent['name']
    should_end_session = False
    
    event_id = intent['slots']['eventId']['value']
    speech_output = "Event " + event_id + " is " + get_event_details(event_id)
    reprompt_text = ""
    session_attributes = {}
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


# This function queries our S3 CSV file for information about a specific event ID.
# It returns a verbal description of the event that was queried.
def get_event_details(event_id):
    returnValue = 'Unknown event'
    
    s3 = boto3.client('s3')
    r = s3.select_object_content(
        Bucket='training-schedule',
        Key='ready/current-schedule.csv',
        Expression='select * from s3object s where "Event ID" = \'' + event_id + '\'',
        ExpressionType="SQL", 
        InputSerialization={'CSV': {"FileHeaderInfo": "Use"}},
        OutputSerialization={'JSON': {}}
    )

    # The returned result is described here: https://boto3.readthedocs.io/en/latest/reference/services/s3.html#S3.Client.select_object_content
    # Basically, inside Payload.Records.Payload we find a string array containing JSON.
    # Convert it to a Python object and we are in business!
    for event in r['Payload']:
        if 'Records' in event:
            records = event['Records']['Payload'].decode('utf-8')
            print(records)
            trainingEvent = json.loads(records)
            return describe_event_details(trainingEvent)

    return returnValue


# Take the incoming object and extract information to describe the event verbally.
# trainingEvents look kinda like this sample:  
# { "Event ID":"105311",
#   "Start Date":"2018-07-02",
#   "End Date":"2018-07-02",
#   "Start Time":"10:30 AM",
#   "End Time":"6:30 PM",
#   "Timezone":"EDT",
#   "Event Type":"Class-PUB",
#   "Status":"CONF",
#   "Delivery Location":
#   "MVP-Studio",
#   "MVP":"Host",
#   "Vendor":"AWS",
#   "Course Code":"AWS-T-ESS",
#   "Course Title":"AWS Technical Essentials",
#   "Revision":"4.x (currently 4.3.2)",
#   "Partner ID":"",
#   "Students (OPS)":"0",
#   "Students (SF)":"0",
#   "Max Students":"12",
#   "Instructors":"Krueger (P)\r"}
def describe_event_details(trainingEvent):

    eventType = trainingEvent["Event Type"]
    # If eventType is STAT have Alexa say "this is a holiday on <start date>"
    if eventType == 'STAT':
      return "Holiday on " + trainingEvent["Start Date"]
    
    # If VAC have Alexa say "this is a vacation event for <Instructors>, from <start date> through <end date>"
    if eventType == 'VAC':
      return "Vacation for " + trainingEvent["Instructors"] + \
             " from " + trainingEvent["Start Date"] + " through " + trainingEvent["End Date"]
    
    # Otherwise,  Have Alexa say describe the event:
    return trainingEvent["Course Title"] + \
        " at " + trainingEvent["Delivery Location"] + \
        " delivered by " + trainingEvent["Instructors"] + \
        " starts on " + trainingEvent["Start Date"] + \
        " at " + trainingEvent["Start Time"] + " " + trainingEvent["Timezone"] + \
        " .  It ends on " + trainingEvent["End Date"] + \
        " and has " + trainingEvent["Students (OPS)"] + " enrolled students.  "


def describe_multiple_event_details(trainingEvents):
    description = ""
    for record in trainingEvents["records"]:
        description = description + describe_event_details(record)
    return description    

        
def whatIsOnTheScheduleFor(intent,session):
    card_title = intent['name']
    should_end_session = False
    
    instructor = intent['slots']['instructor']['value']
    speech_output = "Next on the schedule for " + instructor + ", " + get_upcoming_schedule(instructor)
    reprompt_text = ""
    session_attributes = {}
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
        

# This function queries our S3 CSV file for upcoming events for a particular instructor.
# It returns a verbal description of the events discovered.
def get_upcoming_schedule(instructor):
    returnValue = 'No upcoming events found, check the instructor name: ' + instructor
    today = getToday()
    
    s3 = boto3.client('s3')
    r = s3.select_object_content(
        Bucket='training-schedule',
        Key='ready/current-schedule.csv',
        Expression='select * from s3object s where "Instructors" like \'%' + instructor + '%\'  and "Start Date" > \'' + today + '\' and "MVP" = \'Host\'',
        ExpressionType="SQL", 
        InputSerialization={'CSV': {"FileHeaderInfo": "Use"}},
        OutputSerialization={'JSON': {"RecordDelimiter": ","}}  # Expecting multiple JSONs
    )

    # The returned result is described here: https://boto3.readthedocs.io/en/latest/reference/services/s3.html#S3.Client.select_object_content
    # Basically, inside Payload.Records.Payload we find a string array containing JSON.
    # Convert it to a Python object and we are in business!
    # TODO: ORDER BY IS NOT SUPPORTED IN THE S3 SELECT, SO I THINK THE ORDER COMES FROM THE ORIGINAL SPREADSHEET!
    for event in r['Payload']:
        if 'Records' in event:
            records = event['Records']['Payload'].decode('utf-8')
            
            records = "{\"records\": [" + records[0:len(records)-1] + "]}"
            print(records)
            trainingEvents = json.loads(records)
            return describe_multiple_event_details(trainingEvents)

    return returnValue

# Returns today's date in a format that works well with the CSV file we have, YYYY-MM-DD.
def getToday():
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d")
    
    

# The intent we got from Alexa don't make no sense:
def handle_bad_intent(intent):
    card_title = "Unknown Intent"
    should_end_session = False

    speech_output = "Sorry, I couldn't determine your intent.  I understood '" + intent['name'] + "' as the intent."
    reprompt_text = ""
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """
    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they want """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'] +
          ", intent_name=" + intent_name)

    # Dispatch to your skill's intent handlers
    if intent_name == "getEventId":
        return get_event(intent, session)
    if intent_name == "whatIsOnTheScheduleFor":
        return whatIsOnTheScheduleFor(intent, session)
    if intent_name == "MyNameIsIntent":
        return set_color_in_session(intent, session)
    elif intent_name == "WhatsMyName":
        return get_color_from_session(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        return handle_bad_intent(intent)
#        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.
    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    # print(event)
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    if (event['session']['application']['applicationId'] !=
            "amzn1.ask.skill.cb877bae-48b6-4d10-9e9c-3d28f4c42c18"):
        raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']}, event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
