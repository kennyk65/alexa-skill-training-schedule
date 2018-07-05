# alexa-skill-training-schedule
Artifacts for my Alexa skill - Training operations / scheduling assistant

The interaction-model.json is the model that explains how Alexa determines 'intents' based on voice prompts.  You use this file in the Alexa Developer console:  https://developer.amazon.com/alexa-skills-kit .  One key bit is how it identifies the ARN of the backing lambda function.

trainingSchedule.js is the backing Lambda function, still under development.  At present, I'm having the code do an S3 Select query against a CSV in an S3 bucket, unfortunately the version of the SDK supported by Lambda does not support this new feature, see comments for details.

Things to do.md is just my running scratchpad of things I want to make this thing do.

Publishing:  I used Alexa for business on my account.  You go into your AWS account / Alexa for Business and obtain your ARN - which is basically your account number with trimmings.  Then in the publishing section of the Alexa skills kit you put that number in.  Then back on the AWS side you approve it, and it is all hooked up.
