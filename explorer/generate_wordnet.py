from nltk.corpus import wordnet as wn
import sys

# Set hashtag from compile args
hashtag = sys.argv[1]



#Generate WordNet list by Path Similarity
# Credit to Stack Overflow: https://stackoverflow.com/questions/45145020/with-nltk-how-can-i-generate-different-form-of-word-when-a-certain-word-is-giv
def similar_words(hashtag):
	forms = set() #We'll store the derivational forms in a set to eliminate duplicates
	for hashtag_lemma in wn.lemmas(hashtag): #for each hashtag lemma in WordNet
		forms.add(hashtag_lemma.name().lower()) #add the lemma itself
		for related_lemma in hashtag_lemma.derivationally_related_forms(): #for each related lemma
			forms.add(related_lemma.name().lower()) #add the related lemma

	return forms

if __name__ == '__main__':
	print(similar_words(hashtag))