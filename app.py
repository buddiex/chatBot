from flask import Flask, render_template, session, request
from flask.ext.socketio import SocketIO, emit, disconnect
from random import randint

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

usernames = {}
number_of_users = 0

randmessages =[
'wetin de happen self',
'them just make me oo, make you ask easy questions o',
'me na from warri, where are u from?'
'hhmmm.... there is God o!!!'
]

def sendUserMessage(msg):
	emit('new message',{ 'username' : session['username'],'message': msg }, broadcast=True )

def sendMr2knowReply(msg):
	emit('new message',{ 'username' : 'Mr2know','message': msg }, broadcast=True )

def randomMesage():
	sendMr2knowReply()

@app.route('/')
def index():
	return render_template('index.html')

# When the client emits 'connection', this listens and executes
@socketio.on('connection', namespace='/chat')
def user_connected():
	print('User connected')


# When the client emits 'new message', this listens and executes
@socketio.on('new message', namespace='/chat')
def new_message(data):
	#save data
	#@TODO: get reply from any of the brains(wiki) and send a reply
	#send message to wiki async if possible, the send waiting messages
	sendUserMessage(data)
	# process understand the user message and send a wait message while processing
	msg = "i dey think o... this one hard small"
	sendUserMessage(msg)
	#send message to wiki
	# get reply here
	msg = randmessages[randint(0,len(randmessages))]
	sendMr2knowReply(msg)

# When client emits 'add user' this listens and executes
@socketio.on('add user', namespace='/chat')
def add_user(data):
	print 'Adding User'
	global usernames
	global number_of_users

	session['username'] = data
	usernames[data] = session['username']

	number_of_users += 1;

	emit('login', { 'numUsers' : number_of_users })
	msg = 'Hi {} you are yarning the number one Mr2know! How far na?!'.format(session['username'].upper())
	sendMr2knowReply(msg)


@socketio.on('typing', namespace='/chat')
def typing_response():
	try:
		emit('typing', { 'username' : session['username'] }, broadcast=True )
	except:
		pass


@socketio.on('stop typing', namespace='/chat')
def stop_typing():
	try:
		emit('stop typing', { 'username' : session['username'] }, broadcast = True)
	except:
		pass


@socketio.on('disconnect', namespace='/chat')
def disconnect():
	global usernames
	global number_of_users


	try:
		del usernames[session['username']]
		number_of_users -= 1
		emit('user left', { 'username' : session['username'], 'numUsers' : number_of_users}, broadcast=True)

	except:
		pass



if __name__ == '__main__':
    socketio.run(app)
