# flake8: noqa E501

"""
Tcp to HTTP relay server
"""

import socket

import requests

# import ssl


TCP_IP = "127.0.0.1"  # Localhost
TCP_PORT = 5005  # Arbitrary non-privileged port
BUFFER_SIZE = 1024  # Normally 1024, but we want fast response


def main() -> None:
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

                # Here we would convert or process the data as necessary
                # For now, we'll just forward it directly as a POST request
                # Replace 'https://yourserver.com/endpoint' with your endpoint
                response = requests.post(
                    "https://yourserver.com/endpoint", data=data, verify=True, timeout=5
                )
                # You can send the response back to the TCP client if needed
                conn.send(response.content)  # Echo back to TCP client
        except KeyboardInterrupt:
            break
        except SystemExit:
            break
        except Exception as e:  # pylint: disable=broad-except
            print("Error:", e)
        finally:
            conn.close()
    tcp_server_socket.close()


if __name__ == "__main__":
    main()
