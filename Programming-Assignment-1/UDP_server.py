#!/bin/python

import socket

try:	
	#setting up new datagram socket
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	#timeout after 10 seconds
	s.settimeout(10)
	#set socket to listen on UDP port 7070 
	s.bind(('', 7070))
except Exception as e:
	print(f"There was an error setting up the socket: {e}")
else:
	try:
		while True:
			data, (client_ip, client_port) = s.recvfrom(256)
			msg = data.decode('utf-8')
			s.sendto(f'You sent: {msg}'.encode('utf-8'), (client_ip, client_port))

	except TimeoutError:
		print('Timed out waiting for connections.')
	except Exception as e:
		print(f'Exception: {e}')
finally:
	s.close()
	print(f'Socket closed.\n')				