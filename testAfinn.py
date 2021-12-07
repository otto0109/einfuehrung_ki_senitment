from afinn import Afinn

# ######### DAS IN CMD VORHER EINGEBEN: pip install afinn #########

afinn = Afinn(language='en')

# Bewertung von -5 (negativ) bis 5 (positiv) einzelner Worte. Summiert dann alle:
# Guckt sich nur einzelne Worte an. Keine Beachtung des Kontexts
# D.h.: I am happy -> 3.0 und I am not happy -> 3.0

inputText = 'I am not happy'
score = afinn.score(inputText)
print(score)
