import json
import requests
from subprocess import PIPE, Popen
from time import sleep

from misc import NGROK_PATH, LOCALHOST_API

try:
    (lambda: Popen([NGROK_PATH["win"], "http", "5000"], stdout=PIPE))()
except FileNotFoundError:
    (lambda: Popen(["ngrok", "http", "5000"], stdout=PIPE))()

sleep(3)

_tunnel_url = requests.get(LOCALHOST_API, timeout=3).text
_j = json.loads(_tunnel_url)
_tunnel_url = _j["tunnels"][1]["public_url"]
TUNNEL_URL = _tunnel_url.replace("http", "https")
