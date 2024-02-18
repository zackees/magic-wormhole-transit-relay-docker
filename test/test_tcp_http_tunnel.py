import unittest

import subprocess
import time
import requests

#from threading import Thread

#from tx_relay.http_2_tcp import main as http_2_tcp_main
from tx_relay.tcp_2_http import client_send_to_tcp_relay

CMD_HTTP_2_TCP = "python -m tx_relay.http_2_tcp"
CMD_TCP_2_HTTP = "python -m tx_relay.tcp_2_http"


class MainTester(unittest.TestCase):

    def test_tcp_tunnel(self) -> None:
        process_http_2_tcp = subprocess.Popen(CMD_HTTP_2_TCP, shell=True)
        process_tcp_2_http = subprocess.Popen(CMD_TCP_2_HTTP, shell=True)

        time.sleep(3)

        time_now = time.time()

        try:
            while time.time() - time_now < 60:
                if process_http_2_tcp.poll() is not None:
                    self.fail("http_2_tcp process exited")
                if process_tcp_2_http.poll() is not None:
                    self.fail("tcp_2_http process exited")
                print("---> sending request")
                resp = requests.post("http://127.0.0.1:6000", data="hello", timeout=5)
                resp.raise_for_status()
                print(resp.content)
                print("<--- received response")
        except Exception as e:
            self.fail(str(e))
            pass

        process_http_2_tcp.kill()
        process_tcp_2_http.kill()
        process_http_2_tcp.wait()
        process_tcp_2_http.wait()



if __name__ == "__main__":
    unittest.main()
