import mysql.connector
import database_conf as cfg


def query_posts():
	cnx = mysql.connector.connect(**cfg.mysql)
	cursor = cnx.cursor()
	query = ("""SELECT id, caption, picture_url, hashtag FROM posts LIMIT 0, 30""")

	cursor.execute(query)
	posts = []
	for(id, caption, picture_url, hashtag) in cursor:
		post = {
			'id' : id,
			'caption' : caption,
			'picture_url' : picture_url,
			'hashtag' : hashtag
		}
		posts.append(post)

	cursor.close()
	cnx.close()

	return posts