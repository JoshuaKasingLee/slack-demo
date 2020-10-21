import pytest
import re
from subprocess import Popen, PIPE
import signal
from time import sleep
import requests
import json




# Use this fixture to get the URL of the server. It starts the server for you,
# so you don't need to.
@pytest.fixture
def url():
    url_re = re.compile(r' \* Running on ([^ ]*)')
    server = Popen(["python3", "server.py"], stderr=PIPE, stdout=PIPE)
    line = server.stderr.readline()
    local_url = url_re.match(line.decode())
    if local_url:
        yield local_url.group(1)
        # Terminate the server
        server.send_signal(signal.SIGINT)
        waited = 0
        while server.poll() is None and waited < 5:
            sleep(0.1)
            waited += 0.1
        if server.poll() is None:
            server.kill()
    else:
        server.kill()
        raise Exception("Couldn't get URL from local server")

def test_email_invalid_1_http(url):
    data_in = {
        'email' : "email",
        'password' : "password",
        'name_first' : "first",
        'name_last' : "last"
    }
    response = requests.post(url + 'auth/register', json = data_in)
    assert (response.status_code == 400)