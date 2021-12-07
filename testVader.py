from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# ######### DAS IN CMD VORHER EINGEBEN: pip install vaderSentiment #########

analyzer = SentimentIntensityAnalyzer()

# Berücksichtigt im Gegensatz zu Afinn auch den Kontext ein wenig, sowie "not" usw.
# compound is the normalized, weighted composite score.

inputText = 'I am happy.'
score = analyzer.polarity_scores(inputText)
print(score)

inputText = 'I am not happy.'
score = analyzer.polarity_scores(inputText)
print(score)

inputText = 'I am very happy.'
score = analyzer.polarity_scores(inputText)
print(score)

print('==========================================')
inputText = 'set up was easy and we enjoyed it for just over a week .'
score = analyzer.polarity_scores(inputText)
print(score)
print(score.get('neg'))