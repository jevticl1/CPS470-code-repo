#!/bin/python

import socket
import sys

connection_established = False

def validate_HELLO_message(message):
    print(f"Debug: Validating message: '{message}'")  # Debug print
    parts = message.strip().split()
    print(f"Debug: Message parts: {parts}")  # Debug print
    
    if len(parts) == 2 and parts[0] == "HELLO" and parts[1].isdigit() and len(parts[1]) == 4:
        print("Debug: Validation successful")  # Debug print
        return True, parts[1]
    else:
        print("Debug: Validation failed")  # Debug print
        return False, parts[1] if len(parts) > 1 else "XXXX"

try:    
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(30)
    s.bind(('', (int(sys.argv[1]))))
    print(f'Set up socket on port number {(int(sys.argv[1]))}')

except Exception as e:
    print(f"There was an error setting up the socket: {e}")

else:
    try:
        print("Waiting for initial message...")  # Debug print
        initMessage, (client_ip, client_port) = s.recvfrom(256)
        print(f"Debug: Received raw message: {initMessage}")  # Debug print
        decoded_message = initMessage.decode('utf-8').strip()
        print(f"Debug: Decoded and stripped message: '{decoded_message}'")  # Debug print
        
        is_valid, connection_id = validate_HELLO_message(decoded_message)
        
        if is_valid:
            response = f'OK {connection_id}\n'
            connection_established = True
        else:
            response = f'RESET {connection_id}\n'
        
        print(f"Debug: Sending response: '{response.strip()}'")  # Debug print
        s.sendto(response.encode('utf-8'), (client_ip, client_port))

        # ... rest of the code ...

    except TimeoutError:
        print('Timed out waiting for connections.')
    except Exception as e:
        print(f'Exception: {e}')

finally:
    connection_established = False
    s.close()
    print(f'Socket closed.\n')
