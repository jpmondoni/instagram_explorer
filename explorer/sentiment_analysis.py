from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def analyze_caption(sentence):
	analyzer = SentimentIntensityAnalyzer()
	vs = analyzer.polarity_scores(sentence)
	return vs