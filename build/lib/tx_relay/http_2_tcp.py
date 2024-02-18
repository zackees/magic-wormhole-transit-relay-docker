"""
Simple HTTP to TCP relay server using Flask and Python's built-in socket
library
"""

import socket
import sys

from flask import Flask, jsonify, request

app = Flask(__name__)

TCP_IP = "127.0.0.1"  # The TCP server's hostname or IP address
TCP_PORT = 5005  # The port used by the TCP server
BUFFER_SIZE = 1024  # Buffer size for receiving data


@app.route("/forward", methods=["POST"])
def forward_to_tcp():
    """Forward HTTP POST request to TCP server and return response as JSON"""
    # This endpoint receives HTTP requests and forwards them to the TCP server
    data = request.data  # Get data from POST request

    # Create a socket and connect to TCP server
    tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        tcp_client.connect((TCP_IP, TCP_PORT))
        tcp_client.send(data)  # Send data to TCP server

        # Waiting for response from TCP server if necessary
        response = tcp_client.recv(BUFFER_SIZE)
        return jsonify({"response": response.decode()}), 200
    except KeyboardInterrupt:
        sys.exit(0)
    except SystemExit:
        sys.exit(0)
    except Exception as e:  # pylint: disable=broad-except
        return jsonify({"error": str(e)}), 500
    finally:
        tcp_client.close()

def main() -> None:
    """Main function to run the HTTP to TCP relay server"""
    app.run(host="0.0.0.0", port=5000)  # Default HTTP port


if __name__ == "__main__":
    # Run Flask HTTP server
    main()
    
