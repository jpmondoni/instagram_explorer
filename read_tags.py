from scrap_task import scrap_init
from generate_wordnet import similar_words as sw
import sys

tag_list = []

def main():
	if(sys.argv[1] == "-F"):
		# Todo - Include file not found exception
		__file_name = sys.argv[2]
		with open(__file_name, encoding = 'utf-8') as f:
			tag_list = f.readlines()
		tag_list = [x.strip() for x in tag_list] 
		print(tag_list)

		for tag in tag_list:
			scrap_init(tag)

	if(sys.argv[1] == "-W"):
		__hashtag = sys.argv[2]
		scrap_init(__hashtag)

if __name__ == "__main__":
	main()