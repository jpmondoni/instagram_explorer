import requests, re, sys, os, string
import json
from sql import database_conf as cfg
from mysql.connector import MySQLConnection, Error
from lxml import html
from bs4 import BeautifulSoup
from sentiment_analysis import analyze_caption 


def get_json_script(url, persist):
	page = requests.get(url)
	soup = BeautifulSoup(page.text, "lxml")
	""" instagram generates a js type element and then converts to HTML
		thus, the request result is a list of scripts.
	"""
	scripts = soup.find_all("script", attrs={"type":"text/javascript"})
	for i, script in enumerate(scripts):
		cut = script.text[:18]
		if(cut == "window._sharedData"):
			return json_parser(scripts[i].text, persist)
		else:
			continue


def json_parser(json_script, persist):
	# exclude script definition and semicolon
	explore_data = json.loads(json_script[21:len(json_script)-1])
	posts = (explore_data['entry_data']['TagPage'][0]['graphql']['hashtag']['edge_hashtag_to_media']['edges'])
	hashtag = explore_data['entry_data']['TagPage'][0]['graphql']['hashtag']['name']
	posts_list = []
	for i in range(len(posts)):
		# Todo : get number of likes 
		post_id = (posts[i]['node']['shortcode'])
		try:
			post_caption = (posts[i]['node']['edge_media_to_caption']['edges'][0]['node']['text'])
		except IndexError as e:
			continue

		post_polarity = analyze_caption(post_caption)
		pos = post_polarity['avg_pos']
		neu = post_polarity['avg_neu']
		neg = post_polarity['avg_neg']
		com = post_polarity['avg_com']
		other_tags = post_polarity['hashtag_list']
		post_picture = (posts[i]['node']['display_url'])
		post_timestamp = (posts[i]['node']['taken_at_timestamp'])
		post_body = [post_id, post_caption, post_picture, post_timestamp, pos, neu, neg, hashtag]
		post_dict = {'post_id': post_id,
					 'caption': post_caption,
					 'picture_url' : post_picture,
					 'timestamp' : post_timestamp,
					 'pos': pos,
					 'neg': neg,
					 'neu': neu,
					 'hashtag' : hashtag
					}

		posts_list.append(post_dict)


	if(persist):
		return persist_posts(posts_list)
	else:
		return posts_list

def persist_posts(posts_list):
	conn = MySQLConnection(**cfg.mysql)
	cursor = conn.cursor()
	for post in posts_list:
		try:
			cursor.execute("""INSERT IGNORE INTO posts VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""",
				(post['post_id'],post['caption'],post['picture_url'],post['timestamp'],post['pos'],post['neg'],post['neu'],post['hashtag']))
			conn.commit()
		except:
			continue
	
	return posts_list

def scrap_init(tag, persist):
	base_url = "https://www.instagram.com/explore/tags/"
	explore_url = base_url + tag
	return get_json_script(explore_url, persist)
