#!/bin/python

import socket
import sys
import time
import threading

#list used to keep track of currently connected ids and their timestamps
used_connection_ids = {}


#timeout constraints
server_timeout = 5*60 #5 minutes
connection_id_timeout = 60 #1 minute
cleanup_interval = 10 #10 seconds

def remove_connections():
	while True:
		time.sleep(cleanup_interval)
		current_time = time.time()
		
		#iterate through each connection id to identify timed out connections and remove
		to_remove = [conn_id for conn_id, timestamp in used_connection_ids.items() if current_time - timestamp > connection_id_timeout]

		for conn_id in to_remove:
			del used_connection_ids[conn_id]
			print(f"Removed stale connection ID: {conn_id}")

def udp_server(server_port):
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	try:
		server_socket.bind(('', server_port))
		print(f"Server listening on port {server_port}\n")

		#start the cleanup cycle in a separate thread
		cleanup_thread = threading.Thread(target = remove_connections, daemon = True)
		cleanup_thread.start()

		last_request_time = time.time()

		while True:
			#check if server has timed out (idle for >5 minutes)
			if time.time() - last_request_time > server_timeout:
				print(f"Server timed out due to inacivity. Exiting.")
				break


			try:
				#set a 1 minute timeout for socket
				server_socket.settimeout(60)
				message, client_address = server_socket.recvfrom(1024)
				last_request_time = time.time() #reset last request time on new message

				message_str = message.decode('utf-8').strip() #removes any whitespace or newline characters from message

				if message_str.startswith("HELLO ") and message_str[6:].isdigit():
					connection_id = message_str[6:]

					if connection_id in used_connection_ids:
						response = f"RESET {connection_id}\n"
					else:
						#add connection id to list of used connection ids
						used_connection_ids[connection_id] = time.time()
						client_ip, client_port = client_address
						response = f"OK {connection_id} {client_ip} {client_port}\n"

					server_socket.sendto(response.encode('utf-8'), client_address)
				else:
					#malformed message error
					print(f"Ignoring malformed message from {client_address}: {message_str}")

			except socket.timeout:
				print(f"Socket timeout: no message received in the last minute.\n")

	except Exception as e:
		print(f"An error occurred: {e}\n")

	finally:
		#closing socket when server shuts down
		print("Closing server socket.")
		server_socket.close()


if __name__ == "__main__":
	if len(sys.argv) != 2:
		print("Usage: python UDP_server.py <Server_Port>")
		sys.exit(1)

	try:
		server_port = int(sys.argv[1])
		udp_server(server_port)
		
	except ValueError:
		print("Server port must be an integer.")
		sys.exit(1)





# #initial message validation function
# def validate_HELLO_message(message):
#     parts = message.split()
#     if len(parts) == 2 and parts[0] == "HELLO" and parts[1].isdigit() and len(parts[1]) == 4:
#         return True, parts[1]
#     else:
#         return False, parts[1] if len(parts) > 1 else "NO CONNECTION ID"


# try:	
# 	#setting up new datagram socket
# 	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 	#timeout after 30 seconds
# 	s.settimeout(30)

# 	#set socket to listen on UDP port 7070 
# 	s.bind(('', (int(sys.argv[1]))))
# 	print(f'Set up socket on port number {(int(sys.argv[1]))}')

# #Exception handling for socket setup
# except Exception as e:
# 	print(f"There was an error setting up the socket: {e}")

# else:
# 	try:
# 		#receive initial message and validate 
# 		initMessage, (client_ip, client_port) = s.recvfrom(256)
# 		decoded_message = initMessage.decode('utf-8').strip()
# 		is_valid, connection_id = validate_HELLO_message(decoded_message)

# 		if is_valid:
# 			response = f'OK {connection_id}\n'
# 			connection_established = True
# 		else:
# 			response = f'RESET {connection_id}\n'
			
# 		s.sendto(response.encode('utf-8'), (client_ip, client_port))

# 		#keep socket open for any messages to come through
# 		while connection_established:
# 			#messages logged with data, incoming address logged with addr, data decoded using utf8 into msg var
# 			data, addr = s.recvfrom(256)
# 			msg = data.decode('utf-8').strip()

# 			s.sendto(f'You sent: {msg}\n'.encode('utf-8'), addr)

# 	except TimeoutError:
# 		print(f'Timed out waiting for connections.\n')
# 	except Exception as e:
# 		print(f'Exception: {e}\n')

# #close socket when not in use and reset connection_established var
# finally:
# 	connection_established = False
# 	s.close()
# 	print(f'Socket closed.\n')				