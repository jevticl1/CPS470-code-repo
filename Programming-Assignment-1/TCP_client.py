#!/bin/python

import socket
import sys

def tcp_client(server_ip, server_port, connection_id):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.settimeout(60)

    message = f"HELLO {connection_id}\n"
    server_address = (server_ip, int(server_port))

    try:
        # Connect to the server
        client_socket.connect(server_address)

        # Send the message
        client_socket.sendall(message.encode('utf-8'))

        # Receive the response
        response = client_socket.recv(1024)
        response_str = response.decode('utf-8').strip()

        if response_str.startswith("OK"):
            print(f"Connection established {response_str[3:]}\n")
        elif response_str.startswith("RESET"):
            print(f"Connection error {connection_id}")
        else:
            print(f"Unexpected response: {response_str}")

    except socket.timeout:
        print(f"Connection Error {connection_id}: No response within 60 seconds")
    except ConnectionRefusedError:
        print(f"Connection Error {connection_id}: Connection refused")
    except Exception as e:
        print(f"Connection Error {connection_id}: {str(e)}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(f"Usage: python TCP_client.py <Server_IP> <Server_Port> <Connection_ID>")
        sys.exit(1)

    tcp_client(sys.argv[1], sys.argv[2], sys.argv[3])