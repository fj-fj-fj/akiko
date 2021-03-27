# -*- coding: utf-8 -*-

# I don't want use long or short polling and prefer using webhooks.
# I use `ngrok` for development. I wanted to automate this whole process 
# with connecting, creating a tunnel etc.

# This is a helper module and it does its job well

from time import sleep
import subprocess
import requests
import json
import sys

from misc import NGROK_PATH, LOCALHOST_URL


ngrok = subprocess.Popen([NGROK_PATH,'http','5000'], stdout=subprocess.PIPE)
sleep(3) # to allow the ngrok to fetch the url from the server

tunnel_url = requests.get(LOCALHOST_URL).text #Get the tunnel information
j = json.loads(tunnel_url)

tunnel_url = j['tunnels'][1]['public_url'] #Do the parsing of the get
TUNNEL_URL = tunnel_url.replace('http', 'https')

print(f'\nfrom tunnel | tunnel_url: {TUNNEL_URL}', file=sys.stderr)
