from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def analyze_caption(caption):
	analyzer = SentimentIntensityAnalyzer()
	vs = analyzer.polarity_scores(caption)
	return vs