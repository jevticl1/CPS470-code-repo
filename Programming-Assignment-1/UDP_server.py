#!/bin/python

import socket
import sys

connection_established = False

#initial message validation function
def validate_HELLO_message(message):
    parts = message.split()
    if len(parts) == 2 and parts[0] == "HELLO" and parts[1].isdigit() and len(parts[1]) == 4:
        return True, parts[1]
    else:
        return False, parts[1] if len(parts) > 1 else "NO CONNECTION ID"


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
		decoded_message = initMessage.decode('utf-8').strip()
		is_valid, connection_id = validate_HELLO_message(decoded_message)

		if is_valid:
			response = f'OK {connection_id}\n'
			connection_established = True
		else:
			response = f'RESET {connection_id}\n'
			
		s.sendto(response.encode('utf-8'), (client_ip, client_port))

		#keep socket open for any messages to come through
		while connection_established:
			#messages logged with data, incoming address logged with addr, data decoded using utf8 into msg var
			data, addr = s.recvfrom(256)
			msg = data.decode('utf-8').strip()

			s.sendto(f'You sent: {msg}\n'.encode('utf-8'), addr)

	except TimeoutError:
		print(f'Timed out waiting for connections.\n')
	except Exception as e:
		print(f'Exception: {e}\n')

#close socket when not in use and reset connection_established var
finally:
	connection_established = False
	s.close()
	print(f'Socket closed.\n')				