# tesla-alexa
Code and files to connect Amazon Echo ("Alexa") to Tesla automobiles
Tesla voice user interface for Alexa climate control precondition skill

(c) 2016 Eric Fitzgerald (ericf@hushmail.com)

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

Setup
=====

Basic overview:

1. Buy a Tesla, set up a my.teslamotors.com username and password and connect your car to the mobile app using those creds.
2. Buy an Amazon Echo and set it up.
3. Log into [AWS](https://aws.amazon.com).
4. Navigate to the IAM console, and choose "encryption keys".  Create a new encryption key.  Give it an alias like "teslapw" (it will be used to encrypt your Tesla password so we don't have to store plaintext anywhere).  The key source is KMS.
5. Choose key administators and key users for your new key.  We'll come back to this later.
6. Navigate to the US East (Northern Virginia) region (this is the only region supported by Alexa at this time.
7. Use the Lambda console to create a new function using the Python 2.7 blueprint "Alexa-skills-color-expert-python".  [Reference](https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit/docs/developing-an-alexa-skill-as-a-lambda-function)
8. Choose "Alexa skills kit" as the trigger for the function.  Highlight all the existing python code in the code editor, and replace it with the code from the awslambda-tesla-precondition.py file in this repository.
9. Have the new Lambda function wizard create a new role for the function.
10. After you finish creating the function, make a note of the ARN for the Lambda function (in the upper right-hand corner of the Lambda console when viewing the function).
11. Log into the Amazon Developer Portal using your Amazon account and choose "create an Alexa skill now": https://developer.amazon.com/alexa-skills-kit
12. Type a skill name.  Skill type is "custom interaction".  Invocation name is "Tesla" (this is what you will use to tell Alexa to interact with the Tesla). Audio player: no.
13. Paste the intent schema (json above) and the sample utterances (text above) into the new skill.  Add or edit utterances if you choose.
14. Under configuration/Global fields, choose the "AWS Lambda ARN" endpoint type, choose "North America", and paste in the ARN of the Lambda function you created a moment ago.  "Account linking" should be no.
15. Go back to the AWS console, to IAM, Encryption keys, and add "encrypt & decrypt" permission for the Lambda role you created above.
16. Use the [AWS command line interface](https://aws.amazon.com/cli/) to encrypt your Tesla password with the key that you created above, e.g. "aws cli kms encrypt --key-id alias/(whatever-you-named-it) --plaintext "your-tesla-password-goes-here".  If your password has a dollar sign in it, you have to escape it with a backslash before you encrypt.
17. Copy the contents of the ciphertext field, and paste them into the "ciphertextBlob" variable on line 74 of the Lambda function python code.
18. Edit line 71 of the Lambda function and enter the email address you use for your Tesla login.
19. Save the Lambda function.

At this point, the skill is active and is private to your Amazon account.  Do not try to publish the skill; the Tesla name is trademarked, the API is private, and you don't want random people controlling your Tesla.
