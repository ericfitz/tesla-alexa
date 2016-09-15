# tesla-alexa
Code and files to connect Amazon Echo ("Alexa") to Tesla automobiles
Tesla voice user interface for Alexa climate control precondition skill

(c) Eric Fitzgerald (ericf@hushmail.com)
MIT License (do what you want with it but mention where you got it)
No warranties, express or implied.  Use at your own risk.

Tesla might change their interface at any time, without notice.  The API is not public; it was reverse engineered by Tim Dorr.

This file describes the voice user interface for the Alexa skill.

The skill invokes an AWS Lambda function that turns on or off the Tesla's climate
control system.  The skill does not attempt to set a temperature.

The Lambda function is hard coded to work against the first Tesla in your account.
If you have more than one, then you'll have to modify the code yourself.

Alexa SDK: https://developer.amazon.com/appsandservices/solutions/alexa/alexa-skills-kit/getting-started-guide

I have only tried this as an Alexa custom skill; I doubt it will work as a Smart Home skill.

Intents
=======
Intents specifies the interaction model between the user and the Alexa skill.
I define 3 intents:
*"WakeUpTesla": Wake up the car (in case it's asleep)
*"PreconditionTesla": Precondition the car (turn on the climate control system)
*"TeslaOff": Turn off the climate control system

The intents are provided to the Alexa skills engine as a JSON file, and are referenced in the Lambda code that executes the skill.

You'll have to paste the "intents" JSON into the Alexa SDK.

I chose invocation name "Tesla"

Intents File
------------
```
{
  "intents": [
    {
      "intent": "WakeUpTesla"
    },
    {
      "intent": "PreconditionTesla"
    },
    {
      "intent": "TeslaOff"
    }
  ]
}
```

Utterances
==========
Utterances are the words that humans will say to the Echo to invoke and manipulate the skill.

The default utterance format will be "Alexa, tell Tesla to <intent>" (assuming you choose "Tesla" as the invocation name).
e.g. "Alexa, tell Tesla to precondition".
An alternate, acceptable utterance is "Alexa, start Tesla and precondition"

The more utterance phrases you have, the more flexible Alexa will be in how you invoke the skill.

Note that in the utterances file, each utterance begins with the name of an intent, and then has one or more works associated with the intent.

You'll have to paste these utterances phrases into the Alexa SDK.

Utterances File
---------------
```
WakeUpTesla wake up
PreconditionTesla warm up
PreconditionTesla cool down
PreconditionTesla start
PreconditionTesla precondition
TeslaOff turn off
TeslaOff sleep
```

For reference, this is a sample JSON document returned by the Tesla API:

```
{
    "calendar_enabled": true,
    "remote_start_enabled": true,
    "vehicle_id": 1234567890,
    "display_name": "85D",
    "color": null,
    "backseat_token": null,
    "notifications_enabled": true,
    "vin": "9XXXXX9X99XX999999",
    "backseat_token_updated_at": null,
    "id": 12345678901234567,
    "tokens": [
        "99aaa9999b99c9df",
        "9aa99999e9e9cafb"
    ],
    "id_s": "12345678901234567",
    "state": "online",
    "option_codes": "MS04,RENA,AU01,BC0B,BP00,BR00,BS00,BT85,CDM0,CH00,PPTI,CW02,DA02,DCF0,DRLH,DSH7,DV4W,FG02,HP00,IDCF,IX01,LP01,ME02,MI00,PA00,PF00,PI01,PK00,PS01,PX00,QNET,RFP2,SC01,SP00,SR01,SU01,TM00,TP03,TR00,UTAB,WT19,WTX1,X001,X003,X007,X011,X013,X021,X025,X027,X028,X031,X037,X040,YF00,COUS"
}
```

If you ever decode the option_codes, please drop me a line.  I'd love to understand what they mean.
