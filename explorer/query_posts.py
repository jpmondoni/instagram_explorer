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
			'id' : id.decode('utf8'),
			'caption' : caption.decode('utf8'),
			'picture_url' : picture_url.decode('utf8'),
			'hashtag' : hashtag.decode('utf8')
		}
		posts.append(post)

	cursor.close()
	cnx.close()

	return posts



def main():
	query_posts()

if __name__ == "__main__":
	main()