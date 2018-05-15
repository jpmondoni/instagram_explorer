import requests, re, sys, os, string
import json
import time
from sql import database_conf as cfg
from mysql.connector import MySQLConnection, Error
from lxml import html
from bs4 import BeautifulSoup
from sentiment_analysis import analyze_caption 
from selenium import webdriver


def get_json_script(url, hashtag, persist):

	browser = webdriver.Chrome()
	browser.get(url)

	lenOfPage = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
	match=False
	while(match==False):
		lastCount = lenOfPage
		time.sleep(1)
		lenOfPage = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
		print(lastCount, lenOfPage)
		if lastCount==lenOfPage:
			match=True

	
	soup = BeautifulSoup(browser.page_source, "lxml")

	mck9w_blocks = soup.find_all("div", class_="_mck9w")
	posts_list = []
	for mck9w in mck9w_blocks:
		for a in mck9w.find_all('a'):
			pid = a.get('href').replace("/p/","").replace("/?tagged="+hashtag, "")
		mck9w.find_all("div", clas_="_4rbun")
		for _4rbun in mck9w:
			for img in _4rbun.find_all('img', alt=True, src=True):
				alt = img['alt']
				src = img['src']
		
		post_dict = {
			'post_id': pid,
			'caption': alt,
			'picture_url': src
		}

		posts_list.append(post_dict)

	browser.quit()

	print(len(posts_list))
	#post_parser(posts_list, persist)

def post_parser(posts_list, persist):

	# for i in range(len(posts_list)):
	# 	# Todo : get number of likes 
	# 	post_id = (posts[i]['node']['shortcode'])
	# 	try:
	# 		post_caption = (posts[i]['node']['edge_media_to_caption']['edges'][0]['node']['text'])
	# 	except IndexError as e:
	# 		continue

	# 	post_polarity = analyze_caption(post_caption)
	# 	pos = post_polarity['avg_pos']
	# 	neu = post_polarity['avg_neu']
	# 	neg = post_polarity['avg_neg']
	# 	com = post_polarity['avg_com']
	# 	other_tags = post_polarity['hashtag_list']
	# 	post_picture = (posts[i]['node']['display_url'])
	# 	post_timestamp = (posts[i]['node']['taken_at_timestamp'])
	# 	post_body = [post_id, post_caption, post_picture, post_timestamp, pos, neu, neg, hashtag]
	# 	post_dict = {'post_id': post_id,
	# 				 'caption': post_caption,
	# 				 'picture_url' : post_picture,
	# 				 'timestamp' : post_timestamp,
	# 				 'pos': pos,
	# 				 'neg': neg,
	# 				 'neu': neu,
	# 				 'hashtag' : hashtag
	# 				}

	# 	posts_list.append(post_dict)


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
	return get_json_script(explore_url, tag, persist)
