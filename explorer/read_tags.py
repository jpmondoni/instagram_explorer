from scrap_task import scrap_init
from generate_wordnet import similar_words as sw
import sys

tag_list = []

def main():
	# Init scraping based on a list of words in a file.
	if(sys.argv[1] == "-f"):
		# Todo - Include file not found exception
		__file_name = sys.argv[2]
		with open(__file_name, encoding = 'utf-8') as f:
			tag_list = f.readlines()
		tag_list = [x.strip() for x in tag_list] 
		print('words = ', tag_list)

		for tag in tag_list:
			scrap_init(tag)

	# Init scraping based on a single word.
	elif(sys.argv[1] == "-w"):
		__hashtag = sys.argv[2]
		print('words = ', __hashtag)
		scrap_init(__hashtag)

	# Experimental function to use combo of words using NLTK WordNet
	elif(sys.argv[1] == "-wn"):
		__hashtag = sys.argv[2]
		tag_list = sw(__hashtag)
		print('words = ', tag_list)
		for tag in tag_list:
			# sw(word) function returns a list with [word, similarity], so we need to use the first element.
			scrap_init(tag[0])


if __name__ == "__main__":
	main()