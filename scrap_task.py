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
			return json_parser(scripts[i].text)
		else:
			continue


def json_parser(json_script):
	# exclude script definition and semicolon
	explore_data = json.loads(json_script[21:len(json_script)-1])
	posts = (explore_data['entry_data']['TagPage'][0]['graphql']['hashtag']['edge_hashtag_to_media']['edges'])
	hashtag = explore_data['entry_data']['TagPage'][0]['graphql']['hashtag']['name']
	posts_list = []
	for i in range(len(posts)):
		post_id = (posts[i]['node']['shortcode'])
		try:
			post_caption = (posts[i]['node']['edge_media_to_caption']['edges'][0]['node']['text'])
		except IndexError as e:
			print(e)
		post_polarity = ac(post_caption)
		pos = post_polarity['pos']
		neu = post_polarity['neu']
		neg = post_polarity['neg']
		post_picutre = (posts[i]['node']['display_url'])
		post_timestamp = (posts[i]['node']['taken_at_timestamp'])
		post_body = [post_id, post_caption, post_picutre, post_timestamp, pos, neu, neg, hashtag]
		posts_list.append(post_body)


	return persist_posts(posts_list)

def persist_posts(posts_list):
	conn = MySQLConnection(**cfg.mysql)
	cursor = conn.cursor()
	for post in posts_list:
		try:
			cursor.execute("""INSERT IGNORE INTO posts VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""",
				(post[0],post[1],post[2],post[3],post[4],post[5],post[6],post[7]))
			conn.commit()
		except TypeError :
			print(e)
			conn.rollback()
			continue

def scrap_init(tag):
	base_url = "https://www.instagram.com/explore/tags/"
	explore_url = base_url + tag
	get_json_script(explore_url)
