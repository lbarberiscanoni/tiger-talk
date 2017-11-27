import time
from flask import Flask, request, session
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

theUsers = {}
# Indices for lists in dictionary:
NAME = 0
STATE = 1
COURSES = 2
INTERESTS = 3
#SUBINTERESTS = 4

counter = 0

account_sid = ""
auth_token = ""

SECRET_KEY = 'This is not a secret.'

app = Flask(__name__)
app.config.from_object(__name__)

def new_user():
	return ['', 0, [], [], []]

def do_response(messageFrom, newUser, messageBody):
	global counter
	global theUsers
	myMessage = ''

	if messageBody == 'SUBSCRIBE':
		myMessage = 'Thank you for signing up to the Clemson Events recommendation system!'
		if theUsers[messageFrom][STATE] == 0 and counter == 0:
			myMessage += '\n\nReply with your name to continue or reply with ESCAPE at any time to opt out.'
			counter = 1
	elif messageBody == 'ESCAPE':
		theUsers[messageFrom][STATE] = -1
		myMessage = 'You will be unsubscribed from all further communications.\n\nFeel free to message us any time with SUBSCRIBE if you change your mind.'
	elif messageBody == 'ME':
		myMessage = str(theUsers[messageFrom]) + ' ' + str(counter)
	elif messageBody == 'RESETCOUNTER':
		myMessage = 'Counter will be reset, thank you'
		counter = 0
	elif messageBody == 'CALENDAR':
		theUsers[messageFrom][STATE] = 2
		#LET'S MAKE A CALENDAR
		myMessage = 'Here\'s your calendar!\n\n'
		myMessage += 'Calendar:\n'
		i = 0
		for interest in theUsers[messageFrom][INTERESTS]:
			if i == 0:
				myMessage += 'Mon: '
			elif i == 1:
				myMessage += 'Wed: '
			elif i == 2:
				myMessage += 'Sat: '
			elif i == 3:
				break

			if interest == '1':
				myinterest = 'Sports Event'
			elif interest == '2':
				myinterest = 'Music Event'
			elif interest == '3':
				myinterest = 'Lecture'
			elif interest == '4':
				myinterest = 'Networking Event'
			elif interest == '5':
				myinterest = 'Social'

			myMessage += myinterest + ' ' + str(i+1) + '\n'
			i += 1

		myMessage += '\nAre you okay with these events?'
	#else:
	#	myMessage = 'Sorry but we didn\'t understand that, could please you try again?'
	elif theUsers[messageFrom][STATE] == 0:
		if counter == 0:
			myMessage = 'Reply with your name to continue or reply with ESCAPE at any time to opt out.'
			counter = 1
		elif counter == 1:
			theUsers[messageFrom][NAME] = messageBody
			myMessage = 'Welcome, ' + theUsers[messageFrom][NAME] + '!\nWould you answer a few quick questions about your courses and interests to get started? Just reply yes or no.'
			counter = 2
		elif counter == 2:
			if messageBody[0].lower() == 'n':
				myMessage = 'No worries, we understand.\nYou\'ll still get recommendations but they\'ll be more random for now.\n\nWe\'ll have your first week of recommendations ready in a few hours.'
				theUsers[messageFrom][STATE] = 1
				counter = 3
			elif messageBody[0].lower() == 'y':
				myMessage = 'Great!\nFirst could you tell us about your current class schedule?\n\nPlease use the following format:\nCPSC 2120\nPSYC 3830\nENGL 2150'
				counter = 4
		elif counter == 4:
			i = 0
			for word in messageBody.split():
				if not i % 2:
					coursename = word
				else:
					coursenumber = word
					theUsers[messageFrom][COURSES].append((coursename,coursenumber))
				i+=1
			#myMessage = 'Got it! Now could you tell us a bit about your Interests?\n\nWhich of the following would you be interested in attending? (Reply with the corresponding numbers of all applicable i.e. "2 3 5")\n\n1. Sporting events\n2. Music events\n3. Lecture series\n4. Networking events\n5. Social events\n6. Community outreach\n7. Cultural events'
			#counter = 5
			myMessage = 'Got it! Now could you tell us a bit about your Interests?\n\nWhich of the following would you be interested in attending? (Reply with the corresponding numbers of all applicable i.e. "2 3 5")\n\n1. Sporting events\n2. Music events\n3. Lecture series\n4. Networking events\n5. Social events'
			counter = 7
		elif counter == 5:
			theUsers[messageFrom][INTERESTS] = messageBody.split()
			if theUsers[messageFrom][INTERESTS][0] == '1':
				myinterest = 'sporting events'
			elif theUsers[messageFrom][INTERESTS][0] == '2':
				myinterest = 'music events'
			elif theUsers[messageFrom][INTERESTS][0] == '3':
				myinterest = 'lecture series'
			elif theUsers[messageFrom][INTERESTS][0] == '4':
				myinterest = 'networking events'
			elif theUsers[messageFrom][INTERESTS][0] == '5':
				myinterest = 'social events'
			elif theUsers[messageFrom][INTERESTS][0] == '6':
				myinterest = 'community outreach'
			elif theUsers[messageFrom][INTERESTS][0] == '7':
				myinterest = 'cultural events'
			else:
				myinterest = '?'
			myMessage = 'Got it! I see that you\'re interested in ' + myinterest + '.\nIs there a particular subcategory here [list of categories] you\'re interested in or would you like to consider any of these types of events?'
			counter = 6
		elif counter == 6:
			myMessage = 'Alright, great! We\'ll have your first week of recommended events ready for you in a few hours!'
			theUsers[messageFrom][STATE] = 1
		elif counter == 7:
			myMessage = 'I see you\'re interested in '
			theUsers[messageFrom][INTERESTS] = messageBody.split()
			for interest in theUsers[messageFrom][INTERESTS][:-1]:
				if interest == '1':
					myinterest = 'sports'
				elif interest == '2':
					myinterest = 'music'
				elif interest == '3':
					myinterest = 'lectures'
				elif interest == '4':
					myinterest = 'networking'
				elif interest == '5':
					myinterest = 'socials'
				else:
					myinterest = '?'
				myMessage += myinterest + ', '
			myMessage += 'and '
			interest = theUsers[messageFrom][INTERESTS][-1]
			if interest == '1':
				myinterest = 'sports'
			elif interest == '2':
				myinterest = 'music'
			elif interest == '3':
				myinterest = 'lectures'
			elif interest == '4':
				myinterest = 'networking'
			elif interest == '5':
				myinterest = 'socials'
			else:
				myinterest = '?'
			myMessage += myinterest + '.\n\nWe\'ll have your first week of recommended events ready for you in a few hours!'
			theUsers[messageFrom][STATE] = 1

	elif theUsers[messageFrom][STATE] == 1:
		myMessage = 'We\'re working hard to put together your recommendations, please give us a little more time.\nThank you!'
	elif theUsers[messageFrom][STATE] == 2:
		if messageBody[0].lower() == 'n':
			myMessage = 'That\'s no problem. Which event would you like to change?\nYou can reply with the day or the name of the event'
			counter = 1
		elif messageBody[0].lower() == 'y':
			myMessage = 'Sounds like a plan!\n\nWould you like to share your event calendar with your friend(s)?\nIf so, just reply with their number(s).'
			counter = 2
		theUsers[messageFrom][STATE] = 3
	elif theUsers[messageFrom][STATE] == 3:
		if counter == 1:
			#Here's where we'd modify or cancel an event
			None
		elif counter == 2:
			friendnumbers = messageBody.split()
			#DO DATA CLEANING ON PHONE NUMBERS OFC
			for phonenum in friendnumbers:
				if phonenum in theUsers.keys():
					myMessage = 'We see that ' + phonenum + ' has already registered with our system, would you like to send them a friend request?'
					counter = 3
				else:
					myMessage = 'We see that ' + phonenum + ' has not signed up for Clemson Events yet, would you like to send them an invitation to join?'
					counter = 4
		elif counter == 3:
			if messageBody[0].lower() == 'n':
				myMessage = 'No problem, we won\'t tell them.'
				counter = 5
			elif messageBody[0].lower() == 'y':
				myMessage = 'Fantastic, we\'ll let them that know you\'d like to connect.'
				counter = 5
			myMessage += '\n\nYour calendar has been saved. Feel free to edit or update your reminders.'
		elif counter == 4:
			if messageBody[0].lower() == 'n':
				myMessage = 'That\'s alright, if you change your mind you can invite them later.'
				counter = 5
			elif messageBody[0].lower() == 'y':
				myMessage = 'Awesome, we\'ll send them an invite.'
				counter = 5
			myMessage += '\n\nYour calendar has been saved. Feel free to edit or update your reminders.'
			


	return myMessage


@app.route('/', methods=['GET','POST'])
def holla_back():
	global counter
	global theUsers

	resp = MessagingResponse()
	myMessage = ''

	message_from = request.values.get('From',None)
	message_body = request.values.get('Body',None)

	counter = session.get('counter', 0)

	newUser = False
	if message_from not in theUsers:
		theUsers[message_from] = new_user()
		newUser = True
		counter = 0
	currentUser = theUsers[message_from]

	resp.message(do_response(message_from, newUser, message_body))

	session['counter'] = counter

	return str(resp)

def holla_at(target, newMessage):
	client = Client(account_sid, auth_token)

	message = client.messages.create(
		to=target,
		from_="+18642074702",
		body=newMessage)

	#print(message.sid)

if __name__ == '__main__':
	app.run(debug=True)
