#!/usr/bin/env python

import socket
import wspy

import rospy
from std_msgs.msg import String

connectionOpened = False

class WebSocketServer(wspy.Connection):
	def onopen(self):
		print 'Connection opened at %s:%d' % self.sock.getpeername()
		global connectionOpened
		connectionOpened = True

	def onmessage(self, message):
		print 'Received message "%s"' % message.payload

	def onclose(self, code, reason):
		global connectionOpened
		print 'Connection closed'
		connectionOpened = False

server = wspy.websocket()
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('127.0.0.1', 12345))
server.listen(5)

def callback(data):
	if connectionOpened:
		WebSocketServer(client).send(wspy.TextMessage(unicode(data.data, "utf-8")))
	else:
		print "No connection: %s" % data.data

def listener():
	rospy.init_node('listener', anonymous=True)
	rospy.Subscriber("chatter", String, callback)

listener()

while True:
	client, addr = server.accept()
	WebSocketServer(client).receive_forever()