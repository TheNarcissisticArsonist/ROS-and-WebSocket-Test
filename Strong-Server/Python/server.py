#!/usr/bin/env python

# Modules used for the websocket server
import socket
import wspy

# Modules used for the ROS node
import rospy
from std_msgs.msg import String

connectionOpened = False # If there's a connection, this will be True

# The websocket server object
class WebSocketServer(wspy.Connection):
	# Run upon opening the connection
	def onopen(self):
		print 'Connection opened at %s:%d' % self.sock.getpeername()
		global connectionOpened
		connectionOpened = True

	# Run upon receiving a message
	def onmessage(self, message):
		print 'Received message "%s"' % message.payload

	# Run upon closing the connection
	def onclose(self, code, reason):
		global connectionOpened
		print 'Connection closed'
		connectionOpened = False

# Start the websocket server on 127.0.0.1:12345 (aka localhost:12345)
server = wspy.websocket()
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('127.0.0.1', 12345))
server.listen(5)

# This code is run whenever data is received from the ROS subscriber node
def callback(data):
	if connectionOpened: # If there's a connection opened, send the data over the connection
		WebSocketServer(client).send(wspy.TextMessage(unicode(data.data, "utf-8")))
	else: # Otherwise, just print it
		print "No connection: %s" % data.data

# This code creates the subscriber node
def listener():
	rospy.init_node('listener', anonymous=True)
	rospy.Subscriber("chatter", String, callback)
	# rospy.spin() is not used, because the code is supposed to loop in the while True loop below

listener() # Start the listener

# Run the websocket server
while True:
	client, addr = server.accept()
	WebSocketServer(client).receive_forever()