#!/usr/bin/env python
import socket
import json

# Create raw HTTP request
request = """GET /api/matches/3 HTTP/1.1\r
Host: 127.0.0.1:8000\r
Connection: close\r
\r
"""

# Connect and send
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('127.0.0.1', 8000))
sock.send(request.encode())

# Receive response
response = b""
while True:
    chunk = sock.recv(4096)
    if not chunk:
        break
    response += chunk
sock.close()

# Parse response
response_str = response.decode('utf-8', errors='ignore')
lines = response_str.split('\r\n')

# Find JSON payload (after blank line)
blank_index = 0
for i, line in enumerate(lines):
    if line == '':
        blank_index = i
        break

if blank_index > 0:
    json_str = '\r\n'.join(lines[blank_index+1:])
    try:
        data = json.loads(json_str)
        print("=== RESPONSE JSON ===")
        print(json.dumps(data, indent=2))
        if isinstance(data, list) and len(data) > 2:
            print("\n=== THIRD MATCH ===")
            print(json.dumps(data[2], indent=2))
    except:
        print("Could not parse JSON:")
        print(json_str[:500])
else:
    print("Response headers:")
    for line in lines[:20]:
        print(line)
