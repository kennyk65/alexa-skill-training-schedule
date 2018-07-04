Name:  training schedule

Minimum Viable Product:
Alexa, what is event ###

Alexa responds with:  Given an event ID, If line does not say stat or vac,  say "<course title> at <delivery location> delivered by <instructors> starts on <start date> at <start time>.  It ends on <end date> and has <students ops> enrolled students."

======================
Design:
Take spreadsheet, upload to bucket.
Have First Lambda function copy to another bucket / prefix with well understood name.
Have second Lambda function use S3 select queries on CSV file.
select * from s3object s where "Event ID" = '102700'

==========
Plan:
First function - just take “what is event number xxx” and write to log, parrot it back. - DONE
Second iteration:  Use hard-coded csv file for now.
Develop node app that can take eventid query S3, and dump to log.



what is on my schedule this week / next week / two weeks from now / the week of
what was on my schedule last week
what is my next class


Where do i need to go this week / next week / …..

Where is ____ this week / next week ….

What time zone is _____ in this week

What is scheduled in XXXX this week / next week

What is event #

When is my next day off

When does my next class / event start

on my schedule this week:  determine current date, backup to sunday, find next start date, if in current week say it, find next start date until end of week.  If nothing say there is nothing on your schedule this week.



find <mvp> line that says ‘Host’, read it and

