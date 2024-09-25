#!/bin/python

import socket
import sys

try:
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.settimeout(10)
except Exception as e:
	print(f'Exception while setting up socket: {e}')
else:
	try:
		s.sendto(sys.argv[3].encode('utf-8'), (sys.argv[1], int(sys.argv[2])))
		response = s.recvfrom(256)[0].decode('utf-8')
		print(response)
	except TimeoutError:
		print('Timed out waiting for response.')
	except Exception as e:
		print(f'Exception: {e}')
	finally:
		s.close()