import discogs_client
import re
import json

# User token can be generated in Developer Settings of Discogs account 
# Search parameters may be different - artist, genre, etc. 
# For more information, refer to official Discogs API - https://www.discogs.com/developers/#
d = discogs_client.Client('ExampleApplication/0.1', user_token='')
results = d.search('', style='Krautrock')

releases = []
# retreiving first 200 pages
for i in range(0,200):
	page = results.page(i)
	for r in page:
		releases.append(r.id)

# Storing all results in JSON file for convenience. 
# Most likely parser will crash at least once, so no need to repeat this procedure
releases_file = json.dumps(releases)

with open('releases_file.json', 'w') as f:
     json.dump(releases_file, f)