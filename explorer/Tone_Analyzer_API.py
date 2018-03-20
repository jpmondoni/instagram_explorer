# CTEC 121 Intro to Programming and Problem Solving
# Bruce Elgort / Clark College - Slightly Modified by Jp Mondoni
# Using IBM Watson's Tone Analyzer to detect and interpret emotional, social, and writing cues found in text.
# February 26, 2016 - Modified on September, 2017.
 
import requests
import json
from secret.Watson import username, password
 
def analyze_tone(text):
    username = username()
    password = password()
    watsonUrl = 'https://gateway.watsonplatform.net/tone-analyzer/api/v3/tone?version=2016-05-19'
    headers = {"content-type": "text/plain"}
    data = text
    try:
        r = requests.post(watsonUrl, auth=(username,password),headers = headers,
         data=data)
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