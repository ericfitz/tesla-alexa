# tesla-alexa
Code and files to connect Amazon Echo ("Alexa") to Tesla automobiles

(c) 2016-2020 Eric Fitzgerald (efitz@protonmail.com)

No warranties, express or implied.  Use at your own risk.  Tesla might change their interface at any time, without notice.  The API is not public; it was [reverse engineered by Tim Dorr](http://docs.timdorr.apiary.io/#).

The skill invokes an AWS Lambda function that turns on or off the Tesla's climate
control system.  The skill does not attempt to set a temperature.

The Lambda function is hard coded to work against the first Tesla in your account.
If you have more than one, then you'll have to modify the code yourself.

[Alexa SDK](https://developer.amazon.com/appsandservices/solutions/alexa/alexa-skills-kit/getting-started-guide)

I have only tried this as an Alexa custom skill; I doubt it will work as a Smart Home skill.

Intents
=======
Intents specify the interaction model between the user and the Alexa skill.
I define 3 intents:

* "WakeUpTesla": Wake up the car (in case it's asleep)
* "PreconditionTesla": Precondition the car (turn on the climate control system)
* "TeslaOff": Turn off the climate control system

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

Prerequisites
=============
1. Tesla app on mobile phone correctly set up to remotely control Tesla automobile; remote control functional.
2. Properly configured, working Amazon Echo
3. AWS account https://aws.amazon.com
4. Enrolled in Alexa developer program https://developer.amazon.com/alexa-skills-kit

Setup
=====

Basic overview:

1. Log into [AWS](https://aws.amazon.com).
2. Navigate to the US East (Northern Virginia) region (this is the only region supported by Alexa at this time.

CREATE AND CONFIGURE AN ENCRYPTION KEY
We're going to use the encryption key to encrypt your teslamotors.com password so we don't store the plaintext on AWS
3. Navigate to the Key Management Service (KMS) console, and choose "customer managed keys".
4. Create a new encryption key.  Give it an alias like "teslapw" (it will be used to encrypt your Tesla password so we don't have to store plaintext anywhere).
5. Choose key administators and key users for your new key.  We'll come back to this later.

NOTE ON AWS costs: The key will cost you $1.00 per month.  Key usage will be $0.01 per month.  Lambda usage will be low enough that you don't get billed.

CREATE AND CONFIGURE THE LAMBDA FUNCTION
6. Navigate to the Lambda console.
7. Use the Lambda console to create a new Lambda function.
     Choose "Author from scratch"
     Choose the Python 3.7 runtime
     Give the function a name
     Under "execution role", choose "Create a new role with basic Lambda permissions"
     Create the function
8. Under "designer", choose "Add trigger", and add "Alexa skills kit" as the trigger for the function.  Disable function verification.
9. In the function code pane, highlight all the existing code and replace it with the contents of the awslambda-tesla-precondition.py file in this repository.
10. Save the Lambda function.
11. After you finish creating the function, make a note of the ARN for the Lambda function (in the upper right-hand corner of the Lambda console when viewing the function).

CONFIGURE THE ALEXA SKILL
12. Log into the Amazon Developer Portal using your Amazon account and choose "create an Alexa skill now": https://developer.amazon.com/alexa-skills-kit
13. Type a skill name.  Skill type is "custom interaction".  Invocation name is "Tesla" (this is what you will use to tell Alexa to interact with the Tesla). Audio player: no.
14. Paste the intent schema (json above) and the sample utterances (text above) into the new skill.  Add or edit utterances if you choose.
15. Under configuration/Global fields, choose the "AWS Lambda ARN" endpoint type, choose "North America", and paste in the ARN of the Lambda function you created a moment ago.  "Account linking" should be no.

ADD LAMBDA FUNCTION PERMISSIONS TO THE ENCRYPTION KEY
16. Go back to the AWS console, to KMS, Encryption keys, and add "encrypt & decrypt" permission for the Lambda role you created above.

ADD YOUR TESLA USERNAME AND PASSWORD AS ENCRYPTED ENVIRONMENT VARIABLES
17. Go back to the Lambda console, edit your function, and scroll down to the "environment variables" section.
18. Check the box for "enable encryption in transit".
19. Choose "Use a customer master key" and then choose the key you created above, from the drop-down list.
18. Create an environment variable named "mytesla_username".  Paste your Tesla account user name into the value field.  Press the "Encrypt" button next to it.
19. Create an environment variable named "mytesla_password".  Paste your Tesla account password into the value field.  Press the "Encrypt" button next to it.
19. Save the Lambda function.

At this point, the skill is active and is private to your Amazon account.  Do not try to publish the skill; the Tesla name is trademarked, the API is private, and you don't want random people controlling your Tesla.
