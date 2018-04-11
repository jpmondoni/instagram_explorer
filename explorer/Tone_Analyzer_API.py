# CTEC 121 Intro to Programming and Problem Solving
# Bruce Elgort / Clark College - Slightly Modified by Jp Mondoni
# Using IBM Watson's Tone Analyzer to detect and interpret emotional, social, and writing cues found in text.
# February 26, 2016 - Modified on September, 2017.
 
import requests
import json
from nltk.tokenize import sent_tokenize
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
		return r.text
	except:
		return False
 
def display_results(text):
	data = analyze_tone(text)
	# Display results for document tone. 
	data = json.loads(str(data))
	for i in data['document_tone']['tones']:
		print(i['tone_name'].ljust(20),(str(round(i['score'] * 100,1)) + "%").rjust(10))

	sents = sent_tokenize(text)
	if(len(sents) > 1):
		for i in data['sentences_tone']:
			print("Sentence #",i['sentence_id'],i['text'][:40])
			for j in i['tones']:
				print(j['tone_name'].ljust(20),(str(round(j['score'] * 100,1)) + "%").rjust(10))