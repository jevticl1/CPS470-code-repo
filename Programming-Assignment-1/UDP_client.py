#!/bin/python

import socket
import sys

def udp_client(server_ip, server_port, connection_id):
	client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	client_socket.settimeout(60)

	message = f"HELLO {connection_id}\n"
	server_address = (server_ip, int(server_port))

	try:
		client_socket.sendto(message.encode('utf-8'), server_address)

		response, _ = client_socket.recvfrom(1024)
		response_str = response.decode('utf-8').strip()

		if response_str.startswith("OK"):
			print(f"Connection established {response_str[3:]}\n")
		elif response_str.startswith("RESET"):
			print(f"Connection error {connection_id}")
		else:
			print(f"Unexpected response: {response_str}")

	except socket.timeout:
		print(f"Connection Error {connection_id}: No response within 60 seconds")

	finally:
		client_socket.close()

if __name__ == "__main__":
	if len(sys.argv) != 4:
		print(f"Usage: python UDP_client.py <Server_IP> <Server_Port> <Connection_ID>")
		sys.exit(1)

	udp_client(sys.argv[1], sys.argv[2], sys.argv[3])


# try:
# 	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# 	s.settimeout(10)
# except Exception as e:
# 	print(f'Exception while setting up socket: {e}')
# else:
# 	try:
# 		initMessage = f"HELLO {sys.argv[3]}\n"

# 		s.sendto(initMessage.encode('utf-8'), (sys.argv[1], int(sys.argv[2])))
# 		response = s.recvfrom(256)[0].decode('utf-8')
# 		print(response)
# 	except TimeoutError:
# 		print('Timed out waiting for response.')
# 	except Exception as e:
# 		print(f'Exception: {e}')
# 	finally:
# 		s.close()