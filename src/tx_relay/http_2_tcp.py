import http.server
import socket
import socketserver
import sys

TCP_IP = "127.0.0.1"
TCP_PORT = 6005
BUFFER_SIZE = 1024
PORT = 6000

class TCPForwardingHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        """Forward HTTP POST request to TCP server and return response."""
        content_length = int(self.headers['Content-Length'])  # Gets the size of data
        post_data = self.rfile.read(content_length)  # Gets the data itself

        self.send_response(200)  # Send OK response
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        # Connect to TCP server
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_client:
            try:
                tcp_client.connect((TCP_IP, TCP_PORT))
                tcp_client.sendall(post_data)

                # Waiting for response from TCP server if necessary
                response = tcp_client.recv(BUFFER_SIZE)
                self.wfile.write(b'{"response": "' + response + b'"}')  # Send response back to HTTP client
            except Exception as e:
                error_message = str(e).encode('utf-8')
                self.wfile.write(b'{"http -> tcp error": "' + error_message + b'"}')


class HttpPrintHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        """Print HTTP POST request and return response."""
        content_length = int(self.headers['Content-Length'])  # Gets the size of data
        post_data = self.rfile.read(content_length)  # Gets the data itself

        self.send_response(200)  # Send OK response
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        print(post_data.decode('utf-8'))
        self.wfile.write(b'{"response": "ok"}')  # Send response back to HTTP client

def make() -> HttpPrintHandler:
    return HttpPrintHandler

def run(server_class=socketserver.ThreadingTCPServer, handler_class=TCPForwardingHandler):
    server_address = ('', PORT)  # Listen on all interfaces at port 6000
    httpd = server_class(server_address, handler_class)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()

if __name__ == "__main__":
    run()
