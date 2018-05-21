import requests, re, sys, os, string
import json
import time
from sql import database_conf as cfg
from mysql.connector import MySQLConnection, Error
from lxml import html
from bs4 import BeautifulSoup
from sentiment_analysis import analyze_caption 
from selenium import webdriver


def fetch_posts(url, hashtag, persist):
	""""
	Function fetch_posts
	This function starts a browser to simulate scroll down, to work with infinite scrolls. Then it will browse through the page until it ends and save all the html source code available.
	All posts are within the html source code, thus it's necessary to iterate through all divs that contain a post and save the info we want. 
	Later we will pass this info on to continue the process.
	"""

	# Initiate a Selenium webdriver and go to our url variable.
	browser = webdriver.Chrome()
	browser.get(url)

	source_list = []

	# Scroll through the page and save the source-code into a list. No, this is not the ideal way - but it's working.
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

		# Find divs which class is "_mck9w" and inside, look up for "_4rbun" class. Posts are within this div.
		mck9w_blocks = soup.find_all("div", class_="_mck9w")
		for mck9w in mck9w_blocks:
			pid = ''
			for a in mck9w.find_all('a'):
				pid = a.get('href').replace("/p/","").replace("/?tagged="+hashtag, "")

			# If post already saved, simply ignore.
			if pid in id_set:
				continue
			else:
				id_set.add(pid)

			mck9w.find_all("div", clas_="_4rbun")
			for _4rbun in mck9w:
				for img in _4rbun.find_all('img', alt=True, src=True):
					alt = img['alt']
					src = img['src']
			
			# Assign post info into a dict element
			post_dict = {
				'post_id': pid,
				'caption': alt,
				'picture_url': src,
				'hashtag': hashtag
			}

			posts_list.append(post_dict)

	browser.quit()
	print("Fecthed {0} post(s) using '{1}' hashtag.".format(len(id_set), hashtag))

	# Send a list with all posts to be parsed and then saved into a database, if that's the option.
	return post_parser(posts_list, persist)

def post_parser(posts_found, persist):

	posts_list = []
	for post in posts_found:
		# Assign posts to a parsed dictionary and append it to a list
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

	# Save on MySQL database if persist is True
	if(persist):
		return persist_posts(posts_list)
	else:
		return posts_list

# MySQL Connection and insert function
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
	return fetch_posts(explore_url, tag, persist)
