from scrap_task import scrap_init
import sys

def main():
	__file_name = sys.argv[1]
	with open(__file_name, encoding = 'utf-8') as f:
		tag_list = f.readlines()
	tag_list = [x.strip() for x in tag_list] 
	print(tag_list)

	for tag in tag_list:
		scrap_init(tag)

if __name__ == "__main__":
	main()