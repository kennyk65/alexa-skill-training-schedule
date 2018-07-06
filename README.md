# alexa-skill-training-schedule
Artifacts for my Alexa skill - Training operations / scheduling assistant

The interaction-model.json - the model that explains how Alexa determines 'intents' based on voice prompts.  You use this file in the Alexa Developer console:  https://developer.amazon.com/alexa-skills-kit .  One key bit is how it identifies the ARN of the backing lambda function.  FWiW I've found it is easier to modify this through the website, then just save the resulting JSON here for safe-keeping.

trainingScheduleP.py -  The backing Lambda Python function, still under development.  At present it supports a few 'intents' that I've implemented.  It uses the new S3 Select query against a CSV in an S3 bucket.

trainingScheduleProcessUploadP.py - This function takes the 'SCHEDULE*.csv' file that you upload to the 'training-schedule' S3 bucket, and moves it to a 'ready' folder under a common name, replacing whatever was already there.  This provides a nice, stable S3 object that the other function can query off of.

trainingSchedule.js - This was my first attempt, in NodeJS.  Unfortunately the version of the SDK supported by Lambda does not support the S3 select feature, and I didn't want to go through a packaging step every time I changed a line of code, so I put this on hold.  See comments for details.

trainingScheduleProcessUpload.js - This was my first attempt to do what the *.py file above does.  Ran into an obstacle where the S3.copyObject function wouldn't work in JS.  Opened a support ticket, and switched to Python, which worked just fine.

Things to do.md is just my running scratchpad of things I want to make this thing do.

Two-way handshake:  The 'skill' needs to know about the ARN of the Lambda function as its 'endpoint' so it knows where to send the back-end calls.  The Lambda function does not need to know the ID of the skill, but it is more secure if it does.  It is identified in the trigger for the function and once again in the code just for safety.

Publishing:  I used Alexa for business on my account.  You go into your AWS account / Alexa for Business and obtain your ARN - which is basically your account number with trimmings.  Then in the publishing section of the Alexa skills kit you put that number in.  Then back on the AWS side you approve it, and it is all hooked up.

To use this skill, the AWS account (my account) must send an email invitation.  One only needs an Amazon retail account to use the skill; technically one does not even need an Echo device since you can use an app.  The email contains a link with a token in it; it takes one to their Amazon account and syncs everything up.
