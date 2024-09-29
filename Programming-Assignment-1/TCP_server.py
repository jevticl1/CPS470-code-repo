#!/bin/python

import socket
import sys
import time
import threading

# list used to keep track of currently connected ids and their timestamps
used_connection_ids = {}

# timeout constraints
server_timeout = 5*60  # 5 minutes
connection_id_timeout = 60  # 1 minute
cleanup_interval = 10  # 10 seconds

def remove_connections():
    while True:
        time.sleep(cleanup_interval)
        current_time = time.time()
        
        # iterate through each connection id to identify timed out connections and remove
        to_remove = [conn_id for conn_id, timestamp in used_connection_ids.items() if current_time - timestamp > connection_id_timeout]

        for conn_id in to_remove:
            del used_connection_ids[conn_id]
            print(f"Removed stale connection ID: {conn_id}")

def handle_client(client_socket, client_address):
    try:
        client_socket.settimeout(60)  # 1 minute timeout for receiving data
        message = client_socket.recv(1024).decode('utf-8').strip()

        if message.startswith("HELLO ") and message[6:].isdigit() and len(message[6:]) == 4:
            connection_id = message[6:]

            if connection_id in used_connection_ids:
                response = f"RESET {connection_id}\n"
            else:
                # add connection id to list of used connection ids
                used_connection_ids[connection_id] = time.time()
                client_ip, client_port = client_address
                response = f"OK {connection_id} {client_ip} {client_port}\n"

            client_socket.sendall(response.encode('utf-8'))
        else:
            # malformed message error
            print(f"Ignoring malformed message from {client_address}: {message}")

    except socket.timeout:
        print(f"Client {client_address} timed out.")
    except Exception as e:
        print(f"Error handling client {client_address}: {e}")
    finally:
        client_socket.close()

def tcp_server(server_port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server_socket.bind(('', server_port))
        server_socket.listen(5)
        print(f"Server listening on port {server_port}")

        # start the cleanup cycle in a separate thread
        cleanup_thread = threading.Thread(target=remove_connections, daemon=True)
        cleanup_thread.start()

        last_request_time = time.time()

        while True:
            # check if server has timed out (idle for >5 minutes)
            if time.time() - last_request_time > server_timeout:
                print("Server timed out due to inactivity. Exiting.")
                break

            # set a timeout for accept() to allow checking server timeout
            server_socket.settimeout(60)
            
            try:
                client_socket, client_address = server_socket.accept()
                last_request_time = time.time()  # reset last request time on new connection
                
                # Handle each client in a separate thread
                client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
                client_thread.start()

            except socket.timeout:
                pass

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # closing socket when server shuts down
        print("Closing server socket.")
        server_socket.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python TCP_server.py <Server_Port>")
        sys.exit(1)

    try:
        server_port = int(sys.argv[1])
        tcp_server(server_port)
    except ValueError:
        print("Server port must be an integer.")
        sys.exit(1)