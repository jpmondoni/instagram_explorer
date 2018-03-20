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
	data = json.loads(str(data))
	#print(data)
	for i in data['document_tone']['tone_categories']:
		print(i['category_name'])
		print("-" * len(i['category_name']))
		for j in i['tones']:
			print(j['tone_name'].ljust(20),(str(round(j['score'] * 100,1)) + "%").rjust(10))
		print()
	print()

if __name__ == '__main__':
	analyze_tone("""
		If you’ve ever stood up from your work desk at the end of a long day and winced from the pain in
		your lower back or neck, then you’re likely one of the millions of workers who suffer from the side
		effects of a less than ergonomic office arrangement. Through the years, I’ve tried dozens of products
		designed to equip me with a more ergonomically optimal work environment: lumbar rolls, wrist
		cushions, footstools, etc. However, none of these seemed to work until I discovered the
		WorkAlign2.0 software package from the Ergonomix Company. Though I was initially sceptical about
		the package’s ability to help me properly align the different components of my workstation into one
		ergonomic setting, the software’s quick and easy 30-minute evaluation and alignment process has
		left me feeling relaxed and rejuvenated, even at the end of an 8-hour day.
		""")