import mysql.connector
from sql import database_conf as cfg


def query_posts(search_tag):
	cnx = mysql.connector.connect(**cfg.mysql)
	cursor = cnx.cursor()
	query = ("""SELECT id, caption, picture_url, hashtag FROM posts WHERE hashtag = %s""")
	cursor.execute(query, (search_tag,))
	posts = []
	for(id, caption, picture_url, hashtag) in cursor:
		post = {
			'post_id' : id.decode('utf8'),
			'caption' : caption.decode('utf8'),
			'picture_url' : picture_url.decode('utf8'),
			'hashtag' : hashtag.decode('utf8')
		}
		posts.append(post)

	print(len(posts))

	cursor.close()
	cnx.close()

	return posts


if __name__ == "__main__":
	query_posts('sunset')	