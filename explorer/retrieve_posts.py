from scrap_task import scrap_init
import sys

def generate_list(hashtag):
	return scrap_init(hashtag, False)

if __name__ == "__main__":
	generate_list(sys.argv[1])