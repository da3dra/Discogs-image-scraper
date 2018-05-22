import urllib.request
from bs4 import BeautifulSoup
import re
import json
import socks
import socket
import stem.process
import time
import os.path

SOCKS_PORT=9051

with open('releases_file.json') as f:
	data = json.load(f)
	data = data[1:-1]
	map(int, data.split(','))
	identifiers = [int(s) for s in data.split(',')]

def get_url(url):
	try:
		url = str(url)
		begin = 'src="'
		start_str = re.search('src="', url).start()
		start = int(start_str)
		start = start+len(begin)
		url = url[start:]
		end_str = re.search('"/></span>', url).start()
		end = int(end_str)
		url = url[:end]
		return url
	except TypeError:
		tor_process.kill()

for id in identifiers:

	exists = os.path.isfile(str(id)+'.jpg')

	if not exists:

		tor_process = stem.process.launch_tor_with_config(
		config = {
		'SocksPort': str(SOCKS_PORT),
		},
		)
		socks.setdefaultproxy(proxy_type=socks.PROXY_TYPE_SOCKS5,
			addr="127.0.0.1", 
			port=SOCKS_PORT)
		socket.socket = socks.socksocket
		page_url = 'https://www.discogs.com/release/'+str(id)+'/images'
		print(page_url)
		time.sleep(2)
		try:
			page = urllib.request.urlopen(page_url)
			soup = BeautifulSoup(page, 'html.parser')
			container = soup.find('span', attrs={'class': 'thumbnail_link'})

			if container!=None:
				url = get_url(container)
				image = urllib.request.URLopener()
				image.retrieve(url,str(id)+'.jpg')
			else:
				print('else')
			tor_process.kill()
		except urllib.error.HTTPError:
			print('HTTP Error ',str(id))
			tor_process.kill()
			continue

			