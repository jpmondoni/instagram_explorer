# CTEC 121 Intro to Programming and Problem Solving
# Bruce Elgort / Clark College - Slightly Modified by Jp Mondoni
# Using IBM Watson's Tone Analyzer to detect and interpret emotional, social, and writing cues found in text.
# February 26, 2016 - Modified on September, 2017.
 
import requests
import json
from secret.Watson import auth
 
def analyze_tone(text):
	user = auth()
	username = user['username']
	password = user['password']
	watsonUrl = user['url'] 
	headers = {"content-type": "text/plain"}
	data = text
	try:
		r = requests.post(watsonUrl, auth=(username,password),headers = headers,
		 data=data)
		print(r.text)
		return r.text
	except:
		return False
 
def display_results(data):
	# Display results for document tone. 
	data = json.loads(str(data))
	for i in data['document_tone']['tones']:
		print(i['tone_name'].ljust(20),(str(round(i['score'] * 100,1)) + "%").rjust(10))
