import mysql.connector
from sql import database_conf as cfg

cnx = mysql.connector.connect(**cfg.mysql)


def store_task(session_list):
	return 0

def check_existence(search_this):
	cursor = cnx.cursor()
	query = """SELECT * FROM insights WHERE post_id = %s"""
	cursor.execute(query, (search_this,))
	exists = ""
	for post_id, dominant_color, avg_color, peak in cursor:
		exists = post_id

	if exists == search_this:
		return (True, cursor)
	else:
		return (False, None)

# Test method, used for debug purposes only.
if __name__ == '__main__':
	print(check_existence("rr3"))