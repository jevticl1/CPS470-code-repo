#!/bin/python

import socket
import sys

connection_established = False

#initial message validation function
def validate_HELLO_message(message):
	#splits message into individual parts
	parts = message.split()
	match parts:
		#if the first part is HELLO and the second part contains a 4 digit connection id, then true
		case ["HELLO", connection_id] if connection_id.isdigit() and len(connection_id) == 4:
			connection_established = True
			return True
		case _:
			return False


try:	
	#setting up new datagram socket
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	#timeout after 30 seconds
	s.settimeout(30)

	#set socket to listen on UDP port 7070 
	s.bind(('', (int(sys.argv[1]))))
	print(f'Set up socket on port number {(int(sys.argv[1]))}')

#Exception handling for socket setup
except Exception as e:
	print(f"There was an error setting up the socket: {e}")

else:
	try:
		#receive initial message and validate 
		initMessage, (client_ip, client_port) = s.recvfrom(256)
		if validate_HELLO_message(initMessage.decode()):
				s.sendto(f'OK {initMessage.split()[1]}\n', (client_ip, client_port))
		else:
			s.sendto(f'RESET {initMessage.split()[1]}\n', (client_ip, client_port))

		#keep socket open for any messages to come through
		while connection_established == True:
			#any new messages logged into data var and decoded using utf8 into msg var
			data = s.recvfrom(256)
			msg = data.decode('utf-8')

			s.sendto(f'You sent: {msg}'.encode('utf-8'), (client_ip, client_port))

	except TimeoutError:
		print('Timed out waiting for connections.')
	except Exception as e:
		print(f'Exception: {e}')

#close socket when not in use and reset connection_established var
finally:
	connection_established = False
	s.close()
	print(f'Socket closed.\n')				