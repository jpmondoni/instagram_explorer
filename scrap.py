import requests, re, sys, os, string
import json
import database_conf as cfg
from mysql.connector import MySQLConnection, Error
from lxml import html
from bs4 import BeautifulSoup
from sentiment_analysis import analyze_caption as ac


def get_json_script(url):
	page = requests.get(url)
	soup = BeautifulSoup(page.text, "lxml")
	""" instagram generates a js type element and then converts to HTML
		thus, the request result is a list of scripts.
	"""
	scripts = soup.find_all("script", attrs={"type":"text/javascript"})
	for i, script in enumerate(scripts):
		cut = script.text[:18]
		if(cut == "window._sharedData"):
#			print(scripts[i].text)
			return json_parser(scripts[i].text)
		else:
			continue


def json_parser(json_script):
	# exclude script definition and semicolon
	explore_data = json.loads(json_script[21:len(json_script)-1])
	posts = (explore_data['entry_data']['TagPage'][0]['graphql']['hashtag']['edge_hashtag_to_media']['edges'])
	posts_list = []
	for i in range(len(posts)):
		post_id = (posts[i]['node']['shortcode'])
		post_caption = (posts[i]['node']['edge_media_to_caption']['edges'][0]['node']['text'])
		post_polarity = ac(post_caption)
		pos = post_polarity['pos']
		neu = post_polarity['neu']
		neg = post_polarity['neg']
		post_picutre = (posts[i]['node']['display_url'])
		post_timestamp = (posts[i]['node']['taken_at_timestamp'])
		post_body = [post_id, post_caption, post_picutre, post_timestamp, pos, neu, neg]
		posts_list.append(post_body)

	return persist_posts(posts_list)

def persist_posts(posts_list):
	"""
	for post in posts_list:
		print(post[1])
		print(ac(post[1]))
	"""
def main():
	tag = sys.argv[1]
	base_url = "https://www.instagram.com/explore/tags/"
	explore_url = base_url + tag
	get_json_script(explore_url)

if __name__ == "__main__":
	main()