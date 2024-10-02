#!/bin/python

import socket
import sys

def tcp_client(server_ip, server_port, connection_id):
    try:
        server_ip = socket.gethostbyname(server_ip)  # Validate hostname/IP
    except socket.gaierror:
        print(f"Invalid IP address/hostname: {server_ip}")
        return
    
    try:
        server_port = int(server_port)
        if not (0 <= server_port <= 65535):
            raise ValueError("Port number must be between 0 and 65535")
    except ValueError:
        print(f"Invalid port number: {server_port}")
        return

    try:
        connection_id = int(connection_id)
        if connection_id < 0:
            raise ValueError("Connection ID must be a non-negative integer")
    except ValueError:
        print(f"Invalid connection ID: {connection_id}")
        return

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.settimeout(60)

    message = f"HELLO {connection_id}\n"
    server_address = (server_ip, server_port)

    try:
        client_socket.connect(server_address)
        client_socket.sendall(message.encode('utf-8'))

        # Handle multiple segments by accumulating response data until a full message is received
        response = b""
        while not response.endswith(b"\n"):
            data = client_socket.recv(1024)
            if not data:
                break
            response += data

        response_str = response.decode('utf-8').strip()

        # Check if the OK response has the same connection ID
        if response_str.startswith("OK"):
            response_id = response_str.split()[1]
            if response_id == str(connection_id):
                print(f"Connection established {response_str[3:]}\n")
            else:
                print(f"Connection error: expected ID {connection_id}, but got {response_id}")
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
