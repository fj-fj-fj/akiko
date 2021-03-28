import json
import requests
import subprocess
from time import sleep

from misc import NGROK_PATH, LOCALHOST_URL

_ngrok = subprocess.Popen([NGROK_PATH, 'http', '5000'], stdout=subprocess.PIPE)

sleep(3)  # to allow the ngrok to fetch the url from the server

_tunnel_url = requests.get(LOCALHOST_URL).text

_j = json.loads(_tunnel_url)

_tunnel_url = _j['tunnels'][1]['public_url']

TUNNEL_URL = _tunnel_url.replace('http', 'https')
