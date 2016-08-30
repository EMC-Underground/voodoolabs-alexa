To run this in flask-ask, run the alexa-emc-support-dates.py file.

flask-ask response strings are stored in the templates.yaml file. flask-ask automatically pulls from that file to merge messages with any provided arguments. See the render_template() calls in the alexa-emc-support-dates.py file.

Custom slots must be entered in the Alexa developer's console Interaction Model:
	MODEL
	PRODUCT

Values for these slots are in files stored in the alexa_interaction_model folder.

Interaction schema and utterances are documented in files stored in the alexa_interaction_model folder.

Invocation name is “emc support”

Use “Symmetrix VMAXe” to see a successful query when you test. Other inputs without numbers should also work.

If using ngrok, you must point Alexa at the custom ngrok URL generated when you run ngrok on your machine. Thus, you should consider doing active development using your own amazon developer account rather than the team account to keep from trouncing on one another. 

----------------------------------------
Notes for team
----------------------------------------

Dan M, 2016-09-26:
	- as of the end of 9/26 this code works end-to-end using flask-ask with ngrok
	- THIS CODE IS VERY GREEN (not much testing). I have only tested
	  with the text interface thus far.
	- things that I know don't work:
		- handling the default (no intent match) case... 
		  right now everything defaults to the YesIntent for some reason. 
		  Maybe it is because the YesIntent isn't AMAZON.YesIntent???
		  Is there a "DefaultIntent" we can trap?
		- anything with a number in the name WILL NOT MATCH. 
		  The problem is that Alexa translates voice/text to numbers,
		  but Alexa doesn't know to put it next to the text.
		  For example, voice "X200" ("X two hundred") becomes
		  "X 200" after Alexa translates it. "X200" is what is in the DB.
		  We need to implement a method to strip out all white space
		  in a string and use that when we compare.
		  By taking white space out of the equation entirely we should
		  work around this problem.
	- TODO list:
		- implement a "strip_white_space" utility method (Brin?)
		- continue fleshing out intents, including yes/no/stop, etc (Adam)
		- implement read from S3 (Mark/Chris/Dave)
		- TEST TEST TEST

Dan M., 9/29
	- as of this checkin the "list products" and "list models for prodct" 
	  intents work. I added code to handle them in esdclasses.py and 
	  query_util.py. The alexa_emc_support_dates.py file calls query_util 
	  to implment these queries which return basic delineated strings of
	  of products or models

