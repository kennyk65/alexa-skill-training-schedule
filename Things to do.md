Name:  training schedule

Minimum Viable Product:
Alexa, what is event ###, and Alexa responds with "your event id is ###" - DONE.

Next goal:
Have code S3 select the training-schedule/ready/current-schedule.csv with given event ID.
If line does not say stat or vac,  Have Alexa say "<course title> at <delivery location> delivered by <instructors> starts on <start date> at <start time>.  It ends on <end date> and has <students ops> enrolled students."
If line says stat have Alexa say "this is a holiday on <start date>"
If line says vac have Alexa say "this is a vacation event for <Instructors>, from <start date> through <end date>"
DONE!

======================
Design:
Take spreadsheet, upload to bucket.  - DONE, but not fully automated.
Have First Lambda function copy to another bucket / prefix with well understood name. - DONE, USING PYTHON
Have second Lambda function use S3 select queries on CSV file.
select * from s3object s where "Event ID" = '102700'   -  DONE, USING PYTHON

==========
Capabilities to Develop:

what is on my schedule this week / next week / two weeks from now / the week of
what was on my schedule last week
what is my next class


Where do i need to go this week / next week / …..

Where is <instructor> this week / next week ….
What is <instructor> teaching this week / next week...

What time zone is <instructor> in this week

What is scheduled in <delivery location> this week / next week

What is event #

When is my next day off

When does my next class / event start

on my schedule this week:  determine current date, backup to sunday, find next start date, if in current week say it, find next start date until end of week.  If nothing say there is nothing on your schedule this week.



find <mvp> line that says ‘Host’, read it and

