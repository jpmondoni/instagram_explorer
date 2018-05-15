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

	source_list = []
	lenOfPage = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
	match=False
	while(match==False):
		lastCount = lenOfPage
		time.sleep(1)
		lenOfPage = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
		source_list.append(browser.page_source)
		if lastCount==lenOfPage:
			match=True

	posts_list = []
	id_set = set([])

	for page in source_list:
		soup = BeautifulSoup(page, "lxml")

		mck9w_blocks = soup.find_all("div", class_="_mck9w")
		for mck9w in mck9w_blocks:
			pid = ''
			for a in mck9w.find_all('a'):
				pid = a.get('href').replace("/p/","").replace("/?tagged="+hashtag, "")

			if pid in id_set:
				continue
			else:
				id_set.add(pid)

			mck9w.find_all("div", clas_="_4rbun")
			for _4rbun in mck9w:
				for img in _4rbun.find_all('img', alt=True, src=True):
					alt = img['alt']
					src = img['src']
			
			post_dict = {
				'post_id': pid,
				'caption': alt,
				'picture_url': src,
				'hashtag': hashtag
			}

			posts_list.append(post_dict)

	browser.quit()
	print("Fecthed {0} post(s) using '{1}' hashtag.".format(len(id_set), hashtag))
	post_parser(posts_list, persist)

def post_parser(posts_found, persist):

	posts_list = []
	for post in posts_found:
		post_id = post['post_id']
		caption = post['caption']
		picture_url = post ['picture_url']
		hashtag = post['hashtag']
		post_polarity = analyze_caption(caption)
		pos = post_polarity['avg_pos']
		neu = post_polarity['avg_neu']
		neg = post_polarity['avg_neg']
		com = post_polarity['avg_com']
		other_tags = post_polarity['hashtag_list']
		#post_body = [post_id, caption, post_picture, pos, neu, neg, hashtag]
		post_dict = {'post_id': post_id,
					 'caption': caption,
					 'picture_url' : picture_url,
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
			cursor.execute("""INSERT IGNORE INTO posts VALUES (%s,%s,%s,%s,%s,%s,%s)""",
				(post['post_id'],post['caption'],post['picture_url'],post['pos'],post['neg'],post['neu'],post['hashtag']))
			conn.commit()
		except:
			continue
	
	return posts_list

def scrap_init(tag, persist):
	base_url = "https://www.instagram.com/explore/tags/"
	explore_url = base_url + tag
	return get_json_script(explore_url, tag, persist)
