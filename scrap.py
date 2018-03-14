
import requests, re, sys, os, string
import json
import database_conf as cfg
from mysql.connector import MySQLConnection, Error
from lxml import html
from bs4 import BeautifulSoup


def get_json_script(url):
	page = requests.get(url)
	soup = BeautifulSoup(page.text, "lxml")
	""" instagram generates a js type element and then converts to HTML
		thus, the request result is a list of scripts.
	"""
	scripts = soup.find_all("script", attrs={"type":"text/javascript"})
	scripts.sort(key = len)
	scripts = scripts[::-1]
	return json_parser(scripts[1].text)

def json_parser(json_script):
	# exclude script definition and semicolon
	explore_data = json.loads(json_script[21:len(json_script)-1])
#	print(explore_data.keys())
#	print(explore_data['country_code'])
	hashtag = (explore_data['entry_data']['TagPage'][0]['graphql']['hashtag']['name'])
	posts = (explore_data['entry_data']['TagPage'][0]['graphql']['hashtag']['edge_hashtag_to_media']['edges'])
	posts_list = []

	for post in posts:
		post_caption = (post['node']['edge_media_to_caption']['edges'][0]['node']['text'])
		post_id = (post['node']['shortcode'])
		post_picutre = (post['node']['display_url'])
		post_timestamp = (post['node']['taken_at_timestamp'])

		post_body = [post_id, post_caption, post_picutre, post_timestamp]
				
		posts_list.append(post_body)

		#print(post_body[:-2])

def main():
	tag = "palmeiras"
	base_url = "https://www.instagram.com/explore/tags/"
	explore_url = base_url + tag
	get_json_script(explore_url)

if __name__ == "__main__":
	main()