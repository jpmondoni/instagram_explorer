from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from nltk.tokenize import sent_tokenize
import sys

def analyze_caption(caption):
	analyzer = SentimentIntensityAnalyzer()
	sentence_list = sent_tokenize(caption)
	hashtag_list = []
	avg_pos = avg_neu = avg_neg = avg_com = 0.0
	sum_pos = sum_neu = sum_neg = sum_com = 0.0
	for sentence in sentence_list:
		sentence_polarity = analyzer.polarity_scores(sentence)
		hashtag_set = extract_hashtags(sentence)
		if(len(hashtag_set) > 0):
			hashtag_list.append(hashtag_set)
		else:
			sum_pos += sentence_polarity['pos']
			sum_neu += sentence_polarity['neu']
			sum_neg += sentence_polarity['neg']
			sum_com += sentence_polarity['compound']

	polarity_set = {'sum_pos' : sum_pos,
					'sum_neu' : sum_neu,
					'sum_neg' : sum_neg,
					'sum_com' : sum_com		
				}
	result_set = calc_overal_polarity(polarity_set, len(sentence_list))
	caption_overall = { 'avg_pos' : result_set['avg_pos'],
	 					'avg_neu' : result_set['avg_neu'],
	 					'avg_neg' : result_set['avg_neg'],
	 					'avg_com' : result_set['avg_com'],
	 					'hashtag_list' : hashtag_list
	 				}

	return caption_overall

def calc_overal_polarity(ps, count):
	avg_set = { 'avg_pos' : round(ps['sum_pos']/count,4),
				'avg_neu' : round(ps['sum_neu']/count,4),
				'avg_neg' : round(ps['sum_neg']/count,4),
	 			'avg_com' : round(ps['sum_com']/count,4),
	}
	return avg_set


def extract_hashtags(s):
	return set(part[1:] for part in s.split() if part.startswith('#'))