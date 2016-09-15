"""
This function implements an Alexa skill that invokes the Tesla API to turn on the climate control system.
It can be easily adapted to send any command supported by the Tesla API
(c) 2016 Eric Fitzgerald (ericf@hushmail.com)
MIT License
Based on work by Tim Dorr (Tesla API on Apiary) and Greg Glockner (Python client for Tesla API)
"""

from __future__ import print_function
from urllib import urlencode  # will only work with python 2.x; v3 use urllib.parse
from urllib2 import Request, urlopen  # will only work with python 2.x; v3 use urllib.request
import base64
import json
import boto3

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

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

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    #Tesla Motors username (same as used in Tesla mobile application)
    username = "your-email-address@your-email-provider.com"
    #Tesla Motors password, encrypted with AWS CLI using: aws kms encrypt --key-id alias/keyname --plaintext "yourpassword".  Copy the value of the "CiphertextBlob" field and set it in the next variable.
    #Special note: if your password has a dollar sign ("$") in it, then you need to escape the plaintext of your password with a backslash, e.g. "your$password" should be encrypted as "your\$password".  JSON wft
    ciphertextBlob = "AQXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    kms = boto3.client('kms')
    password = kms.decrypt(CiphertextBlob = base64.b64decode(ciphertextBlob))['Plaintext']

    # Dispatch to your skill's intent handlers
    if intent_name == "WakeUpTesla":
        return wake_up_tesla_in_session(intent, session, username, password)
    elif intent_name == "PreconditionTesla":
        return precondition_tesla_in_session(intent, session, username, password)
    elif intent_name == "TeslaOff":
        return turn_off_tesla_in_session(intent, session, username, password)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here

# --------------- Functions that control the skill's behavior ------------------


def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to the Tesla automobile preconditioner. " \
                    "Please tell me what to do by saying, " \
                    "precondition. " \
                    "You can also say: " \
                    "wake up " \
                    "or " \
                    "sleep."
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Welcome to the Tesla automobile preconditioner. " \
                    "Please tell me what to do by saying, " \
                    "precondition. " \
                    "You can also say: " \
                    "wake up " \
                    "or " \
                    "sleep."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "OK"
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def wake_up_tesla_in_session(intent, session, uname, pw):
    """
    Send the wake command to the Tesla.
    """

    session_attributes = {}
    reprompt_text = None
    # Setting reprompt_text to None signifies that we do not want to reprompt
    # the user. If the user does not respond or says something that is not
    # understood, the session will end.
    should_end_session = True

    speech_output = "Sending wake command to Tesla."

    c = Connection(uname, pw)
    v = c.vehicles[0]
    v.wake_up()

    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))


def precondition_tesla_in_session(intent, session, uname, pw):
    """
    Send the precondition command to the Tesla.
    """

    session_attributes = {}
    reprompt_text = None
    should_end_session = True

    speech_output = "Sending preconditioning start command to Tesla."

    c = Connection(uname, pw)
    v = c.vehicles[0]
    v.command('auto_conditioning_start')

    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))

def turn_off_tesla_in_session(intent, session, uname, pw):
    """
    Send the sleep command to the Tesla.
    """

    session_attributes = {}
    reprompt_text = None
    should_end_session = True

    speech_output = "Sending preconditioning stop command to Tesla."

    c = Connection(uname, pw)
    v = c.vehicles[0]
    v.command('auto_conditioning_stop')

    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))


# --------------- Helpers that build all of the responses ----------------------


def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': 'SessionSpeechlet - ' + title,
            'content': 'SessionSpeechlet - ' + output
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

#Tesla API reversing props to Tim Dorr http://docs.timdorr.apiary.io
#Tesla Python class props to Greg Glockner https://github.com/gglockner/teslajson
class Connection(object):
	"""Connection to Tesla Motors API"""
	def __init__(self,
			email='',
			password='',
			access_token='',
			url="https://owner-api.teslamotors.com",
			api="/api/1/",
			client_id = "e4a9949fcfa04068f59abb5a658f2bac0a3428e4652315490b659d5ab3f35a9e",
			client_secret = "c75f14bbadc8bee3a7594412c31416f8300256d7668ea7e6e7f06727bfb9d220"):
		"""Initialize connection object

		Sets the vehicles field, a list of Vehicle objects
		associated with your account

		Required parameters:
		email: your login for teslamotors.com
		password: your password for teslamotors.com

		Optional parameters:
		access_token: API access token
		url: base URL for the API
		api: API string
		client_id: API identifier
		client_secret: Secret API identifier
		"""
		self.url = url
		self.api = api
		if not access_token:
			oauth = {
				"grant_type" : "password",
				"client_id" : client_id,
				"client_secret" : client_secret,
				"email" : email,
				"password" : password }
			auth = self.__open("/oauth/token", data=oauth)
			access_token = auth['access_token']
		self.access_token = access_token
		self.head = {"Authorization": "Bearer %s" % self.access_token}
		self.vehicles = [Vehicle(v, self) for v in self.get('vehicles')['response']]

	def get(self, command):
		"""Utility command to get data from API"""
		return self.__open("%s%s" % (self.api, command), headers=self.head)

	def post(self, command, data={}):
		"""Utility command to post data to API"""
		return self.__open("%s%s" % (self.api, command), headers=self.head, data=data)

	def __open(self, url, headers={}, data=None):
		"""Raw urlopen command"""
		req = Request("%s%s" % (self.url, url), headers=headers)
		try:
			req.data = urlencode(data).encode('utf-8') # Python 3
		except:
			try:
				req.add_data(urlencode(data)) # Python 2
			except:
				pass
		resp = urlopen(req)
		charset = resp.info().get('charset', 'utf-8')
		return json.loads(resp.read().decode(charset))


class Vehicle(dict):
	"""Vehicle class, subclassed from dictionary.

	There are 3 primary methods: wake_up, data_request and command.
	data_request and command both require a name to specify the data
	or command, respectively. These names can be found in the
	Tesla JSON API."""
	def __init__(self, data, connection):
		"""Initialize vehicle class

		Called automatically by the Connection class
		"""
		super(Vehicle, self).__init__(data)
		self.connection = connection

	def data_request(self, name):
		"""Get vehicle data"""
		result = self.get('data_request/%s' % name)
		return result['response']

	def wake_up(self):
		"""Wake the vehicle"""
		return self.post('wake_up')

	def command(self, name, data={}):
		"""Run the command for the vehicle"""
		return self.post('command/%s' % name, data)

	def get(self, command):
		"""Utility command to get data from API"""
		return self.connection.get('vehicles/%i/%s' % (self['id'], command))

	def post(self, command, data={}):
		"""Utility command to post data to API"""
		return self.connection.post('vehicles/%i/%s' % (self['id'], command), data)
