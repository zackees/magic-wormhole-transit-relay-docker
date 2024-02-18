# flake8: noqa E501

"""
Tcp to HTTP relay server
"""

import socket

import requests

# import ssl


TCP_IP = "localhost"  # Localhost
TCP_PORT = 6005  # Arbitrary non-privileged port
BUFFER_SIZE = 1024  # Normally 1024, but we want fast response

FAKE_RESPONSE = True

def send_request(data: bytes, endpoint: str) -> bytes:
    """Send data to the endpoint"""
    if FAKE_RESPONSE:
        return b'{"response": "fake"}'
    response = requests.post(
        endpoint, data=data, timeout=5
    )
    response.raise_for_status()
    return response.content



def run(endpoint: str) -> None:
    """Main function to run the TCP to HTTP relay server"""
    tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_server_socket.bind((TCP_IP, TCP_PORT))
    tcp_server_socket.listen(1)

    while True:
        conn, addr = tcp_server_socket.accept()
        print("Connection address:", addr)
        try:
            while True:
                data = conn.recv(BUFFER_SIZE)
                if not data:
                    break
                print("received data:", data)
                data = send_request(data, endpoint)
                conn.send(data)
        except KeyboardInterrupt:
            break
        except SystemExit:
            break
        except Exception as e:  # pylint: disable=broad-except
            print("Error:", e)
        finally:
            conn.close()
    tcp_server_socket.close()


def client_send_to_tcp_relay(port: int, data: bytes) -> bytes:
    """Assumes a server is already up and running."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((TCP_IP, port))
        s.sendall(data)
        return s.recv(BUFFER_SIZE)


def main() -> None:
    run("http://localhost:6000/endpoint")


if __name__ == "__main__":
    main()
