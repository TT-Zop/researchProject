#!/usr/bin/env python3

import sys
import boto
from boto.mturk.connection import MTurkConnection

mtc = MTurkConnection(aws_access_key_id = 'AKIAJYNVYU7Y53VOHOLA',
aws_secret_access_key = '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',
host = 'mechanicalturk.sandbox.amazonaws.com')

account_balance = mtc.get_account_balance()[0]
print("You have a balance of:", account_balance)

question_html_value = """
<html>
<head>
<meta http-equiv='Content-Type' content='text/html; charset=UTF-8'/>
<script src='https://s3.amazonaws.com/mturk-public/externalHIT_v1.js' type='text/javascript'></script>
</head>
<body>
<!-- HTML to handle creating the HIT form -->
<form name='mturk_form' method='post' id='mturk_form' action='https://workersandbox.mturk.com/mturk/externalSubmit'>
<input type='hidden' value='' name='assignmentId' id='assignmentId'/>
<!-- This is where you define your question(s) --> 
<h1>Please name the company that created the iPhone</h1>
<p><textarea name='answer' rows=3 cols=80></textarea></p>
<!-- HTML to handle submitting the HIT -->
<p><input type='submit' id='submitButton' value='Submit' /></p></form>
<script language='Javascript'>turkSetAssignmentID();</script>
</body>
</html>
"""
# The first parameter is the HTML content
# The second is the height of the frame it will be shown in
# Check out the documentation on HTMLQuestion for more details
html_question = boto.mturk.question.HTMLQuestion(question_html_value, 500)
# These parameters define the HIT that will be created
# question is what we defined above
# max_assignments is the # of unique Workers you're requesting
# title, description, and keywords help Workers find your HIT
# duration is the # of seconds Workers have to complete your HIT
# reward is what Workers will be paid when you approve their work
# Check out the documentation on CreateHIT for more details
response = mtc.create_hit(question=html_question,
                          max_assignments = 20,
                          title="Answer a few questions",
                          description="Help research a topic",
                          keywords="question, answer, research",
                          duration=600,
                          reward=0.10)
# The response included several fields that will be helpful later
hit_type_id = response[0].HITTypeId
hit_id = response[0].HITId
print("The HIT has been created. View it at this link:")
print("https://workersandbox.mturk.com/mturk/preview?groupId={}".format(hit_type_id))
print("Your HIT ID is:", hit_id)

