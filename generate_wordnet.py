from nltk.corpus import wordnet as wn
import sys

hashtag = sys.argv[1]
# Set a minimum similarity value
min_simularity = 0.1
word_list = []

#Generate WordNet list by Path Similarity
def similar_words(hashtag):
	tag_net = wn.synsets(hashtag)
	root_word = tag_net[0]
	for tag in tag_net:
		lemma = tag.lemmas()[0].name()
		similarity = root_word.path_similarity(tag)
		if(isinstance(similarity, float)):
			if(lemma != hashtag and similarity >= min_simularity):
				ls = [lemma, similarity]
				word_list.append(ls)

	return world_list

